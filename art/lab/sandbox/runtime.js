// Runs INSIDE the game's closure. Payload and renderer are embedded in releases.
// Category art hooks. Ranged origins share the scaled art rig; other combat rules are unchanged.
window.GRIMSPIRE_ART_REVISION=LAB_PAYLOAD.revision;
const labArt = new Map();
const labSlots = {W01:'mortar',W02:'rail',W03:'scatter',W04:'bolter',W05:'las',W06:'flamer',W07:'chain',W08:'fist'};
const labSettings = LAB_PAYLOAD.settings;
// Simulation geometry exists before asynchronous PNG loading (including online replay).
const labDocs=new Map(Object.entries(LAB_PAYLOAD.assets).map(([slot,doc])=>[labSlots[slot]||slot,doc]));
const labOriginalProp = prop;
const labImage = src => src ? new Promise((resolve,reject)=>{const i=new Image();i.onload=()=>resolve(i);i.onerror=()=>reject(new Error('Weapon image failed to load'));i.src=src}) : Promise.resolve(null);
const labReady = Promise.all(Object.entries(LAB_PAYLOAD.assets).map(async ([slot,doc])=>{
  const frames=await Promise.all(doc.frames.map(async f=>({body:await labImage(f.body),trim:await labImage(f.trim),emis:await labImage(f.emis)})));
  const k=labSlots[slot]||slot;labArt.set(k,{doc,frames});
})).then(()=>{window.GRIMSPIRE_ART_READY=true}).catch(e=>{window.GRIMSPIRE_ART_ERROR=e.message;console.error(e)});
// Old payloads retain their shared scale; the foreground arm was always human-sized.
const labAssetScale=d=>d.game_scale??(d===labDocs.get('ARM')?1:labSettings.scale);
function labDraw(a,anchor,size=1,glow=true){
  const {doc,frames}=a,f=frames[Math.floor(time*Math.max(1,doc.fps||8))%frames.length];
  ctx.save();ctx.imageSmoothingEnabled=false;ctx.scale(PX*size*labAssetScale(doc),PX*size*labAssetScale(doc));
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
  const oldY=oldGrip[1];
  ctx.save();ctx.translate((oldGrip[0]-ax)*PX*(s||1),(oldY-ay)*PX*(s||1));
  labDraw(a,grip,s||1,glow);ctx.restore();
};
// One rig for drawing and firing: scale around the sprite grip, keeping the
// original hand position fixed. PNG load timing must never affect simulation.
function labWeaponPoint(k,point){
  const d=labDocs.get(k),old=SPR.P[k],grip=d?.markers.grip||d?.markers.pivot;
  if(!d||!old||!grip||!point)return null;
  const g=old.g||[old.r[2]/SPR.up*.3,old.r[3]/SPR.up/2];
  const handY=(g[1]-(old.m?old.m[1]:g[1]))*PX,z=PX*labAssetScale(d);
  return [(point[0]-grip[0])*z,handY+(point[1]-grip[1])*z];
}
function labWeaponWorldPoint(t,k,point){
  const local=labWeaponPoint(k,point);if(!local)return null;
  const a=t.aim||0,c=Math.cos(a),s=Math.sin(a);
  let x=1.5+local[0]*c-local[1]*s,y=-12+local[0]*s+local[1]*c;
  // Match drawTrooper's leg drop, squash, facing, tilt and water bob exactly.
  if(typeof legPose==='function'&&typeof RIG!=='undefined'){
    const[an,af,bn,bf]=legPose(t),R=RIG,K=typeof TROOP_H==='number'?TROOP_H/((SPR.M.feet-50)*SPR.M.sc):SPR.k;
    const ext=(a,b)=>R.thH*Math.cos(a)+(R.shH-R.ov)*Math.cos(a-b);
    y+=(R.thH+R.shH-R.ov-Math.max(ext(an,bn),ext(af,bf)))*K;
  }
  const sq=t.sq||0;x*=t.face*(1+sq*.22);y*=1-sq*.3;
  const tilt=t.tilt||0,ct=Math.cos(tilt),st=Math.sin(tilt),lay=Math.min(1,Math.abs(tilt)/1.45);
  const bob=t.wet?Math.sin(time*2.4+t.x)*1.2:0;
  return[t.x+x*ct-y*st,t.y+bob-lay*3+x*st+y*ct];
}
if(typeof origin==='function'){
  const labOriginalOrigin=origin;
  origin=function(t){
    const id=S.weapon?.[t.team],k=typeof HELD!=='undefined'?HELD[id]:id;
    if(!['mortar','rail','scatter','bolter','las','flamer'].includes(k))return labOriginalOrigin(t);
    const doc=labDocs.get(k),muzzle=doc?.markers.muzzle;
    if(!muzzle)return labOriginalOrigin(t);
    const point=labWeaponWorldPoint(t,k,muzzle);if(!point)return labOriginalOrigin(t);
    const grip=doc.markers.grip||doc.markers.pivot,hand=labWeaponWorldPoint(t,k,grip);
    // A longer barrel must not allow shooting through a nearby wall.
    if(hand&&typeof isSolid==='function'){
      const dx=point[0]-hand[0],dy=point[1]-hand[1],n=Math.max(1,Math.ceil(Math.hypot(dx,dy)*2));
      for(let i=0;i<=n;i++){const x=hand[0]+dx*i/n,y=hand[1]+dy*i/n;if(isSolid(x,y)){point[0]=x;point[1]=y;break}}
    }
    const[dx,dy]=aimVec(t);return[point[0],point[1],dx,dy];
  };
}
// A single straight forearm and glove, drawn over the weapon grip. It uses
// trooper pixel scale, independent of weapon enlargement; no shoulder/elbow rig.
function labDrawGunHand(k){
  if(!['mortar','rail','scatter','bolter','las','flamer'].includes(k))return;
  const m=SPR.P[k];if(!m?.g)return;
  const handY=(m.g[1]-(m.m?m.m[1]:m.g[1]))*PX;
  const art=labArt.get('ARM');
  if(art){
    const d=art.doc,anchor=d.markers.hand||d.markers.pivot||[d.w-1,d.h/2];
    ctx.save();ctx.translate(0,handY);
    // Cancel weapon scale: the arm retains the trooper's pixel size.
    labDraw(art,anchor,1,false);ctx.restore();return;
  }
  ctx.save();ctx.translate(0,handY);ctx.scale(PX,PX);
  ctx.globalCompositeOperation='source-over';ctx.globalAlpha=1;
  ctx.shadowColor='transparent';ctx.shadowBlur=0;ctx.shadowOffsetX=0;ctx.shadowOffsetY=0;
  ctx.imageSmoothingEnabled=false;
  // Blocked-out sleeve, cuff and fingers share the game's art-pixel grid.
  ctx.fillStyle='#070b12';ctx.fillRect(-14,-3,12,6);
  ctx.fillStyle='#354152';ctx.fillRect(-13,-2,10,4);
  ctx.fillStyle='#536277';ctx.fillRect(-12,-2,7,1);
  ctx.fillStyle='#222b39';ctx.fillRect(-12,1,8,1);
  ctx.fillStyle='#111926';ctx.fillRect(-5,-3,3,6);
  ctx.fillStyle='#6c7887';ctx.fillRect(-4,-2,2,4);
  ctx.fillStyle='#070b12';ctx.fillRect(-2,-3,5,6);ctx.fillRect(-3,-2,2,3);
  ctx.fillStyle='#687484';ctx.fillRect(-1,-2,3,4);
  ctx.fillStyle='#a0a9b4';ctx.fillRect(0,-2,2,1);ctx.fillRect(1,0,1,1);ctx.fillRect(1,2,1,1);
  ctx.fillStyle='#374251';ctx.fillRect(-1,0,2,1);ctx.fillRect(-1,2,2,1);
  // Thumb wraps around the rear/top of the handle.
  ctx.fillStyle='#8995a3';ctx.fillRect(-2,-2,1,2);
  ctx.restore();
}
// Existing chain animation belongs to the old blade silhouette.
const labOriginalWeapon=drawWeapSpr;
drawWeapSpr=function(k,rimOnly){
  let drawn;
  if(k==='chain'&&labArt.has(k)){const m=SPR.P[k];prop(k,m.g[0],m.m?m.m[1]:m.g[1],1,!rimOnly,true);drawn=true}
  else drawn=labOriginalWeapon(k,rimOnly);
  if(drawn&&!rimOnly)labDrawGunHand(k);
  return drawn;
};

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
