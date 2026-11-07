---
name: setup-env
description: Use when setting up a fresh checkout of Selenium-Python-Example, restoring its Python environment, or diagnosing missing dependencies or Chrome before running pytest.
---

# Setup environment

Run commands from the repository root. Follow the checked-in manifests and lockfile; preserve existing environments, credentials, and dependency versions.

## Install

Use `uv` (install it from https://docs.astral.sh/uv/getting-started/installation/ if missing).
Inspect `pyproject.toml`, `uv.lock`, and `.github/workflows/pr.yml` first.
The current CI uses Python 3.14; `~=3.11` allows newer Python 3.x.

```bash
uv python install 3.14
uv sync --python 3.14 --locked --all-extras --dev
```

`uv sync` creates `.venv`; activation is unnecessary with `uv run`.
If an existing environment uses another compatible Python, preserve it unless a change is needed.
If locked sync fails, report the actual error; do not regenerate `uv.lock` or upgrade packages as a setup shortcut.

Install Google Chrome using the operating system's supported installer if absent.
Selenium Manager resolves the matching driver on first launch and may need network access.
Do not install Playwright browsers or an unrelated global ChromeDriver.

## Configure

Inspect the selected tests and `tests/conftest.py` for required settings.
The repository has no `.env.example`; do not attempt to copy one.
If needed, create a root `.env` only when absent and populate it privately with user-provided values.
Preserve existing values and confirm `.env` is ignored before adding credentials.

Valid-login tests read `EMAIL` and `PASSWORD`; email tests also use
`MAILINATOR_API_KEY` and `MAILINATOR_DOMAIN_NAME`.
Database and visual regression tests require their own services; they are not setup prerequisites.
Pass the target explicitly with pytest's `--base-url`; setting `BASE_URL` alone does not configure pytest.

## Common problems

- Browser download or registry access fails: report the destination and error; retain TLS verification and proxy settings.
- Chrome reports missing Linux libraries: install the distribution's required Chrome dependencies.
- Credentials or optional services are unavailable: complete installation and report which settings or services are missing.
