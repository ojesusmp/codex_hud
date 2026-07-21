#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BIN="$HOME/.local/bin"
MIN_PYTHON="3.10"
codex_command="${CODO_CODEX_COMMAND:-codex}"
codex_home="${CODEX_HOME:-$HOME/.codex}"
check_only=false
install_prerequisites=false

usage() {
    cat <<'EOF'
Usage: ./install.sh [--check] [--install-prerequisites]

  --check                  Verify requirements without changing anything.
  --install-prerequisites  Approve installation of missing prerequisites.
EOF
}

for arg in "$@"; do
    case "$arg" in
        --check) check_only=true ;;
        --install-prerequisites) install_prerequisites=true ;;
        -h|--help) usage; exit 0 ;;
        *) printf 'install.sh: unknown option: %s\n' "$arg" >&2; usage >&2; exit 2 ;;
    esac
done

python_is_supported() {
    command -v python3 >/dev/null 2>&1 && python3 - <<'PY' >/dev/null 2>&1
import sys
raise SystemExit(sys.version_info < (3, 10))
PY
}

missing=()
[[ "$(uname -s)" == Linux && -d /proc ]] || missing+=("Linux with /proc (this platform is not supported)")
python_is_supported || missing+=("Python $MIN_PYTHON or newer")
command -v "$codex_command" >/dev/null 2>&1 || missing+=("Codex CLI ($codex_command)")
command -v tmux >/dev/null 2>&1 || missing+=("tmux")

print_missing() {
    printf 'Codex HUD prerequisite check found:\n' >&2
    local item
    for item in "${missing[@]}"; do
        printf '  - missing: %s\n' "$item" >&2
    done
}

