#!/usr/bin/env python3
"""Heuristic public-release and local-search security checks; stdlib only.

This check is NOT a substitute for reviewing files before public publication.
"""
import base64
import hashlib
import json
import re
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]
problems = []
allowed_dirs = {'.github', 'assets', 'data', 'docs', 'scripts', 'src', 'tests'}
allowed_root = {
    '.gitignore', 'README.md', 'CHANGELOG.md',
    'LICENSE', 'LICENSE-CONTENT.md', 'CITATION.cff',
    'SECURITY.md', 'FrontierAtlas_Interactive.html'
}
for p in sorted(root.rglob('*')):
    if not p.is_file():
        continue
    rel = p.relative_to(root)
    parts = rel.parts
    if '.git' in parts or '__pycache__' in parts or '.pytest_cache' in parts:
        continue
    if len(parts) == 1 and rel.name not in allowed_root:
        problems.append(f'unexpected root file: {rel}')
    if len(parts) > 1 and parts[0] not in allowed_dirs:
        problems.append(f'unapproved directory: {rel}')
    if re.search(r'(^|/)(\.env(?:\..*)?|id_rsa.*|id_ed25519.*|credentials[^/]*\.json)$', rel.as_posix(), re.I):
        problems.append(f'credential-like filename: {rel}')
    if p.suffix.lower() in {'.docx','.pdf','.pem','.key','.p12','.pfx','.sqlite','.sqlite3','.db'}:
        problems.append(f'private/non-web artifact requires review: {rel}')
    if p.stat().st_size > 5 * 1024 * 1024:
        problems.append(f'oversize file requires review: {rel}')
    if p.suffix.lower() in {'.py','.md','.yml','.yaml','.html','.js','.css','.json','.csv','.cff','.txt'} or rel.name == 'LICENSE':
        content = p.read_text('utf-8-sig',errors='replace')
        patterns = {
            'private key block': r'-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----',
            'AWS access key': r'\b(?:AKIA|ASIA)[0-9A-Z]{16}\b',
            'GitHub credential': r'\b(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})\b',
            'Slack token': r'\bxox[baprs]-[0-9A-Za-z-]{20,}\b',
            'OpenAI-style secret': r'\bsk-(?:proj-)?[A-Za-z0-9_-]{32,}\b',
        }
        # This Python script intentionally contains these detection patterns.
        if rel.as_posix() != 'scripts/prepublish_audit.py':
            for label, pattern in patterns.items():
                if re.search(pattern,content):
                    problems.append(f'possible {label}: {rel}')

app = (root / 'src/app.js').read_text(encoding='utf-8')
css = (root / 'src/style.css').read_text(encoding='utf-8')
page = (root / 'docs/index.html').read_text(encoding='utf-8')
for name, source in [('script',app),('style',css)]:
    expected = base64.b64encode(hashlib.sha256(source.encode('utf-8')).digest()).decode('ascii')
    if f"'sha256-{expected}'" not in page:
        problems.append(f'Content Security Policy missing correct {name} SHA-256 hash')
if "connect-src 'none'" not in page or "default-src 'none'" not in page:
    problems.append('CSP does not prohibit non-authorized network connections')
if "'unsafe-inline'" in page or "'unsafe-eval'" in page:
    problems.append('CSP contains an unsafe JavaScript/style directive')
if any(s in app for s in ('fetch(', 'XMLHttpRequest(', 'sendBeacon(', 'eval(', 'new Function(')):
    problems.append('Browser logic includes network request or dynamic code evaluation')
if '<script src=' in page or '<iframe ' in page or '<link rel="stylesheet"' in page:
    problems.append('Unexpected external executable or embedded content in HTML')
if (root / 'docs/index.html').read_bytes() != (root / 'FrontierAtlas_Interactive.html').read_bytes():
    problems.append('GitHub Pages and offline outputs differ')

atlas = json.loads((root / 'data/atlas.json').read_text(encoding='utf-8'))
for key, source in atlas['sources'].items():
    url = source['url'].strip()
    if not url.startswith('https://') or re.match(r'^https://(?:localhost|127\.|10\.|192\.168\.|172\.(?:1[6-9]|2\d|3[01])\.)',url,re.I):
        problems.append(f'non-public / non-HTTPS source URL: {key}')

if problems:
    print('FAIL: publication audit found',len(problems),'issue(s)')
    for issue in problems:
        print(' -',issue)
    sys.exit(1)
print('PASS: public-file allowlist, heuristic credential scan, CSP hashes, local-only browser code, HTTPS bibliography, and site parity.')
print('WARNING: heuristic screening is not a security guarantee. Review staged files and Git history before publishing.')
