// Runs INSIDE the game's closure. Payload and renderer are embedded in releases.
// Category art hooks; firing and collision rules remain the game's rules.
window.GRIMSPIRE_ART_REVISION=LAB_PAYLOAD.revision;
const labArt = new Map();
const labSlots = {W01:'mortar',W02:'rail',W03:'scatter',W04:'bolter',W05:'las',W06:'flamer',W07:'chain',W08:'fist'};
const labSettings = LAB_PAYLOAD.settings;
const labOriginalProp = prop;
const labImage = src => src ? new Promise((resolve,reject)=>{const i=new Image();i.onload=()=>resolve(i);i.onerror=()=>reject(new Error('Weapon image failed to load'));i.src=src}) : Promise.resolve(null);
const labReady = Promise.all(Object.entries(LAB_PAYLOAD.assets).map(async ([slot,doc])=>{
  const frames=await Promise.all(doc.frames.map(async f=>({body:await labImage(f.body),trim:await labImage(f.trim),emis:await labImage(f.emis)})));
  const k=labSlots[slot]||slot;labArt.set(k,{doc,frames});
})).then(()=>{window.GRIMSPIRE_ART_READY=true}).catch(e=>{window.GRIMSPIRE_ART_ERROR=e.message;console.error(e)});
function labDraw(a,anchor,size=1,glow=true){
  const {doc,frames}=a,f=frames[Math.floor(time*Math.max(1,doc.fps||8))%frames.length];
  ctx.save();ctx.imageSmoothingEnabled=false;ctx.scale(PX*size*labSettings.scale,PX*size*labSettings.scale);
  const x=-anchor[0],y=-anchor[1];
  if(f.body){
    // Isolate the darkening mask on a cached canvas, so it cannot tint scenery.
    if(!f.dark){const c=document.createElement('canvas');c.width=doc.w;c.height=doc.h;const g=c.getContext('2d');g.drawImage(f.body,0,0);g.globalCompositeOperation='source-atop';g.fillStyle=`rgba(5,6,9,${labSettings.darkness})`;g.fillRect(0,0,c.width,c.height);f.dark=c}
    ctx.globalCompositeOperation='source-over';ctx.drawImage(f.dark,x,y)}
  if(f.trim)ctx.drawImage(f.trim,x,y);
  if(glow&&f.emis){ctx.globalAlpha=labSettings.emissive;ctx.shadowColor=labSettings.glowColor;ctx.shadowBlur=labSettings.bloom;ctx.drawImage(f.emis,x,y);ctx.shadowBlur=0;ctx.globalCompositeOperation='lighter';ctx.globalAlpha=labSettings.emissive*.55;ctx.drawImage(f.emis,x,y)}
  ctx.restore();
}
prop = function(k,ax,ay,s,glow,dark){
  const a=labArt.get(k);if(!a)return labOriginalProp(k,ax,ay,s,glow,dark);
  const {doc,frames}=a,f=frames[Math.floor(time*Math.max(1,doc.fps||8))%frames.length];
  // Keep the hand at the existing grip. Art has an explicit preview scale.
  const old=SPR.P[k],grip=doc.markers.grip||doc.markers.pivot||[doc.w*.3,doc.h/2];
  const oldGrip=old.g||[old.r[2]/SPR.up*.3,old.r[3]/SPR.up/2];
  const oldY=old.m?old.m[1]:oldGrip[1];
  ctx.save();ctx.translate((oldGrip[0]-ax)*PX*(s||1),(oldY-ay)*PX*(s||1));
  labDraw(a,grip,s||1,glow);ctx.restore();
};
// Existing chain animation belongs to the old blade silhouette.
const labOriginalWeapon=drawWeapSpr;
drawWeapSpr=function(k,rimOnly){if(k!=='chain'||!labArt.has(k))return labOriginalWeapon(k,rimOnly);const m=SPR.P[k];prop(k,m.g[0],m.m?m.m[1]:m.g[1],1,!rimOnly,true);return true};

