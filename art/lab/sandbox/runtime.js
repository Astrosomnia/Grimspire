// Runs INSIDE the game's closure. Payload and renderer are embedded in releases.
// These hooks affect weapon art only; firing rules remain the game's rules.
window.GRIMSPIRE_ART_REVISION=LAB_PAYLOAD.revision;
const labArt = new Map();
const labSlots = {W01:'mortar',W02:'rail',W03:'scatter',W04:'bolter',W05:'las',W06:'flamer',W07:'chain',W08:'fist'};
const labSettings = LAB_PAYLOAD.settings;
const labOriginalProp = prop;
const labImage = src => src ? new Promise((resolve,reject)=>{const i=new Image();i.onload=()=>resolve(i);i.onerror=()=>reject(new Error('Weapon image failed to load'));i.src=src}) : Promise.resolve(null);
const labReady = Promise.all(Object.entries(LAB_PAYLOAD.assets).map(async ([slot,doc])=>{
  const frames=await Promise.all(doc.frames.map(async f=>({body:await labImage(f.body),trim:await labImage(f.trim),emis:await labImage(f.emis)})));
  const k=labSlots[slot];labArt.set(k,{doc,frames});
})).then(()=>{window.GRIMSPIRE_ART_READY=true}).catch(e=>{window.GRIMSPIRE_ART_ERROR=e.message;console.error(e)});
prop = function(k,ax,ay,s,glow,dark){
  const a=labArt.get(k);if(!a)return labOriginalProp(k,ax,ay,s,glow,dark);
  const {doc,frames}=a,f=frames[Math.floor(time*Math.max(1,doc.fps||8))%frames.length];
  // Keep the hand at the existing grip. Art has an explicit preview scale.
  const old=SPR.P[k],grip=doc.markers.grip||doc.markers.pivot||[doc.w*.3,doc.h/2];
  const oldGrip=old.g||[old.r[2]/SPR.up*.3,old.r[3]/SPR.up/2];
  const oldY=old.m?old.m[1]:oldGrip[1];
  const zoom=PX*(s||1)*labSettings.scale;
  ctx.save();ctx.imageSmoothingEnabled=false;
  ctx.translate((oldGrip[0]-ax)*PX*(s||1),(oldY-ay)*PX*(s||1));ctx.scale(zoom,zoom);
  const x=-grip[0],y=-grip[1];
  if(f.body){
    // Isolate the darkening mask on a cached canvas, so it cannot tint scenery.
    if(!f.dark){const c=document.createElement('canvas');c.width=doc.w;c.height=doc.h;const g=c.getContext('2d');g.drawImage(f.body,0,0);g.globalCompositeOperation='source-atop';g.fillStyle=`rgba(5,6,9,${labSettings.darkness})`;g.fillRect(0,0,c.width,c.height);f.dark=c}
    ctx.globalCompositeOperation='source-over';ctx.drawImage(f.dark,x,y)}
  if(f.trim)ctx.drawImage(f.trim,x,y);
  if(glow&&f.emis){ctx.globalAlpha=labSettings.emissive;ctx.shadowColor=labSettings.glowColor;ctx.shadowBlur=labSettings.bloom;ctx.drawImage(f.emis,x,y);ctx.shadowBlur=0;ctx.globalCompositeOperation='lighter';ctx.globalAlpha=labSettings.emissive*.55;ctx.drawImage(f.emis,x,y)}
  ctx.restore();
};
// Existing chain animation belongs to the old blade silhouette.
const labOriginalWeapon=drawWeapSpr;
drawWeapSpr=function(k,rimOnly){if(k!=='chain'||!labArt.has(k))return labOriginalWeapon(k,rimOnly);const m=SPR.P[k];prop(k,m.g[0],m.m?m.m[1]:m.g[1],1,!rimOnly,true);return true};

if(location.pathname==='/api/game'){
  // Preview uses local play only. Do not send sandbox matches or reports to live services.
  for(const id of ['goNet','goReport','pReport']){const el=document.getElementById(id);if(el){el.hidden=true;el.addEventListener('click',e=>{e.preventDefault();e.stopImmediatePropagation()},true)}}
}
