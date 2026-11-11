import { readFile } from 'node:fs/promises';
import vm from 'node:vm';
import assert from 'node:assert/strict';

export async function runChecks() {
  const src = await readFile(new URL('../art/lab/forge.html', import.meta.url), 'utf8');
  const scripts = [...src.matchAll(/<script(?:\s[^>]*)?>([\s\S]*?)<\/script>/g)].map(m => m[1]).filter(Boolean);
  for (const script of scripts) new vm.Script(script);
  const lines = src.split('\n');
  const get = prefix => { const line = lines.find(x => x.startsWith(prefix)); assert.ok(line, prefix); return line; };
  const defs = ['const LK=', 'const emptyPx=', 'const newFrame=', 'const cp=', 'function snapDoc()', 'function addFrame(dup)', 'function serialise()', 'function paintCol()'].map(get).join('\n');
  const box = {Uint8ClampedArray, JSON, Math, Date, ART:12, hex2rgb:()=>[100,150,200],
    pxToURL:p=>p.some((v,i)=>i%4===3&&v)?Array.from(p):null,
    commitFloat(){},pushDoc(){},buildStrip(){},changed(){},outcome:[]};
  vm.runInNewContext(`let doc={w:2,h:2,frames:[],markers:{},base:1,game_scale:1},fi=0,layer='height',col='#123456';\n${defs}\n`+
    `doc.frames.push(newFrame());doc.frames[0].height.set([80,80,80,255],0);`+
    `if(paintCol().some(v=>v!==141))throw Error('height must paint grey');`+
    `const snap=snapDoc();doc.frames[0].height[0]=200;if(snap.frames[0].height[0]!==80)throw Error('snapshot aliases height');`+
    `doc.frames[0].height[0]=80;addFrame(true);if(doc.frames[1].height[0]!==80||doc.frames[1].height===doc.frames[0].height)throw Error('height frame duplication');`+
    `if(serialise().frames[0].height[0]!==80)throw Error('missing serialized height');doc.frames[0].height.fill(0);if(serialise().frames[0].height!==null)throw Error('blank height fallback');outcome.push('editing/save/duplicate/snapshot')`,box);
  assert.equal(box.outcome.length,1);
  const cut=(start,end)=>{const i=src.indexOf(start),j=src.indexOf(end,i);assert.ok(i>=0&&j>i,start);return src.slice(i,j)};
  const des=cut('async function deserialise(o,id)','\nfunction draftSave()');
  const desBox={Uint8ClampedArray,Math,outcome:[]};
  await vm.runInNewContext(`let doc,fi,undoS=[],redoS=[],sel,float;const cache={clear(){}},noMarks=()=>({}),splitCode=(a,b)=>[a||'',b||''],clamp=(v,a,b)=>Math.max(a,Math.min(b,v));`+
    `const urlToPx=async(u,w,h)=>u?Uint8ClampedArray.from(u):new Uint8ClampedArray(w*h*4);const updDocUI=()=>{},buildStrip=()=>{},fit=()=>{},updZoom=()=>{},palCheck=()=>{},need=()=>{};\n${des}\n`+
    `(async()=>{await deserialise({w:1,h:1,name:'legacy',frames:[{body:[3,3,3,255]}]});if(doc.frames[0].height.some(Boolean))throw Error('legacy fallback');`+
    `await deserialise({w:1,h:1,name:'new',frames:[{body:[3,3,3,255],height:[128,128,128,255]}]});if(doc.frames[0].height[0]!==128||doc.frames[0].height[3]!==255)throw Error('height lost');outcome.push('legacy and authored load')})()`,desBox);
  assert.equal(desBox.outcome.length,1);
  const resize=cut('function resizeDoc(', '\n\nconst WEAPON_LIBRARY=');
  const resizeBox={Uint8ClampedArray,Math,outcome:[]};
  vm.runInNewContext(`let doc={w:1,h:1,base:0,markers:{},frames:[{}]},trace=null;const LK=['body','emis','trim','cloth','guts','height'];for(const k of LK)doc.frames[0][k]=new Uint8ClampedArray([7,7,7,255]);doc.frames[0].height.set([160,160,160,255]);`+
    `const commitFloat=()=>{},pushDoc=()=>{},cache={clear(){}},updDocUI=()=>{},buildStrip=()=>{},fit=()=>{},updZoom=()=>{},changed=()=>{},clamp=(v,a,b)=>Math.max(a,Math.min(b,v));\n${resize}\n`+
    `resizeDoc(3,3,'c');let p=doc.frames[0].height;if(p.length!==36||p[16]!==160||p[19]!==255||p[3]!==0)throw Error('height resize');outcome.push('resize')`,resizeBox);
  assert.equal(resizeBox.outcome.length,1);
  const bake=cut('function bakeTrace()', '// ---------- snapshots ----------');
  const bakeBox={Uint8ClampedArray,Math,outcome:[]};
  vm.runInNewContext(`let doc={w:1,h:1,frames:[{body:new Uint8ClampedArray(4),emis:new Uint8ClampedArray(4),guts:new Uint8ClampedArray(4),height:new Uint8ClampedArray(4)}]},fi=0,trace={x:0,y:0,r:0,s:1,img:{}},layer='height',sel=null,bkNeon=false,bkClean=false;`+
    `const $=s=>({value:s==='#bkCut'?128:'raw'}),rgb2hsl=()=>[0,0,0],PAL=[['stone',['#000000']]],hex2rgb=()=>[0,0,0],clamp=(x,a,b)=>Math.max(a,Math.min(b,x)),mkc=()=>({getContext:()=>({translate(){},rotate(){},scale(){},drawImage(){},getImageData(){return {data:new Uint8ClampedArray([100,150,200,255])}}})}),commitFloat=()=>{},insideR=()=>true,cp=a=>new Uint8ClampedArray(a),ramp=()=>['#000000'],pushPx=()=>{},touch=()=>{},status=()=>{};\n${bake}\n`+
    `bakeTrace();let h=doc.frames[0].height,b=doc.frames[0].body;if(h[0]!==141||h[1]!==141||h[2]!==141||h[3]!==255||b.some(Boolean))throw Error('trace isolation');outcome.push('trace isolation')`,bakeBox);
  assert.equal(bakeBox.outcome.length,1);
  assert.match(src, /height\/\$\{code\}\$\{i\?'\.f'\+\(i\+1\):''\}\.height\.png/);
  return 'PASS: editor parses; grayscale painting and trace, legacy load, save/blank fallback, frame copies, snapshots, resize, per-frame export names';
}
