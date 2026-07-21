# Security policy

## Supported versions

Security fixes are applied to the latest release and the `main` branch.

| Version | Supported |
|---|---|
| Latest release | Yes |
| `main` | Yes |
| Older releases | Best effort |

## Reporting a vulnerability

Use [GitHub private vulnerability reporting](https://github.com/ojesusmp/codex-hud/security/advisories/new). Do not open a public issue for a suspected vulnerability.

Include the affected version, operating system, reproduction steps, expected behavior and impact. Remove session text, credentials, private paths, access tokens and other sensitive data before submitting evidence.

## Security boundaries

Codex HUD:

- reads on-device process metadata, Git state, system statistics and Codex configuration;
- parses only `token_count` events from the newest Codex session JSONL file;
- does not make network requests;
- does not read authentication or credential files;
- does not print raw session messages;
- invokes only documented local commands such as `git`, `codex`, `tmux` and optional `omx`;
- treats the optional `CODEX_HUD_MEMORY_STATUS` value as display text only.

The HUD inherits the permissions of the account that runs it. Review the source before installation and install only from a trusted revision.
