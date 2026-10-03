(()=>{
const chart=document.querySelector('.moon-chart'), source=document.querySelector('#lunar-data');
if(!chart||!source)return;
const ns='http://www.w3.org/2000/svg', data=JSON.parse(source.textContent), tracks=['mind','act','coupling'];
const modelLayer=chart.querySelector('#lunar-models'), markLayer=chart.querySelector('#lunar-marks');
const reduced=matchMedia('(prefers-reduced-motion:reduce)').matches;
let selected=null, animation=0, started=false;
function el(tag,attrs={},text){const n=document.createElementNS(ns,tag);Object.entries(attrs).forEach(([k,v])=>n.setAttribute(k,v));if(text!=null)n.textContent=text;return n;}
function point(track,score){const path=chart.querySelector('#flight-'+track), total=path.getTotalLength(), goal=605-(605-163)*score/100;let lo=0,hi=total;for(let i=0;i<20;i++){const mid=(lo+hi)/2;if(path.getPointAtLength(mid).y>goal)lo=mid;else hi=mid;}return path.getPointAtLength((lo+hi)/2);}
tracks.forEach(track=>[0,25,50,75,100].forEach(score=>{const p=point(track,score), left=track==='mind', g=el('g',{class:'orbit-tick '+track+'-tick'});g.append(el('path',{d:`M${p.x-5} ${p.y}h10`}),el('text',{x:p.x-18,y:p.y+4,'text-anchor':'end'},score));markLayer.append(g);}));
const nodes=[];
tracks.forEach((track,ti)=>{
const ranked=[...data.models].sort((a,b)=>b[track]-a[track]);
ranked.forEach((model,rank)=>{const score=model[track];if(!Number.isFinite(score)||score<0||score>100)return;
const g=el('g',{class:'live-craft '+track+'-craft','data-model':model.id,tabindex:'0',role:'button','aria-label':`${model.name}, ${track}, rank ${rank+1}, ${score} out of 100`});
const craft=el('g',{class:'vessel'});craft.append(el('circle',{r:rank===0?17:14,class:'craft-aura'}),el('path',{d:'M0-12C-5-7-7 0-5 8L0 5 5 8C7 0 5-7 0-12Z',class:'craft-shell'}),el('circle',{cx:0,cy:-2,r:2.5,class:'craft-window'}),el('path',{d:'M-2 10Q0 23 2 10',class:'engine-glow'}));
const left=track==='mind', dx=left?-23:23, label=el('g',{class:'model-label'});
label.append(el('text',{x:dx,y:-1,'text-anchor':left?'end':'start',class:'model-name'},`${String(rank+1).padStart(2,'0')}  ${model.name}`),el('text',{x:dx,y:20,'text-anchor':left?'end':'start',class:'model-value'},score.toFixed(0)));
g.append(craft,label);modelLayer.append(g);nodes.push({g,track,model,score,rank,ti});
g.addEventListener('click',()=>select(model.id));g.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();select(model.id);}});
});});
const controls=document.querySelector('.model-select');
[ {id:null,name:'All models'},...data.models].forEach(model=>{const b=document.createElement('button');b.type='button';b.textContent=model.name;b.dataset.model=model.id||'';b.addEventListener('click',()=>select(model.id));controls.append(b);});
function select(id){selected=id;nodes.forEach(n=>n.g.classList.toggle('is-muted',id!==null&&id!==n.model.id));controls.querySelectorAll('button').forEach(b=>b.setAttribute('aria-pressed',String((b.dataset.model||null)===id)));}
select(null);
function paint(progress){nodes.forEach(n=>{const delay=n.rank*.07+n.ti*.025,t=Math.max(0,Math.min(1,(progress-delay)/(1-delay))),e=1-Math.pow(1-t,3),p=point(n.track,n.score*e);n.g.setAttribute('transform',`translate(${p.x.toFixed(2)} ${p.y.toFixed(2)})`);n.g.style.opacity=String(.15+.85*Math.min(1,t*4));const ahead=point(n.track,Math.min(100,n.score*e+.2));const angle=Math.atan2(ahead.y-p.y,ahead.x-p.x)*180/Math.PI+90;n.g.querySelector('.vessel').setAttribute('transform',`rotate(${angle.toFixed(1)})`);});}
function replay(){cancelAnimationFrame(animation);if(reduced){paint(1);return;}const start=performance.now();function frame(now){const t=Math.min(1,(now-start)/2200);paint(t);if(t<1)animation=requestAnimationFrame(frame);}animation=requestAnimationFrame(frame);}
document.querySelector('.lunar-replay').addEventListener('click',replay);
paint(reduced?1:0);
if('IntersectionObserver'in window){new IntersectionObserver((entries,observer)=>{if(entries.some(e=>e.isIntersecting)&&!started){started=true;replay();observer.disconnect();}},{threshold:.25}).observe(chart);}else replay();
// Public update hook for live results; persist values in data/lunar-preview.json for releases.
window.Mind2ActLunar={replay,select};
})();
