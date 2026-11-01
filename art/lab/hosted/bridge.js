/* Shared Forge controls: every repository read is pinned to a commit. */
(async()=>{
while(!doc)await new Promise(r=>setTimeout(r,50));
let state=null,repoDocs=[],assetFamilies=[],busy=false,prepared=null,newer=false;
const panel=document.createElement('dialog');panel.className='wide';panel.innerHTML=`
<h3>Shared Forge</h3><p id="sharedStatus">Connecting to GitHub…</p><p id="sharedWarning" class="note"></p>
<label class="row">Test target <select id="sharedSlot">${['Launcher','Carbine','Scatter','Dakka','Las gun','Flamer','Chainsword','Claw'].map((n,i)=>`<option value="W0${i+1}">W0${i+1} · ${n}</option>`).join('')}<option value="ARM">Single foreground arm</option><option value="PROP">Ground prop / set piece</option><option value="TROOPER">Trooper frame / part</option><option value="BACKGROUND">Background / skyline</option></select></label>
<label class="row"><input id="sharedWeaponsOnly" type="checkbox" checked> On a weapon save, exclude category dummies from this new build (earlier tests stay in history)</label>
<label class="row">Art variant <select id="sharedVariant"><option value="grid">Grid study</option><option value="detail">Source detail</option><option value="custom">Custom / alternative</option></select></label>
<div class="row"><label>Darkness <input id="sharedDark" type="number" min="0" max="1" step="0.05" value="0.66"></label><label>Emissive <input id="sharedEmis" type="number" min="0" max="2" step="0.1" value="1"></label><label>Bloom <input id="sharedBloom" type="number" min="0" max="30" step="1" value="0"></label></div>
<div class="row"><label>Asset scale <input id="sharedScale" type="number" min="0.05" max="4" step="0.01" value="1"></label><label>Glow colour <input id="sharedColor" type="color" value="#59edff"></label></div>
<p class="note">Lighting and scale apply to the saved asset set. Ground props use their baseline or bottom centre; trooper frames are static art tests, without an articulated rig. Category dummies are for testing; Go live requires their game integration first. Source-detail sprites need a smaller scale than grid sprites. Weapons scale around their grip; ranged shots, flashes and aiming guides follow the muzzle marker. Damage, ammunition and weapon behaviour stay the same.</p>
<label>Update note<textarea id="sharedNotes" rows="3" placeholder="What changed and why?"></textarea></label>
<p class="note">Testing several weapons? Save revision for each weapon slot, then Save &amp; test in game once. The saved build includes all those weapon changes. Saving another sprite to the same slot replaces that slot in the new build; earlier revisions stay in history.</p>
<div class="row"><button id="sharedSave">Save revision</button><button id="sharedTest">Save & test in game</button><button id="sharedRefresh">Refresh shared library</button></div>
<div class="row"><button id="sharedPrepare">Review saved release…</button><button id="sharedClose">Close</button></div>
<p class="note">Test builds open a local battle automatically. Use the Forge test controls to place your prop on the map. TEST provides weapons and extra troopers. Saved revisions include artwork, lighting settings, game source and renderer code. “Ready” in the old editor does not publish anything.</p>
<p id="sharedResult" style="white-space:pre-wrap;overflow-wrap:anywhere"></p>
<h4>Releases</h4><div id="sharedReleases"></div><h4>Saved history</h4><div id="sharedHistory"></div>`;document.body.append(panel);
const q=s=>panel.querySelector(s),message=t=>q('#sharedResult').textContent=t;
const badge=document.createElement('button');badge.id='bSharedForge';badge.textContent='Shared Forge · connecting';document.querySelector('#bGame').after(badge);
const review=document.createElement('dialog');review.className='wide';review.innerHTML='<h3>Review release</h3><pre style="white-space:pre-wrap;overflow-wrap:anywhere"></pre><p><label><input type="checkbox"> I tested this saved revision, checked its scale, rig and effects, and approve this exact build for main.</label></p><div class="row"><button id="publishExact" disabled>Go live</button><button id="checkPublic" hidden>Check public deployment</button><button id="closeReview">Close</button></div>';document.body.append(review);
const signOut=document.createElement('button');signOut.textContent='Sign out';badge.after(signOut);
function showError(e){message(e.message);if(e.status===401){const a=document.createElement('a');a.href='/auth/github';a.textContent='Sign in with GitHub again';q('#sharedResult').append(document.createElement('br'),a)}}
async function get(path){const r=await fetch('/api/'+path,{cache:'no-store'});const data=await r.json();if(!r.ok){const e=Error(data.error||'GitHub request failed');e.status=r.status;throw e}return data}
async function post(path,body){if(!state)throw Error('The GitHub connection is not ready');const r=await fetch('/api/'+path,{method:'POST',headers:{'Content-Type':'application/json','X-Forge-CSRF':state.csrf},body:JSON.stringify(body)});const d=await r.json();if(!r.ok){const e=Error(d.error||'Save failed');e.status=r.status;throw e}return d}
const opts=()=>({darkness:+q('#sharedDark').value,emissive:+q('#sharedEmis').value,bloom:+q('#sharedBloom').value,scale:+q('#sharedScale').value,glowColor:q('#sharedColor').value});
function setOptions(v){for(const[id,key]of[['sharedDark','darkness'],['sharedEmis','emissive'],['sharedBloom','bloom'],['sharedScale','scale'],['sharedColor','glowColor']])q('#'+id).value=v[key]}
function link(parent,label,url){const a=document.createElement('a');a.textContent=label;a.href=url;a.target='_blank';a.rel='noopener';parent.append(a)}
function history(){const releases=q('#sharedReleases');releases.textContent='';for(const x of(state.state.integrations||[]).slice().reverse()){const row=document.createElement('p');row.textContent=x.revision+' · '+(x.deployment?'Public deployment verified':'Main updated; deployment unverified')+' · '+x.main_commit.slice(0,10)+' ';link(row,'Review PR',x.pr);releases.append(row)}if(!releases.childNodes.length)releases.textContent='No releases from the hosted Forge yet.';const root=q('#sharedHistory');root.textContent='';for(const r of state.state.revisions.slice().reverse().slice(0,40)){const row=document.createElement('div');row.className='row';const text=document.createElement('span');text.textContent=r.id+' · '+r.slot+' · '+r.variant+' · '+r.notes;row.append(text);link(row,'Test saved build','/api/game?debug=1&grounds=1&revision='+encodeURIComponent(r.id));const b=document.createElement('button');b.textContent='Open saved art';b.onclick=()=>run(async()=>{const data=await get('revision?id='+encodeURIComponent(r.id));const d=data.payload.assets[data.manifest.selected_slot];await deserialise(d,'saved-'+r.id);setOptions(data.payload.settings);q('#sharedSlot').value=data.manifest.selected_slot;q('#sharedVariant').value=data.manifest.variant;q('#sharedNotes').value='';panel.close();status('Loaded saved art '+r.id)});row.append(b);root.append(row)}}
async function refresh(initial=false){const next=await get('status'),library=await get('library?ref='+encodeURIComponent(next.head));repoDocs=library.docs;assetFamilies=library.assets||[];assetCache.clear();state=next;newer=false;badge.textContent='Shared Forge · '+state.user.login;q('#sharedPrepare').hidden=state.permissions?.release===false;q('#sharedStatus').textContent='GitHub '+state.head.slice(0,10)+' · game '+state.main.slice(0,10)+' · '+(state.state.current||'No shared revision saved yet');q('#sharedWarning').textContent='';history();if(initial){if(state.state.current){const saved=await get('revision?id='+encodeURIComponent(state.state.current));setOptions(saved.payload.settings)}else setOptions(state.defaults)}document.querySelector('#libNote').textContent='One card per asset. Open its current artwork, or browse animation states, versions and sources. Saves add draft versions; New creates a separate asset. Archive keeps reference material recoverable.';if(document.querySelector('#dLib').open)buildLib()}
async function run(fn){if(busy)return;busy=true;panel.querySelectorAll('button').forEach(b=>b.disabled=true);try{await fn()}catch(e){showError(e)}finally{busy=false;panel.querySelectorAll('button').forEach(b=>b.disabled=false);q('#sharedPrepare').disabled=state?.permissions?.release===false}}
async function open(){if(panel.open)return;q('#sharedSlot').value=/^W0[1-8]$/.test(doc.code)?doc.code:/^A/.test(doc.code)?'ARM':/^T/.test(doc.code)?'TROOPER':/^B/.test(doc.code)?'BACKGROUND':/^[CSE]/.test(doc.code)?'PROP':'W04';q('#sharedVariant').value=/source detail/i.test(doc.name)?'detail':/grid/i.test(doc.name)?'grid':'custom';panel.showModal()}
async function save(){commitFloat();message('Saving revision to GitHub…');if(!state)await refresh(true);const r=await post('save',{expected_head:state.head,sprite:serialise(),slot:q('#sharedSlot').value,variant:q('#sharedVariant').value,weapon_only:q('#sharedWeaponsOnly').checked,settings:opts(),notes:q('#sharedNotes').value.trim()||('Test '+(doc.name||'untitled asset')+' as '+q('#sharedSlot').selectedOptions[0].textContent)});Object.assign(doc,{id:r.id,asset_id:r.asset_id,state_key:r.state_key,source_version:r.id});dirtyDoc=true;draftSave();prepared=null;message('Saved to GitHub: '+r.revision+'\nGame fingerprint: '+r.manifest.files['game.html'].slice(0,16)+'\nNothing has been published to main.');link(q('#sharedResult'),'Open saved test build','/api/game?debug=1&grounds=1&revision='+encodeURIComponent(r.revision));try{await refresh()}catch(e){message('Saved '+r.revision+'. Library refresh failed: '+e.message);link(q('#sharedResult'),'Open saved test build','/api/game?debug=1&grounds=1&revision='+encodeURIComponent(r.revision))}return r}
// The built-in Library now reads repository documents; browser storage is only a recovery draft.
const assetCache=new Map();
async function hydrate(it){if(it.frames)return it;if(!assetCache.has(it.id))assetCache.set(it.id,(await get('asset?ref='+encodeURIComponent(state.head)+'&id='+encodeURIComponent(it.id))).sprite);return {...assetCache.get(it.id),id:it.id}}
const oldLocalLib=localLib;localLib=()=>state?repoDocs:oldLocalLib();
const familyStyle=document.createElement('style');familyStyle.textContent='#libList .libItem:has(details[open]){grid-column:1/-1;display:grid;grid-template-columns:80px minmax(0,1fr)} #libList details .row{padding:5px 0;border-top:1px solid var(--edge)} #libList summary{cursor:pointer} #libList select{max-width:100%}';document.head.append(familyStyle);
const originalBuildLib=buildLib;
buildLib=async()=>{
 if(!state)return originalBuildLib();
 const box=document.querySelector('#libList');box.textContent='';
 let controls=document.querySelector('#catalogControls');
 if(!controls){controls=document.createElement('div');controls.id='catalogControls';controls.className='row';
 const search=document.createElement('input');search.id='catalogSearch';search.placeholder='Search assets…';search.setAttribute('aria-label','Search assets');search.oninput=()=>buildLib();
 const view=document.createElement('select');view.id='catalogView';view.setAttribute('aria-label','Library view');
 for(const label of ['Current assets','Archive']){const o=document.createElement('option');o.textContent=label;view.append(o)}view.onchange=()=>buildLib();
 const filter=document.createElement('select');filter.id='catalogCategory';filter.setAttribute('aria-label','Art category');
 for(const label of ['All art','Weapons','Troopers','Arms','Other art']){const o=document.createElement('option');o.textContent=label;filter.append(o)}filter.onchange=()=>buildLib();
 controls.append(search,view,filter);box.before(controls)}
 const term=document.querySelector('#catalogSearch').value.toLowerCase(),category=document.querySelector('#catalogCategory').value,archive=document.querySelector('#catalogView').value==='Archive';
 const items=assetFamilies.filter(f=>f.archived===archive&&(category==='All art'||f.category===category)&&[f.code,f.name,...f.versions.map(v=>v.name)].join(' ').toLowerCase().includes(term));
 async function openEntry(it,button){button.disabled=true;try{const d=await hydrate(it);await deserialise(d,it.id);document.querySelector('#dLib').close();status('Opened '+it.name)}catch(e){status(e.message)}finally{button.disabled=false}}
 function buttonFor(it,label){const b=document.createElement('button');b.textContent=label;b.onclick=()=>openEntry(it,b);return b}
 for(const f of items){const it=f.versions.find(v=>v.id===f.current);if(!it)continue;
 const row=document.createElement('div');row.className='libItem';row.style.alignItems='start';
 const img=document.createElement('img');img.width=80;img.height=80;img.style='object-fit:contain;image-rendering:pixelated';img.alt='';img.loading='lazy';img.src=it.thumbnail||('/api/thumbnail?ref='+encodeURIComponent(state.head)+'&id='+encodeURIComponent(it.id));
 const body=document.createElement('div');body.style='flex:1;min-width:0';
 const title=document.createElement('b');title.textContent=(f.code?f.code+' · ':'')+f.name;
 const info=document.createElement('p');info.className='note';info.textContent=(it.w||'?')+'×'+(it.h||'?')+' · '+it.frame_count+' frames'+(f.states.length>1?' · '+f.states.length+' states':'')+(it.role==='draft'?' · Latest draft':' · Catalog default');
 body.append(title,info);
 const actions=document.createElement('div');actions.className='row';actions.append(buttonFor(it,'Open'));
 if(f.states.length>1){const select=document.createElement('select');select.setAttribute('aria-label',f.name+' animation state');
 for(const st of f.states){const o=document.createElement('option');o.value=st.current;o.textContent=st.label;select.append(o)}select.value=f.current;
 const openState=document.createElement('button');openState.textContent='Open state';openState.onclick=()=>openEntry(f.versions.find(v=>v.id===select.value),openState);actions.append(select,openState)}body.append(actions);
 const details=document.createElement('details'),summary=document.createElement('summary');summary.textContent='Versions & sources ('+f.versions.length+')';details.append(summary);
 // Populate on demand: old copies never become top-level cards.
 details.ontoggle=()=>{if(!details.open||details.dataset.loaded)return;details.dataset.loaded='1';
 for(const st of f.states){const heading=document.createElement('h4');heading.textContent=st.label;details.append(heading);
 for(const v of f.versions.filter(v=>v.state_key===st.key).slice().reverse()){
 const line=document.createElement('div');line.className='row';const label=document.createElement('span');label.style='flex:1;overflow-wrap:anywhere';
 const role=v.role==='draft'?'Draft':v.id===st.baseline?'Catalog default':v.role==='component'?'Component':v.role==='source'?'Source':'Earlier version';
 label.textContent=role+' · '+v.name+' · '+v.w+'×'+v.h+' · '+v.frame_count+' frames';label.title=v.id;
 line.append(label,buttonFor(v,'Open version'));details.append(line)}}};
 body.append(details);row.append(img,body);box.append(row)}
 if(!items.length)box.textContent='No assets match this search.';
};
// Rig pickers consume full documents only for the selected parts.
const originalRigLoad=typeof rigLoad==='function'?rigLoad:async()=>{};rigLoad=async()=>{for(const id of Object.values(rig.pick)){const i=repoDocs.findIndex(d=>d.id===id);if(i>=0&&!repoDocs[i].frames)repoDocs[i]={...repoDocs[i],...await hydrate(repoDocs[i])}}return originalRigLoad()};
async function saveCurrentAsset(){
 commitFloat();if(!state)await refresh();
 const result=await post('save-asset',{expected_head:state.head,sprite:serialise()});
 Object.assign(doc,{id:result.id,asset_id:result.asset_id,state_key:result.state_key,source_version:result.id});dirtyDoc=true;draftSave();await refresh();status('Saved asset to shared Library');return result;
}
saveToLib=async()=>{try{await saveCurrentAsset()}catch(e){status('Save failed: '+e.message)}};
document.querySelector('#bSave').onclick=saveToLib;document.querySelector('#bSave').textContent='Save asset';
const gameButton=document.querySelector('#bGame');gameButton.href='#shared-forge';gameButton.textContent='Test in game';gameButton.addEventListener('click',e=>{e.preventDefault();e.stopImmediatePropagation();open()},true);badge.onclick=open;
q('#sharedClose').onclick=()=>panel.close();q('#sharedSave').onclick=()=>run(save);
q('#sharedTest').onclick=()=>run(async()=>{
  // Open during the click gesture; always leave failures visible in the Forge.
  const tab=window.open('about:blank','grimspire-shared-test');
  if(tab){tab.document.title='Preparing Grimspire test';tab.document.body.textContent='Saving your artwork and preparing the testing grounds…'}
  try{const r=await save();const url='/api/game?debug=1&grounds=1&revision='+encodeURIComponent(r.revision);if(tab&&!tab.closed)tab.location.replace(url);else message('Saved '+r.revision+'. Your browser blocked the test window.');link(q('#sharedResult'),'Open saved test build',url)}
  catch(e){if(tab&&!tab.closed){tab.document.body.textContent='The test build could not be saved: '+e.message+'. Return to the Forge to retry.'}throw e}
});
q('#sharedRefresh').onclick=()=>run(async()=>{if(!confirm('Refresh the shared library? Your current canvas is kept. Review newer saved artwork before saving over its preview slot.'))return;await refresh();message('Shared library refreshed. Your canvas is unchanged; open the new saved art from Library if you want to continue from it.')});
q('#sharedPrepare').onclick=()=>run(async()=>{if(!state?.state.current)throw Error('Save a shared revision first');prepared=await post('prepare',{revision:state.state.current});review.querySelector('pre').textContent='Revision: '+prepared.revision+'\nMain base: '+prepared.base+'\nCandidate: '+prepared.candidate+'\nGame fingerprint: '+prepared.game_hash+'\n\n'+prepared.notes+'\n\nChanges:\n'+prepared.files.join('\n')+'\n\nReview PR: '+prepared.pr;review.querySelector('input').checked=false;review.querySelector('#publishExact').disabled=true;review.querySelector('#checkPublic').hidden=true;review.showModal()});
review.querySelector('input').onchange=e=>review.querySelector('#publishExact').disabled=!e.target.checked;
review.querySelector('#closeReview').onclick=()=>review.close();
review.querySelector('#publishExact').onclick=async()=>{const b=review.querySelector('#publishExact');b.disabled=true;try{const r=await post('publish',{ticket:prepared.ticket,game_hash:prepared.game_hash,approve:review.querySelector('input').checked});review.querySelector('pre').textContent='Main updated to '+r.main_commit+'\nRevision '+r.revision+'\nPublic deployment is not yet verified.'+(r.warning?'\n'+r.warning:'');review.querySelector('#checkPublic').hidden=false;await refresh()}catch(e){review.querySelector('pre').textContent=e.message;b.disabled=false}};
review.querySelector('#checkPublic').onclick=async()=>{try{const r=await post('check-deployment',{revision:prepared.revision});review.querySelector('pre').textContent=r.message+(r.url?'\n'+r.url:'')}catch(e){review.querySelector('pre').textContent=e.message}};
signOut.onclick=async()=>{if(!state){location.href='/auth/github';return}await fetch('/auth/logout',{method:'POST',headers:{'X-Forge-CSRF':state.csrf}});location.href='/'};
try{await refresh(true)}catch(e){badge.textContent='Shared Forge · connection needs attention';q('#sharedStatus').textContent='GitHub connection needs attention';q('#sharedWarning').textContent=e.message;showError(e)}
setInterval(async()=>{if(!state||busy||review.open)return;try{const next=await get('status');if(next.head!==state.head||next.main!==state.main){newer=true;badge.textContent='Shared Forge · updates available';q('#sharedWarning').textContent='New artwork or code is available. Your canvas has been kept. Refresh the shared library before saving.'}}catch{}},30000);
})();
