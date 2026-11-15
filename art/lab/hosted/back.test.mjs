import test from 'node:test';
import assert from 'node:assert/strict';
import {sprite, ROOT, LAB, DEFAULTS} from './model.mjs';
import {preview, save, saveAsset, openAsset} from './worker.mjs';

// The Back layer (14 Nov 2026): non-solid art drawn behind a set piece. Optional, validated like any PNG
// layer, kept through save, reopen and the revision payload; an old tab that omits it can't silently drop it.
const PNG='data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR4AWPIy8v7DwAE4gJKkLFQhwAAAABJRU5ErkJggg==';
const makeSprite=()=>({forge:1,code:'K05',name:'Bridge back test',w:1,h:1,fps:8,markers:{},frames:[{body:PNG,back:PNG}]});
class Repository {
  constructor(){this.files={};this.lab='test-lab-head';this.main='test-main-head';this.currentState={schema:1,current:null,revisions:[],integrations:[]}}
  async head(branch){return branch===LAB?this.lab:this.main}
  async state(){return structuredClone(this.currentState)}
  async file(path,ref,optional=false){
    if(path==='index.html')return '<!doctype html>\n// BEGIN GRIMSPIRE_ART_RUNTIME\n// END GRIMSPIRE_ART_RUNTIME\n';
    if(path in this.files)return this.files[path];
    if(optional)return null;
    throw Error('Missing fixture: '+path);
  }
  async append(state,paths){Object.assign(this.files,paths);this.currentState=state;this.lab='saved-lab-head';return this.lab}
}
test('back is optional and validated like other PNG layers',()=>{
  const old=makeSprite();delete old.frames[0].back;assert.doesNotThrow(()=>sprite(old,'K05'));
  const d=makeSprite();assert.equal(sprite(d,'K05').frames[0].back,PNG);
  d.frames[0].back='https://example.invalid/back.png';assert.throws(()=>sprite(d,'K05'),/embedded PNGs/);
});
test('back survives library save, reopen, preview and revision payload',async()=>{
  const g=new Repository();
  const asset=await saveAsset(g,{expected_head:g.lab,sprite:makeSprite()},{id:42,login:'tester'});
  const reopened=await openAsset(g,g.lab,asset.id);assert.equal(reopened.frames[0].back,PNG);
  const request={expected_head:g.lab,slot:'K05',sprite:reopened,settings:{...DEFAULTS},notes:'Back test',variant:'custom'};
  assert.match(await preview(g,request),/"back":"data:image\/png;base64,/);
  const saved=await save(g,request,{id:42,login:'tester'});
  assert.equal(JSON.parse(g.files[ROOT+'/revisions/'+saved.revision+'/payload.json']).assets.K05.frames[0].back,PNG);
});
test('a stale editor cannot silently drop a Back layer',async()=>{
  const g=new Repository(),original=await saveAsset(g,{expected_head:g.lab,sprite:makeSprite()},{id:42,login:'tester'});
  const stale=structuredClone(await openAsset(g,g.lab,original.id));delete stale.frames[0].back;
  await assert.rejects(saveAsset(g,{expected_head:g.lab,sprite:stale},{id:42,login:'tester'}),/Back layer/);
});
