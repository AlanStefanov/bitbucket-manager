# BBM — Bitbucket Repository Manager

## Overview
`bbm` is a terminal user interface (TUI) for managing Bitbucket Cloud repositories,
built with the [Textual](https://textual.textualize.io/) framework. It offers screens
for repository exploration, mass permission management, PR auto-approval, project
migration, smart archiving, and dependency analysis.

Because it is a terminal app, it is served to the browser via `textual-serve`, which
renders the TUI in a web terminal. This is what makes it visible in the Replit preview pane.

## Architecture
- **Language:** Python 3.11
- **TUI framework:** Textual 8.x (`src/bbm/tui/`)
- **Web serving:** `textual-serve` (`serve.py` at repo root)
- **HTTP/API:** `requests` (Bitbucket Cloud REST API v2.0)
- **Package layout:** `src/bbm/` (src-layout, configured in `pyproject.toml`)
- **Entry points:**
  - `python -m bbm` runs the TUI directly in a terminal
  - `python serve.py` serves the TUI over HTTP on port 5000 (used by the workflow & deployment)

## Replit Setup
- Workflow "Start application" runs `python serve.py` on port 5000 (webview).
- `serve.py` binds host `0.0.0.0` and adds `src/` to `PYTHONPATH` so the subprocess
  (`python -m bbm`) can import the `bbm` package.
- Deployment target: `vm` (always-running, because textual-serve maintains persistent
  websocket terminal sessions).

## Configuration
The app reads Bitbucket credentials from environment variables (or a `.env` file at the
repo root). These are only needed for live Bitbucket operations; the app boots and renders
without them.

| Variable | Description |
|----------|-------------|
| `BB_TOKEN` | Bitbucket API token (id.atlassian.com) |
| `BB_USERNAME` | Atlassian account email |
| `BB_WORKSPACE` | Bitbucket workspace slug |
| `DEV_DIR` | Optional clone directory |

See `.env.example` for the full template.

## User Preferences
(none recorded yet)
