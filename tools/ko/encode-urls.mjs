import fs from 'fs';
const HAN = /https?:\/\/[^\s<>"()]*[\uac00-\ud7a3][^\s<>"()]*/g;
let total = 0;
for (const f of fs.readdirSync('book').filter(x => x.endsWith('.md'))) {
  const p = 'book/' + f;
  let t = fs.readFileSync(p, 'utf8'), n = 0;
  t = t.replace(HAN, m => {
    const tail = (m.match(/[；;，、。·）】」』]+$/) || [''])[0];
    const core = tail ? m.slice(0, m.length - tail.length) : m;
    n++; return encodeURI(core) + tail;
  });
  if (n) { fs.writeFileSync(p, t); console.log(p, 'encoded', n); total += n; }
}
console.log('total', total);
