import {signAppJwt,privateKeyStatus} from './github-key.mjs';
import {Buffer} from 'node:buffer';
import {organiseAssets} from './families.mjs';
import {BUILD_SHA} from './generated/build-info.mjs';
import {REPO,LAB,ROOT,DEFAULTS,SLOTS,Problem,check,utf,json,sha,options,sprite,clean,build,revision,loadSnapshot} from './model.mjs';
const sec=()=>Math.floor(Date.now()/1000), b64=b=>Buffer.from(b).toString('base64url');
const headers={'Cache-Control':'no-store','X-Content-Type-Options':'nosniff','Referrer-Policy':'no-referrer','X-Frame-Options':'DENY'};
const response=(data,status=200)=>new Response(json(data),{status,headers:{...headers,'Content-Type':'application/json'}});
const html=(s,status=200,extra={})=>new Response(s,{status,headers:{...headers,'Content-Type':'text/html; charset=utf-8',...extra}});
const redirect=(url,cookies=[])=>{const h=new Headers({...headers,Location:url});for(const c of cookies)h.append('Set-Cookie',c);return new Response(null,{status:302,headers:h})};
const cookie=(name,value,age)=>`${name}=${value}; Path=/; Max-Age=${age}; Secure; HttpOnly; SameSite=Lax`;
function cookies(request){return Object.fromEntries((request.headers.get('cookie')||'').split(';').map(s=>s.trim().split(/=(.*)/s)).filter(a=>a.length>=2).map(a=>[a[0],a[1]]))}
async function key(env){check(env.GITHUB_CLIENT_SECRET,'Add GITHUB_CLIENT_SECRET as a Cloudflare Secret',503);return crypto.subtle.importKey('raw',await crypto.subtle.digest('SHA-256',utf('grimspire-forge.cookies.v1\0'+env.APP_ORIGIN+'\0'+env.GITHUB_CLIENT_SECRET)),'AES-GCM',false,['encrypt','decrypt'])}
export async function seal(env,value){const iv=crypto.getRandomValues(new Uint8Array(12));return b64(iv)+'.'+b64(await crypto.subtle.encrypt({name:'AES-GCM',iv},await key(env),utf(JSON.stringify(value))))}
export async function unseal(env,s,kind){try{const[a,b]=s.split('.');const value=JSON.parse(new TextDecoder().decode(await crypto.subtle.decrypt({name:'AES-GCM',iv:Buffer.from(a,'base64url')},await key(env),Buffer.from(b,'base64url'))));check(value.kind===kind&&value.exp>sec(),'Session expired',401);return value}catch{throw new Problem('Sign in to the Forge again',401)}}
export function roleFor(env,id){
  const uid=String(id);if(uid===env.ALLOWED_GITHUB_USER_ID)return 'owner';
  const allowed=(env.COLLABORATOR_GITHUB_IDS||'').split(',').map(x=>x.trim()).filter(x=>/^[1-9][0-9]*$/.test(x));
  check(allowed.includes(uid),'This GitHub account has not been invited to the Forge',403);return 'collaborator';
}
function ownerOnly(user,env){check(String(user.id)===env.ALLOWED_GITHUB_USER_ID,'Only the Forge owner can release changes to the live game',403)}
async function session(req,env){const raw=cookies(req).forge_session;check(raw,'Sign in to the Forge',401);const user=await unseal(env,raw,'session');return {...user,role:roleFor(env,user.id)}}

