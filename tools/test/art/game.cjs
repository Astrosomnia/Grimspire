// Shared loader for the art renderer tests: reads the live game (index.html on main),
// its art runtime (between the GRIMSPIRE_ART_RUNTIME markers) and its LAB_PAYLOAD.
const fs=require('fs'),path=require('path');
const file=process.env.GRIMSPIRE_GAME||path.join(__dirname,'../../../index.html');
const source=fs.readFileSync(file,'utf8');
const A='// BEGIN GRIMSPIRE_ART_RUNTIME\n',B='// END GRIMSPIRE_ART_RUNTIME';
const runtime=source.slice(source.indexOf(A)+A.length,source.indexOf(B));
const line=source.split('\n').find(l=>l.startsWith('const LAB_PAYLOAD='));
const payload=JSON.parse(line.slice('const LAB_PAYLOAD='.length).replace(/;\s*$/,''));
if(!runtime.includes('labDraw')||!payload.assets)throw Error('Could not find the art runtime or payload in '+file);
module.exports={file,source,runtime,payload,doc:slot=>structuredClone(payload.assets[slot])};