install_system_packages() {
    local packages=("$@")
    ((${#packages[@]})) || return 0

    local elevate=()
    if ((EUID != 0)); then
        if ! command -v sudo >/dev/null 2>&1; then
            printf 'Cannot install system prerequisites automatically: sudo was not found.\n' >&2
            return 1
        fi
        elevate=(sudo)
    fi

    if command -v apt-get >/dev/null 2>&1; then
        "${elevate[@]}" apt-get update
        "${elevate[@]}" apt-get install -y "${packages[@]}"
    elif command -v dnf >/dev/null 2>&1; then
        "${elevate[@]}" dnf install -y "${packages[@]}"
    elif command -v yum >/dev/null 2>&1; then
        "${elevate[@]}" yum install -y "${packages[@]}"
    elif command -v zypper >/dev/null 2>&1; then
        "${elevate[@]}" zypper --non-interactive install "${packages[@]}"
    elif command -v pacman >/dev/null 2>&1; then
        "${elevate[@]}" pacman -Sy --needed --noconfirm "${packages[@]}"
    elif command -v apk >/dev/null 2>&1; then
        "${elevate[@]}" apk add "${packages[@]}"
    else
        printf 'No supported package manager was found; install manually: %s\n' "${packages[*]}" >&2
        return 1
    fi
}

install_missing() {
    if [[ "$(uname -s)" != Linux || ! -d /proc ]]; then
        printf 'Codex HUD cannot install on this platform; Linux with /proc is required.\n' >&2
        return 1
    fi

    local packages=()
    python_is_supported || packages+=(python3)
    command -v tmux >/dev/null 2>&1 || packages+=(tmux)
    if ! command -v "$codex_command" >/dev/null 2>&1 && ! command -v curl >/dev/null 2>&1; then
        packages+=(curl)
    fi
    install_system_packages "${packages[@]}"

    if ! command -v "$codex_command" >/dev/null 2>&1; then
        if [[ "$codex_command" != codex ]]; then
            printf 'Cannot automatically install custom Codex command: %s\n' "$codex_command" >&2
            return 1
        fi
        printf 'Installing Codex CLI with the official OpenAI installer...\n'
        curl -fsSL https://chatgpt.com/codex/install.sh | sh
        hash -r
    fi
}

if ((${#missing[@]})); then
    print_missing
    if $check_only; then
        printf 'Prerequisite check failed; no changes were made.\n' >&2
        exit 1
    fi

    if ! $install_prerequisites; then
        if [[ -t 0 ]]; then
            printf 'Install the missing prerequisites now? [y/N] ' >&2
            read -r answer
            [[ "$answer" =~ ^[Yy]([Ee][Ss])?$ ]] || {
                printf 'Installation cancelled; no changes were made.\n' >&2
                exit 1
            }
        else
            printf 'Approval is required before installing prerequisites.\n' >&2
            printf 'Review the list, then rerun: ./install.sh --install-prerequisites\n' >&2
            exit 1
        fi
    fi
    install_missing

    missing=()
    python_is_supported || missing+=("Python $MIN_PYTHON or newer")
    command -v "$codex_command" >/dev/null 2>&1 || missing+=("Codex CLI ($codex_command)")
    command -v tmux >/dev/null 2>&1 || missing+=("tmux")
    if ((${#missing[@]})); then
        print_missing
        printf 'Prerequisite installation did not make every requirement available; HUD installation stopped.\n' >&2
        exit 1
    fi
fi

if $check_only; then
    printf 'Codex HUD prerequisites are ready: Linux, Python %s+, Codex CLI, and tmux.\n' "$MIN_PYTHON"
    exit 0
fi

mkdir -p "$BIN" "$codex_home"
install -m 700 "$ROOT/bin/codex-hud" "$BIN/codex-hud"
install -m 700 "$ROOT/bin/codo" "$BIN/codo"
python3 - <<'PY'
from pathlib import Path
import os
import re
home=Path.home(); codex_home=Path(os.environ.get('CODEX_HOME', home/'.codex')); cfg=codex_home/'config.toml'; text=cfg.read_text() if cfg.exists() else ''
marker='# codex-hud:managed-status-line'
line='status_line = ["current-dir", "model-with-reasoning", "codex-version", "git-branch", "context-remaining", "used-tokens", "five-hour-limit", "weekly-limit", "session-id"]'
if re.search(r'(?m)^status_line\s*=',text):
    if marker in text:
        text=re.sub(r'(?m)^# codex-hud:managed-status-line\nstatus_line\s*=.*$',marker+'\n'+line,text,count=1)
    else:
        print('Preserved existing user-owned Codex status_line.')
else:
    if '[tui]' in text: text=text.replace('[tui]','[tui]\n'+marker+'\n'+line,1)
    else: text=text.rstrip()+'\n\n[tui]\n'+marker+'\n'+line+'\n'
cfg.write_text(text)

tmux=home/'.tmux.conf'; old=tmux.read_text() if tmux.exists() else ''
start='# CODEX-HUD:START'; end='# CODEX-HUD:END'; exe=home/'.local/bin/codex-hud'
legacy_start='# CODEX-HUD+:START'; legacy_end='# CODEX-HUD+:END'
block=f'''# CODEX-HUD:START
set -g status on
set -g status-position bottom
set -g status-interval 5
set -g status-style "bg=#111827,fg=#d1d5db"
set -g status-left-length 70
set -g status-right-length 190
set -g status-left "#[fg=#55d7a0,bold]#(id -un)@#H #[fg=#60a5fa][#S:#I.#P] #[fg=#d1d5db]#{{pane_current_path}} "
set -g status-right "#[fg=#a7f3d0]#({exe} --compact) #[fg=#fbbf24]%Y-%m-%d %H:%M:%S"
set -g window-status-format "#[fg=#64748b] #I:#W "
set -g window-status-current-format "#[fg=#f8fafc,bold] #I:#W* "
# CODEX-HUD:END'''
if legacy_start in old and legacy_end in old:
    old=old.split(legacy_start,1)[0].rstrip()+'\n\n'+old.split(legacy_end,1)[1].lstrip()
if start in old and end in old:
    pre=old.split(start,1)[0].rstrip(); post=old.split(end,1)[1].lstrip(); new='\n\n'.join(x for x in (pre,block,post) if x)+'\n'
else: new=(old.rstrip()+'\n\n'+block+'\n').lstrip()
tmux.write_text(new)
PY
chmod 600 "$codex_home/config.toml"
chmod 644 "$HOME/.tmux.conf"
if [[ -n "${TMUX:-}" ]]; then tmux source-file "$HOME/.tmux.conf"; fi
printf 'Installed Codex HUD (heads-up display):\n  HUD: %s\n  launcher: %s\nRestart Codex once, then run: codo\n' "$BIN/codex-hud" "$BIN/codo"
