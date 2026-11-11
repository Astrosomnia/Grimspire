import test from 'node:test';
import assert from 'node:assert/strict';
import {sprite, ROOT, LAB, DEFAULTS} from './model.mjs';
import {preview, save, saveAsset, openAsset} from './worker.mjs';

// A small embedded PNG exercises the same validation and storage path as art
// without depending on mutable library or revision files.
const PNG='data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR4AWPIy8v7DwAE4gJKkLFQhwAAAABJRU5ErkJggg==';
const makeSprite=()=>({forge:1,code:'K05',name:'Bridge height test',w:1,h:1,fps:8,markers:{},frames:[{body:PNG,height:PNG}]});

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

test('height is optional, frame-specific and validated like other PNG layers',()=>{
  const old=makeSprite();delete old.frames[0].height;
  assert.doesNotThrow(()=>sprite(old,'K05'));
  assert.equal(old.frames[0].height,undefined);
  const d=makeSprite();d.frames.push({body:PNG,height:null});
  assert.equal(sprite(d,'K05').frames[0].height,PNG);
  assert.equal(d.frames[1].height,null);
  d.frames[1].height='https://example.invalid/height.png';
  assert.throws(()=>sprite(d,'K05'),/embedded PNGs/);
  d.frames[1].height='data:image/png;base64,bogus!';
  assert.throws(()=>sprite(d,'K05'),/Malformed PNG encoding/);
  const wrong=Buffer.from(PNG.slice(22),'base64');wrong.writeUInt32BE(2,16);
  d.frames[1].height='data:image/png;base64,'+wrong.toString('base64');
  assert.throws(()=>sprite(d,'K05'),/PNG size differs from canvas/);
});

test('authored height survives library save, reopen, unsaved preview and revision payload',async()=>{
  const g=new Repository(), input=makeSprite();
  const asset=await saveAsset(g,{expected_head:g.lab,sprite:input},{id:42,login:'tester'});
  const reopened=await openAsset(g,g.lab,asset.id);
  assert.equal(reopened.frames[0].height,PNG);
  const request={expected_head:g.lab,slot:'K05',sprite:reopened,settings:{...DEFAULTS},notes:'Height test',variant:'custom'};
  const html=await preview(g,request);
  assert.match(html,/"height":"data:image\/png;base64,/);
  const saved=await save(g,request,{id:42,login:'tester'});
  const payload=JSON.parse(g.files[ROOT+'/revisions/'+saved.revision+'/payload.json']);
  assert.equal(payload.assets.K05.frames[0].height,PNG);
});

test('stale editors cannot silently drop a map, while an explicit clear is allowed',async()=>{
  const g=new Repository(), original=await saveAsset(g,{expected_head:g.lab,sprite:makeSprite()},{id:42,login:'tester'});
  const loaded=await openAsset(g,g.lab,original.id);
  const stale=structuredClone(loaded);delete stale.frames[0].height;
  await assert.rejects(saveAsset(g,{expected_head:g.lab,sprite:stale},{id:42,login:'tester'}),/Refresh the Forge/);
  const request={expected_head:g.lab,slot:'K05',sprite:stale,settings:{...DEFAULTS},notes:'Old editor save',variant:'custom'};
  await assert.rejects(save(g,request,{id:42,login:'tester'}),/Refresh the Forge/);
  assert.equal(g.currentState.current,null);
  loaded.frames[0].height=null;
  const cleared=await saveAsset(g,{expected_head:g.lab,sprite:loaded},{id:42,login:'tester'});
  assert.equal((await openAsset(g,g.lab,cleared.id)).frames[0].height,null);
});

test('old editors can continue saving old assets that have no height map',async()=>{
  const g=new Repository(), old=makeSprite();delete old.frames[0].height;
  const saved=await saveAsset(g,{expected_head:g.lab,sprite:old},{id:42,login:'tester'});
  const reopened=await openAsset(g,g.lab,saved.id);
  assert.equal(reopened.frames[0].height,undefined);
  await assert.doesNotReject(saveAsset(g,{expected_head:g.lab,sprite:reopened},{id:42,login:'tester'}));
});

test('an old source version cannot erase a newer map after a library refresh',async()=>{
  const g=new Repository(), legacy=makeSprite();delete legacy.frames[0].height;
  const oldVersion=await saveAsset(g,{expected_head:g.lab,sprite:legacy},{id:42,login:'tester'});
  const opened=await openAsset(g,g.lab,oldVersion.id);
  const updated=structuredClone(opened);updated.frames[0].height=PNG;
  await saveAsset(g,{expected_head:g.lab,sprite:updated},{id:42,login:'tester'});
  await assert.rejects(saveAsset(g,{expected_head:g.lab,sprite:opened},{id:42,login:'tester'}),/Refresh the Forge/);
});
