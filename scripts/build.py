#!/usr/bin/env python3
"""Compile self-contained static site. Uses Python standard library only."""
from pathlib import Path
import base64
import hashlib
import json
ROOT=Path(__file__).resolve().parents[1]
template=(ROOT/'src/index.template.html').read_text(encoding='utf-8')
style=(ROOT/'src/style.css').read_text(encoding='utf-8')
js=(ROOT/'src/app.js').read_text(encoding='utf-8')
data=json.loads((ROOT/'data/atlas.json').read_text(encoding='utf-8'))
serialized=json.dumps(data,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c').replace('>','\\u003e').replace('&','\\u0026')
def digest(value: str) -> str:
    return base64.b64encode(hashlib.sha256(value.encode('utf-8')).digest()).decode('ascii')

# Hash-based CSP allows only the exact local site logic and stylesheet.
# This works for offline files and GitHub Pages; no remote script dependency.
csp=(
    "default-src 'none'; "
    f"script-src 'sha256-{digest(js)}'; "
    f"style-src 'sha256-{digest(style)}'; "
    "script-src-attr 'none'; style-src-attr 'none'; "
    "img-src 'self' data:; font-src 'none'; connect-src 'none'; "
    "object-src 'none'; frame-src 'none'; worker-src 'none'; "
    "base-uri 'none'; form-action 'none'"
)
output=(template.replace('/*INLINE_CSP*/',csp)
       .replace('/*INLINE_CSS*/',style)
       .replace('/*INLINE_DATA*/',serialized)
       .replace('/*INLINE_JS*/',js))
assert '/*INLINE_' not in output
for path in [ROOT/'docs/index.html',ROOT/'FrontierAtlas_Interactive.html']:
    path.write_text(output,encoding='utf-8')
print(f'Built offline HTML site: {len(data["problems"])} problems, {len(data["sources"])} reference records')