if(location.pathname==='/api/game'){
  // Preview uses local play only. Do not send sandbox matches or reports to live services.
  for(const id of ['goNet','goReport','pReport']){const el=document.getElementById(id);if(el){el.hidden=true;el.addEventListener('click',e=>{e.preventDefault();e.stopImmediatePropagation()},true)}}
}

// Category dummies are independent of the weapon slots. Props have no collision or damage model.
const labGroundAnchor=d=>[d.w/2,Number.isFinite(d.base)?d.base+1:d.h];
let labProps=[],labBackground=null,labPlacing=false;
if(typeof drawWard==='function'){
  const original=drawWard;
  drawWard=function(lights){
    if(labBackground&&labArt.has('BACKGROUND')){ctx.save();ctx.translate(labBackground.x,labBackground.y);labDraw(labArt.get('BACKGROUND'),labGroundAnchor(labArt.get('BACKGROUND').doc));ctx.restore()}
    original(lights);
    for(const p of labProps){const art=labArt.get('PROP');if(!art)continue;ctx.save();ctx.translate(p.x,p.y);labDraw(art,labGroundAnchor(art.doc));ctx.restore()}
  };
}
if(typeof drawTrooper==='function'){
  const original=drawTrooper;
  drawTrooper=function(t){const a=labArt.get('TROOPER');if(!a||!t.alive)return original(t);ctx.save();ctx.translate(t.x,t.y);ctx.scale(t.face||1,1);labDraw(a,labGroundAnchor(a.doc));ctx.restore()};
}
if(location.pathname==='/api/game'&&new URLSearchParams(location.search).get('grounds')==='1'){
  labReady.then(()=>{
    const tools=document.createElement('div');tools.id='forgeTestTools';
    tools.style.cssText='position:fixed;top:12px;left:12px;z-index:10000;background:#10151eee;color:#eee;padding:10px;border:1px solid #59edff;max-width:330px;font:14px system-ui';
    const note=document.createElement('div');note.textContent='Forge testing grounds · '+LAB_PAYLOAD.revision;tools.append(note);
    const add=(label,fn)=>{const b=document.createElement('button');b.textContent=label;b.onclick=fn;tools.append(b)};
    const placeNear=()=>{const t=S.active||troopers.find(t=>t.alive);if(!t)return;const x=clamp(t.x+45,10,W-10);labProps.push({x,y:surf(x)+1})};
    if(labArt.has('PROP')){
      add('Add prop nearby',placeNear);
      add('Place prop on map',()=>{labPlacing=true;note.textContent='Tap a ground surface to place your prop.'});
      add('Clear props',()=>{labProps=[]});
      cv.addEventListener('pointerdown',e=>{if(!labPlacing)return;e.preventDefault();e.stopImmediatePropagation();const p=toWorld(e.clientX,e.clientY);let y=clamp(Math.round(p.y),0,H-1),x=clamp(Math.round(p.x),1,W-2);if(isSolid(x,y)){while(y>0&&isSolid(x,y-1))y--}else{while(y<H-1&&!isSolid(x,y))y++}labProps.push({x,y});labPlacing=false;note.textContent='Prop placed · visual dummy, no collision or damage.'},true);
    }
    const start=()=>{
      labProps=[];newGame('hot',undefined,mkCfg('hot',[0,1],false));DBG.inf=true;dbgBuild();
      for(const tm of S.order)for(const w of ARS)if(w.ammo>=0&&!w.off)S.ammo[tm][w.id]=9;
      const chosen=labSlots[LAB_PAYLOAD.selected_slot];if(chosen)selectWeapon(chosen);
      if(labArt.has('PROP'))placeNear();
      if(labArt.has('BACKGROUND')){const t=S.active||troopers[0];labBackground={x:t.x,y:surf(t.x)+1}}
    };
    add('Restart local test',start);document.body.append(tools);start();
    window.GRIMSPIRE_FORGE_TEST={get props(){return labProps},category:LAB_PAYLOAD.selected_slot};
  }).catch(e=>{const p=document.createElement('p');p.textContent='Testing grounds failed: '+e.message;p.style.cssText='position:fixed;top:0;z-index:10001;background:#300;color:white';document.body.append(p)});
}
