import fs from 'node:fs';
import {spawnSync} from 'node:child_process';
import {createHash} from 'node:crypto';
const base='.production/insets-20261010-200358';
const run=JSON.parse(fs.readFileSync(`${base}/export.json`,'utf8'));
const previous=JSON.parse(fs.readFileSync(`${base}/before/renders/delivery.json`,'utf8'));
const output=`${base}/rendered`;
fs.mkdirSync(output,{recursive:true});
const ff='/home/xzy/miniconda3/envs/xvla-stable/bin/ffmpeg';
function capture(args){const r=spawnSync(ff,['-hide_banner','-loglevel','error',...args],{stdio:'inherit'});if(r.status!==0)throw Error('Capture failed');}
for(const t of [3.5,18.5,20,21.5,23,25,26.5,27.5,28.5,29.3,35,52.2,59.5,61.9])capture(['-ss',String(t),'-i',run.master,'-frames:v','1','-q:v','2','-y',`${output}/frame-${String(t).replace('.','-')}.jpg`]);
capture(['-ss','17.8','-i',run.master,'-t','11.8','-vf','fps=1,scale=640:360,tile=3x4','-frames:v','1','-q:v','2','-y',`${output}/restored-cases.jpg`]);
function audioHash(file){const r=spawnSync(ff,['-v','error','-i',file,'-map','0:a:0','-c:a','copy','-f','adts','-'],{maxBuffer:32*1024*1024});if(r.status!==0)throw Error('Audio demux failed');return createHash('sha256').update(r.stdout).digest('hex');}
const audio={previous:previous.master,current:run.master,previous_aac_sha256:audioHash(previous.master),current_aac_sha256:audioHash(run.master)};
audio.bit_identical=audio.previous_aac_sha256===audio.current_aac_sha256;
fs.writeFileSync(`${base}/audio-continuity.json`,JSON.stringify(audio,null,2));
console.log(JSON.stringify({rendered:output,audio}));
