# Frequently asked questions

## Does Codex HUD upload telemetry?

No. The executable makes no network requests and renders on-device information only.

## Is this Codex Hub?

No. The name is **Codex HUD**, where HUD means “heads-up display.” The repository and executable are both named `codex-hud`.

## Does it read prompts or responses?

It searches the newest Codex session log for the most recent `token_count` event. It does not render raw prompt or response text.

## Why is cost shown as `n/a`?

The available Codex session telemetry does not provide an authoritative monetary cost. The project intentionally avoids speculative estimates.

## Can I use it without OMX?

Yes. OMX is optional; its line becomes an unavailable placeholder.

## What do OMX `turns` and `total-turns` mean?

`turns` is OMX's `session_turns` counter: completed lead-session turns recorded by the OMX notification hook. `total-turns` is OMX's `total_turns` metric from `.omx/metrics.json`, shown by the full OMX preset. They count turns, not tokens, tool calls, or subagents.

In OMX 0.20.2, session startup resets both counters and each completed lead-session turn increments both, so they normally show the same number. The separate labels are retained because they are produced by OMX and may diverge in other versions or longer-lived metrics files.

## Can I use it without tmux?

Yes. Use one-shot or watch mode. Only the tmux status integration and `--tmux` require tmux.

## Why are macOS and Windows unsupported?

The process collectors currently rely on Linux `/proc`. Portable collectors are welcome if they keep the read-only and dependency-free design.

## How do I show a memory provider?

Set `CODEX_HUD_MEMORY_STATUS` to a display-safe value such as `ready`. Do not place a credential in this variable.

## Can I publish HUD output in an issue?

Only after redacting the user, hostname, paths, repository, branch, session identifier, account details and any other identifying information.
