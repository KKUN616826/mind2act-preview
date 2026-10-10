import fs from 'node:fs';
import {spawnSync} from 'node:child_process';
const base='.production/categories-20261010-215252';
const run=JSON.parse(fs.readFileSync(`${base}/export.json`,'utf8'));
const output=`${base}/rendered`;fs.mkdirSync(output,{recursive:true});
const ff='/home/xzy/miniconda3/envs/xvla-stable/bin/ffmpeg';
function cmd(args){const r=spawnSync(ff,['-hide_banner','-loglevel','error',...args],{stdio:'inherit'});if(r.status!==0)throw Error('Capture failed');}
const frames=[3.5,8.5,14,20.5,28.15,28.35,31.8,33.3,34.4,34.9,35.15,35.65,37.7,39.7,42.5,44,45.7,47.3,48.6,51.7,54.3,56.5,58.8,60.9,62.2,64.4,70.5,73.8];
for(const t of frames)cmd(['-ss',String(t),'-i',run.master,'-frames:v','1','-q:v','2','-y',`${output}/frame-${String(t).replace('.','-')}.jpg`]);
for(const [name,start,duration,fps,grid]of [['summary',29.63,12,2,'4x6'],['breadth',41.48,12,2,'4x6'],['difficulty',53.33,12,2,'4x6']])cmd(['-ss',String(start),'-i',run.master,'-t',String(duration),'-vf',`fps=${fps},scale=480:270,tile=${grid}`,'-frames:v','1','-q:v','2','-y',`${output}/${name}-motion.jpg`]);
console.log(JSON.stringify({master:run.master,output,frames}));
