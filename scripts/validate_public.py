#!/usr/bin/env python3
"""Validate public-release documentation, links, paths, and secret patterns."""
from __future__ import annotations
import pathlib, re, sys
ROOT=pathlib.Path(__file__).resolve().parents[1]
REQUIRED={
 'README.md','LICENSE','SECURITY.md','CONTRIBUTING.md','CODE_OF_CONDUCT.md','SUPPORT.md','CHANGELOG.md',
 'docs/ARCHITECTURE.md','docs/CONFIGURATION.md','docs/COMPATIBILITY.md','docs/PRIVACY.md','docs/TROUBLESHOOTING.md','docs/RELEASING.md','docs/FAQ.md',
 '.github/CODEOWNERS','.github/PULL_REQUEST_TEMPLATE.md','.github/ISSUE_TEMPLATE/bug_report.yml',
 '.github/ISSUE_TEMPLATE/feature_request.yml','.github/ISSUE_TEMPLATE/config.yml','.github/workflows/ci.yml',
}
TEXT_SUFFIXES={'.md','.py','.sh','.yml','.yaml','.toml','.txt','.cff',''}
SECRET_PATTERNS={
 'GitHub token':re.compile(r'(?:ghp_|github_pat_)[A-Za-z0-9_]{20,}'),
 'cloud access key':re.compile(r'AKIA[0-9A-Z]{16}'),
 'private key':re.compile(r'-----BEGIN [A-Z ]*PRIVATE KEY-----'),
 'credentialed URL':re.compile(r'https?://[^\s/:]+:[^\s/@]+@'),
}
ABSOLUTE_USER_PATH=re.compile(r'(?<![A-Za-z0-9])/(?:home|Users)/[A-Za-z0-9._-]+/')
PRIVATE_IPV4=re.compile(r'\b(?:10(?:\.\d{1,3}){3}|192\.168(?:\.\d{1,3}){2}|172\.(?:1[6-9]|2\d|3[01])(?:\.\d{1,3}){2}|100\.(?:6[4-9]|[7-9]\d|1[01]\d|12[0-7])(?:\.\d{1,3}){2})\b')
LINK=re.compile(r'\[[^\]]+\]\(([^)]+)\)')
errors=[]
for rel in sorted(REQUIRED):
    if not (ROOT/rel).is_file(): errors.append(f'missing required file: {rel}')
for path in ROOT.rglob('*'):
    if not path.is_file() or '.git' in path.parts or '__pycache__' in path.parts: continue
    if path.suffix not in TEXT_SUFFIXES: continue
    rel=path.relative_to(ROOT); text=path.read_text(errors='replace')
    if ABSOLUTE_USER_PATH.search(text): errors.append(f'user-specific absolute path: {rel}')
    if PRIVATE_IPV4.search(text): errors.append(f'private-network address: {rel}')
    for label,pattern in SECRET_PATTERNS.items():
        if pattern.search(text): errors.append(f'possible {label}: {rel}')
    if path.suffix=='.md':
        if not text.startswith('# '): errors.append(f'Markdown file lacks title: {rel}')
        for target in LINK.findall(text):
            target=target.split('#',1)[0]
            if not target or re.match(r'^[a-z]+://',target): continue
            if not (path.parent/target).resolve().exists(): errors.append(f'broken link in {rel}: {target}')
if errors:
    print('\n'.join(f'ERROR: {e}' for e in errors),file=sys.stderr); raise SystemExit(1)
print(f'PASS: public-release audit ({len(REQUIRED)} required files)')
