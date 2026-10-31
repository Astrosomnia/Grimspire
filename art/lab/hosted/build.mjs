import {readFile,mkdir,writeFile,copyFile} from 'node:fs/promises';
import {execFileSync} from 'node:child_process';
const here=new URL('./',import.meta.url),out=new URL('./generated/',here);
await mkdir(new URL('public/',out),{recursive:true});
let forge=await readFile(new URL('../forge.html',here),'utf8');
if(!forge.includes('<script src="sandbox/bridge.js"></script>'))throw Error('Forge integration hook has changed');
forge=forge.replace('<script src="sandbox/bridge.js"></script>','<script src="/bridge.js"></script>').replace('<title>Grimspire Art Lab — Forge</title>','<title>Grimspire Forge</title>');
await writeFile(new URL('public/forge.html',out),forge);
await copyFile(new URL('./bridge.js',here),new URL('public/bridge.js',out));
let build='uncommitted-local-build';try{build=execFileSync('git',['rev-parse','HEAD'],{cwd:here,encoding:'utf8',stdio:['ignore','pipe','ignore']}).trim()}catch{}
await writeFile(new URL('build-info.mjs',out),'export const BUILD_SHA='+JSON.stringify(build)+';\n');
console.log('Built hosted Forge assets. Secrets remain in Cloudflare.');
