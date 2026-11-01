// Explicit provenance migration. Display codes and test slots are not identities.
export function organiseAssets(source,saved,migration){
 const definitions=migration.assets||[],membership=new Map();
 for(const f of definitions)for(const m of f.members)membership.set(m.id,{asset_id:f.id,state_key:m.state||'',role:m.role,legacy_hash:m.legacy_hash});
 const docs=[...source.entries,...saved.entries.map(e=>{
  // Earlier registrations had no dimensions; retain their IDs and document paths.
  const meta=source.entries.find(s=>s.id==='alt-'+e.path.split('/').pop().replace(/\.json$/,''));
  return {...meta,...e};
 })].map(e=>({...e,...membership.get(e.id),...(e.asset_id?{asset_id:e.asset_id,state_key:e.state_key||'',role:'draft'}:{})}));
 // Unknown historical imports remain recoverable in Archive, without guessing from code.
 for(const d of docs)if(!d.asset_id){d.asset_id='legacy-'+d.id;d.state_key='';d.role='source'}
 const assets=[];
 for(const d of docs){let f=assets.find(f=>f.id===d.asset_id);if(!f){const known=definitions.find(f=>f.id===d.asset_id);f={id:d.asset_id,name:known?.name||d.asset_name||d.name||'Untitled',code:known?.code||d.code||'',category:known?.category||d.category||'Other art',archived:known?.archived??!d.asset_id.startsWith('custom-'),defaults:known?.current||{},versions:[],states:[]};assets.push(f)}f.versions.push(d)}
 for(const f of assets){
  for(const key of new Set(f.versions.map(d=>d.state_key))){
   const versions=f.versions.filter(d=>d.state_key===key),draft=versions.filter(d=>d.role==='draft').at(-1),baseline=versions.find(d=>d.id===f.defaults[key]),current=draft||baseline||versions[0];
   f.states.push({key,label:key?(key[0].toUpperCase()+key.slice(1)).replaceAll('_',' '):'Artwork',current:current.id,baseline:baseline?.id||null});
  }
  f.current=f.states.find(s=>s.key==='idle')?.current||f.states.find(s=>s.key==='')?.current||f.states[0]?.current;
 }
 return {docs,assets};
}
