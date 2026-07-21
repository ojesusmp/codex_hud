# Changelog

All notable changes are documented here. The project follows semantic versioning.

## [1.1.0] - 2026-07-21

### Added

- Expanded public documentation and GitHub community files.
- Generic `CODEX_HUD_MEMORY_STATUS` display integration.
- Version command and privacy-oriented repository checks.
- `codo` launcher with automatic tmux/HUD lifecycle, optional dedicated Codex profile, and transparent option forwarding.
- Installer preflight for Linux, Python 3.10+, Codex CLI, and tmux, with explicit approval before installing missing prerequisites.
- Clear, consistent **Codex HUD** naming across the repository, executable output, and installer.
- Copy-ready instructions for installing the heads-up display from another Codex session.

### Changed

- Renamed the GitHub repository from `codex_hud` to `codex-hud`; GitHub redirects the former URL.
- Removed the unrelated Codex Guides plugin from the HUD prerequisite path.
- Removed product-specific memory integration and environment-specific examples.
- Installer now preserves an existing user-owned Codex status line.
- Managed native footer no longer duplicates directory, model, or context fields.

## [1.0.0] - 2026-07-20

### Added

- Colored multi-line Codex telemetry HUD.
- Token, context and account progress graphics.
- Robot indicators for active agents.
- Codex, tmux and OMX integration.
- Installer, uninstaller, unit tests and GitHub Actions CI.
