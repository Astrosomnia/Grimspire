// Use the Web Crypto RSA path supported natively by Workers, independent of
// node:crypto PEM parsing/algorithm aliases. Never emit key material in errors.
import {Problem} from './model.mjs';
const fail=(code,message)=>{const e=new Problem(message,503);e.keyCode=code;throw e};
const concat=(...arrays)=>{const out=new Uint8Array(arrays.reduce((n,a)=>n+a.length,0));let at=0;for(const a of arrays){out.set(a,at);at+=a.length}return out};
function der(tag,bytes){let n=bytes.length,len;if(n<128)len=Uint8Array.of(n);else{const digits=[];while(n){digits.unshift(n&255);n=Math.floor(n/256)}len=Uint8Array.of(128|digits.length,...digits)}return concat(Uint8Array.of(tag),len,bytes)}
export function parsePrivateKey(value){
 if(typeof value!=='string'||!value.trim())fail('missing','GITHUB_PRIVATE_KEY is missing from Cloudflare runtime secrets.');
 let text=value.trim();if(text.startsWith('"')&&text.endsWith('"')){try{const decoded=JSON.parse(text);if(typeof decoded==='string')text=decoded}catch{}}
 text=text.replace(/\\r\\n/g,'\n').replace(/\\n/g,'\n').replace(/\r\n?/g,'\n').replace(/^\uFEFF/,'').trim();
 if(text.includes('ENCRYPTED PRIVATE KEY')||text.includes('Proc-Type: 4,ENCRYPTED'))fail('encrypted','The private key is password-encrypted. Use the unmodified PEM downloaded from the GitHub App.');
 const match=text.match(/^-----BEGIN (RSA PRIVATE KEY|PRIVATE KEY)-----\s*([A-Za-z0-9+/=\s]+)\s*-----END \1-----$/);
 if(!match)fail('missing_pem','GITHUB_PRIVATE_KEY is not a complete PEM. Re-paste the entire downloaded file, including BEGIN and END lines, as a Cloudflare Secret.');
 let data;try{data=Uint8Array.from(atob(match[2].replace(/\s/g,'')),c=>c.charCodeAt(0))}catch{fail('invalid_base64','The PEM text is incomplete or its base64 content was altered. Re-paste the complete downloaded file.')}
 if(data.length<128||data[0]!==0x30)fail('invalid_der','The private-key contents are incomplete or not an RSA private key. Re-paste the original downloaded file.');
 const format=match[1]==='RSA PRIVATE KEY'?'pkcs1':'pkcs8';
 if(format==='pkcs1'){
  // PrivateKeyInfo = SEQUENCE(version=0, rsaEncryption AlgorithmIdentifier,
  // OCTET STRING containing the original PKCS#1 RSAPrivateKey).
  const algorithm=Uint8Array.of(0x30,0x0d,0x06,0x09,0x2a,0x86,0x48,0x86,0xf7,0x0d,0x01,0x01,0x01,0x05,0x00);
  data=der(0x30,concat(Uint8Array.of(0x02,0x01,0x00),algorithm,der(0x04,data)));
 }
 return{data,format};
}
export async function importPrivateKey(value){const {data,format}=parsePrivateKey(value);try{return{key:await crypto.subtle.importKey('pkcs8',data,{name:'RSASSA-PKCS1-v1_5',hash:'SHA-256'},false,['sign']),format}}catch{fail('unreadable','The PEM was recognised but its RSA key could not be imported. Check that the complete original GitHub private key was saved.') }}
export async function signAppJwt(env,now=Math.floor(Date.now()/1000)){
 const {key}=await importPrivateKey(env.GITHUB_PRIVATE_KEY);
 const b64=b=>{let s='';for(const v of b)s+=String.fromCharCode(v);return btoa(s).replace(/\+/g,'-').replace(/\//g,'_').replace(/=+$/,'')};
 const encode=o=>b64(new TextEncoder().encode(JSON.stringify(o)));
 const unsigned=encode({alg:'RS256',typ:'JWT'})+'.'+encode({iat:now-60,exp:now+540,iss:env.GITHUB_APP_ID});
 try{return unsigned+'.'+b64(new Uint8Array(await crypto.subtle.sign('RSASSA-PKCS1-v1_5',key,new TextEncoder().encode(unsigned))))}catch{fail('signing_failed','The private key was imported, but the Worker could not sign the GitHub App request.')}
}
export async function privateKeyStatus(value){try{const {format}=await importPrivateKey(value);return{readable:true,format}}catch(e){return{readable:false,reason:e.keyCode||'unreadable'}}}