export class GitHub{
  constructor(env,fetcher=fetch){this.env=env;this.fetch=async(input,init)=>{try{return await fetcher.call(globalThis,input,init)}catch(e){const reason=/illegal invocation/i.test(e.message)?'runtime binding':/too many subrequests/i.test(e.message)?'request limit':'network transport';throw new Problem('GitHub request failed at '+reason+'. The request outcome could not be confirmed.',503)}};this.token=null}
  async auth(){if(!this.pending)this.pending=this.authenticate();return this.pending}
  async authenticate(){if(this.token)return this.token;const env=this.env;check(env.GITHUB_PRIVATE_KEY&&env.GITHUB_APP_ID&&env.GITHUB_INSTALLATION_ID,'Missing GitHub App credentials in Cloudflare',503);const token=await signAppJwt(env);const r=await this.fetch('https://api.github.com/app/installations/'+env.GITHUB_INSTALLATION_ID+'/access_tokens',{method:'POST',headers:{Authorization:'Bearer '+token,Accept:'application/vnd.github+json','User-Agent':'Grimspire-Forge','Content-Type':'application/json'},body:JSON.stringify({repositories:['Grimspire']})});check(r.ok,'GitHub App authentication failed. Check its key, App ID and installation.',503);this.token=(await r.json()).token;return this.token}
  async call(path,method='GET',data,optional=false){const r=await this.fetch('https://api.github.com/repos/'+REPO+path,{method,headers:{Authorization:'Bearer '+await this.auth(),Accept:'application/vnd.github+json','User-Agent':'Grimspire-Forge','Content-Type':'application/json'},...(data===undefined?{}:{body:JSON.stringify(data)})});if(optional&&r.status===404)return null;if(!r.ok){let message='';try{message=(await r.json()).message||''}catch{}throw new Problem('GitHub rejected '+method+' '+path.split('?')[0]+': '+message+(r.status===422?' — another revision may have been saved; refresh before retrying.':''),r.status===401||r.status===403?503:409)}return r.status===204?null:r.json()}
  async head(branch){return(await this.call('/git/ref/heads/'+branch)).object.sha}
  commit(id){return this.call('/git/commits/'+id)}
  async file(path,ref,optional=false){const d=await this.call('/contents/'+path+'?ref='+encodeURIComponent(ref),'GET',undefined,optional);if(d===null)return null;check(d.type==='file','Unsupported repository file: '+path);const blob=d.encoding==='base64'?d:await this.call('/git/blobs/'+d.sha);check(blob.encoding==='base64','Unsupported repository blob: '+path);return Buffer.from(blob.content.replace(/\s/g,''),'base64').toString('utf8')}
  async state(ref){const s=await this.file(ROOT+'/state.json',ref,true);return s?JSON.parse(s):{schema:1,current:null,revisions:[],integrations:[]}}
  async treeCommit(parent,files,message){const base=await this.commit(parent),tree=await this.call('/git/trees','POST',{base_tree:base.tree.sha,tree:Object.entries(files).map(([path,content])=>({path,mode:'100644',type:'blob',content}))});return(await this.call('/git/commits','POST',{message,tree:tree.sha,parents:[parent]})).sha}
  // Never force a ref. A sibling commit fails if another editor advanced it.
  update(branch,id){return this.call('/git/refs/heads/'+branch,'PATCH',{sha:id,force:false})}
  async append(state,files,parent,message){const id=await this.treeCommit(parent,{...files,[ROOT+'/state.json']:json(state)},message);await this.update(LAB,id);return id}
  snapshot(id,ref){return loadSnapshot(this,id,ref)}
}
// Catalog entries contain small thumbnails; pixel data is fetched only when opened.
export async function assetLibrary(g,ref){
 const source=JSON.parse(await g.file(ROOT+'/assets.json',ref,true)||'{"entries":[]}');
 const saved=JSON.parse(await g.file(ROOT+'/library.json',ref,true)||'{"entries":[]}');
 const migration=JSON.parse(await g.file(ROOT+'/families.json',ref,true)||'{"assets":[]}');
 return organiseAssets(source,saved,migration);
}
export async function assetIndex(g,ref){return (await assetLibrary(g,ref)).docs}
export async function openAsset(g,ref,id){
 const entry=(await assetIndex(g,ref)).find(e=>e.id===id);check(entry,'Asset no longer exists; refresh the Library');
 check(/^art\/lab\/hosted\/(catalog|library)\/[a-zA-Z0-9_.-]+\.forge\.json$/.test(entry.path),'Invalid asset path');
 const raw=await g.file(entry.path,ref);check(await sha(raw)===entry.sha256,'Asset hash mismatch');
 return {...sprite(JSON.parse(raw),'ASSET'),asset_id:entry.asset_id,state_key:entry.state_key,source_version:entry.id};
}
export async function retainAsset(g,d,head,paths){
 const library=await assetLibrary(g,head);
 let family=library.assets.find(f=>f.id===d.asset_id);
 // Recover exact old payloads and browser drafts by provenance, never by display code.
 if(!family&&!d.asset_id){
  const old=library.docs.find(e=>e.id===d.source_version||e.id===d.id||(d.legacy_hash&&e.legacy_hash===d.legacy_hash));
  if(old){family=library.assets.find(f=>f.id===old.asset_id);d.state_key=old.state_key}
 }
 check(!d.asset_id||family,'This asset identity is no longer registered. Refresh the Library.');
 const assetId=family?.id||'custom-'+crypto.randomUUID();
 const stateKey=family?(d.state_key||''):'';
 check(!family||family.states.some(s=>s.key===stateKey),'Choose an existing animation state before saving.');
 d={...d,asset_id:assetId,state_key:stateKey};delete d.legacy_hash;
 const raw=json(d),hash=await sha(raw),id='asset-'+hash.slice(0,24),path=ROOT+'/library/'+id+'.forge.json';
 const index=JSON.parse(await g.file(ROOT+'/library.json',head,true)||'{"schema":1,"entries":[]}');
 if(!index.entries.some(e=>e.id===id))index.entries.push({id,path,sha256:hash,asset_id:assetId,state_key:stateKey,asset_name:family?.name||d.name||'Untitled',code:d.code||'',name:d.name||'Untitled',w:d.w,h:d.h,frame_count:d.frames.length,category:family?.category||(/^A/.test(d.code)?'Arms':/^T/.test(d.code)?'Troopers':/^W/.test(d.code)?'Weapons':'Other art')});
 paths[path]=raw;paths[ROOT+'/library.json']=json(index);return {id,asset_id:assetId,state_key:stateKey};
}
export async function saveAsset(g,body,user){
 const d=sprite(body.sprite,'ASSET'),head=await g.head(LAB);check(head===body.expected_head,'Another update arrived. Refresh the shared library before saving.');
 const paths={},identity=await retainAsset(g,d,head,paths),state=await g.state(head);
 const commit=await g.append(state,paths,head,'Save Forge asset '+(d.code||'')+' '+d.name);return{...identity,commit};
}
// The test build: the shared build's art with this sprite in the chosen slot, on the current main game.
async function testBuild(g,body,head,main){check(SLOTS[body.slot],'Choose a test target');const d=sprite(body.sprite,body.slot),opts=options(body.settings);const state=await g.state(head);let payload={assets:{}};
  if(state.current){const prior=await g.snapshot(state.current,head);payload=JSON.parse(prior['payload.json'])}
  if(body.weapon_only===true&&/^W0[1-8]$/.test(body.slot))payload.assets=Object.fromEntries(Object.entries(payload.assets).filter(([k])=>/^W0[1-8]$/.test(k)||k==='ARM'));
  // Freeze each carried asset at its old effective size before changing the selected one.
  for(const [slot,art] of Object.entries(payload.assets))payload.assets[slot]={...art,game_scale:art.game_scale??(slot==='ARM'?1:payload.settings?.scale??1)};
  d.game_scale=opts.scale;
  payload={...payload,assets:{...payload.assets,[body.slot]:d},selected_slot:body.slot,settings:{...opts,scale:1}};
  if(!payload.assets.ARM){const arm=await g.file(ROOT+'/catalog/single-gun-arm-shoulder-v002.forge.json',head,true)||await g.file(ROOT+'/catalog/single-gun-arm-v001.forge.json',head,true);if(arm)payload.assets.ARM={...JSON.parse(arm),game_scale:1}}
  const source=await g.file('index.html',main);return{d,payload,state,source}}
