import fs from 'fs';
const src = fs.readFileSync('index.html','utf8');
const start = src.indexOf('function parseReadme');
const fn = src.slice(start, src.indexOf('\n}', start) + 2);
const COST_W = src.match(/const COST_W = \{.*?\};/s)[0];
const NUMS = src.match(/const NUMS = .*?;/)[0];
const XREF = src.match(/const XREF_RE = new RegExp\(.*?;/s)[0];
eval(COST_W + '\n' + NUMS + '\n' + XREF + '\n' + fn + '\nglobalThis.__P = parseReadme; globalThis.__X = XREF_RE;');
const parseReadme = globalThis.__P, XREF_RE = globalThis.__X;
const files = fs.readdirSync('book').filter(f=>f.endsWith('.md'));
const parseGlossary = (() => { const gs = src.indexOf('function parseGlossary'); const g = src.slice(gs, src.indexOf('\n}', gs) + 2); eval('let GLOSS=[];let GLOSS_RE=null;let GLOSS_BY={};\n' + g + '\nglobalThis.__G = parseGlossary;'); return globalThis.__G; })();
const readme = fs.readFileSync('README.md','utf8');
const bookLinks = [...new Set(Array.from(readme.matchAll(/\]\((book\/[^)]+\.md)\)/g), m => m[1]))].sort();
const onDisk = fs.readdirSync('book').filter(f=>f.endsWith('.md')&&!f.includes('-kr.md')).map(f=>'book/'+f).sort();
console.log('SEAM links==disk:', JSON.stringify(bookLinks)===JSON.stringify(onDisk), bookLinks.length+'/'+onDisk.length, bookLinks.filter(x=>!onDisk.includes(x)).concat(onDisk.filter(x=>!bookLinks.includes(x))));
const gloss = parseGlossary(readme); console.log('SEAM glossary:', gloss.length, 'first=', gloss[0]?.term);
let all=0, ratio={}, empt=0;
for(const f of files){
  const t = fs.readFileSync('book/'+f,'utf8');
  const secs = parseReadme(t);
  const ents = secs.flatMap(s=>s.entries);
  all += ents.length;
  for(const e of ents){ ratio[e.ratio]=(ratio[e.ratio]||0)+1; if(!e.cost||!e.gain||!e.src||!e.human) empt++; }
  console.log(f, 'secs='+secs.length, 'entries='+ents.length);
}
console.log('TOTAL', all, 'empty-field-entries', empt, 'ratio', JSON.stringify(ratio));
const X = (s)=>{ XREF_RE.lastIndex=0; const out=[]; let m; while((m=XREF_RE.exec(s))) out.push(m[0]); return out; };
for(const s of ['제13절 44항 참조','이 절 3항','제8~10항','12,13항','제9절','근로기준법 제26조','제1항만','见第 8 节第 16 条','本节第 3 条','第 9 节','제13절의 44항'])
  console.log('XREF', JSON.stringify(s), '->', JSON.stringify(X(s)));
