#!/usr/bin/env python3
"""Entrypoint for the LLM layer.

    python -m self_assessment_wiki.synth.build status                 # what's stale, no model calls
    python -m self_assessment_wiki.synth.build extract                # corpus -> extracts/ (cached)
    python -m self_assessment_wiki.synth.build compose                # extracts/ -> docs/
    python -m self_assessment_wiki.synth.build all                    # both, in order

Run this locally: it is deliberately not part of the scheduled GitHub
Actions refresh, so it can use whatever Claude or OpenAI subscription you
already have (see --backend) rather than a CI API key.
"""
from __future__ import annotations

import argparse
import sys

from . import compose, extract
from .config import DEFAULT_BACKEND, DEFAULT_CONCURRENCY, DEFAULT_MODELS
from .llm import BACKENDS, LLMError, get_backend


def _model(args, stage: str) -> str:
    if args.model:
        return args.model
    return DEFAULT_MODELS.get(args.backend, {}).get(stage, "")


def cmd_status(args) -> int:
    plans = extract.plan(args.only if args.command == "status" else None)
    todo = sum(len(p.todo) for p in plans)
    cached = sum(len(p.chunks) - len(p.todo) for p in plans)
    orphans = sum(p.orphans for p in plans)
    print("Extract stage (corpus -> extracts/)")
    print(f"  {len(plans)} corpus documents, {cached + todo} chunks")
    print(f"  {cached} cached, {todo} need extracting, {orphans} stale cache entries to prune")
    for p in plans:
        if p.todo or p.orphans:
            print(f"    {p.doc}: {len(p.todo)} new, {p.orphans} stale")

    model = _model(args, "compose")
    works = compose.plan(model)
    stale = [w for w in works if w.stale]
    print(f"\nCompose stage (extracts/ -> docs/), model {args.backend}:{model}")
    print(f"  {len(works)} pages, {len(stale)} stale")
    for w in works:
        mark = "*" if w.stale else "="
        print(f"    {mark} {w.spec['id']:<24} {len(w.notes):>4} notes  {w.reason}")
    if todo:
        print("\nCompose reads only what extract has already written - "
              "run `extract` first for the full picture.")
    return 0


def cmd_extract(args) -> int:
    model = _model(args, "extract")
    if args.dry_run:
        plans = extract.plan(args.only)
        todo = sum(len(p.todo) for p in plans)
        print(f"would make {todo} model call(s) to {args.backend}:{model}")
        for p in plans:
            if p.todo:
                print(f"  {p.doc}: {len(p.todo)}")
        return 0
    backend = get_backend(args.backend, model, timeout=args.timeout)
    done, failed = extract.run(backend, only=args.only, limit=args.limit,
                               concurrency=args.concurrency)
    print(f"\nextracted {done} chunk(s), {failed} failed")
    return 1 if failed and not done else 0


def cmd_compose(args) -> int:
    model = _model(args, "compose")
    if args.dry_run:
        for w in compose.plan(model, only=args.only, force=args.force):
            print(f"{'*' if w.stale else '='} {w.spec['id']:<24} {len(w.notes):>4} notes  {w.reason}")
        return 0
    backend = get_backend(args.backend, model, timeout=args.timeout)
    written, failed = compose.run(backend, model, only=args.only, force=args.force)
    print(f"\nwrote {written} page(s), {failed} failed")
    return 1 if failed and not written else 0


def cmd_all(args) -> int:
    rc = cmd_extract(args)
    if rc and not args.keep_going:
        return rc
    args.only = None  # --only applies to whichever stage was named, not both
    return cmd_compose(args)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="synth.build", description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("command", choices=["status", "extract", "compose", "all"])
    parser.add_argument("--only", nargs="*", help="extract: corpus paths; compose: page ids")
    parser.add_argument("--backend", default=DEFAULT_BACKEND, choices=BACKENDS,
                        help=f"default {DEFAULT_BACKEND} (uses your Claude Code subscription)")
    parser.add_argument("--model", help="override the per-stage default model")
    parser.add_argument("--concurrency", type=int, default=DEFAULT_CONCURRENCY)
    parser.add_argument("--limit", type=int, help="extract: stop after N chunks (cost control)")
    parser.add_argument("--force", action="store_true", help="compose: rewrite even if up to date")
    parser.add_argument("--dry-run", action="store_true", help="plan only, no model calls")
    parser.add_argument("--timeout", type=int, default=900, help="per-call timeout, seconds")
    parser.add_argument("--keep-going", action="store_true", help="all: compose even if extract failed")
    args = parser.parse_args(argv)

    try:
        return {"status": cmd_status, "extract": cmd_extract,
                "compose": cmd_compose, "all": cmd_all}[args.command](args)
    except LLMError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
