# Configuration

## Environment variables

| Variable | Default | Purpose |
|---|---|---|
| `NO_COLOR` | unset | Disable ANSI color when set to any non-empty value. |
| `CODEX_HUD_MEMORY_STATUS` | `off` | Display-only generic memory-provider status. |
| `HOME` | process environment | Locates Codex and OMX configuration. |
| `TMUX` / `TMUX_PANE` | tmux environment | Enables pane installation and pane selection. |

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
status_line = ["current-dir", "project-root", "model-name", "model-with-reasoning", "codex-version", "git-branch", "context-used", "context-remaining", "context-window-size", "used-tokens", "total-input-tokens", "total-output-tokens", "five-hour-limit", "weekly-limit", "session-id"]
```

An existing user-defined `status_line` is preserved.

## tmux managed block

The installer adds a block delimited by `CODEX-HUD+:START` and `CODEX-HUD+:END`. Re-running installation replaces only that block. The uninstaller removes only that block.
