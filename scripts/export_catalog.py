#!/usr/bin/env python3
"""Regenerate distributable CSV and Markdown indexes from data/atlas.json."""
import csv,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
atlas=json.loads((ROOT/'data/atlas.json').read_text(encoding='utf-8'))
fields=['id','domain','topic','subtopic','title','question','justification','bottleneck','direction','first_test','status','route','references']
def csv_safe(value):
    """Treat cells as text in spreadsheet viewers, not executable formulas."""
    s=str(value)
    return "'"+s if re.match(r'^\s*[=+@\-]',s) else s
with (ROOT/'data/problems.csv').open('w',newline='',encoding='utf-8-sig') as file:
    writer=csv.DictWriter(file,fieldnames=fields); writer.writeheader()
    for p in atlas['problems']:
        row={k:p.get(k,'') for k in fields}
        row['references']='; '.join(atlas['sources'][s]['url'] for s in p['refs'])
        writer.writerow({key:csv_safe(value) for key,value in row.items()})
with (ROOT/'data/references.csv').open('w',newline='',encoding='utf-8-sig') as file:
    writer=csv.writer(file);writer.writerow(['ref_id','key','title','url','type','problem_ids'])
    for k,s in sorted(atlas['sources'].items(),key=lambda it:atlas['refnum'][it[0]]):
        writer.writerow([csv_safe(x) for x in [f'R{atlas["refnum"][k]}',k,s['title'],s['url'],s['kind'],'; '.join(p['id'] for p in atlas['problems'] if k in p['refs'])]])
lines=['# FrontierAtlas — Research Problem Catalog','',f'**Snapshot:** {atlas["metadata"]["as_of"]}  ','**Status:** Research synthesis, proposed investigations are not established solutions.','','## Problems','']
for p in atlas['problems']:
    lines.extend([f'### {p["id"]} · {p["title"]}','',f'**Domain:** {p["domain"]} · **Topic:** {p["topic"]} · **Subtopic:** {p["subtopic"]}  ',f'**Classification:** {p["status"]} · **Research approach:** {p["route"]}','','**Open question:** '+p['question'],'','**Scientific rationale:** '+p['justification'],'','**Bottleneck:** '+p['bottleneck'],'','**Research direction:** '+p['direction'],'','**First decisive test:** '+p['first_test'],'','**Sources:**',*[f'- [R{atlas["refnum"][r]}] [{atlas["sources"][r]["title"]}]({atlas["sources"][r]["url"]})' for r in p['refs']],''])
(ROOT/'docs/RESEARCH_CATALOG.md').write_text('\n'.join(lines),encoding='utf-8')
print('Exported CSV indexes and comprehensive Markdown catalog')
