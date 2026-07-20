# Troubleshooting

| Problem | Cause | Resolution |
|---|---|---|
| Model or token fields show `?`/`0` | Codex configuration or session telemetry is unavailable. | Start a Codex session and confirm the Codex data directory is readable. |
| OMX shows unavailable | OMX is not installed or not on `PATH`. | Install OMX or ignore the optional line. |
| Agent count remains zero | No tracked non-leader agent is active. | Start an agent workflow and confirm OMX tracking state exists. |
| Colors are unreadable | Terminal palette or accessibility preference differs. | Set `NO_COLOR=1` or adjust terminal colors. |
| Boxes/robots have incorrect width | Font lacks Unicode or emoji-width support. | Use a compatible terminal font or plain output. |
| `--tmux` reports tmux required | Command is outside a tmux client. | Start tmux, then rerun `codex-hud --tmux`. |
| HUD pane duplicates an OMX pane | OMX recreated its managed pane. | Keep both, or run `codex-hud --tmux` again to reuse the first HUD-like pane. |
| Native footer does not change | Codex loaded configuration before installation. | Restart Codex once. |
| Existing native footer is unchanged | Installer preserved a user-owned `status_line`. | Edit `[tui].status_line` manually using the documented field list. |
| tmux bar does not change | tmux has not reloaded configuration. | Run `tmux source-file ~/.tmux.conf`. |

For diagnostic output that is safer to share, use:

```bash
NO_COLOR=1 codex-hud
python3 -m unittest discover -s tests -v
```

Redact identifying values before posting output publicly.
