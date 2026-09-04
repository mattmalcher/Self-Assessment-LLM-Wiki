# Self Assessment LLM Wiki

A GitHub Pages wiki covering the legal and HMRC-publication landscape
around UK Self Assessment (Income Tax) - primary and secondary
legislation, case law, HMRC manuals and policy publications, rates and
allowances, and customer-facing guidance - kept current by an automated
refresh pipeline instead of manual edits.

**Site:** https://mattmalcher.github.io/Self-Assessment-LLM-Wiki/ (enable
GitHub Pages under Settings -> Pages -> Source: GitHub Actions, and Settings
-> Actions -> General -> Workflow permissions: Read and write, for the
first deploy)

Start with [`docs/index.md`](docs/index.md) for the wiki's own explanation
of its scope, and
[`docs/meta/refresh-process.md`](docs/meta/refresh-process.md) for how the
pipeline works.

## Repo layout

```
docs/           the wiki content (MkDocs source)
pipeline/       the fetch pipeline: sources.yml (the registry), fetchers/,
                fetch.py (entrypoint), manifest.json (cache state)
mkdocs.yml      site config (Material theme)
.github/workflows/
  refresh.yml   scheduled + manual: runs the pipeline, opens a PR if
                anything changed
  pages.yml     builds + deploys docs/ to GitHub Pages on push to main
```

## Local development

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

mkdocs serve              # http://127.0.0.1:8000, live reload

python -m pipeline.fetch --dry-run          # check the registry resolves
python -m pipeline.fetch --only <source-id> # fetch one source
python -m pipeline.fetch                    # fetch everything due
```

See [`pipeline/sources.yml`](pipeline/sources.yml) for the source registry
and [`docs/meta/refresh-process.md`](docs/meta/refresh-process.md) for how
to add a source.
