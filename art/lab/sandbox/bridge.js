// Companion controls. The browser never receives a GitHub credential.
(()=>{
const panel=document.createElement('dialog');panel.className='wide';panel.innerHTML=`
<h3>Git sandbox</h3><p id="labState">Connecting…</p>
<p class="note">Save records the art, weapon lighting, renderer code and game source as one revision. Testing opens that exact build. Browser-only Save still keeps a local draft.</p>
<label class="row">Preview behaviour <select id="labSlot">${['Launcher','Carbine','Scatter','Dakka','Las gun','Flamer','Chainsword','Claw'].map((n,i)=>`<option value="W0${i+1}">W0${i+1} · ${n}</option>`).join('')}</select></label>
<p class="note">A new sprite can use any existing weapon behaviour for testing. Its own code does not have to be registered.</p>
<div class="row"><label>Darkness <input id="labDark" type="number" min="0" max="1" step="0.05" value="0.66"></label><label>Emissive <input id="labEmis" type="number" min="0" max="2" step="0.1" value="1"></label></div>
<div class="row"><label>Bloom <input id="labBloom" type="number" min="0" max="30" step="1" value="0"></label><label>Weapon scale <input id="labScale" type="number" min="0.05" max="4" step="0.01" value="1"></label><label>Glow colour <input id="labColor" type="color" value="#59edff"></label></div>
<p class="note">Lighting settings apply to the saved weapon set. Source-detail art needs a smaller scale than grid art. Firing behaviour and effect origins follow the current game rules; this adapter changes weapon rendering.</p>
<label>Update note<textarea id="labNotes" rows="3" placeholder="What changed and why?"></textarea></label>
<div class="row"><button id="labSave">Save revision to Git</button><button id="labTest">Save & test in game</button><button id="labRetry">Retry push</button></div>
<div class="row"><button id="labPrepare">Review release…</button><button id="labRefresh">Refresh from main</button><button id="labClose">Close</button></div>
<pre id="labResult" style="white-space:pre-wrap;overflow-wrap:anywhere"></pre>
<p class="note">In the game: start a local battle, then open TEST for weapon supply, extra troopers and an unlimited timer. Online play is disabled in the companion preview.</p>`;
document.body.append(panel);
const q=s=>panel.querySelector(s);let state=null,prepared=null,busy=false;
const review=document.createElement('dialog');review.className='wide';review.innerHTML='<h3>Go live</h3><pre style="white-space:pre-wrap;overflow-wrap:anywhere"></pre><p><label><input type="checkbox"> I tested this exact revision in the game, checked scale, anchors and effects, and approve it for main.</label></p><p class="note">This updates main. Deployment depends on the repository’s publishing configuration. A newer main commit blocks promotion and requires a fresh test.</p><div class="row"><button id="labLive" disabled>Go live</button><button id="labCancel">Cancel</button></div>';document.body.append(review);
const result=t=>q('#labResult').textContent=t;
async function connect(){const r=await fetch('/api/state',{cache:'no-store'});if(!r.ok)throw Error('Start python3 art/lab/sandbox/serve.py in your clone and open its 127.0.0.1 URL.');state=await r.json();if(state.error)throw Error(state.error);q('#labState').textContent=state.branch+' · '+state.head.slice(0,10)+' · '+(state.current?state.current.revision:'No Git revision saved yet');return state}
async function api(path,body){if(!state)await connect();const r=await fetch('/api/'+path,{method:'POST',headers:{'Content-Type':'application/json','X-Lab-Token':state.token},body:JSON.stringify(body)});const data=await r.json();if(!r.ok||data.error)throw Error(data.error||'Operation failed');return data}
async function run(fn){if(busy)return;busy=true;panel.querySelectorAll('button').forEach(b=>b.disabled=true);try{await fn()}catch(e){result(e.message)}finally{busy=false;panel.querySelectorAll('button').forEach(b=>b.disabled=false)}}
const opts=()=>({darkness:+q('#labDark').value,emissive:+q('#labEmis').value,bloom:+q('#labBloom').value,scale:+q('#labScale').value,glowColor:q('#labColor').value});
async function save(){commitFloat();await connect();const data=await api('save',{sprite:serialise(),slot:q('#labSlot').value,notes:q('#labNotes').value,settings:opts(),expected_head:state.head});prepared=null;result(JSON.stringify(data,null,2));await connect();return data}
async function open(){if(!doc){status('Forge is still loading');return}if(panel.open)return;panel.showModal();q('#labSlot').value=/^W0[1-8]$/.test(doc.code)?doc.code:'W04';try{await connect()}catch(e){result(e.message)}}
const button=document.createElement('button');button.textContent='Git sandbox';button.id='bGitSandbox';button.onclick=open;document.querySelector('#bGame').after(button);
document.querySelector('#bGame').addEventListener('click',e=>{e.preventDefault();e.stopImmediatePropagation();open()},true);
q('#labClose').onclick=()=>panel.close();q('#labSave').onclick=()=>run(save);
q('#labTest').onclick=()=>run(async()=>{const tab=window.open('about:blank','grimspire-art-test');try{await save();const url='/api/game?debug=1&revision='+encodeURIComponent(state.current.revision);if(tab)tab.location.href=url;else{const a=document.createElement('a');a.href=url;a.target='_blank';a.textContent='Open saved game revision';q('#labResult').append(document.createElement('br'),a)}}catch(e){if(tab)tab.close();throw e}});
q('#labRetry').onclick=()=>run(async()=>result(JSON.stringify(await api('push',{}),null,2)));
q('#labRefresh').onclick=()=>run(async()=>{result(JSON.stringify(await api('refresh',{}),null,2));await connect()});
q('#labPrepare').onclick=()=>run(async()=>{await connect();prepared=await api('prepare',{revision:state.current&&state.current.revision});result(JSON.stringify(prepared,null,2));review.querySelector('pre').textContent=JSON.stringify(prepared,null,2);review.querySelector('input').checked=false;review.querySelector('#labLive').disabled=true;review.showModal()});
review.querySelector('input').onchange=e=>review.querySelector('#labLive').disabled=!e.target.checked;
review.querySelector('#labCancel').onclick=()=>review.close();
review.querySelector('#labLive').onclick=async()=>{const b=review.querySelector('#labLive');b.disabled=true;try{if(!review.querySelector('input').checked)return;const data=await api('publish',{commit:prepared.commit,tested_hash:prepared.game_sha256,confirm:'GO LIVE'});review.querySelector('pre').textContent=JSON.stringify(data,null,2)}catch(e){review.querySelector('pre').textContent=e.message;b.disabled=false}};
})();
