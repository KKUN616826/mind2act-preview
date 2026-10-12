const models=JSON.parse(document.querySelector('#roster').textContent).models;
const worlds={mind:['Mind World','Memory, goal selection, and task-level planning.'],act:['Act World','Timely, precise, and stable physical execution.'],coupling:['Mind2Act','Reasoning and execution coordinated through feedback.']};
const scene=document.querySelector('#scene'),tip=document.querySelector('.tooltip');
let currentWorld='mind';
function render(key, notify=true){currentWorld=key;if(notify&&window.parent!==window)window.parent.postMessage({type:'mind2act-world',world:key},location.origin);document.querySelectorAll('[role=tab]').forEach(b=>b.setAttribute('aria-selected',b.dataset.world===key));document.querySelector('#world-title').textContent=worlds[key][0];document.querySelector('#world-description').textContent=worlds[key][1];tip.hidden=true;document.querySelector('.stage').dataset.world=key;
const light=key==='mind',mix=key==='coupling',ink=light?'#47697a':'#a9c9d5';
const height=Math.max(400,scene.getBoundingClientRect().height*1440/scene.getBoundingClientRect().width);
const sy=y=>y*height/680;
scene.setAttribute('viewBox',`0 0 1440 ${height}`);
const moon={mind:'media/images/mind-moon-upper.png',act:'media/images/act-moon-lower.png',coupling:'media/images/lunar-ranking-moon.png'}[key];
let art=`<defs><linearGradient id="daynight"><stop stop-color="#e5ecd9"/><stop offset=".28" stop-color="#d8e4df"/><stop offset=".6" stop-color="#657e94"/><stop offset="1" stop-color="#172640"/></linearGradient><radialGradient id="day" cx="50%" cy="0%" r="95%"><stop stop-color="#e3e8da"/><stop offset=".55" stop-color="#c3d5d7"/><stop offset="1" stop-color="#8facbd"/></radialGradient><radialGradient id="sky" cx="50%" cy="12%" r="85%"><stop stop-color="#476a80"/><stop offset=".45" stop-color="#213b56"/><stop offset="1" stop-color="#102134"/></radialGradient><radialGradient id="halo"><stop stop-color="#dce9de" stop-opacity=".25"/><stop offset="1" stop-color="#dce9de" stop-opacity="0"/></radialGradient><linearGradient id="ground" x2="0" y2="1"><stop stop-color="#647b89"/><stop offset="1" stop-color="#263e54"/></linearGradient></defs><rect width="1440" height="${height}" fill="url(#${light?'day':mix?'daynight':'sky'})"/><ellipse cx="720" cy="90" rx="500" ry="340" fill="url(#halo)"/>`;
for(let i=0;i<65;i++){let x=(i*191+83)%1440,y=(i*73+29)%490;art+=`<circle cx="${x}" cy="${y}" r="${i%7===0?2:1}" fill="#dce8ec" opacity="${.15+(i%4)*.12}"/>`}
// Nested arrival arcs give the horizontal field a readable destination and depth.
for(let i=0;i<5;i++){let ry=210+i*78,rx=ry*1.2;art+=`<ellipse cx="720" cy="${sy(75)}" rx="${rx}" ry="${sy(ry)}" fill="none" stroke="${ink}" stroke-opacity="${.25-i*.025}" stroke-dasharray="3 9"/>`;art+=`<path d="M1297 ${sy(75+ry)}H1307" stroke="${ink}" opacity=".55"/><text text-anchor="middle" x="1332" y="${sy(75+ry)+5}" fill="${ink}" opacity=".65" font-size="12">${100-i*20}</text>`}
art+=`<path transform="scale(1 ${height/680})" d="M0 670 Q180 648 360 670T710 661T1080 668L1440 652V680H0Z" fill="${light?'#9fb8bf':mix?'#526c80':'#1a3045'}" opacity=".45"/><image href="${moon}" x="645" y="22" width="150" height="150"/>`;
const sorted=[...models].sort((a,b)=>b[key]-a[key]);sorted.forEach((m,i)=>{let radius=235+(100-m[key])*5.2,angle=[-.2,.7,-.85,.12,-.42,.95,-.15,.5,-.9,.05,-.55][i],x=720+radius*1.2*Math.sin(angle),y=sy(60+radius*Math.cos(angle));const icon=m.icon_svg.replace(/<title>[\s\S]*?<\/title>/,'').replace('<svg ','<svg x="-11" y="-11" width="22" height="22" ');art+=`<g class="node" tabindex="0" role="button" aria-label="${m.name}: ${m[key]} illustrative points" data-id="${m.id}" transform="translate(${x} ${y})" style="animation-delay:${i*.035}s"><g class="float-badge" style="--float-delay:${-i*.47}s;--float-duration:${4.6+(i%4)*.55}s"><circle r="23" fill="${light?'#35546c':'#bed7de'}" opacity=".09"/><circle r="17" fill="${light?'#d2dfe0':'#e4ece7'}" stroke="${light?'#52758a':'#b3cbd2'}" stroke-width="1.5"/><g class="icon">${icon}</g></g></g>`});scene.innerHTML=art;
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

