const models=JSON.parse(document.querySelector('#roster').textContent).models;
const worlds={mind:['Mind Score','Memory, goal selection, and task-level planning.'],act:['Act Score','Timely, precise, and stable physical execution.'],coupling:['Mind2Act Score','Reasoning and execution coordinated through feedback.']};
const scene=document.querySelector('#scene'),tip=document.querySelector('.tooltip');
let currentWorld='mind';
function render(key, notify=true){currentWorld=key;if(notify&&window.parent!==window)window.parent.postMessage({type:'mind2act-world',world:key},location.origin);document.querySelectorAll('[role=tab]').forEach(b=>b.setAttribute('aria-selected',b.dataset.world===key));document.querySelector('#world-title').textContent=worlds[key][0];document.querySelector('#world-description').textContent=worlds[key][1];tip.hidden=true;document.querySelector('.stage').dataset.world=key;
const light=false,mix=key==='coupling',ink=light?'#47697a':'#a9c9d5';
const height=Math.max(400,scene.getBoundingClientRect().height*1440/scene.getBoundingClientRect().width);
const sy=y=>y*height/680;
scene.setAttribute('viewBox',`0 0 1440 ${height}`);
const moon={mind:'media/images/mind-moon-upper.png',act:'media/images/act-moon-lower.png',coupling:'media/images/lunar-ranking-moon.png'}[key];
let art=`<image href="media/images/earth-moon-distance-approved.webp" x="0" y="0" width="1440" height="${height}" preserveAspectRatio="none"/><rect width="1440" height="${height}" fill="${key==='act'?'#92bcd2':key==='coupling'?'#adc4c3':'#0c2034'}" opacity="${key==='act'?'.10':key==='coupling'?'.04':'.1'}"/>`;
// Quiet distance rails leave the generated Earth and Moon unobstructed.
for(let i=0;i<5;i++){const y=sy(220+i*75);art+=`<path d="M1300 ${y}H1312" stroke="#c6dce7" opacity=".7"/><text text-anchor="middle" x="1340" y="${y+5}" fill="#d5e5ed" font-size="15">${100-i*20}</text>`}
const sorted=[...models].sort((a,b)=>b[key]-a[key]);sorted.forEach((m,i)=>{let radius=235+(100-m[key])*5.2,angle=[-.2,.7,-.85,.12,-.42,.95,-.15,.5,-.9,.05,-.55][i],x=720+radius*1.2*Math.sin(angle),y=sy(60+radius*Math.cos(angle));const icon=m.icon_svg.replace(/<title>[\s\S]*?<\/title>/,'').replace('<svg ','<svg x="-19" y="-19" width="38" height="38" ');art+=`<g class="node" tabindex="0" role="button" aria-label="${m.name}: ${m[key]} illustrative points" data-id="${m.id}" transform="translate(${x} ${y})" style="animation-delay:${i*.035}s"><g class="float-badge" style="--float-delay:${-i*.47}s;--float-duration:${4.6+(i%4)*.55}s"><circle r="36" fill="${light?'#35546c':'#bed7de'}" opacity=".09"/><circle r="28" fill="${light?'#d2dfe0':'#e4ece7'}" stroke="${light?'#52758a':'#b3cbd2'}" stroke-width="1.5"/><g class="icon">${icon}</g></g></g>`});scene.innerHTML=art;
scene.querySelectorAll('.node').forEach(n=>{function show(){const m=models.find(m=>m.id===n.dataset.id);tip.replaceChildren();const b=document.createElement('b');b.textContent=m.name;const t=document.createElement('small');t.textContent=worlds[key][0]+' · '+m[key]+' / 100 · illustrative';tip.append(b,t);tip.hidden=false}n.addEventListener('mouseenter',show);n.addEventListener('focus',show);n.addEventListener('click',show);n.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();show()}})});}
document.querySelectorAll('[data-world]').forEach(b=>b.addEventListener('click',()=>render(b.dataset.world)));render('mind');

// Parent-controlled desktop height; retain intrinsic sizing for standalone/mobile.
let resizeFrame;
new ResizeObserver(()=>{cancelAnimationFrame(resizeFrame);resizeFrame=requestAnimationFrame(()=>render(currentWorld,false))}).observe(document.querySelector('.stage'));
const tabs=[...document.querySelectorAll('[role=tab]')];
for(const [index,tab] of tabs.entries()) tab.addEventListener('keydown',event=>{
 if(!['ArrowLeft','ArrowRight','Home','End'].includes(event.key))return;
 event.preventDefault();const next=event.key==='Home'?0:event.key==='End'?2:(index+(event.key==='ArrowRight'?1:2))%3;
 tabs[next].focus();render(tabs[next].dataset.world);
});

