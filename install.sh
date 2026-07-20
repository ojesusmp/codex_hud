#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BIN="$HOME/.local/bin"
mkdir -p "$BIN" "$HOME/.codex"
install -m 700 "$ROOT/bin/codex-hud" "$BIN/codex-hud"
install -m 700 "$ROOT/bin/codo" "$BIN/codo"
python3 - <<'PY'
from pathlib import Path
import re
home=Path.home(); cfg=home/'.codex/config.toml'; text=cfg.read_text() if cfg.exists() else ''
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
start='# CODEX-HUD+:START'; end='# CODEX-HUD+:END'; exe=home/'.local/bin/codex-hud'
block=f'''# CODEX-HUD+:START
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
# CODEX-HUD+:END'''
if start in old and end in old:
    pre=old.split(start,1)[0].rstrip(); post=old.split(end,1)[1].lstrip(); new='\n\n'.join(x for x in (pre,block,post) if x)+'\n'
else: new=(old.rstrip()+'\n\n'+block+'\n').lstrip()
tmux.write_text(new)
PY
chmod 600 "$HOME/.codex/config.toml"
chmod 644 "$HOME/.tmux.conf"
if command -v tmux >/dev/null && [ -n "${TMUX:-}" ]; then tmux source-file "$HOME/.tmux.conf"; fi
printf 'Installed %s and %s\nRestart Codex once, then run: codo\n' "$BIN/codex-hud" "$BIN/codo"
