"""Backend-agnostic text completion.

Four backends, chosen with --backend:

  claude-cli   shells out to the `claude` CLI, so it runs on a Claude Code
               subscription with no API key (the default)
  codex-cli    shells out to `codex exec`, likewise on a ChatGPT subscription
  anthropic    Anthropic API, needs ANTHROPIC_API_KEY
  openai       OpenAI API, needs OPENAI_API_KEY

All four expose the same `complete(system, prompt) -> str`. The CLI backends
are the point of this layer: the synthesis stage is meant to be run locally
against whatever subscription the operator already pays for, which is why it
is not part of the scheduled GitHub Actions refresh.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import tempfile
import time
from pathlib import Path

BACKENDS = ("claude-cli", "codex-cli", "anthropic", "openai")


class LLMError(RuntimeError):
    pass


class Backend:
    name = "?"

    def __init__(self, model: str, *, timeout: int = 900):
        self.model = model
        self.timeout = timeout

    def complete(self, system: str, prompt: str) -> str:
        raise NotImplementedError

    def call(self, system: str, prompt: str, *, retries: int = 3) -> str:
        """complete() with backoff; transient CLI/API failures are common
        enough over a few hundred chunks that one flake shouldn't sink a run."""
        last: Exception | None = None
        for attempt in range(retries):
            try:
                out = self.complete(system, prompt)
                if out.strip():
                    return out
                last = LLMError("empty response")
            except Exception as exc:  # noqa: BLE001 - re-raised below
                last = exc
            time.sleep(3 * (attempt + 1))
        raise LLMError(f"{self.name}: failed after {retries} attempts: {last}")


class ClaudeCLI(Backend):
    name = "claude-cli"

    def complete(self, system: str, prompt: str) -> str:
        exe = shutil.which("claude")
        if not exe:
            raise LLMError("`claude` not on PATH - install Claude Code, or use --backend anthropic")
        with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as fh:
            fh.write(system)
            system_file = fh.name
        cmd = [
            exe, "-p",
            "--output-format", "json",
            "--model", self.model,
            "--system-prompt-file", system_file,
            # No tool use is wanted here: this is pure text-in/text-out.
            "--restricted",
            "--strict-mcp-config",
        ]
        cmd += [a for a in os.environ.get("SYNTH_CLAUDE_CLI_ARGS", "").split() if a]
        try:
            proc = subprocess.run(
                cmd, input=prompt, capture_output=True, text=True, timeout=self.timeout,
            )
        finally:
            Path(system_file).unlink(missing_ok=True)
        if proc.returncode != 0:
            raise LLMError(f"claude exited {proc.returncode}: {proc.stderr.strip()[:2000]}")
        try:
            payload = json.loads(proc.stdout)
        except json.JSONDecodeError:
            return proc.stdout  # older CLIs that ignore --output-format
        if payload.get("is_error"):
            raise LLMError(f"claude reported an error: {str(payload.get('result'))[:2000]}")
        return payload.get("result", "")


class CodexCLI(Backend):
    name = "codex-cli"

    def complete(self, system: str, prompt: str) -> str:
        exe = shutil.which("codex")
        if not exe:
            raise LLMError("`codex` not on PATH - install the Codex CLI, or use --backend openai")
        # codex exec has no system-prompt flag, so the system text is folded
        # into the top of the prompt.
        with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as fh:
            out_file = fh.name
        cmd = [exe, "exec", "--model", self.model, "--skip-git-repo-check",
               "--output-last-message", out_file, "-"]
        cmd += [a for a in os.environ.get("SYNTH_CODEX_CLI_ARGS", "").split() if a]
        try:
            proc = subprocess.run(
                cmd, input=f"{system}\n\n---\n\n{prompt}",
                capture_output=True, text=True, timeout=self.timeout,
            )
            if proc.returncode != 0:
                raise LLMError(f"codex exited {proc.returncode}: {proc.stderr.strip()[:2000]}")
            text = Path(out_file).read_text() if Path(out_file).exists() else ""
        finally:
            Path(out_file).unlink(missing_ok=True)
        return text or proc.stdout


class AnthropicAPI(Backend):
    name = "anthropic"

    def complete(self, system: str, prompt: str) -> str:
        try:
            import anthropic  # lazy: only the API backends need the SDK
        except ImportError as exc:
            raise LLMError("pip install -r requirements-synth.txt for the anthropic backend") from exc
        if not os.environ.get("ANTHROPIC_API_KEY"):
            raise LLMError("ANTHROPIC_API_KEY is not set")
        client = anthropic.Anthropic()
        msg = client.messages.create(
            model=self.model,
            max_tokens=16000,
            system=system,
            messages=[{"role": "user", "content": prompt}],
        )
        return "".join(b.text for b in msg.content if b.type == "text")


class OpenAIAPI(Backend):
    name = "openai"

    def complete(self, system: str, prompt: str) -> str:
        try:
            import openai  # lazy: only the API backends need the SDK
        except ImportError as exc:
            raise LLMError("pip install -r requirements-synth.txt for the openai backend") from exc
        if not os.environ.get("OPENAI_API_KEY"):
            raise LLMError("OPENAI_API_KEY is not set")
        client = openai.OpenAI()
        resp = client.responses.create(
            model=self.model,
            instructions=system,
            input=prompt,
        )
        return resp.output_text


_CLASSES = {
    "claude-cli": ClaudeCLI,
    "codex-cli": CodexCLI,
    "anthropic": AnthropicAPI,
    "openai": OpenAIAPI,
}


def get_backend(name: str, model: str, *, timeout: int = 900) -> Backend:
    if name not in _CLASSES:
        raise LLMError(f"unknown backend {name!r}; expected one of {', '.join(BACKENDS)}")
    return _CLASSES[name](model, timeout=timeout)


def extract_json(text: str) -> dict:
    """Pull the first JSON object out of a model response.

    Models wrap JSON in prose or fences often enough that asking nicely isn't
    sufficient, so this scans for the first balanced {...} run.
    """
    text = text.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1] if "\n" in text else text
        if text.rstrip().endswith("```"):
            text = text.rstrip()[:-3]
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    start = text.find("{")
    while start != -1:
        depth, in_str, esc = 0, False, False
        for i in range(start, len(text)):
            ch = text[i]
            if in_str:
                if esc:
                    esc = False
                elif ch == "\\":
                    esc = True
                elif ch == '"':
                    in_str = False
                continue
            if ch == '"':
                in_str = True
            elif ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    try:
                        return json.loads(text[start:i + 1])
                    except json.JSONDecodeError:
                        break
        start = text.find("{", start + 1)
    raise LLMError(f"no JSON object in response: {text[:400]!r}")
