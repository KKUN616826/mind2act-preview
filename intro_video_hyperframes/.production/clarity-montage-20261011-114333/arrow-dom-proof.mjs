import fs from 'node:fs';
import path from 'node:path';
import {createRequire} from 'node:module';
const require=createRequire(import.meta.url);
const puppeteer=require('/home/xzy/.npm/_npx/a0439c230146586f/node_modules/puppeteer-core');
const project=process.cwd();
const proofDir=path.join(project,'.production/clarity-montage-20261011-114333');
const phase=process.argv[2]||'before';
let source=fs.readFileSync(path.join(project,'compositions/08-coordination.html'),'utf8');
source=source.replace(/<template>/,'').replace(/<\/template>/,'').replace('<head>','<head><base href="file://'+project+'/"><style>html,body{margin:0;width:1920px;height:1080px;overflow:hidden}</style><script src="assets/lib/gsap.min.js"></script><script>window.__timelines={};</script>');
const htmlPath=path.join(proofDir,'arrow-proof-'+phase+'.html');
fs.writeFileSync(htmlPath,source);
const browser=await puppeteer.launch({executablePath:'/home/xzy/.cache/puppeteer/chrome-headless-shell/linux-148.0.7778.97/chrome-headless-shell-linux64/chrome-headless-shell',headless:true,args:['--no-sandbox','--allow-file-access-from-files']});
const page=await browser.newPage(); await page.setViewport({width:1920,height:1080,deviceScaleFactor:1});
await page.goto('file://'+htmlPath); await page.evaluate(()=>document.fonts.ready);
const result=[];
for(const t of [1.35,1.60,1.95,2.20,2.43,2.58,2.75,2.95,3.20,3.45,3.68,3.85,3.90,4.03]){
  result.push(await page.evaluate(t=>{window.__timelines.coordination.seek(t);return {t,paths:['forward','return'].map(id=>{const el=document.getElementById('coord-'+id+'-pulse');const s=getComputedStyle(el);return {id,length:el.getTotalLength(),pathLength:el.getAttribute('pathLength'),dashArray:s.strokeDasharray,dashOffset:s.strokeDashoffset,attributeOffset:el.getAttribute('stroke-dashoffset'),opacity:s.opacity};})}},t));
}
fs.writeFileSync(path.join(proofDir,'arrow-dom-'+phase+'.json'),JSON.stringify(result,null,2));
await browser.close();
console.log(JSON.stringify(result));
