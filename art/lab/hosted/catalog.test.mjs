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

test('Provenance migration groups every source and old registration, with explicit defaults and archive',async()=>{
 const {organiseAssets}=await import('./families.mjs');const saved=JSON.parse(await read(ROOT+'/library.json')),migration=JSON.parse(await read(ROOT+'/families.json'));
 const {docs,assets}=organiseAssets(catalog,saved,migration);
 assert.equal(docs.length,catalog.entries.length+saved.entries.length);assert.equal(assets.filter(f=>!f.archived).length,32);assert.equal(assets.filter(f=>f.archived).length,4);
 assert(docs.every(d=>!d.asset_id.startsWith('legacy-')));assert(docs.every(d=>d.w&&d.h&&d.frame_count));
 const ids=migration.assets.flatMap(f=>f.members.map(m=>m.id));assert.equal(new Set(ids).size,ids.length);
 for(let i=1;i<=8;i++){const code='W0'+i,f=assets.find(f=>f.code===code);assert.equal(f.current,`alt-${code}_aligned_v001.forge`);assert(f.versions.some(d=>d.id==='game-'+['mortar','rail','scatter','bolter','las','flamer','chain_old','fist'][i-1]))}
 const trooper=assets.find(f=>f.id==='asset-t01');assert.equal(trooper.states.length,8);assert.equal(trooper.current,'game-trooper-idle');assert(trooper.versions.some(d=>d.id==='walk-redrawn-v4-walk'));
 const minigun=assets.find(f=>f.id==='asset-w18');assert.equal(minigun.current,'game-minigun');assert(minigun.states.some(s=>s.key==='barrel_phase_0'));
 for(const f of assets)for(const id of Object.values(f.defaults))assert(f.versions.some(d=>d.id===id),id);
});
class CatalogStore extends Store{async file(p,ref,optional){return this.files[p]??read(p).catch(e=>{if(optional&&e.code==='ENOENT')return null;throw e})}}
test('Old-version edits keep asset identity; New with the same code creates another card; drafts do not approve art',async()=>{
 const {assetLibrary}=await import('./worker.mjs'),g=new CatalogStore();
 const old=await openAsset(g,g.headValue,'study-W01_grid.forge');old.name='My edited mortar';
 const first=await saveAsset(g,{expected_head:g.headValue,sprite:old},{});assert.equal(first.asset_id,'asset-w01');
 const reopened=await openAsset(g,g.headValue,first.id);reopened.notes='Another edit';const second=await saveAsset(g,{expected_head:g.headValue,sprite:reopened},{});assert.equal(second.asset_id,first.asset_id);
 let library=await assetLibrary(g,g.headValue),family=library.assets.find(f=>f.id==='asset-w01');assert.equal(family.current,second.id);assert.equal(family.states[0].baseline,'alt-W01_aligned_v001.forge');assert.equal(family.versions.at(-1).role,'draft');
 const fresh=structuredClone(old);delete fresh.asset_id;delete fresh.source_version;delete fresh.id;fresh.name='A different mortar';
 const created=await saveAsset(g,{expected_head:g.headValue,sprite:fresh},{});assert.notEqual(created.asset_id,first.asset_id);
 library=await assetLibrary(g,g.headValue);assert.equal(library.assets.filter(f=>!f.archived).length,33);
 const again=await openAsset(g,g.headValue,created.id);again.notes='same new asset';const next=await saveAsset(g,{expected_head:g.headValue,sprite:again},{});assert.equal(next.asset_id,created.asset_id);
});
test('Trooper edits retain animation state and preserve the other states and complete layers',async()=>{
 const {assetLibrary}=await import('./worker.mjs'),g=new CatalogStore(),walk=await openAsset(g,g.headValue,'game-trooper-walk');
 const original=structuredClone(walk.frames);walk.notes='Walk adjustment';const r=await saveAsset(g,{expected_head:g.headValue,sprite:walk},{});
 assert.equal(r.asset_id,'asset-t01');assert.equal(r.state_key,'walk');assert.deepEqual((await openAsset(g,g.headValue,r.id)).frames,original);
 const t=(await assetLibrary(g,g.headValue)).assets.find(f=>f.id==='asset-t01');assert.equal(t.current,'game-trooper-idle');assert.equal(t.states.find(s=>s.key==='walk').current,r.id);assert.equal(t.states.find(s=>s.key==='jump').current,'game-trooper-jump');
 walk.state_key='made-up';await assert.rejects(saveAsset(g,{expected_head:g.headValue,sprite:walk},{}),/animation state/);
});
test('Legacy saved-build payloads recover their family by exact content provenance after editing',async()=>{
 const g=new CatalogStore(),d=JSON.parse(await read(ROOT+'/catalog/saved-b915644502eac9699af2.forge.json'));
 d.legacy_hash=await sha(JSON.stringify(d));d.name='Revised old mortar';d.updated=Date.now();
 const r=await saveAsset(g,{expected_head:g.headValue,sprite:d},{});assert.equal(r.asset_id,'asset-w01');
});
