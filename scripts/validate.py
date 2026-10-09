#!/usr/bin/env python3
"""Validate coverage, source mappings, and static-site build consistency."""
import json,re,sys
from pathlib import Path
from urllib.parse import urlparse
from collections import Counter
ROOT=Path(__file__).resolve().parents[1]
a=json.loads((ROOT/'data/atlas.json').read_text(encoding='utf-8'))
p=a['problems'];sources=a['sources'];ids=[x['id'] for x in p]
errors=[]
def check(predicate,message):
    if not predicate: errors.append(message)
check(len(p)==100,'Atlas must have exactly 100 entries')
check(len(set(ids))==len(ids),'Problem IDs must be unique')
check(len(sources)==88,'Expected the 88-source reference index')
expected={'Physics':20,'Chemistry':20,'Genetics':20,'Psychology':20,'Physiology':20}
check(Counter(x['domain'] for x in p)==expected,'Incorrect domain distribution')
check(len({(x['domain'],x['topic']) for x in p})==25,'Expected 25 domain/topic pairs')
check(len({(x['domain'],x['topic'],x['subtopic']) for x in p})==50,'Expected 50 nested subtopics')
topic_counts=Counter((x['domain'],x['topic']) for x in p)
sub_counts=Counter((x['domain'],x['topic'],x['subtopic']) for x in p)
check(all(n==4 for n in topic_counts.values()),'Each topic must have four entries')
check(all(n==2 for n in sub_counts.values()),'Each subtopic must have two entries')
for x in p:
    for f in ('id','domain','topic','subtopic','title','question','justification','bottleneck','direction','first_test','status','route'):
        check(isinstance(x.get(f),str) and bool(x[f].strip()),f'{x["id"]}: missing field {f}')
    check(1<=len(x['refs'])<=4,f'{x["id"]}: expected 1–4 source keys')
    for ref in x['refs']: check(ref in sources, f'{x["id"]}: unknown reference {ref}')
for k,v in sources.items():
    check(all(v.get(f) for f in ('url','title','kind')),f'{k}: incomplete source record')
    uri=urlparse(v['url']); check(uri.scheme=='https' and bool(uri.netloc),f'{k}: HTTPS source URL required')
check(set(sources)==set(a['refnum']), 'Reference numbering does not cover all sources')
check(len(set(a['refnum'].values()))==len(sources),'Duplicate reference number')
page=ROOT/'docs/index.html'; standalone=ROOT/'FrontierAtlas_Interactive.html'
check(page.exists() and standalone.exists(),'Missing site output')
if page.exists() and standalone.exists():
    content=page.read_text(encoding='utf-8')
    check(content==standalone.read_text(encoding='utf-8'),'Site and standalone HTML differ')
    check('<script id="atlas-data"' in content,'Embedded structured data missing')
    check('/*INLINE_' not in content,'Unreplaced compilation placeholder')
    check(all(f'id="{id}"' in content for id in ('query','domain','topic','subtopic','status','route','results','sourceList')),'Missing interactive controls')
for path in ['README.md','CITATION.cff','LICENSE','LICENSE-CONTENT.md','docs/RESEARCH_CATALOG.md','data/problems.csv','data/references.csv']:
    check((ROOT/path).exists(),f'Missing {path}')
if errors:
    print('FAILED:',len(errors),'validation errors')
    for e in errors: print(' -',e)
    sys.exit(1)
print('PASS: 100 problems, 5 domains, 25 topics, 50 subtopics, 88 sources; citations, data, web build and essential repository files validated.')
print('NOTE: Structural validation does not verify scientific claims, live URLs, or peer-reviewed open status.')
