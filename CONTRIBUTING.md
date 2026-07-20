# Contributing

Contributions are welcome through issues and pull requests.

## Development setup

```bash
git clone https://github.com/ojesusmp/codex_hud.git
cd codex_hud
python3 -m py_compile bin/codex-hud tests/test_hud.py
python3 -m unittest discover -s tests -v
NO_COLOR=1 bin/codex-hud
```

No runtime Python dependencies are required.

## Pull requests

1. Create a focused branch from `main`.
2. Keep telemetry collection read-only and on-device.
3. Never add credentials, real session logs, private hostnames, private addresses or user-specific absolute paths.
4. Add or update tests for behavioral changes.
5. Update README, configuration, privacy and changelog documentation when applicable.
6. Run the complete verification commands before opening the pull request.

## Design guidelines

- Fail softly when optional tools or data are unavailable.
- Preserve existing Codex and tmux user configuration.
- Keep the compact renderer to one line.
- Respect `NO_COLOR`.
- Avoid network access and third-party runtime dependencies.
- Label inferred information clearly; never invent cost data.

## Commit messages

Use short imperative messages. Conventional Commit prefixes such as `feat:`, `fix:`, `docs:`, `test:` and `chore:` are encouraged.
