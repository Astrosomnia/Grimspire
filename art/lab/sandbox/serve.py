#!/usr/bin/env python3
"""Local Git companion: python3 art/lab/sandbox/serve.py. Requires git + gh login."""
import argparse, datetime, functools, http.server, json, os, re, secrets, subprocess, tempfile, threading, uuid
from pathlib import Path
from urllib.parse import urlsplit, parse_qs, unquote
from build import ROOT, SLOTS, DEFAULTS, build, digest, encode, settings, sprite, clean_source
REPO=ROOT.parents[2]
LAB=ROOT.parent
BRANCH='art/weapon-lab'
LOCK=threading.Lock()


def git(*args, cwd=None, data=None, env=None, raw=False):
    p=subprocess.run(['git',*args],cwd=cwd or REPO,input=data,capture_output=True,env=env,timeout=90)
    if p.returncode:raise ValueError(p.stderr.decode(errors='replace').strip() or 'Git operation failed')
    return p.stdout if raw else p.stdout.decode().strip()

def current():
    p=ROOT/'current.json'
    return json.loads(p.read_text()) if p.exists() else None

def head():return git('rev-parse','HEAD')

def snapshot(revision=None):
    c=current()
    revision=revision or (c and c['revision'])
    if not revision or not re.fullmatch(r'[0-9TZa-f-]+',revision):raise ValueError('Save a revision first')
    p=ROOT/'revisions'/revision
    m=json.loads((p/'manifest.json').read_text())
    for name,sha in m['files'].items():
        if name not in ['game.html','payload.json','source.html','runtime.js']:raise ValueError('Invalid release file')
        if digest((p/name).read_bytes())!=sha:raise ValueError('Release hash mismatch: '+name)
    return p,m

def ensure_branch(expected):
    if git('branch','--show-current')!=BRANCH:raise ValueError('Switch to '+BRANCH+' before saving')
    if expected!=head():raise ValueError('Workspace changed. Reload before saving.')
    dirty=git('status','--porcelain','--untracked-files=all')
    allowed={'art/lab/sandbox/game.html','art/lab/sandbox/runtime.js','art/lab/sandbox/base.json'}
    for line in dirty.splitlines():
        # Preserve spacing of status lines; git() strips the first line.
        path=line[3:] if line[:2].strip() in ('M','A','??') else line.lstrip(' MADRCU?!')
        if path not in allowed and line.lstrip(' MADRCU?!') not in allowed:raise ValueError('Commit or stash other changes before saving: '+line)

