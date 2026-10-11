import fs from 'node:fs';
import path from 'node:path';
import {spawnSync} from 'node:child_process';
import {createHash} from 'node:crypto';
const production='.production/coordination-20261010-174012';
const ff='/home/xzy/miniconda3/envs/xvla-stable/bin/ffmpeg';
const fp='/home/xzy/miniconda3/envs/xvla-stable/bin/ffprobe';
const check=JSON.parse(fs.readFileSync(`${production}/check-final.json`,'utf8'));
if(!check.ok) throw Error('Composition gate failed');
const now=new Date();
const parts=Object.fromEntries(new Intl.DateTimeFormat('en-CA',{timeZone:'Asia/Shanghai',year:'numeric',month:'2-digit',day:'2-digit',hour:'2-digit',minute:'2-digit',second:'2-digit',hourCycle:'h23'}).formatToParts(now).map(p=>[p.type,p.value]));
const stamp=`${parts.year}${parts.month}${parts.day}-${parts.hour}${parts.minute}${parts.second}`;
const created_at=`${parts.year}-${parts.month}-${parts.day}T${parts.hour}:${parts.minute}:${parts.second}+08:00`;
const master=`renders/mind2act-world-promo-1080p-${stamp}.mp4`;
const web=`renders/mind2act-world-promo-web-${stamp}.mp4`;
const poster=`renders/mind2act-world-poster-${stamp}.jpg`;
const run={id:`mind2act-world-promo-${stamp}`,created_at,master,web,poster,authored_duration:62.2222222222,framework:'HyperFrames 0.8.143',preview_url:'http://localhost:3052/#project/mind2act-hyperframes-blank-20261010-111117'};
fs.writeFileSync(`${production}/export.json`,JSON.stringify(run,null,2));
console.log(JSON.stringify(run));
function command(bin,args,log){const fd=log?fs.openSync(log,'w'):null;const r=spawnSync(bin,args,{stdio:fd?['ignore',fd,fd]:'inherit'});if(fd)fs.closeSync(fd);if(r.status!==0)throw Error(`${bin} failed: ${r.status}`);}
command('bash',['scripts/hyperframes.sh','render','--quality','delivery','--fps','30','--workers','4','--gpu','--output',master],`${production}/render.log`);
console.log('MASTER_READY '+master);
command(ff,['-hide_banner','-loglevel','error','-i',master,'-c:v','libx264','-preset','slow','-crf','23','-pix_fmt','yuv420p','-threads','8','-c:a','copy','-movflags','+faststart','-n',web]);
command(ff,['-hide_banner','-loglevel','error','-ss','3.5','-i',master,'-frames:v','1','-q:v','2','-n',poster]);
run.files={};
for(const [name,file] of [['master',master],['web',web]]){
  const probe=spawnSync(fp,['-v','error','-show_format','-show_streams','-of','json',file],{encoding:'utf8'});
  if(probe.status!==0)throw Error('ffprobe failed');
  const j=JSON.parse(probe.stdout),v=j.streams.find(s=>s.codec_type==='video'),a=j.streams.find(s=>s.codec_type==='audio');
  if(v.width!==1920||v.height!==1080||v.codec_name!=='h264'||v.pix_fmt!=='yuv420p'||a.codec_name!=='aac'||a.channels!==2||Math.abs(Number(j.format.duration)-62.233333)>.04)throw Error('Export format invalid');
  fs.writeFileSync(`${production}/ffprobe-${name}.json`,JSON.stringify(j,null,2));
  command(ff,['-hide_banner','-v','error','-i',file,'-f','null','-'],`${production}/decode-${name}.log`);
  run.files[name]={path:file,bytes:fs.statSync(file).size,sha256:createHash('sha256').update(fs.readFileSync(file)).digest('hex'),duration:Number(j.format.duration),video_codec:v.codec_name,width:v.width,height:v.height,pixel_format:v.pix_fmt,fps:v.r_frame_rate,audio_codec:a.codec_name,audio_sample_rate:a.sample_rate,audio_channels:a.channels};
}
run.subtitles=[];
for(const ext of ['srt','vtt']){const f=`renders/mind2act-world-narration-${stamp}.${ext}`;fs.copyFileSync(`assets/generated/audio/coordination-20261010-174012/narration.${ext}`,f);run.subtitles.push(f);}
run.checks={composition:`${production}/check-final.json`,audio:`${production}/audio/audio-integration.json`,source_evidence:`${production}/loop-provenance.json`,decode_master:'pass',decode_web:'pass'};
run.music_source='assets/audio/The Midnight - The Equaliser (Not Alone).mp3';
run.music_treatment='BGM-only Demucs instrumental stem; newly generated narration mixed separately.';
run.production_manifest=`${production}/manifest.json`;
fs.writeFileSync(`${production}/delivery-candidate.json`,JSON.stringify(run,null,2));
console.log('EXPORT_READY '+JSON.stringify(run));
