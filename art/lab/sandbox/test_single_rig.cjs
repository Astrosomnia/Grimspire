const fs=require('fs'),vm=require('vm'),assert=require('assert'),{createCanvas}=require('@napi-rs/canvas');
const source=fs.readFileSync(__dirname+'/../forge.html','utf8');const fn=source.slice(source.indexOf('function rigFrame(now)'),source.indexOf('// ---------- notes ----------'));
const canvas=createCanvas(900,700),native=canvas.getContext('2d'),calls=[];const g=new Proxy(native,{get(t,k){if(k==='drawImage')return(...args)=>{calls.push({image:args[0],m:t.getTransform(),x:args[1],y:args[2]});return t.drawImage(...args)};const v=t[k];return typeof v==='function'?v.bind(t):v},set(t,k,v){t[k]=v;return true}});
const part=(w,h,m)=>({w,h,m,c:createCanvas(w,h)}),torso=part(30,50,{hip:[15,45],shoulder:[20,15]}),arm=part(18,8,{hand:[14,3],shoulder:[0,3]}),weapon=part(32,16,{grip:[10,10],muzzle:[31,5]});
let reach=50;const elements={'#dRig':{open:true},'#rigCv':{width:900,height:700,getBoundingClientRect:()=>({width:900,height:700}),getContext:()=>g},'#rigInfo':{},'#rigAim':{value:0},'#rigAimLbl':{}};
const box={window:{devicePixelRatio:1},rig:{parts:{torso,arm,weapon},t0:0},rigOpt:{sweep:false,walk:false,left:false,joints:false},requestAnimationFrame(){},WORLD:1.85,clamp:(x,a,b)=>Math.max(a,Math.min(b,x)),$:s=>s==='#rigReach'?{value:reach}:elements[s]};vm.createContext(box);vm.runInContext(fn,box);
const point=(call,p)=>{const {m}=call,x=p[0]+.5+call.x,y=p[1]+.5+call.y;return [m.a*x+m.c*y+m.e,m.b*x+m.d*y+m.f]};
let fixedShoulder,firstHand;
for(const extension of [50,100])for(const aim of [-60,0,70])for(const size of [.6,1.4]){
 reach=extension;elements['#rigAim'].value=aim;weapon.scale=size;calls.length=0;box.rigFrame(0);
 const a=calls.find(c=>c.image===arm.c),w=calls.find(c=>c.image===weapon.c);assert(a&&w);
 assert.equal(calls.at(-1).image,arm.c,'Single arm is the foreground layer');
 const shoulder=point(a,arm.m.shoulder),hand=point(a,arm.m.hand),grip=point(w,weapon.m.grip);
 if(fixedShoulder)assert(Math.hypot(shoulder[0]-fixedShoulder[0],shoulder[1]-fixedShoulder[1])<1e-4,'Reach, aim and weapon scale must keep the shoulder planted');fixedShoulder=shoulder;
 assert(Math.hypot(hand[0]-grip[0],hand[1]-grip[1])<1e-4,'The grip must stay on the hand '+JSON.stringify({hand,grip,extension,aim,size}));
 if(aim===0&&size===.6){if(firstHand)assert(hand[0]>firstHand[0],'Reach extends the hand from a fixed shoulder');firstHand=hand}
 assert(!elements['#rigInfo'].textContent.includes('Add an upper arm'));
}
console.log('Single-arm rig: fixed shoulder pivot, attached weapon grip, independent weapon scale, aim/reach, foreground layering and no elbow segments passed.');
