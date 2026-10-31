// Native Canvas + game-hook harness: exercise placement, anchoring and local launch.
const fs=require('fs'),vm=require('vm'),assert=require('assert');const {createCanvas,Image}=require('@napi-rs/canvas');
const root=__dirname+'/../',runtime=fs.readFileSync(__dirname+'/runtime.js','utf8');
const doc=JSON.parse(fs.readFileSync(root+'releases/weapons-v001/W04_grid.forge.json'));doc.code='C01';doc.markers={};doc.base=null;
function element(){return{children:[],style:{},append(...x){this.children.push(...x)},addEventListener(){}}}
(async()=>{
const canvas=createCanvas(180,120),ctx=canvas.getContext('2d'),body=element(),handlers={};let starts=0,originalWard=0,originalTroop=0;
const payload={revision:'category-test',selected_slot:'PROP',assets:{PROP:doc,TROOPER:doc,BACKGROUND:doc},settings:{darkness:0,emissive:1,bloom:0,scale:1,glowColor:'#59edff'}};
const box={window:{},location:{pathname:'/api/game',search:'?grounds=1'},URLSearchParams,Image,console,document:{body,getElementById:()=>null,createElement:type=>type==='canvas'?createCanvas(1,1):element()},LAB_PAYLOAD:payload,ctx,SPR:{up:4,P:{}},PX:1,time:0,prop:()=>{throw Error('Prop must not use a weapon slot')},drawWeapSpr:()=>false,drawWard:()=>originalWard++,drawTrooper:()=>originalTroop++,S:{active:{x:30,y:90},order:[0,1],ammo:[{},{}]},troopers:[],W:180,H:120,DBG:{inf:false},ARS:[{id:'mortar',ammo:1}],clamp:(x,a,b)=>Math.max(a,Math.min(b,x)),surf:()=>90,isSolid:(x,y)=>y>=90,toWorld:(x,y)=>({x,y}),cv:{addEventListener:(n,fn)=>handlers[n]=fn},newGame:()=>starts++,mkCfg:()=>({}),dbgBuild:()=>{},selectWeapon:()=>{throw Error('A prop must not select a weapon')}};
vm.createContext(box);vm.runInContext(runtime+';globalThis.testHooks={ready:labReady,drawWard:(...a)=>drawWard(...a),drawTrooper:(...a)=>drawTrooper(...a)}',box);
await box.testHooks.ready;await new Promise(r=>setImmediate(r));
assert.equal(starts,1);assert.equal(box.DBG.inf,true);assert.equal(box.window.GRIMSPIRE_FORGE_TEST.category,'PROP');assert.equal(box.window.GRIMSPIRE_FORGE_TEST.props.length,1);assert.equal(box.window.GRIMSPIRE_FORGE_TEST.props[0].y,91);
box.testHooks.drawWard([]);assert.equal(originalWard,1);const pixels=ctx.getImageData(50,70,45,20).data;assert([...pixels].some((v,i)=>i%4===3&&v>0),'Ground prop actually draws above its base');assert.equal(ctx.getImageData(75,92,1,1).data[3],0,'Art does not extend below its baseline');
const tools=body.children[0],place=tools.children.find(x=>x.textContent==='Place prop on map');place.onclick();let stopped=0;handlers.pointerdown({clientX:120,clientY:70,preventDefault(){},stopImmediatePropagation(){stopped++}});assert.equal(stopped,1);assert.equal(box.window.GRIMSPIRE_FORGE_TEST.props[1].y,90);assert.equal(box.window.GRIMSPIRE_FORGE_TEST.props[1].x,120);
box.testHooks.drawTrooper({alive:true,x:30,y:90,face:1});assert.equal(originalTroop,0);box.testHooks.drawTrooper({alive:false});assert.equal(originalTroop,1);
console.log('Category tests: automatic local launch, infinite timer, grounded prop pixels, placement interception, baseline and trooper dummy passed.');
})().catch(e=>{console.error(e);process.exit(1)});
