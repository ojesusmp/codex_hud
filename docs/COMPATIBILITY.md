# Compatibility

| Platform/tool | Status | Notes |
|---|---|---|
| Linux | Supported | Requires `/proc`. |
| Python 3.10+ | Supported | Standard library only. |
| Codex CLI | Supported | Session schema changes may require updates. |
| tmux | Optional | Required for `--tmux` and status-bar integration. |
| Oh My Codex | Optional | Missing OMX produces a safe placeholder. |
| macOS | Not supported | Linux `/proc` collectors need a portability layer. |
| Windows | Not supported | Linux process and shell assumptions need a portability layer. |

Terminal fonts differ. If Unicode graphics render incorrectly, use a font with box-drawing and emoji coverage or run with `NO_COLOR=1` for simplified output.
