#!/usr/bin/env bash
set -euo pipefail
rm -f "$HOME/.local/bin/codex-hud" "$HOME/.local/bin/codo"
python3 - <<'PY'
from pathlib import Path
import re
home=Path.home()
tmux=home/'.tmux.conf'
if tmux.exists():
    s=tmux.read_text(); a='# CODEX-HUD+:START'; b='# CODEX-HUD+:END'
    if a in s and b in s: tmux.write_text((s.split(a,1)[0].rstrip()+'\n\n'+s.split(b,1)[1].lstrip()).strip()+'\n')
cfg=home/'.codex/config.toml'
if cfg.exists():
    s=cfg.read_text()
    s=re.sub(r'(?m)^# codex-hud:managed-status-line\nstatus_line\s*=.*\n?','',s,count=1)
    cfg.write_text(s)
PY
printf 'Removed CODEX HUD+ executables and managed configuration.\n'
