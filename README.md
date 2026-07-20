# CODEX HUD+

[![CI](https://github.com/ojesusmp/codex_hud/actions/workflows/ci.yml/badge.svg)](https://github.com/ojesusmp/codex_hud/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)

A colorful, zero-dependency telemetry HUD for Codex CLI and Oh My Codex. It provides a live terminal dashboard, a compact tmux status segment, a concise native Codex TUI status line, and the optional `codo` launcher.

```text
╭─[ CODEX HUD+  LIVE TELEMETRY ]──────────────────────────────────────────────────────────╮
⌂ user@workstation  cwd:~/project  git:main+
◆ MODEL <model>  reasoning:high  codex:<version>  sid:<session>  cost:n/a
◈ TOKENS cached:<count> new:<count> out:<count> think:<count> total:<count> ctx:<used>/<window>
CTX █████████░░░ 72%  ACCOUNT ████░░░░░░░░ 34% <plan>/<window> reset:<time>
🤖🤖 agents:2  ⬡ mcp:3  ⚡ hooks:1  ● MEMORY:ready  project:example
▣ SYSTEM mem:███░░░░░ <used>/<total> node:<rss> codex:<rss> load:<averages> disk:<percent>
◉ OMX [OMX] example/main | team:2 workers | turns:42
╰──────────────────────────────────────────────────────────────────────────────────────────╯
```

## Features

- User, hostname, current directory, project and Git branch/dirty state
- Active model, reasoning effort, approval/sandbox policy, Codex version and shortened session identifier
- Cached input, non-cached input, output, reasoning and total token counts
- Context-window use with a color-coded progress bar
- Account plan, usage window, reset time and available credits
- Active-agent robot indicators, configured MCP count and hook-plugin count
- Optional generic memory-provider status through an environment variable
- RAM, Node/Codex RSS, largest process, load, disk use and uptime
- Full OMX mode, team, turn and workflow status when OMX is installed
- ANSI colors with a `NO_COLOR` fallback
- No third-party Python dependencies and no outbound telemetry
- `codo` launcher with automatic tmux/HUD lifecycle and transparent Codex option forwarding

The HUD does not estimate billing. It shows `cost:n/a` because Codex session telemetry does not currently provide an authoritative monetary cost.

## Requirements

| Requirement | Status |
|---|---|
| Linux with `/proc` | Required |
| Python 3.10 or newer | Required |
| Codex CLI | Recommended for complete session telemetry |
| tmux | Optional, required for `--tmux` and the status-bar integration |
| Oh My Codex (`omx`) | Optional, enables the OMX line |

macOS and Windows are not currently supported because process and memory collection use Linux `/proc`.

## Installation

```bash
git clone https://github.com/ojesusmp/codex_hud.git
cd codex_hud
./install.sh
```

The installer:

1. Installs `codex-hud` into `~/.local/bin`.
2. Installs `codo`, an optional Codex launcher that manages the tmux HUD pane.
3. Adds a concise, non-repeating Codex status line only when no user-owned status line exists.
4. Adds a clearly marked, replaceable block to `~/.tmux.conf`.
5. Reloads tmux when run inside an active tmux client.

Restart Codex once after installation so it reloads `[tui].status_line`.

## Usage

```bash
codex-hud                # render one full frame
codex-hud --watch        # refresh every two seconds
codex-hud --compact      # render one status-bar-friendly line
codex-hud --tmux         # upgrade an existing HUD pane or open a new pane
codex-hud --interval 1   # set the watch refresh interval
codex-hud --version      # print the installed version
NO_COLOR=1 codex-hud     # disable ANSI color
codo                     # launch Codex with an automatically managed HUD
codo --search            # pass any Codex option through unchanged
codo exec "run tests"    # Codex subcommands and arguments also pass through
```

### `codo` launcher

`codo` enters a dedicated tmux session when needed, opens the HUD pane, runs Codex, and removes the pane when Codex exits. It does not change the Codex security policy. All arguments belong to Codex and are forwarded in their original order.

If `~/.codex/codo.config.toml` exists, `codo` loads it as the standard Codex `codo` profile. This is the recommended place for launcher-specific model, reasoning, sandbox, or approval defaults:

```toml
# ~/.codex/codo.config.toml
model_reasoning_effort = "medium"
approval_policy = "on-request"
sandbox_mode = "workspace-write"
```

Environment controls are documented in [Configuration](docs/CONFIGURATION.md). Explicit `--profile`, `--model`, and `model_reasoning_effort` arguments suppress the matching launcher default.

### Optional memory status

The public HUD does not probe a specific memory product or credential path. Set a display-only status value when desired:

```bash
export CODEX_HUD_MEMORY_STATUS=ready
```

The value is displayed but is never interpreted as a command or transmitted.

## Display layers

1. **Native Codex footer**: a non-repeating model, branch, context, token, limit and session summary.
2. **tmux status bar**: a compact model/token/account/system summary.
3. **HUD pane**: colored multi-line telemetry, progress graphics, robots and OMX state.

See [Configuration](docs/CONFIGURATION.md) for the full field list and customization options.

## Privacy and safety

CODEX HUD+ is read-only and operates entirely on-device. It parses only `token_count` events from the newest Codex session log and never sends telemetry. It does not read credential stores or print authentication values. See [Privacy](docs/PRIVACY.md) and [Security](SECURITY.md).

## Documentation

- [Architecture](docs/ARCHITECTURE.md)
- [Configuration](docs/CONFIGURATION.md)
- [Compatibility](docs/COMPATIBILITY.md)
- [Privacy](docs/PRIVACY.md)
- [FAQ](docs/FAQ.md)
- [Troubleshooting](docs/TROUBLESHOOTING.md)
- [Contributing](CONTRIBUTING.md)
- [Support](SUPPORT.md)
- [Security policy](SECURITY.md)
- [Changelog](CHANGELOG.md)

## Uninstallation

```bash
./uninstall.sh
```

The uninstaller removes the executable and the managed tmux block. A native Codex status line is removed only when it still carries the CODEX HUD+ managed marker.

## License

[MIT](LICENSE)
