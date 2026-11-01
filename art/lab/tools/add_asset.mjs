#!/usr/bin/env node
// Add a Forge sprite made outside the Forge to the shared Library, the same way the Forge saves one.
//   node art/lab/tools/add_asset.mjs sprite.forge.json [--asset <asset_id> --state <state_key>]
//   node art/lab/tools/add_asset.mjs --list            (asset ids, names and states)
// Without --asset the sprite becomes a new asset; with it, a new version of that asset.
// Writes art/lab/hosted/library/asset-<hash>.forge.json and updates library.json. Commit both.
import {readFile,writeFile} from 'node:fs/promises';import {fileURLToPath} from 'node:url';import path from 'node:path';
import {sprite} from '../hosted/model.mjs';import {retainAsset,assetLibrary} from '../hosted/worker.mjs';
const repo=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'../../..');
const local={async file(p,ref,optional=false){try{return await readFile(path.join(repo,p),'utf8')}catch(e){if(optional)return null;throw e}}};
const args=process.argv.slice(2),opt=k=>{const i=args.indexOf(k);return i<0?undefined:args[i+1]};
if(args[0]==='--list'){const lib=await assetLibrary(local,'local');for(const a of lib.assets)console.log(a.id.padEnd(44),(a.category||'').padEnd(10),a.name,'· states:',a.states.map(s=>s.key||'(default)').join(', '));process.exit(0)}
if(!args[0])throw Error('Usage: add_asset.mjs sprite.forge.json [--asset <asset_id> --state <state_key>]');
const d=sprite(JSON.parse(await readFile(args[0],'utf8')),'ASSET');
for(const k of['asset_id','state_key','source_version','legacy_hash','id'])delete d[k];
if(opt('--asset')){d.asset_id=opt('--asset');d.state_key=opt('--state')||''}
const paths={},r=await retainAsset(local,d,'local',paths);
for(const[p,v]of Object.entries(paths))await writeFile(path.join(repo,p),v);
console.log('Added',r.id,'to asset',r.asset_id,r.state_key?'state '+r.state_key:'','\nFiles:',Object.keys(paths).join(', '));
