import fs from 'node:fs';
import {spawnSync} from 'node:child_process';
const base='.production/coordination-20261010-174012';
const run=JSON.parse(fs.readFileSync(`${base}/export.json`,'utf8'));
const output=`${base}/rendered`;
fs.mkdirSync(output,{recursive:true});
const ff='/home/xzy/miniconda3/envs/xvla-stable/bin/ffmpeg';
function capture(args){const r=spawnSync(ff,['-hide_banner','-loglevel','error',...args],{stdio:'inherit'});if(r.status!==0)throw Error('Capture failed');}
const selected=[0,1.6,2.48,3.5,8.8,10.83,11.35,13.5,17,20.5,25.5,28.3,29.3,32,33.97,34.1,34.6,35.8,36.6,37,39.3,40.3,46.7,49.5,50.8,52.2,57,59.5,61.9];
for(const t of selected)capture(['-ss',String(t),'-i',run.master,'-frames:v','1','-q:v','2','-y',`${output}/frame-${String(t).replace('.','-')}.jpg`]);
capture(['-i',run.master,'-vf',"fps=1/2.5,scale=480:270,drawtext=fontfile=assets/fonts/IBMPlexMono-400.ttf:text='%{pts\\:hms}':fontsize=17:fontcolor=white:box=1:boxcolor=black@0.65:x=8:y=8,tile=4x7",'-frames:v','1','-q:v','2','-y',`${output}/whole-film.jpg`]);
capture(['-ss','1.8','-i',run.master,'-t','1.6','-vf','fps=10,scale=480:270,tile=4x4','-frames:v','1','-q:v','2','-y',`${output}/intro-logo-sequence.jpg`]);
capture(['-ss','10.1','-i',run.master,'-t','1.6','-vf','fps=10,scale=480:270,tile=4x4','-frames:v','1','-q:v','2','-y',`${output}/insight-logo-sequence.jpg`]);
capture(['-ss','33.8','-i',run.master,'-t','1.2','-vf','fps=10,scale=640:360,tile=4x3','-frames:v','1','-q:v','2','-y',`${output}/first-outcome-sequence.jpg`]);
capture(['-ss','36.4','-i',run.master,'-t','1.2','-vf','fps=10,scale=640:360,tile=4x3','-frames:v','1','-q:v','2','-y',`${output}/second-outcome-sequence.jpg`]);
console.log(output);
