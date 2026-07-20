# Architecture

CODEX HUD+ is a single Python executable with no imported third-party packages.

```text
Codex configuration ─┐
Codex session JSONL ─┼─> read-only collectors ─> normalized frame ─> full renderer
Linux /proc ─────────┤                                      ├─────> compact renderer
Git / tmux / OMX ────┘                                      └─────> tmux pane/status bar
```

The separate `codo` shell launcher owns only process lifecycle: it enters tmux, asks `codex-hud --tmux` for a pane, forwards arguments to Codex, and removes that pane on exit. Codex continues to own all CLI option parsing and security policy.

## Collectors

- **Codex config:** model, reasoning effort and configured MCP server count.
- **Session telemetry:** newest `token_count` and `turn_context` events for usage plus active model/policy data.
- **Linux process data:** memory totals and RSS through `/proc`.
- **Git:** repository root, branch and dirty state.
- **OMX:** optional rendered orchestration status.
- **Agent tracking:** non-leader active thread count from OMX state when available.
- **Hooks:** plugin-file count in standard OMX hook directories.

## Rendering

The full renderer uses ANSI 256-color sequences, Unicode box drawing, progress blocks and robot symbols. `NO_COLOR` disables ANSI sequences. The compact renderer intentionally emits one plain line for tmux.

## Failure model

Optional collectors use bounded subprocess timeouts and return placeholders when unavailable. The HUD should remain usable when Codex session data, Git, tmux or OMX is absent.

## Trust model

All collection is read-only. Displayed paths, branch names and the optional memory-status value are data. They are never evaluated as shell commands. The program performs no network request.
