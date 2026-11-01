const fs=require('fs'),vm=require('vm'),assert=require('assert'),{createCanvas,Image}=require('@napi-rs/canvas');
const root=__dirname+'/../',source=fs.readFileSync(__dirname+'/game.html','utf8');
const props=JSON.parse(source.match(/P:(\{.*?\}),up:/)[1]),rig=JSON.parse(source.match(/const RIG=(\{.*?\});/)[1]);
const draw=source.slice(source.indexOf('function drawTrooper(t)'),source.indexOf('function drawTrooperProc(t)'));
const legs=source.slice(source.indexOf('function legPose(t)'),source.indexOf('let FRAME_L='));
const ids={W01:'mortar',W02:'rail',W03:'scatter',W04:'bolter',W05:'las',W06:'flamer',W07:'chain',W08:'fist'};
const assets={};for(const slot of Object.keys(ids))assets[slot]=JSON.parse(fs.readFileSync(root+'hosted/library/'+slot+'_aligned_v001.forge.json'));
(async()=>{const canvas=createCanvas(350,250),ctx=canvas.getContext('2d'),blank=createCanvas(1,1),payload={revision:'alignment-test',assets,settings:{darkness:.6,emissive:1,bloom:2,scale:1.2,glowColor:'#ffff00'}};let selected='mortar',captured=null,wall=false;
const sprite={ready:true,M:{frame:[114,158],crop:[56,44],sc:.25,feet:661},T:{torso:[15,1]},P:props,up:4,k:27/(611*.25),ax:48.5,ay:154.25,team:[blank],lit:[blank],emis:[blank],legsD:blank};
const box={window:{},location:{pathname:'/test'},Image,console,document:{createElement:()=>createCanvas(1,1)},LAB_PAYLOAD:payload,ctx,SPR:sprite,RIG:rig,TROOP_H:27,PX:27/(611/12),time:0,S:{weapon:['mortar'],active:null},HELD:Object.fromEntries(Object.values(ids).map(k=>[k,k])),TEAM:[{col:'#fff'}],DPR:1,scale:1,lightOn:()=>({rims:[{w:0},{w:0}],blast:0}),curW:()=>({id:selected}),key:()=>false,prop:()=>{},drawWeapSpr:()=>false,drawTrooperProc:()=>{},origin:t=>[t.x+13*t.face,t.y-12,Math.cos(t.aim)*t.face,Math.sin(t.aim)],aimVec:t=>[Math.cos(t.aim)*t.face,Math.sin(t.aim)],isSolid:(x,y)=>wall&&x>=108};
box.__capture=(a,anchor)=>{const m=ctx.getTransform(),point=p=>({x:m.a*(p[0]-anchor[0])+m.c*(p[1]-anchor[1])+m.e,y:m.b*(p[0]-anchor[0])+m.d*(p[1]-anchor[1])+m.f});captured={grip:point(a.doc.markers.grip),muzzle:point(a.doc.markers.muzzle)}};
vm.createContext(box);vm.runInContext(legs+draw,box);
let runtime=fs.readFileSync(__dirname+'/runtime.js','utf8').replace('  const x=-anchor[0],y=-anchor[1];','  globalThis.__capture(a,anchor);const x=-anchor[0],y=-anchor[1];');
vm.runInContext(runtime+';globalThis.hooks={ready:labReady,origin:t=>origin(t),point:(t,k,p)=>labWeaponWorldPoint(t,k,p)}',box);
// Make the real weapon caller, including its original atlas grip/barrel arguments.
vm.runInContext("drawWeapSpr=function(k,rim){const m=SPR.P[k];prop(k,m.g[0],m.m?m.m[1]:m.g[1],1,!rim,true);return true}",box);
const t={x:100,y:120,team:0,face:1,aim:0,alive:true,anim:.7};box.S.active=t;const before=box.hooks.origin(t);await box.hooks.ready;assert.deepEqual(box.hooks.origin(t),before,'Async art loading cannot change simulation origin');
let checked=0;
for(const[slot,k]of Object.entries(ids)){selected=k;box.S.weapon[0]=k;for(const face of[-1,1])for(const aim of[-1.1,-.4,0,.7])for(const pose of[{},{moving:true},{sq:.2,tilt:.17}]){Object.assign(t,{face,aim,moving:false,sq:0,tilt:0},pose);let previousGrip;
for(const z of[.8,1,1.2,1.6]){payload.settings.scale=z;ctx.resetTransform();ctx.clearRect(0,0,350,250);captured=null;box.drawTrooper(t);assert(captured,k+' render missing');if(previousGrip){assert(Math.abs(captured.grip.x-previousGrip.x)<1e-4);assert(Math.abs(captured.grip.y-previousGrip.y)<1e-4)}previousGrip=captured.grip;
if(!['chain','fist'].includes(k)){const out=box.hooks.origin(t);assert(Math.abs(out[0]-captured.muzzle.x)<1e-4,k+' muzzle x mismatch '+JSON.stringify({out,captured,face,aim,z,pose}));assert(Math.abs(out[1]-captured.muzzle.y)<1e-4,k+' muzzle y mismatch');assert.equal(out[2],Math.cos(aim)*face);assert.equal(out[3],Math.sin(aim))}checked++}}}
// Unsupported tools use their original firing origin. A barrel blocked by terrain fires into that wall.
box.S.weapon[0]='rope';Object.assign(t,{face:1,aim:0,tilt:0,sq:0,moving:false});assert.equal(box.hooks.origin(t)[0],113);box.S.weapon[0]='rail';payload.settings.scale=1.2;wall=true;const blocked=box.hooks.origin(t);assert(blocked[0]>=108&&blocked[0]<108.6);wall=false;assert(box.hooks.origin(t)[0]>blocked[0]);
console.log('Alignment: '+checked+' actual drawTrooper transforms checked across all eight assets, four scales, both facings, aim and movement/pose; grip fixed, ranged muzzle exact, pre-load determinism, tool fallback and wall blocking passed.');
})().catch(e=>{console.error(e);process.exit(1)});