def save(body):
    ensure_branch(body['expected_head'])
    slot=body.get('slot')
    if slot not in SLOTS:raise ValueError('Choose an existing preview behaviour')
    doc=sprite(body['sprite']);opts=settings(body.get('settings',{}))
    notes=body.get('notes','').strip()
    if not notes:raise ValueError('Add a short change note')
    if len(notes)>4000:raise ValueError('Change note is too long')
    c=current();payload=json.loads((ROOT/'revisions'/c['revision']/'payload.json').read_text()) if c else {'assets':{}}
    payload['assets'][slot]=doc;payload['settings']=opts
    revision=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'-'+uuid.uuid4().hex[:8]
    base=json.loads((ROOT/'base.json').read_text())['commit']
    if not re.fullmatch('[0-9a-f]{40}',base):raise ValueError('Invalid baseline commit')
    # Verify that the pinned baseline exists locally before writing anything.
    git('cat-file','-e',base+':index.html')
    payload['revision']=revision
    game=build(payload,source=(ROOT/'game.html').read_text(),runtime=(ROOT/'runtime.js').read_text());p=ROOT/'revisions'/revision;p.mkdir(parents=True)
    files={'game.html':game,'payload.json':encode(payload),'source.html':(ROOT/'game.html').read_bytes(),'runtime.js':(ROOT/'runtime.js').read_bytes()}
    manifest={'schema':1,'revision':revision,'base_main':base,'notes':notes,'slots':sorted(payload['assets']),'files':{n:digest(v) for n,v in files.items()},'status':'draft','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
    for n,raw in files.items():(p/n).write_bytes(raw)
    (p/'manifest.json').write_bytes(encode(manifest))
    (ROOT/'current.json').write_bytes(encode({'revision':revision}))
    with (LAB/'CHANGELOG.md').open('a') as f:f.write('\n## '+revision+' — sandbox draft\n\n'+notes+'\n\nGame SHA-256: `'+manifest['files']['game.html']+'`. Base main: `'+base+'`. Slots: '+', '.join(manifest['slots'])+'. No production change.\n')
    git('add','--','art/lab/sandbox','art/lab/CHANGELOG.md')
    git('commit','-m','Art sandbox '+revision+'\n\n'+notes)
    commit=head()
    try:git('push','origin','HEAD:refs/heads/'+BRANCH);return {'revision':revision,'commit':commit,'pushed':True}
    except ValueError as e:return {'revision':revision,'commit':commit,'pushed':False,'warning':'Saved locally. Push failed: '+str(e)}

def refresh():
    ensure_branch(head())
    old=json.loads((ROOT/'base.json').read_text())['commit']
    base_source=clean_source(git('show',old+':index.html',raw=True).decode()).encode()
    if (ROOT/'game.html').read_bytes().rstrip()!=base_source.rstrip():raise ValueError('Sandbox game code has custom edits. Reconcile those with current main before changing base.json, then save and retest.')
    new=remote_main()
    if new==old:return {'status':'Already based on current main'}
    source=clean_source(git('show',new+':index.html',raw=True).decode()).encode()
    if source.decode().count('requestAnimationFrame(frame);\nif(document.fonts')!=1 or b'const LAB_PAYLOAD=' in source:raise ValueError('Main renderer changed or already contains a promoted art adapter. Claude must reconcile the sandbox adapter before refreshing.')
    (ROOT/'game.html').write_bytes(source)
    (ROOT/'base.json').write_bytes(encode({'commit':new,'source':'index.html'}))
    return {'status':'Main refreshed locally. Save a NEW revision and retest before release.','base_main':new}

def remote_main():
    git('fetch','origin','main')
    return git('rev-parse','refs/remotes/origin/main')

def prepare(body):
    ensure_branch(head())
    git('push','origin','HEAD:refs/heads/'+BRANCH)
    p,m=snapshot(body.get('revision'))
    if git('status','--porcelain'):raise ValueError('Save or commit workspace changes before preparing a release')
    baseline=remote_main()
    if baseline!=m['base_main']:raise ValueError('Main has advanced. Refresh sandbox against current main, resolve changes and retest before release.')
    # Never merge the long-lived experiment branch. Construct a focused commit
    # whose ONLY parent is the exact main revision used by the test build.
    cached=ROOT/'prepared.local.json'
    if cached.exists():
        previous=json.loads(cached.read_text())
        if previous.get('revision')==m['revision'] and previous.get('base_main')==baseline and previous.get('pr_url'):
            remote=git('ls-remote','origin','refs/heads/'+previous['branch']).split()
            if remote and remote[0]==previous['commit']:return previous
    revision=m['revision'];candidate=(p/'game.html').read_bytes()
    receipt={'revision':revision,'base_main':baseline,'game_sha256':digest(candidate),'slots':m['slots'],'notes':m['notes'],'status':'prepared, not deployed'}
    with tempfile.TemporaryDirectory() as tmp:
        env={**os.environ,'GIT_INDEX_FILE':str(Path(tmp)/'index')}
        git('read-tree',baseline,env=env)
        for path,raw in {'index.html':candidate,'debug/index.html':candidate.replace(b'<head>',b'<head><script>window.GS_DEBUG=true;</script>',1),'art/integrations/'+revision+'.json':encode(receipt)}.items():
            blob=git('hash-object','-w','--stdin',data=raw)
            git('update-index','--add','--cacheinfo','100644,'+blob+','+path,env=env)
        tree=git('write-tree',env=env)
    sha=git('commit-tree',tree,'-p',baseline,data=('Promote art sandbox '+revision+'\n\n'+m['notes']+'\n\nTested game SHA-256: '+digest(candidate)+'\n').encode())
    branch='art/release-'+revision
    existing=git('ls-remote','origin','refs/heads/'+branch).split()
    if existing:
        existing_sha=existing[0]
        if git('rev-parse',existing_sha+'^{tree}')!=tree or git('rev-parse',existing_sha+'^')!=baseline:raise ValueError('Release branch already exists with different content. Save a new revision.')
        sha=existing_sha
    else:git('push','origin',sha+':refs/heads/'+branch)
    prepared={**receipt,'commit':sha,'branch':branch,'main_before':baseline}
    # gh handles authentication; nothing is sent to or stored in the browser.
    desc='Art revision '+revision+'\n\n'+m['notes']+'\n\nBase main: '+baseline+'\nGame SHA-256: '+digest(candidate)+'\n\nOnly the embedded game, debug build and release receipt are promoted. The lab branch is not merged.'
    with tempfile.NamedTemporaryFile('w',suffix='.md') as f:
        f.write(desc);f.flush()
        try:
            q=subprocess.run(['gh','pr','create','--repo','Astrosomnia/Grimspire','--base','main','--head',branch,'--title','Art release '+revision,'--body-file',f.name],cwd=REPO,capture_output=True,text=True,timeout=90)
            if q.returncode:prepared['warning']='Release branch is ready; PR creation failed: '+q.stderr.strip()
            else:prepared['pr_url']=q.stdout.strip()
        except FileNotFoundError:prepared['warning']='Install GitHub CLI (gh) to create the review PR automatically.'
    (ROOT/'prepared.local.json').write_bytes(encode(prepared))
    return prepared

def publish(body):
    ensure_branch(head())
    prepared=json.loads((ROOT/'prepared.local.json').read_text());p,m=snapshot(prepared['revision'])
    if not prepared.get('pr_url'):raise ValueError('Create the focused review PR with gh before publishing. Install GitHub CLI, authenticate, then prepare again.')
    if body.get('commit')!=prepared['commit'] or body.get('confirm')!='GO LIVE':raise ValueError('Confirm the exact prepared commit')
    if body.get('tested_hash')!=prepared['game_sha256']:raise ValueError('Confirm the tested game hash')
    if current()['revision']!=prepared['revision'] or git('status','--porcelain'):raise ValueError('Workspace changed after review. Save, test and prepare the new revision.')
    remote=git('ls-remote','origin','refs/heads/'+prepared['branch']).split()[0]
    if remote!=prepared['commit']:raise ValueError('Release branch changed after preparation')
    if git('rev-parse',prepared['commit']+'^')!=prepared['main_before']:raise ValueError('Release must be a direct child of tested main')
    if remote_main()!=prepared['main_before']:raise ValueError('Main changed after review. Refresh and retest.')
    # This is a fast-forward, guarded atomically against a concurrent main push.
    # A branch protection rejection is reported; no bypass or retry with force.
    git('push','--force-with-lease=refs/heads/main:'+prepared['main_before'],'origin',prepared['commit']+':refs/heads/main')
    prepared['status']='merged to main; deployment unverified'
    prepared['approval']={'method':'Explicit Forge Go live confirmation','game_sha256':body['tested_hash'],'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
    (ROOT/'prepared.local.json').write_bytes(encode(prepared))
    receipts=ROOT/'integrations';receipts.mkdir(exist_ok=True)
    (receipts/(prepared['revision']+'.json')).write_bytes(encode(prepared))
    with (LAB/'CHANGELOG.md').open('a') as f:f.write('\nPromoted `'+prepared['revision']+'` to main commit `'+prepared['commit']+'`. Deployment has not been verified.\n')
    try:
        git('add','--','art/lab/sandbox/integrations','art/lab/CHANGELOG.md')
        git('commit','-m','Record integration '+prepared['revision'])
        git('push','origin','HEAD:refs/heads/'+BRANCH)
    except ValueError as e:prepared['warning']='Main was updated; lab receipt sync failed: '+str(e)
    return prepared

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self,*a,**kw):super().__init__(*a,directory=str(REPO),**kw)
    def log_message(self,*a):pass
    def send_json(self,data,status=200):
        raw=encode(data);self.send_response(status);self.send_header('Content-Type','application/json');self.send_header('Cache-Control','no-store');self.send_header('Content-Length',str(len(raw)));self.end_headers();self.wfile.write(raw)
    def host_ok(self):return self.headers.get('Host')=='127.0.0.1:'+str(self.server.server_port)
    def do_GET(self):
        if not self.host_ok():return self.send_json({'error':'Use the 127.0.0.1 launch URL'},403)
        path=unquote(urlsplit(self.path).path)
        if path=='/api/state':
            try:return self.send_json({'head':head(),'branch':git('branch','--show-current'),'current':current(),'token':self.server.token,'defaults':DEFAULTS,'base':json.loads((ROOT/'base.json').read_text())})
            except ValueError as e:return self.send_json({'error':str(e)},409)
        if path=='/api/game':
            try:
                p,m=snapshot(parse_qs(urlsplit(self.path).query).get('revision',[None])[0]);raw=(p/'game.html').read_bytes();self.send_response(200);self.send_header('Content-Type','text/html; charset=utf-8');self.send_header('Cache-Control','no-store');self.end_headers();return self.wfile.write(raw)
            except (ValueError,OSError) as e:return self.send_json({'error':str(e)},409)
        # Do not expose git credentials, the Git database, symlinks or arbitrary
        # workspace files through the companion's static server.
        resolved=(REPO/path.lstrip('/')).resolve()
        if (LAB not in resolved.parents and resolved!=LAB) or any(x.startswith('.') for x in Path(path).parts) or resolved.name=='prepared.local.json':return self.send_json({'error':'Not served'},403)
        return super().do_GET()
    def do_POST(self):
        origin='http://127.0.0.1:'+str(self.server.server_port)
        if not self.host_ok() or self.headers.get('Origin')!=origin or self.headers.get('X-Lab-Token')!=self.server.token:return self.send_json({'error':'Open the Forge from this companion'},403)
        try:
            size=int(self.headers.get('Content-Length','0'))
            if not 0<size<=12_000_000:raise ValueError('Invalid request size')
            if self.headers.get_content_type()!='application/json':raise ValueError('Expected JSON')
            body=json.loads(self.rfile.read(size))
            with LOCK:
                path=urlsplit(self.path).path
                if path=='/api/save':result=save(body)
                elif path=='/api/prepare':result=prepare(body)
                elif path=='/api/publish':result=publish(body)
                elif path=='/api/refresh':result=refresh()
                elif path=='/api/push':
                    if git('branch','--show-current')!=BRANCH:raise ValueError('Wrong branch')
                    git('push','origin','HEAD:refs/heads/'+BRANCH);result={'pushed':True}
                elif path=='/api/revision':
                    p,m=snapshot();result=m
                else:raise ValueError('Unknown operation')
            self.send_json(result)
        except (ValueError,OSError,KeyError,TypeError,subprocess.TimeoutExpired) as e:self.send_json({'error':str(e)},409)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--port',type=int,default=8765);args=parser.parse_args()
    if git('rev-parse','--show-toplevel')!=str(REPO):raise SystemExit('Run from a Grimspire clone')
    server=http.server.ThreadingHTTPServer(('127.0.0.1',args.port),Handler);server.token=secrets.token_urlsafe(32)
    print('Open http://127.0.0.1:'+str(server.server_port)+'/art/lab/forge.html',flush=True)
    server.serve_forever()
if __name__=='__main__':main()
