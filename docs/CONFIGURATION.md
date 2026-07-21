# Configuration

## Environment variables

| Variable | Default | Purpose |
|---|---|---|
| `NO_COLOR` | unset | Disable ANSI color when set to any non-empty value. |
| `CODEX_HUD_MEMORY_STATUS` | `off` | Display-only generic memory-provider status. |
| `CODEX_HUD_TIMEZONE` | local system timezone | IANA timezone used for account reset dates and times, such as `America/New_York`. |
| `HOME` | process environment | Locates Codex and OMX configuration. |
| `CODEX_HOME` | `~/.codex` | Overrides the Codex configuration and session-data directory. |
| `TMUX` / `TMUX_PANE` | tmux environment | Enables pane installation and pane selection. |
| `CODO_TMUX` | `auto` | `auto`, `on`, or `required` starts tmux when outside it; `off` runs directly. |
| `CODO_HUD` | `auto` | `auto`/`on` starts the HUD when available, `required` fails if unavailable, and `off` disables it. |
| `CODO_MODEL` | unset | Optional model override passed to Codex. |
| `CODO_REASONING_EFFORT` | unset | Optional `model_reasoning_effort` override passed to Codex. |
| `CODO_CODEX_COMMAND` | `codex` | Alternate Codex executable, useful for testing or versioned installations. |
| `CODO_HUD_COMMAND` | `codex-hud` | Alternate HUD executable. |

## Reset timezone

Account reset timestamps use the local timezone and display as `Sat 07/25 12:52 EDT`. Set an IANA timezone with either method:

```bash
export CODEX_HUD_TIMEZONE=America/New_York
```

Or save it persistently without changing shell startup files:

```bash
mkdir -p ~/.config/codex-hud
printf '%s\n' America/New_York > ~/.config/codex-hud/timezone
```

The environment variable takes precedence over the file. If either value is invalid or absent, the HUD uses the operating system's local timezone.

## Command options

| Option | Effect |
|---|---|
| `--compact` | Render one plain status line. |
| `--watch` | Refresh continuously. |
| `--tmux` | Replace an existing HUD-like pane or create a bottom pane. |
| `--interval SECONDS` | Set watch refresh interval; minimum is 0.5 seconds. |
| `--version` | Print the installed HUD version. |

## Native Codex fields

When the installer owns the status line, it enables:

```toml
[tui]
# codex-hud:managed-status-line
status_line = ["current-dir", "model-with-reasoning", "codex-version", "git-branch", "context-remaining", "used-tokens", "five-hour-limit", "weekly-limit", "session-id"]
```

An existing user-defined `status_line` is preserved. The managed list intentionally avoids pairs that repeat the same information (`current-dir`/`project-root`, `model-name`/`model-with-reasoning`, and `context-used`/`context-remaining`).

## Codo profile and option forwarding

When `~/.codex/codo.config.toml` exists, `codo` automatically invokes Codex with `--profile codo`. The file uses ordinary top-level Codex configuration keys. Every argument supplied to `codo` is forwarded to Codex, so global flags, prompts, images, and subcommands remain available without a second option vocabulary.

The launcher does not enable full access. Users who deliberately need a different permission policy should put it in their Codex profile or pass the official Codex flags for that invocation.

## tmux managed block

The installer adds a block delimited by `CODEX-HUD:START` and `CODEX-HUD:END`. Re-running installation replaces only that block. The installer and uninstaller also recognize the legacy `CODEX-HUD+` markers so upgrades do not duplicate the status bar.
