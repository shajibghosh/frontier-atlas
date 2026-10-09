'use strict';
(() => {
  const atlas = JSON.parse(document.getElementById('atlas-data').textContent);
  const entries = atlas.problems;
  const $ = id => document.getElementById(id);
  const html = value => String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const clean = value => String(value ?? '').normalize('NFKD').toLocaleLowerCase();
  const unique = arr => [...new Set(arr)].sort((a,b) => a.localeCompare(b));
  const storage = {
    get(key, fallback) { try { return JSON.parse(localStorage.getItem(key)) ?? fallback; } catch { return fallback; } },
    set(key, value) { try { localStorage.setItem(key, JSON.stringify(value)); } catch {} }
  };
  let favorites = new Set(storage.get('frontieratlas.saved.v1', []));
  let pageSize = 12;
  let sourceSize = 16;
  let compact = false;
  const D = ['Physics','Chemistry','Genetics','Psychology','Physiology'];
  const icons = {Physics:'◉',Chemistry:'⬡',Genetics:'⌘',Psychology:'◈',Physiology:'♡'};
  const filters = ['domain','topic','subtopic','status','route'];

  function fillSelect(id, values, allLabel) {
    const el = $(id), previous = el.value;
    el.innerHTML = `<option value="">${html(allLabel)}</option>` + values.map(v => `<option value="${html(v)}">${html(v)}</option>`).join('');
    el.value = values.includes(previous) ? previous : '';
  }
  function optionsFor(id) {
    const domain = $('domain').value, topic = $('topic').value;
    if (id === 'topic') return unique(entries.filter(p => !domain || p.domain === domain).map(p => p.topic));
    if (id === 'subtopic') return unique(entries.filter(p => (!domain || p.domain === domain) && (!topic || p.topic === topic)).map(p => p.subtopic));
    if (id === 'status') return unique(entries.map(p => p.status));
    return unique(entries.map(p => p.route));
  }
  function cascade(from) {
    if (from === 'domain') { fillSelect('topic',optionsFor('topic'),'All topics'); fillSelect('subtopic',optionsFor('subtopic'),'All subtopics'); }
    if (from === 'topic') fillSelect('subtopic',optionsFor('subtopic'),'All subtopics');
  }
  function matching() {
    const query = clean($('query').value.trim());
    const filtered = entries.filter(p => {
      if (filters.some(id => $(id).value && p[id] !== $(id).value)) return false;
      if ($('savedOnly').checked && !favorites.has(p.id)) return false;
      if (!query) return true;
      const refs = p.refs.map(key => atlas.sources[key]?.title ?? '');
      return clean([p.id,p.domain,p.topic,p.subtopic,p.title,p.question,p.justification,p.bottleneck,p.direction,p.first_test,p.route,p.status,...refs].join(' ')).includes(query);
    });
    if ($('sort').value === 'title') filtered.sort((a,b) => a.title.localeCompare(b.title));
    if ($('sort').value === 'domain') filtered.sort((a,b) => (a.domain+a.title).localeCompare(b.domain+b.title));
    return filtered;
  }
  function card(p) {
    const sources = p.refs.map(key => {
      const ref = atlas.sources[key];
      return `<a href="${html(ref.url)}" target="_blank" rel="noopener noreferrer" referrerpolicy="no-referrer">[${atlas.refnum[key]}] ${html(ref.title)} ↗</a>`;
    }).join('');
    return `<article class="problem-card" id="${html(p.id)}" aria-labelledby="title-${html(p.id)}">
      <div class="card-kicker"><span class="id-tag">${html(p.id)}</span><button type="button" class="save-btn ${favorites.has(p.id) ? 'saved':''}" data-save="${html(p.id)}" aria-label="${favorites.has(p.id)?'Remove saved':'Save'} ${html(p.id)}" title="Save this problem">${favorites.has(p.id)?'★':'☆'}</button></div>
      <h3 id="title-${html(p.id)}">${html(p.title)} <a class="problem-permalink" href="#${html(p.id)}" title="Link to ${html(p.id)}">#</a></h3>
      <div class="topic-path">${html(p.domain)} <span>/</span> ${html(p.topic)} <span>/</span> ${html(p.subtopic)}</div>
      <p class="card-q">${html(p.question)}</p>
      <p class="card-field"><strong>Why it matters:</strong> ${html(p.justification)}</p>
      <p class="card-field"><strong>Key bottleneck:</strong> ${html(p.bottleneck)}</p>
      <div class="status-row"><span class="status">${html(p.status)}</span><span class="status">${html(p.route)}</span></div>
      <details class="card-extra"><summary>Research direction and first test</summary><p><strong>Proposed investigation:</strong> ${html(p.direction)}</p><p><strong>First falsifiable milestone:</strong> ${html(p.first_test)}</p></details>
      <div class="ref-collection"><span>SOURCE${p.refs.length > 1?'S':''}</span>${sources}</div>
    </article>`;
  }
  function render() {
    const data = matching();
    $('results').classList.toggle('compact',compact);
    $('results').innerHTML = data.slice(0,pageSize).map(card).join('');
    $('resultCount').textContent = `${data.length} of ${entries.length} research problems`;
    $('savedCount').textContent = `${favorites.size} saved`;
    $('noResults').hidden = data.length !== 0;
    $('showMore').hidden = data.length <= pageSize;
    $('showMore').textContent = `Show more problems (${Math.min(data.length-pageSize,12)} more) ↓`;
    const active = filters.filter(id=>$(id).value).map(id=>$(`${id}`).value);
    if ($('query').value.trim()) active.unshift(`Search: ${$('query').value.trim()}`);
    if ($('savedOnly').checked) active.push('Saved only');
    $('activeFilters').innerHTML = active.map(x=>`<span class="active-filter">${html(x)}</span>`).join('');
    updateURL();
  }
  function updateURL() {
    if (!['http:','https:'].includes(location.protocol)) return;
    const params = new URLSearchParams();
    filters.forEach(f=>{if($(f).value)params.set(f,$(f).value);});
    // Search terms remain local and are never inserted into shareable URL query strings.
    if ($('sort').value !== 'default')params.set('sort',$('sort').value);
    if ($('savedOnly').checked)params.set('saved','1');
    const target = location.pathname + (params.toString()?`?${params}`:'') + location.hash;
    try { history.replaceState(null,'',target); } catch {}
  }
  function setFromURL() {
    const params = new URLSearchParams(location.search);
    const d = params.get('domain'); if(d && D.includes(d)) $('domain').value=d;
    cascade('domain');
    const t=params.get('topic'); if(t && [...$('topic').options].some(o=>o.value===t))$('topic').value=t;
    cascade('topic');
    for(const id of ['subtopic','status','route']) { const v=params.get(id); if(v && [...$(id).options].some(o=>o.value===v))$(id).value=v; }
    $('query').value='';
    const sort=params.get('sort'); if(['default','title','domain'].includes(sort)) $('sort').value=sort;
    $('savedOnly').checked=params.get('saved')==='1';
  }
  function reset() {
    $('query').value=''; filters.forEach(f=>$(f).value=''); cascade('domain'); $('savedOnly').checked=false; $('sort').value='default'; pageSize=12; render();
  }
  function download(content, filename, type) {
    const blob=new Blob([content],{type}); const url=URL.createObjectURL(blob);
    const anchor=document.createElement('a'); anchor.href=url;anchor.download=filename;document.body.appendChild(anchor);anchor.click();anchor.remove();setTimeout(()=>URL.revokeObjectURL(url),1000);
  }
  function csvValue(value) {
    let s=String(value??'');
    if (/^[\s]*[=+@\-]/.test(s)) s="'"+s; // spreadsheet formula-injection defense
    return '"'+s.replaceAll('"','""')+'"';
  }
  function exportProblems(format) {
    const subset=matching();
    const stem='frontieratlas-filtered-'+subset.length;
    if (format==='json') {
      const keys=[...new Set(subset.flatMap(p=>p.refs))];
      const obj={metadata:{...atlas.metadata, export_count:subset.length},problems:subset,sources:Object.fromEntries(keys.map(k=>[k,atlas.sources[k]])),refnum:Object.fromEntries(keys.map(k=>[k,atlas.refnum[k]]))};
      download(JSON.stringify(obj,null,2),stem+'.json','application/json;charset=utf-8');
    } else if(format==='csv') {
      const cols=['id','domain','topic','subtopic','title','question','justification','bottleneck','direction','first_test','status','route','references'];
      const rows=[cols.map(csvValue).join(',')];
      for(const p of subset){const r={...p,references:p.refs.map(k=>atlas.sources[k].url).join('; ')};rows.push(cols.map(c=>csvValue(r[c])).join(','));}
      download('\uFEFF'+rows.join('\r\n')+'\r\n',stem+'.csv','text/csv;charset=utf-8');
    } else if(format==='md') {
      const rows=['# FrontierAtlas · Selected research problems','','Research questions compiled '+atlas.metadata.as_of+'. Proposed directions are not proven results.',''];
      for(const p of subset){rows.push(`## ${p.id} · ${p.title}`,'',`**${p.domain} / ${p.topic} / ${p.subtopic}** · ${p.status}`,'',`**Open question:** ${p.question}`,'',`**Why it matters:** ${p.justification}`,'',`**Bottleneck:** ${p.bottleneck}`,'',`**Research direction:** ${p.direction}`,'',`**First test:** ${p.first_test}`,'','**Sources:**',...p.refs.map(k=>`- [${atlas.sources[k].title}](${atlas.sources[k].url})`),'');}
      download(rows.join('\n'),stem+'.md','text/markdown;charset=utf-8');
    }
  }
  function renderSources() {
    const query=clean($('sourceSearch').value.trim());
    const pairs=Object.entries(atlas.sources).sort((a,b)=>atlas.refnum[a[0]]-atlas.refnum[b[0]]);
    const filtered=pairs.filter(([key,s])=>clean([`R${atlas.refnum[key]}`,s.title,s.kind,s.url].join(' ')).includes(query));
    $('sourceList').innerHTML=filtered.slice(0,sourceSize).map(([key,s])=>`<div class="reference-entry"><b>R${atlas.refnum[key]}</b><div><a href="${html(s.url)}" target="_blank" rel="noopener noreferrer" referrerpolicy="no-referrer">${html(s.title)} ↗</a><p>${html(s.kind)} · ${entries.filter(p=>p.refs.includes(key)).length} related problem(s)</p></div></div>`).join('');
    $('sourceCount').textContent=`${filtered.length} references`;
    $('showSources').hidden=filtered.length<=sourceSize;
    $('showSources').textContent=`Show more references (${Math.min(filtered.length-sourceSize,16)} more) ↓`;
  }
  function init() {
    fillSelect('domain',D,'All domains');
    fillSelect('topic',optionsFor('topic'),'All topics');
    fillSelect('subtopic',optionsFor('subtopic'),'All subtopics');
    fillSelect('status',optionsFor('status'),'All classifications');
    fillSelect('route',optionsFor('route'),'All approaches');
    setFromURL();
    $('domainTiles').innerHTML=D.map(d=>`<button type="button" class="discipline-tile" data-domain="${html(d)}"><span class="domain-icon">${icons[d]}</span><strong>${html(d)}<span class="arrow">↗</span></strong><small>20 questions · 5 topics</small></button>`).join('');
    $('domainTiles').addEventListener('click',e=>{const b=e.target.closest('[data-domain]'); if(!b)return; reset();$('domain').value=b.dataset.domain; cascade('domain');render();$('explorer').scrollIntoView({behavior:'smooth'});});
    $('query').addEventListener('input',()=>{pageSize=12;render()});
    filters.forEach(f=>$(f).addEventListener('change',()=>{cascade(f);pageSize=12;render()}));
    $('sort').addEventListener('change',()=>{pageSize=12;render()});
    $('savedOnly').addEventListener('change',()=>{pageSize=12;render()});
    ['reset','emptyReset'].forEach(id=>$(id).addEventListener('click',reset));
    $('showMore').addEventListener('click',()=>{pageSize+=12;render()});
    $('results').addEventListener('click',e=>{const b=e.target.closest('[data-save]');if(!b)return;const id=b.dataset.save;if(favorites.has(id))favorites.delete(id);else favorites.add(id);storage.set('frontieratlas.saved.v1',[...favorites]);render()});
    $('compactView').addEventListener('click',()=>{compact=true;$('gridView').classList.remove('active');$('compactView').classList.add('active');$('gridView').setAttribute('aria-pressed','false');$('compactView').setAttribute('aria-pressed','true');render()});
    $('gridView').addEventListener('click',()=>{compact=false;$('gridView').classList.add('active');$('compactView').classList.remove('active');$('gridView').setAttribute('aria-pressed','true');$('compactView').setAttribute('aria-pressed','false');render()});
    $('exportButton').addEventListener('click',()=>{$('exportMenu').hidden=!$('exportMenu').hidden;$('exportButton').setAttribute('aria-expanded',String(!$('exportMenu').hidden))});
    $('exportMenu').addEventListener('click',e=>{const b=e.target.closest('[data-export]');if(!b)return;exportProblems(b.dataset.export);$('exportMenu').hidden=true;$('exportButton').setAttribute('aria-expanded','false')});
    document.addEventListener('click',e=>{if(!e.target.closest('.results-controls')){$('exportMenu').hidden=true;$('exportButton').setAttribute('aria-expanded','false')}});
    $('sourceSearch').addEventListener('input',()=>{sourceSize=16;renderSources()});
    $('showSources').addEventListener('click',()=>{sourceSize+=16;renderSources()});
    const oldTheme=storage.get('frontieratlas.theme.v1','light'); document.documentElement.dataset.theme=oldTheme==='dark'?'dark':'light';
    $('themeToggle').addEventListener('click',()=>{let t=document.documentElement.dataset.theme==='dark'?'light':'dark';document.documentElement.dataset.theme=t;storage.set('frontieratlas.theme.v1',t)});
    document.addEventListener('keydown',e=>{if(e.key==='/'&&!e.ctrlKey&&!e.metaKey&&!/INPUT|TEXTAREA|SELECT/.test(document.activeElement.tagName)){e.preventDefault();$('query').focus();$('explorer').scrollIntoView({behavior:'smooth'})} if(e.key==='Escape'){$('exportMenu').hidden=true;$('exportButton').setAttribute('aria-expanded','false')}});
    render();renderSources();
    if(/^#(P\d{2}|C\d{2}|G\d{2}|PS\d{2}|PH\d{2})$/.test(location.hash)){
      const target=location.hash.slice(1);
      const idx=entries.findIndex(p=>p.id===target);
      if(idx>=0 && ![...filters].some(x=>$(x).value)&&!$('query').value){pageSize=Math.max(pageSize,idx+1);render();requestAnimationFrame(()=>$(target)?.scrollIntoView());}
    }
  }
  init();
})();