// Try art in the game without saving anything. Same build as Save & test, nothing committed.
export async function preview(g,body){const head=await g.head(LAB),main=await g.head('main'),{payload,source}=await testBuild(g,body,head,main);return build(source,'',{...payload,revision:'unsaved preview'})}
// Same test build tools/build.py makes: noindex, TEST panel on, its own title.
export function debugBuild(game){return game.replace('<meta property="og:url" content="https://astrosomnia.github.io/Grimspire/">','<meta name="robots" content="noindex">').replace('<style>body{margin:0}</style>\n','<style>body{margin:0}</style>\n<script>window.GS_DEBUG=1</script>\n').replace('<title>Grimspire</title>','<title>Grimspire Test</title>')}
export async function save(g,body,user){check(typeof body.notes==='string'&&body.notes.trim().length>0&&body.notes.length<=4000,'Add a short update note');check(['grid','detail','custom'].includes(body.variant),'Choose a sprite variant');const head=await g.head(LAB);check(head===body.expected_head,'Another revision or code update arrived. Refresh the shared library before saving your draft.');const main=await g.head('main');
  let {d,payload,state,source}=await testBuild(g,body,head,main);
  const id=new Date().toISOString().replace(/[-:.]/g,'').slice(0,15)+'Z-'+crypto.randomUUID().slice(0,8);
  const retained={},identity=await retainAsset(g,d,head,retained);Object.assign(d,{asset_id:identity.asset_id,state_key:identity.state_key,source_version:identity.id});
  payload={...payload,revision:id,assets:{...payload.assets,[body.slot]:d}};
  // Store the payload only; the game is rebuilt from main@base_main and checked against this fingerprint.
  const game=build(source,'',payload),payloadRaw=json(payload);
  const manifest={schema:2,id,created:new Date().toISOString(),author:{id:user.id,login:user.login},base_main:main,source_lab_commit:head,notes:body.notes.trim(),selected_slot:body.slot,original_code:d.code||'',variant:body.variant,slots:Object.keys(payload.assets),files:{'game.html':await sha(game),'payload.json':await sha(payloadRaw)},stored:['payload.json'],status:'draft'};
  const paths={[revision(id)+'/payload.json']:payloadRaw,[revision(id)+'/manifest.json']:json(manifest),...retained};state.current=id;state.revisions.push({id,created:manifest.created,notes:manifest.notes,slot:body.slot,variant:body.variant,author:user.login});const commit=await g.append(state,paths,head,'Forge revision '+id+'\n\n'+manifest.notes);return{revision:id,commit,manifest,...identity}
}
// One line in the shared log on main, added by the release commit itself.
export async function logEntry(g,main,m,login){const log=await g.file('docs/LOG.md',main,true);if(log===null)return null;const day=new Date().toISOString().slice(0,10),entry='## '+day+' · Forge · Art release '+m.id+'\n- '+m.notes.split('\n')[0].slice(0,300)+'\n- Slots: '+(m.slots||[]).join(', ')+'. Released by '+login+'. Receipt: `art/integrations/'+m.id+'.json`\n\n';const i=log.indexOf('\n## ');return i<0?log+'\n'+entry:log.slice(0,i+1)+entry+log.slice(i+1)}
export async function prepare(g,body,user,env){ownerOnly(user,env);const head=await g.head(LAB),state=await g.state(head);check(state.current===body.revision,'A newer saved revision exists. Review that revision or save the desired art again.');const snap=await g.snapshot(body.revision,head),m=snap.manifest;check(Object.keys(JSON.parse(snap['payload.json']).assets).every(k=>/^W0[1-8]$/.test(k)||k==='ARM'),'This revision contains category test dummies. Props, trooper frames and backgrounds need a game integration before Go live; their visual test does not define collision, spawning or animation rules.');const main=await g.head('main');check(main===m.base_main,'Claude updated main after this revision was saved. Save a new revision against current main and test it again.');
  const receipt={revision:m.id,base_main:main,game_sha256:m.files['game.html'],notes:m.notes,source_lab_commit:m.source_lab_commit,status:'prepared; deployment unverified'};const branch='art/release-'+m.id;let candidate;const existing=await g.call('/git/ref/heads/'+branch,'GET',undefined,true);
  if(existing){candidate=existing.object.sha;const c=await g.commit(candidate);check(c.parents.length===1&&c.parents[0].sha===main,'Release branch has changed');check(await sha(await g.file('index.html',candidate))===m.files['game.html'],'Release artwork changed');}
  else{const files={'index.html':snap['game.html'],'debug/index.html':debugBuild(snap['game.html']),['art/integrations/'+m.id+'.json']:json(receipt)},log=await logEntry(g,main,m,user.login);if(log!==null)files['docs/LOG.md']=log;candidate=await g.treeCommit(main,files,'Promote Forge '+m.id+'\n\n'+m.notes+'\n\nGame SHA-256: '+m.files['game.html']);await g.call('/git/refs','POST',{ref:'refs/heads/'+branch,sha:candidate})}
  const prs=await g.call('/pulls?state=open&head=Astrosomnia:'+encodeURIComponent(branch)+'&base=main');const pr=prs[0]||await g.call('/pulls','POST',{title:'Forge art release '+m.id,head:branch,base:'main',body:m.notes+'\n\nTested game SHA-256: `'+m.files['game.html']+'`\nBase main: `'+main+'`\n\nOnly the saved game, debug build and integration receipt are promoted. The lab branch is not merged.'});
  const approval={kind:'release',exp:sec()+1800,user:user.id,revision:m.id,lab_head:head,base:main,candidate,branch,game_hash:m.files['game.html'],pr:pr.html_url};return{...approval,ticket:await seal(env,approval),notes:m.notes,files:['index.html','debug/index.html','art/integrations/'+m.id+'.json']}
}
export async function publish(g,body,user,env){ownerOnly(user,env);const release=await unseal(env,body.ticket,'release');check(release.user===user.id&&body.approve===true,'Confirm approval of this exact revision');check(body.game_hash===release.game_hash,'Tested build hash does not match');check(await g.head(LAB)===release.lab_head,'The shared workspace changed after review. Review the release again.');check(await g.head('main')===release.base,'Main changed after review. Save and retest against current main.');check(await g.head(release.branch)===release.candidate,'The release branch changed after review');const c=await g.commit(release.candidate);check(c.parents.length===1&&c.parents[0].sha===release.base,'Release is not a direct child of tested main');
  // Compare the full candidate tree to the expected build, including all other files.
  const state=await g.state(release.lab_head),snap=await g.snapshot(release.revision,release.lab_head),m=snap.manifest;const base=await g.commit(release.base);const receipt=await g.file('art/integrations/'+m.id+'.json',release.candidate);const log=await g.file('docs/LOG.md',release.candidate,true),logged=log!==null&&log!==await g.file('docs/LOG.md',release.base,true);const tree=await g.call('/git/trees','POST',{base_tree:base.tree.sha,tree:[['index.html',snap['game.html']],['debug/index.html',debugBuild(snap['game.html'])],['art/integrations/'+m.id+'.json',receipt],...(logged?[['docs/LOG.md',log]]:[])].map(([path,content])=>({path,content,mode:'100644',type:'blob'}))});check(tree.sha===c.tree.sha&&await sha(snap['game.html'])===release.game_hash,'Candidate contains changes outside the tested release');
  const checks=await g.call('/commits/'+release.candidate+'/check-runs'),status=await g.call('/commits/'+release.candidate+'/status');check((checks.check_runs||[]).every(x=>x.status==='completed'&&['success','neutral','skipped'].includes(x.conclusion)),'Release checks are pending or failed');check((status.statuses||[]).every(x=>x.state==='success'),'Release commit statuses are pending or failed');
  // Atomic fast-forward: if main moves in the gap after the checks above, GitHub
  // refuses this sibling commit. No force, merge fallback or protection bypass.
  await g.update('main',release.candidate);
  const integration={revision:release.revision,main_commit:release.candidate,game_sha256:release.game_hash,approved_by:user.login,approved_at:new Date().toISOString(),pr:release.pr,status:'main updated; deployment unverified'};state.integrations=state.integrations||[];state.integrations.push(integration);let warning;
  try{await g.append(state,{[ROOT+'/events/'+release.revision+'-integrated.json']:json(integration)},release.lab_head,'Record Forge approval and integration '+release.revision)}catch{warning='Main was updated. The lab log could not be advanced because another save arrived; the production integration receipt remains recorded.'}
  return{...integration,warning}
}
export async function handle(request,env,dependencies={}){const fetcher=dependencies.fetch||fetch,url=new URL(request.url);try{
  check(url.origin===env.APP_ORIGIN,'Use the configured Forge URL',400);
  if(url.pathname==='/health')return response({service:'Grimspire Forge',build_sha:BUILD_SHA,private_key:await privateKeyStatus(env.GITHUB_PRIVATE_KEY),configured:!!(env.GITHUB_APP_ID&&env.GITHUB_CLIENT_ID&&env.GITHUB_INSTALLATION_ID&&env.GITHUB_PRIVATE_KEY&&env.GITHUB_CLIENT_SECRET),deployment:'Hosted application code is running'});
  if(url.pathname==='/auth/github'){
    check(request.method==='GET','Method not allowed',405);const nonce=crypto.randomUUID(),state=await seal(env,{kind:'oauth',nonce,exp:sec()+600});return redirect('https://github.com/login/oauth/authorize?'+new URLSearchParams({client_id:env.GITHUB_CLIENT_ID,redirect_uri:env.APP_ORIGIN+'/auth/github/callback',state:nonce}),[cookie('forge_oauth',state,600)])}
  if(url.pathname==='/auth/github/callback'){
    const pending=await unseal(env,cookies(request).forge_oauth||'','oauth');check(pending.nonce===url.searchParams.get('state'),'GitHub sign-in state did not match',403);const code=url.searchParams.get('code');check(code&&code.length<1024,'GitHub did not provide an authorization code');const tokenResponse=await fetcher('https://github.com/login/oauth/access_token',{method:'POST',headers:{Accept:'application/json','Content-Type':'application/json'},body:JSON.stringify({client_id:env.GITHUB_CLIENT_ID,client_secret:env.GITHUB_CLIENT_SECRET,code,redirect_uri:env.APP_ORIGIN+'/auth/github/callback'})});check(tokenResponse.ok,'GitHub sign-in exchange failed',503);const token=await tokenResponse.json();check(token.access_token,'GitHub sign-in failed. Try signing in again.',401);const result=await fetcher('https://api.github.com/user',{headers:{Authorization:'Bearer '+token.access_token,Accept:'application/vnd.github+json','User-Agent':'Grimspire-Forge'}});check(result.ok,'Could not verify GitHub identity',401);const user=await result.json();roleFor(env,user.id);return redirect('/forge.html',[cookie('forge_oauth','',0),cookie('forge_session',await seal(env,{kind:'session',id:user.id,login:user.login,csrf:crypto.randomUUID(),exp:sec()+21600}),21600)])}
  let user;try{user=await session(request,env)}catch(e){if(url.pathname.startsWith('/api/'))throw e;return html('<!doctype html><meta name="viewport" content="width=device-width"><title>Grimspire Forge</title><style>body{background:#090c12;color:#e6e4dd;font:18px system-ui;max-width:600px;margin:15vh auto;padding:24px}a{display:inline-block;background:#63e7e9;color:#091014;padding:14px 24px;border-radius:8px;text-decoration:none}</style><h1>Grimspire Forge</h1><p>Our shared weapon and art workspace. Sign in to draw, save revisions and test in the game.</p><a href="/auth/github">Sign in with GitHub</a>')}
  if(url.pathname==='/auth/logout'){check(request.method==='POST','Use the sign-out button',405);check(request.headers.get('Origin')===env.APP_ORIGIN&&request.headers.get('X-Forge-CSRF')===user.csrf,'Request origin or session did not match',403);return redirect('/',[cookie('forge_session','',0)])}
  const g=new GitHub(env,fetcher);
  if(request.method==='GET'&&url.pathname==='/api/status'){const[lab,main]=await Promise.all([g.head(LAB),g.head('main')]);return response({user:{login:user.login,id:user.id,role:user.role},permissions:{release:user.role==='owner'},csrf:user.csrf,build_sha:BUILD_SHA,head:lab,main,state:await g.state(lab),defaults:DEFAULTS})}
  if(request.method==='GET'&&url.pathname==='/api/library'){
    const ref=url.searchParams.get('ref');check(/^[a-f0-9]{40}$/.test(ref||''),'Refresh the workspace before loading the library');
    return response({head:ref,...await assetLibrary(g,ref)})
  }
  if(request.method==='GET'&&url.pathname==='/api/thumbnail'){
    const ref=url.searchParams.get('ref');check(/^[a-f0-9]{40}$/.test(ref||''),'Refresh the Library first');
    const d=await openAsset(g,ref,url.searchParams.get('id'));return new Response(Buffer.from(d.frames[0].body.slice(22),'base64'),{headers:{...headers,'Content-Type':'image/png'}});
  }
  if(request.method==='GET'&&url.pathname==='/api/asset'){
    const ref=url.searchParams.get('ref');check(/^[a-f0-9]{40}$/.test(ref||''),'Refresh the Library first');
    return response({sprite:await openAsset(g,ref,url.searchParams.get('id'))});
  }
  if(request.method==='GET'&&url.pathname==='/api/revision'){const id=url.searchParams.get('id'),head=await g.head(LAB),s=await g.snapshot(id,head);const payload=JSON.parse(s['payload.json']);for(const d of Object.values(payload.assets))if(!d.asset_id)d.legacy_hash=await sha(JSON.stringify(d));return response({manifest:s.manifest,payload})}
  if(request.method==='GET'&&url.pathname==='/api/game'){const id=url.searchParams.get('revision'),head=await g.head(LAB),s=await g.snapshot(id,head);return html(s['game.html'],200,{'Content-Security-Policy':"connect-src 'none'; frame-src 'none'; form-action 'none'; base-uri 'none'; object-src 'none'"})}
  // Unsaved test: the editor posts a form into the test window, so the game page loads with this URL.
  if(request.method==='POST'&&url.pathname==='/api/game'){check(request.headers.get('Origin')===env.APP_ORIGIN,'Request origin did not match',403);check(+(request.headers.get('Content-Length')||0)<=12_000_000,'Test art is too large',413);const form=await request.formData();check(form.get('csrf')===user.csrf,'Session did not match. Reload the Forge and try again.',403);const raw=form.get('body');check(typeof raw==='string'&&utf(raw).length<=12_000_000,'Test art is too large',413);let game;try{game=await preview(g,JSON.parse(raw))}catch(e){if(!(e instanceof Problem))throw e;return html('<!doctype html><meta name="viewport" content="width=device-width"><title>Test failed</title><body style="background:#090c12;color:#e6e4dd;font:18px system-ui;max-width:600px;margin:15vh auto;padding:24px"><h1>Couldn\'t build the test</h1><p>'+e.message.replace(/[<&]/g,c=>c==='<'?'&lt;':'&amp;')+'</p><p>Close this tab and try again from the Forge.</p>',e.status)}return html(game,200,{'Content-Security-Policy':"connect-src 'none'; frame-src 'none'; form-action 'none'; base-uri 'none'; object-src 'none'"})}
  if(url.pathname.startsWith('/api/')){
    check(request.method==='POST','Method not allowed',405);check(request.headers.get('Origin')===env.APP_ORIGIN&&request.headers.get('X-Forge-CSRF')===user.csrf,'Request origin or session did not match',403);check(request.headers.get('Content-Type')?.startsWith('application/json'),'Expected JSON',415);check(+(request.headers.get('Content-Length')||0)<=12_000_000,'Save is too large',413);const raw=await request.text();check(utf(raw).length<=12_000_000,'Save is too large',413);const body=JSON.parse(raw);
    if(url.pathname==='/api/save-asset')return response(await saveAsset(g,body,user));
    if(url.pathname==='/api/save')return response(await save(g,body,user));
    if(url.pathname==='/api/prepare')return response(await prepare(g,body,user,env));
    if(url.pathname==='/api/publish')return response(await publish(g,body,user,env));
    if(url.pathname==='/api/check-deployment'){ownerOnly(user,env);const head=await g.head(LAB),s=await g.snapshot(body.revision,head);const main=await g.head('main');check(await sha(await g.file('index.html',main))===s.manifest.files['game.html'],'Main no longer contains this revision');let pages;try{const deployments=await g.call('/deployments?sha='+main+'&environment=github-pages&per_page=1');if(deployments[0]){const statuses=await g.call('/deployments/'+deployments[0].id+'/statuses');const success=statuses.find(x=>x.state==='success'&&x.environment_url);if(success)pages={html_url:success.environment_url}}}catch{}if(!pages)try{pages=await g.call('/pages','GET',undefined,true)}catch{}if(!pages?.html_url)return response({verified:false,message:'GitHub Pages could not be identified. Main is updated; public deployment remains unverified.'});const publicURL=new URL(pages.html_url);check(publicURL.protocol==='https:'&&publicURL.hostname==='astrosomnia.github.io','Unexpected public game URL');publicURL.searchParams.set('forge_verify',crypto.randomUUID());const r=await fetcher(publicURL.href,{cache:'no-store'});const verified=r.ok&&await sha(await r.text())===s.manifest.files['game.html'];let logged=false;if(verified){const state=await g.state(head),record={revision:body.revision,observed_main_commit:main,game_sha256:s.manifest.files['game.html'],url:pages.html_url,verified_at:new Date().toISOString()};const item=(state.integrations||[]).find(x=>x.revision===body.revision);if(item)item.deployment=record;try{await g.append(state,{[ROOT+'/events/'+body.revision+'-deployment.json']:json(record)},head,'Verify public deployment '+body.revision);logged=true}catch{}}return response({verified,logged,url:pages.html_url,main_commit:main,revision:body.revision,message:verified?'Public game matches the approved build.'+(logged?' Verification recorded in GitHub.':' Verification log could not be saved; retry to record it.'):'The public game has not yet matched this build. Try checking again shortly.'})}
    throw new Problem('Unknown Forge operation',404)
  }
  check(request.method==='GET'||request.method==='HEAD','Method not allowed',405);check(['/','/forge','/forge.html','/bridge.js'].includes(url.pathname),'Not found',404);const assetURL=new URL(request.url);if(url.pathname==='/')assetURL.pathname='/forge.html';const r=await env.ASSETS.fetch(new Request(assetURL,request));const h=new Headers(r.headers);for(const[k,v]of Object.entries(headers))h.set(k,v);return new Response(r.body,{status:r.status,headers:h})
}catch(e){if(e instanceof Problem)return response({error:e.message},e.status);const category=['TypeError','SyntaxError','RangeError'].includes(e?.name)?e.name:'InternalError';return response({error:'Forge backend '+category+' while handling '+url.pathname+'. Retry or report this operation to the developer.',code:'forge_'+category.toLowerCase(),operation:url.pathname},500)}}
export default{fetch:handle};
