import test from 'node:test';import assert from 'node:assert/strict';import {readFile} from 'node:fs/promises';import {sprite,sha,ROOT,LAB} from './model.mjs';import {saveAsset,save,openAsset,assetIndex} from './worker.mjs';
const root=new URL('../../../',import.meta.url),read=p=>readFile(new URL(p,root),'utf8');
const catalog=JSON.parse(await read(ROOT+'/assets.json'));
test('Every indexed source loads with matching hashes, layers, frame sizes and anchors',async()=>{for(const e of catalog.entries){const raw=await read(e.path);assert.equal(await sha(raw),e.sha256,e.id);sprite(JSON.parse(raw),'ASSET')}assert(catalog.entries.some(e=>e.id==='single-gun-arm-v001'));assert(catalog.entries.some(e=>e.id==='game-trooper-walk'&&e.frame_count===4))});
class Store{
 constructor(){this.headValue='a'.repeat(40);this.files={};this.stateValue={current:null,revisions:[]}}
 head(){return this.headValue}state(){return structuredClone(this.stateValue)}
 async file(p,ref,optional){return this.files[p]??(optional?null:read(p))}
 async append(state,files,parent){assert.equal(parent,this.headValue);Object.assign(this.files,files);this.stateValue=state;this.headValue=(parseInt(this.headValue[0],16)+1).toString(16).repeat(40);return this.headValue}
}
test('Independent saves retain different sprites and all versions; stale saves are refused',async()=>{const g=new Store(),d=JSON.parse(await read(ROOT+'/catalog/single-gun-arm-v001.forge.json'));
 const a=await saveAsset(g,{expected_head:g.headValue,sprite:d},{login:'test'});const before=g.headValue;
 d.name='Changed arm';const b=await saveAsset(g,{expected_head:g.headValue,sprite:d},{login:'test'});assert.notEqual(a.id,b.id);
 const entries=await assetIndex(g,g.headValue);assert(entries.some(e=>e.id===a.id));assert(entries.some(e=>e.id===b.id));assert.equal((await openAsset(g,g.headValue,a.id)).name,'Gun arm · single foreground sprite');
 await assert.rejects(saveAsset(g,{expected_head:before,sprite:d},{}),/Another update/);
 await assert.rejects(openAsset(g,g.headValue,'../../secret'),/no longer exists/);
});
