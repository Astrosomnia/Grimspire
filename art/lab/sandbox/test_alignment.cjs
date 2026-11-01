const fs=require('fs'),vm=require('vm'),assert=require('assert'),{createCanvas,Image}=require('@napi-rs/canvas');
const root=__dirname+'/../',source=fs.readFileSync(__dirname+'/game.html','utf8');
const props=JSON.parse(source.match(/P:(\{.*?\}),up:/)[1]),rig=JSON.parse(source.match(/const RIG=(\{.*?\});/)[1]);
const draw=source.slice(source.indexOf('function drawTrooper(t)'),source.indexOf('function drawTrooperProc(t)'));
const legs=source.slice(source.indexOf('function legPose(t)'),source.indexOf('let FRAME_L='));
const ids={W01:'mortar',W02:'rail',W03:'scatter',W04:'bolter',W05:'las',W06:'flamer',W07:'chain',W08:'fist'};
const assets={};for(const slot of Object.keys(ids))assets[slot]=JSON.parse(fs.readFileSync(root+'hosted/library/'+slot+'_aligned_v001.forge.json'));
assets.ARM=JSON.parse(fs.readFileSync(root+'hosted/catalog/single-gun-arm-v001.forge.json'));
(async()=>{const canvas=createCanvas(350,250),ctx=canvas.getContext('2d'),blank=createCanvas(1,1),payload={revision:'alignment-test',assets,settings:{darkness:.6,emissive:1,bloom:2,scale:1.2,glowColor:'#ffff00'}};let selected='mortar',captured=null,armCaptured=null,wall=false;
const sprite={ready:true,M:{frame:[114,158],crop:[56,44],sc:.25,feet:661},T:{torso:[15,1]},P:props,up:4,k:27/(611*.25),ax:48.5,ay:154.25,team:[blank],lit:[blank],emis:[blank],legsD:blank};
const box={window:{},location:{pathname:'/test'},Image,console,document:{createElement:()=>createCanvas(1,1)},LAB_PAYLOAD:payload,ctx,SPR:sprite,RIG:rig,TROOP_H:27,PX:27/(611/12),time:0,S:{weapon:['mortar'],active:null},HELD:Object.fromEntries(Object.values(ids).map(k=>[k,k])),TEAM:[{col:'#fff'}],DPR:1,scale:1,lightOn:()=>({rims:[{w:0},{w:0}],blast:0}),curW:()=>({id:selected}),key:()=>false,prop:()=>{},drawWeapSpr:()=>false,drawTrooperProc:()=>{},origin:t=>[t.x+13*t.face,t.y-12,Math.cos(t.aim)*t.face,Math.sin(t.aim)],aimVec:t=>[Math.cos(t.aim)*t.face,Math.sin(t.aim)],isSolid:(x,y)=>wall&&x>=108};
box.__capture=(a,anchor)=>{const m=ctx.getTransform(),point=p=>({x:m.a*(p[0]-anchor[0])+m.c*(p[1]-anchor[1])+m.e,y:m.b*(p[0]-anchor[0])+m.d*(p[1]-anchor[1])+m.f});if(a.doc.code==='A01'){armCaptured={shoulder:point(a.doc.markers.shoulder),hand:point(a.doc.markers.hand)};return}captured={grip:point(a.doc.markers.grip),muzzle:point(a.doc.markers.muzzle)}};
vm.createContext(box);vm.runInContext(legs+draw,box);
vm.runInContext("drawWeapSpr=function(k,rim){const m=SPR.P[k];prop(k,m.g[0],m.m?m.m[1]:m.g[1],1,!rim,true);return true}",box);
let runtime=fs.readFileSync(__dirname+'/runtime.js','utf8').replace('  const x=-anchor[0],y=-anchor[1];','  globalThis.__capture(a,anchor);const x=-anchor[0],y=-anchor[1];');
vm.runInContext(runtime+';globalThis.hooks={ready:labReady,origin:t=>origin(t),point:(t,k,p)=>labWeaponWorldPoint(t,k,p),shoulder:t=>labAimWorldPoint(t,[0,0])}',box);
// Make the real weapon caller, including its original atlas grip/barrel arguments.

const t={x:100,y:120,team:0,face:1,aim:0,alive:true,anim:.7};box.S.active=t;const before=box.hooks.origin(t);await box.hooks.ready;assert.deepEqual(box.hooks.origin(t),before,'Async art loading cannot change simulation origin');
let checked=0;
for(const mode of ['legacy','per-asset']){
for(const[slot,k]of Object.entries(ids)){selected=k;box.S.weapon[0]=k;for(const face of[-1,1])for(const aim of[-1.1,-.4,0,.7])for(const pose of[{},{moving:true},{sq:.2,tilt:.17}]){Object.assign(t,{face,aim,moving:false,sq:0,tilt:0},pose);let previousGrip;
for(const z of[.8,1,1.2,1.6]){if(mode==='legacy')payload.settings.scale=z;else{payload.settings.scale=2.3;assets[slot].game_scale=z}ctx.resetTransform();ctx.clearRect(0,0,350,250);captured=null;armCaptured=null;box.drawTrooper(t);assert(captured,k+' render missing');assert(armCaptured,k+' arm missing');const shoulder=box.hooks.shoulder(t);assert(Math.hypot(armCaptured.shoulder.x-shoulder[0],armCaptured.shoulder.y-shoulder[1])<1e-4,k+' shoulder must be the fixed pivot');assert(Math.hypot(armCaptured.hand.x-captured.grip.x,armCaptured.hand.y-captured.grip.y)<1e-4,k+' grip must attach to arm hand');if(previousGrip){assert(Math.abs(captured.grip.x-previousGrip.x)<1e-4);assert(Math.abs(captured.grip.y-previousGrip.y)<1e-4)}previousGrip=captured.grip;
if(!['chain','fist'].includes(k)){const out=box.hooks.origin(t);assert(Math.abs(out[0]-captured.muzzle.x)<1e-4,k+' muzzle x mismatch '+JSON.stringify({out,captured,face,aim,z,pose}));assert(Math.abs(out[1]-captured.muzzle.y)<1e-4,k+' muzzle y mismatch');assert.equal(out[2],Math.cos(aim)*face);assert.equal(out[3],Math.sin(aim))}checked++}}}
}
// One asset's change cannot alter another weapon's simulation origin.
box.S.weapon[0]='rail';const independentOrigin=box.hooks.origin(t);assets.W08.game_scale=.65;assert.deepEqual(box.hooks.origin(t),independentOrigin,'Claw scale cannot change rail origin');
// Unsupported tools use their original firing origin. A barrel blocked by terrain fires into that wall.
box.S.weapon[0]='rope';Object.assign(t,{face:1,aim:0,tilt:0,sq:0,moving:false});assert.equal(box.hooks.origin(t)[0],113);box.S.weapon[0]='rail';payload.settings.scale=1.2;wall=true;const blocked=box.hooks.origin(t);assert(blocked[0]>=108&&blocked[0]<108.6);wall=false;assert(box.hooks.origin(t)[0]>blocked[0]);
// The foreground hand is visual only, appears once after the normal gun pass,
// and keeps human proportions when the gun is enlarged.
const originalHand=box.labDrawGunHand;let handCalls=0;
box.labDrawGunHand=k=>{if(['mortar','rail','scatter','bolter','las','flamer'].includes(k))handCalls++;return originalHand(k)};
selected='rail';box.S.weapon[0]='rail';ctx.resetTransform();ctx.translate(100,100);
box.drawWeapSpr('rail',true);assert.equal(handCalls,0,'Rim passes must not duplicate the arm');
box.drawWeapSpr('rail',false);assert.equal(handCalls,1,'Gun pass must draw one foreground arm');
const handHash=z=>{payload.settings.scale=z;ctx.resetTransform();ctx.clearRect(0,0,350,250);ctx.translate(100,100);originalHand('rail');return Buffer.from(ctx.getImageData(0,0,350,250).data)};
assert.deepEqual(handHash(1),handHash(1.6),'The human hand must not grow with weapon scale');
for(const k of ['rope','frag','sun','mine']){ctx.resetTransform();ctx.clearRect(0,0,350,250);originalHand(k);assert(!ctx.getImageData(0,0,350,250).data.some(v=>v),'Thrown and unregistered assets must not use the held arm')}
const matrix=ctx.getTransform();originalHand('rail');assert.deepEqual(ctx.getTransform(),matrix,'Hand rendering must restore the parent transform');
assets.ARM.game_scale=1;const human=handHash(1);assets.ARM.game_scale=1.4;assert.notDeepEqual(handHash(1),human,'The arm can have its own scale');assert.deepEqual(handHash(1),handHash(2),'Arm scale stays independent of shared weapon scale');
console.log('Shoulder pivot: arm shoulder fixed at the aim joint; all eight held grips attached to the arm hand across aim, facing, pose and asset scales.');
console.log('Foreground hand: normal/rim layering, one arm per gun pass, human-scale invariance, non-gun exclusion and transform restoration passed.');
console.log('Alignment: '+checked+' actual drawTrooper transforms checked across all eight assets, four scales in legacy and per-asset modes, both facings, aim and movement/pose; grip fixed, ranged muzzle exact, pre-load determinism, tool fallback and wall blocking passed.');
})().catch(e=>{console.error(e);process.exit(1)});
