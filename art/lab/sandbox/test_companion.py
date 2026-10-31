"""Exercise real Git save/promotion, release hashes, stale-main rejection and repeat releases."""
import importlib.util, json, os, shutil, subprocess, tempfile, unittest
from pathlib import Path
import threading, urllib.request, urllib.error
import serve
from unittest.mock import patch
from build import ROOT, build, clean_source

SOURCE_REPO=ROOT.parents[2]

def fixture(where):
    repo=where/'clone';remote=where/'remote.git';repo.mkdir()
    def g(*args,cwd=repo):return subprocess.check_output(['git',*args],cwd=cwd,stderr=subprocess.DEVNULL).decode().strip()
    g('init','--bare',str(remote));g('init','-b','main');g('config','user.name','Art Test');g('config','user.email','test@example.invalid')
    (repo/'index.html').write_bytes((ROOT/'game.html').read_bytes());(repo/'debug').mkdir();(repo/'debug/index.html').write_bytes((ROOT/'game.html').read_bytes())
    g('add','.');g('commit','-m','Base game');baseline=g('rev-parse','HEAD');g('remote','add','origin',str(remote));g('push','origin','main');g('checkout','-b','art/weapon-lab')
    shutil.copytree(SOURCE_REPO/'art/lab',repo/'art/lab',ignore=shutil.ignore_patterns('__pycache__','prepared.local.json','current.json','revisions','integrations'))
    (repo/'art/lab/sandbox/base.json').write_text(json.dumps({'commit':baseline}))
    g('add','.');g('commit','-m','Install sandbox');g('push','origin','art/weapon-lab')
    return repo,remote,baseline,g

