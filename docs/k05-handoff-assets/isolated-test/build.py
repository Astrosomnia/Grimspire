from pathlib import Path
import json
import sys
root=Path(__file__).resolve().parent
source=(root/'k05-base.html').read_text()
draft_path=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else root.parent/'K05-relief-draft.forge.json'
draft=json.loads(draft_path.read_text())
needle='const LAB_PAYLOAD='
start=source.index(needle)
end=source.index('\n',start)
addition='\n// Local isolated test only: use the exact saved Forge draft on request.\nconst K05_TEST_DRAFT='+json.dumps(draft,separators=(',',':'))+';\nconst K05_TEST_MODE=new URLSearchParams(location.search).get("bridge")==="original"?"original":"draft";\nif(K05_TEST_MODE==="draft")LAB_PAYLOAD.assets.K05=K05_TEST_DRAFT;\nLAB_PAYLOAD.selected_slot="K05";\n'
source=source[:end]+addition+source[end:]
old='const pickK=k=>{const v=[...labArt.keys()]'
new='const pickK=k=>{if(k==="K05")return "K05";const v=[...labArt.keys()]'
assert source.count(old)==1
source=source.replace(old,new,1)
old='if(seed===undefined)seed=(RR()*2147483647)|0;'
assert source.count(old)==1
source=source.replace(old,'if(seed===undefined)seed=151133;',1)
old="for(const o of opts){u-=o[1];if(u<=0){pick=o[0];break}}"
new=old+"if(opts.some(o=>o[0]==='B'))pick='B';"
assert source.count(old)==1
source=source.replace(old,new,1)
old="const note=document.createElement('div');note.textContent='Forge testing grounds · '+LAB_PAYLOAD.revision;tools.append(note);"
new="const note=document.createElement('div');note.textContent='ISOLATED K05 TEST · '+K05_TEST_MODE.toUpperCase()+' · seed 151133 · all bridge spans forced to K05';tools.append(note);"
assert source.count(old)==1
source=source.replace(old,new,1)
(root/'k05-isolated.html').write_text(source)
print('Built',root/'k05-isolated.html')
