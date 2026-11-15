import { readFile } from 'node:fs/promises';
import vm from 'node:vm';
import assert from 'node:assert/strict';

// Back layer (14 Nov 2026): the editor keeps it through editing, snapshots, frame copies, save, load and resize.
export async function runChecks() {
  const src = await readFile(new URL('../art/lab/forge.html', import.meta.url), 'utf8');
  const scripts = [...src.matchAll(/<script(?:\s[^>]*)?>([\s\S]*?)<\/script>/g)].map(m => m[1]).filter(Boolean);
  for (const script of scripts) new vm.Script(script);
  const lines = src.split('\n');
  const get = prefix => { const line = lines.find(x => x.startsWith(prefix)); assert.ok(line, prefix); return line; };
  const defs = ['const LK=', 'const emptyPx=', 'const newFrame=', 'const cp=', 'function snapDoc()', 'function addFrame(dup)', 'function serialise()', 'function paintCol()'].map(get).join('\n');
  const box = {Uint8ClampedArray, JSON, Math, Date, ART:12, hex2rgb:()=>[100,150,200],
    pxToURL:p=>p.some((v,i)=>i%4===3&&v)?Array.from(p):null, commitFloat(){},pushDoc(){},buildStrip(){},changed(){},outcome:[]};
  vm.runInNewContext(`let doc={w:2,h:2,frames:[],markers:{},base:1,game_scale:1},fi=0,layer='back',col='#123456';\n${defs}\n`+
    `if(!LK.includes('back'))throw Error('back not a layer');doc.frames.push(newFrame());doc.frames[0].back.set([90,40,20,255],0);`+
    `if(paintCol().join()!=='100,150,200')throw Error('back paints in colour');`+
    `const snap=snapDoc();doc.frames[0].back[0]=200;if(snap.frames[0].back[0]!==90)throw Error('snapshot aliases back');`+
    `doc.frames[0].back[0]=90;addFrame(true);if(doc.frames[1].back[0]!==90||doc.frames[1].back===doc.frames[0].back)throw Error('back frame duplication');`+
    `if(serialise().frames[0].back[0]!==90)throw Error('missing serialized back');doc.frames[0].back.fill(0);if(serialise().frames[0].back!==null)throw Error('blank back fallback');outcome.push('ok')`,box);
  assert.equal(box.outcome.length,1);
  const cut=(start,end)=>{const i=src.indexOf(start),j=src.indexOf(end,i);assert.ok(i>=0&&j>i,start);return src.slice(i,j)};
  const des=cut('async function deserialise(o,id)','\nfunction draftSave()');
  const desBox={Uint8ClampedArray,Math,outcome:[]};
  await vm.runInNewContext(`let doc,fi,undoS=[],redoS=[],sel,float;const cache={clear(){}},noMarks=()=>({}),splitCode=(a,b)=>[a||'',b||''],clamp=(v,a,b)=>Math.max(a,Math.min(b,v));`+
    `const urlToPx=async(u,w,h)=>u?Uint8ClampedArray.from(u):new Uint8ClampedArray(w*h*4);const updDocUI=()=>{},buildStrip=()=>{},fit=()=>{},updZoom=()=>{},palCheck=()=>{},need=()=>{};\n${des}\n`+
    `(async()=>{await deserialise({w:1,h:1,name:'legacy',frames:[{body:[3,3,3,255]}]});if(doc.frames[0].back.some(Boolean))throw Error('legacy fallback');`+
    `await deserialise({w:1,h:1,name:'new',frames:[{body:[3,3,3,255],back:[60,50,40,255]}]});if(doc.frames[0].back[0]!==60)throw Error('back lost');outcome.push('ok')})()`,desBox);
  assert.equal(desBox.outcome.length,1);
  assert.match(src, /parts\.push\(\['back','back'\]\)/);
  return 'PASS: back layer edits, saves, loads and exports';
}