class CompanionTest(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.repo,self.remote,self.baseline,self.g=fixture(Path(self.temp.name))
        self.real_run=subprocess.run
        def run(command,**kw):
            if command[0]=='gh':return subprocess.CompletedProcess(command,0,'https://github.com/Astrosomnia/Grimspire/pull/123\n','')
            return self.real_run(command,**kw)
        self.patcher=patch('subprocess.run',side_effect=run);self.patcher.start()
        self.original=(serve.REPO,serve.LAB,serve.ROOT);serve.REPO=self.repo;serve.LAB=self.repo/'art/lab';serve.ROOT=serve.LAB/'sandbox'
        self.doc=json.loads((serve.LAB/'releases/weapons-v001/W04_grid.forge.json').read_text())
    def tearDown(self):
        self.patcher.stop();serve.REPO,serve.LAB,serve.ROOT=self.original;self.temp.cleanup()
    def save(self,notes='Dakka lighting test'):
        return serve.save({'expected_head':serve.head(),'sprite':self.doc,'slot':'W04','notes':notes,'settings':{}})
    def test_full_flow_and_second_release(self):
        self.assertTrue(self.save()['pushed']);p,m=serve.snapshot();self.assertEqual(self.baseline,self.g('rev-parse','refs/remotes/origin/main'))
        payload=json.loads((p/'payload.json').read_text());game=(p/'game.html').read_text()
        self.assertEqual(clean_source(game),(p/'source.html').read_text());self.assertEqual(game.count('// BEGIN GRIMSPIRE_ART_ADAPTER'),1)
        prepared=serve.prepare({});self.assertEqual(serve.prepare({})['commit'],prepared['commit']);self.assertEqual(self.g('rev-parse',prepared['commit']+'^'),self.baseline)
        changes=self.g('diff-tree','--no-commit-id','--name-only','-r',prepared['commit']).splitlines()
        self.assertEqual(len(changes),3);self.assertIn('index.html',changes);self.assertNotIn('art/lab/forge.html',changes)
        result=serve.publish({'commit':prepared['commit'],'tested_hash':prepared['game_sha256'],'confirm':'GO LIVE'})
        self.assertEqual(result['status'],'merged to main; deployment unverified')
        self.assertEqual(self.g('ls-remote','origin','refs/heads/main').split()[0],prepared['commit'])
        self.assertIn('refreshed',serve.refresh()['status']);self.save('Second revision');again=serve.prepare({})
        serve.publish({'commit':again['commit'],'tested_hash':again['game_sha256'],'confirm':'GO LIVE'})
        self.assertEqual(self.g('ls-remote','origin','refs/heads/main').split()[0],again['commit'])
    def test_stale_main_cannot_be_overwritten(self):
        self.save();p=serve.prepare({});tree=self.g('rev-parse',self.baseline+'^{tree}')
        # A concurrent Claude commit reaches main after release preparation.
        later=subprocess.check_output(['git','commit-tree',tree,'-p',self.baseline],input=b'Claude update\n',cwd=self.repo).decode().strip()
        self.g('push','origin',later+':refs/heads/main')
        with self.assertRaisesRegex(ValueError,'Main changed'):serve.publish({'commit':p['commit'],'tested_hash':p['game_sha256'],'confirm':'GO LIVE'})
        self.assertEqual(self.g('ls-remote','origin','refs/heads/main').split()[0],later)
    def test_http_boundaries_and_exact_revision_url(self):
        first=self.save();self.save('Second browser revision')
        server=serve.http.server.ThreadingHTTPServer(('127.0.0.1',0),serve.Handler);server.token='test-only'
        threading.Thread(target=server.serve_forever,daemon=True).start()
        url='http://127.0.0.1:'+str(server.server_port)
        try:
            state=json.load(urllib.request.urlopen(url+'/api/state'));self.assertEqual(state['token'],'test-only')
            html=urllib.request.urlopen(url+'/api/game?revision='+first['revision']).read().decode()
            self.assertIn(first['revision'],html)
            for path in ['/.git/config','/index.html','/art/lab/%2e%2e/%2e%2e/%2egit/config']:
                with self.assertRaises(urllib.error.HTTPError) as e:urllib.request.urlopen(url+path)
                self.assertEqual(e.exception.code,403)
            req=urllib.request.Request(url+'/api/publish',data=b'{}',headers={'Content-Type':'application/json','Origin':'https://example.invalid','X-Lab-Token':'test-only'})
            with self.assertRaises(urllib.error.HTTPError) as e:urllib.request.urlopen(req)
            self.assertEqual(e.exception.code,403)
        finally:server.shutdown();server.server_close()
    def test_atomic_main_lease_rejects_race_during_publish(self):
        self.save();p=serve.prepare({});original=serve.remote_main
        later=[None]
        def race():
            previous=original();tree=self.g('rev-parse',previous+'^{tree}')
            later[0]=subprocess.check_output(['git','commit-tree',tree,'-p',previous],input=b'Concurrent update\n',cwd=self.repo).decode().strip()
            self.g('push','origin',later[0]+':refs/heads/main')
            return previous
        with patch.object(serve,'remote_main',side_effect=race):
            with self.assertRaises(ValueError):serve.publish({'commit':p['commit'],'tested_hash':p['game_sha256'],'confirm':'GO LIVE'})
        self.assertEqual(self.g('ls-remote','origin','refs/heads/main').split()[0],later[0])
    def test_tampered_release_and_wrong_confirmation_rejected(self):
        self.save();p=serve.prepare({})
        with self.assertRaisesRegex(ValueError,'tested game hash'):serve.publish({'commit':p['commit'],'tested_hash':'wrong','confirm':'GO LIVE'})
        path,m=serve.snapshot();(path/'game.html').write_text('tampered')
        with self.assertRaisesRegex(ValueError,'hash mismatch'):serve.snapshot()
        with self.assertRaises(ValueError):serve.prepare({})
    def test_dirty_and_stale_saves_rejected(self):
        (self.repo/'unrelated.txt').write_text('Other work')
        with self.assertRaisesRegex(ValueError,'other changes'):self.save()
        (self.repo/'unrelated.txt').unlink()
        with self.assertRaisesRegex(ValueError,'Workspace changed'):serve.save({'expected_head':'wrong'})
    def test_new_sprite_can_preview_as_existing_weapon(self):
        self.doc['code']='';self.doc['name']='New concept'
        self.save();p,m=serve.snapshot();self.assertEqual(json.loads((p/'payload.json').read_text())['assets']['W04']['code'],'')

if __name__=='__main__':unittest.main()
