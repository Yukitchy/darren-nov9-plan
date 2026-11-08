
const ROUTE=P.filter(Boolean).map(p=>[p[0],p[1]]);
const m=L.map('map',{zoomControl:false,scrollWheelZoom:false,dragging:!L.Browser.mobile,tap:false,attributionControl:true});
const css=k=>getComputedStyle(document.documentElement).getPropertyValue(k).trim(), hex=h=>[1,3,5].map(i=>parseInt(h.slice(i,i+2),16));
const URL_='https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Light_Gray_Base/MapServer/tile/{z}/{y}/{x}';
const GL=L.GridLayer.extend({createTile(c,done){const t=document.createElement('canvas');t.width=t.height=256;const g=t.getContext('2d'),im=new Image();im.crossOrigin='anonymous';
  const SEA=hex(css('--map-sea')),LAND=hex(css('--map-land'));
  im.onload=()=>{g.drawImage(im,0,0);const d=g.getImageData(0,0,256,256),a=d.data;
   for(let i=0;i<a.length;i+=4){const l=(a[i]+a[i+1]+a[i+2])/765,s=Math.min(1,Math.max(0,(l-.82)/.03)),w=Math.min(1,Math.max(0,(l-.95)/.05));
    for(let k=0;k<3;k++)a[i+k]=SEA[k]+(LAND[k]+(255-LAND[k])*w-SEA[k])*s}
   g.putImageData(d,0,0);done(null,t)}; im.onerror=e=>done(e,t);
  im.src=L.Util.template(URL_,{z:c.z,x:c.x,y:c.y});return t}});
new GL({maxNativeZoom:16,maxZoom:19,attribution:'Tiles &copy; Esri'}).addTo(m);
const all=L.latLngBounds(ROUTE).pad(.25); m.fitBounds(all);
const red=css('--red');
L.polyline(ROUTE,{color:'#1a1a1a',weight:2,opacity:.35,dashArray:'4 6'}).addTo(m);
const done=L.polyline([],{color:red,weight:4}).addTo(m);
const lab=(t,d,c)=>L.divIcon({className:'pk '+c,html:(c.includes('geo')?'':'<div class="pin"></div>')+'<span class="lb d-'+d+'">'+t+'</span>',iconSize:[14,14],iconAnchor:[7,7]});
GEO.forEach(g=>L.marker([g[0],g[1]],{icon:lab(g[2],'c','geo'),interactive:false}).addTo(m));
const mk=P.map(p=>p&&p[3]!==''&&L.marker([p[0],p[1]],{icon:lab(p[3],p[4],''),interactive:false}).addTo(m));
const lunchL=L.layerGroup();LUNCH.forEach(c=>L.marker([c[0],c[1]],{icon:lab(c[2],c[3],'cafe'),interactive:false}).addTo(lunchL));
const lunchB=LUNCH.length?L.latLngBounds(LUNCH.map(c=>[c[0],c[1]])).pad(.55):null;
const where=document.querySelector('.where'); let cur=-1;
const setW=(d,t)=>{where.firstChild.textContent=d;where.lastChild.textContent=t};
function go(i){if(i===cur)return;cur=i;document.getElementById('map').classList.toggle('far',i===0);lunchL[i===LI?'addTo':'remove'](m);document.getElementById('map').classList.toggle('lunch',i===LI);
 document.querySelectorAll('.step').forEach((s,j)=>s.classList.toggle('on',j===i));
 mk.forEach((k,j)=>k&&k.getElement()&&k.getElement().classList.toggle('on',j===i));
 document.querySelectorAll('.dn').forEach((b,j)=>{b.classList.toggle('on',j===i);if(j===i)b.parentNode.scrollTo({left:b.offsetLeft-b.parentNode.offsetLeft-b.parentNode.clientWidth/2+16})});
 document.querySelectorAll('.ar').forEach(b=>b.disabled=(i+ +b.dataset.d<0||i+ +b.dataset.d>=P.length));
 done.setLatLngs(P.slice(1,i+1).filter(Boolean).map(p=>[p[0],p[1]]));
 if(!P[i]){m.flyToBounds(all,{duration:.8});setW('Mon, November 9','The whole day');return}
 if(i===LI){m.flyToBounds(lunchB,{duration:.8});setW(DAYS[i],P[i][2]);return}
 m.flyTo([P[i][0],P[i][1]],i===1?13:i===2?14:15,{duration:.8}); setW(DAYS[i],P[i][2]);}
const io=new IntersectionObserver(es=>es.forEach(en=>{if(en.isIntersecting)go(+en.target.dataset.i)}),{rootMargin:'-55% 0px -40% 0px'});
document.querySelectorAll('.step').forEach(s=>io.observe(s));
const line=()=>innerWidth>=900?0:document.querySelector('.mapbox').getBoundingClientRect().height;
let snapping=false, tmr;
const jump=i=>{const st=document.querySelector('.step[data-i="'+i+'"]');if(st){snapping=true;scrollBy({top:st.getBoundingClientRect().top-line(),behavior:'smooth'});setTimeout(()=>snapping=false,900);go(i)}};
document.querySelectorAll('.dn').forEach(b=>b.onclick=()=>jump(+b.dataset.i));
document.querySelectorAll('.ar').forEach(b=>b.onclick=()=>jump(Math.max(0,Math.min(P.length-1,Math.max(cur,0)+ +b.dataset.d))));
go(0);
function snap(){if(snapping)return;const L0=line(),lim=innerHeight*.3;let best=null;
 document.querySelectorAll('.intro,.step').forEach(e=>{const d=e.getBoundingClientRect().top-L0;if(Math.abs(d)<lim&&(!best||Math.abs(d)<Math.abs(best)))best=d});
 if(best!==null&&Math.abs(best)>2&&scrollY+innerHeight<document.documentElement.scrollHeight-2){snapping=true;scrollBy({top:best,behavior:'smooth'});setTimeout(()=>snapping=false,700)}}
addEventListener('scroll',()=>{clearTimeout(tmr);tmr=setTimeout(snap,140)},{passive:true});
