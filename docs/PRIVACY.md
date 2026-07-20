# Privacy

CODEX HUD+ is designed for on-device observability.

## Data read

- current user, hostname and working directory;
- Git repository name, branch and dirty state;
- Codex model and reasoning configuration;
- the newest Codex `token_count` telemetry event;
- Linux memory, process, load, disk and uptime statistics;
- counts and status summaries from optional tmux and OMX integrations.

## Data not read

- raw prompt or response text for display;
- GitHub, OpenAI or other credential stores;
- SSH keys, cookies, API keys or password files;
- arbitrary files outside the documented configuration/state paths.

## Network behavior

The executable makes no network requests. Optional commands it invokes may have their own behavior; the HUD uses only local status/version operations.

## Public bug reports

Do not publish raw session files or complete environment dumps. Redact personal names, machine names, addresses, repository names, paths, account identifiers and credentials.
