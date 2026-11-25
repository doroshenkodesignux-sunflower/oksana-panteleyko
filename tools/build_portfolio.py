#!/usr/bin/env python3
"""Build the "All projects" pages from the main pages.

portfolio.html     <- index.html (EN shell)
portfolio-ua.html  <- ua.html    (UA shell)

The shell keeps the head (styles), menu, header, the request form, contacts,
footer and scripts; the main-page sections in between are replaced by the
portfolio intro and the project list. Run after build_ua.py.
"""
import re, pathlib, html

ROOT = pathlib.Path(__file__).resolve().parent.parent

SBID = {1: '2025', 2: '2025', 6: '2022'}   # SBID finalists: Alberti 2025, So. Shell 2025, French House 2022

PROJECTS = [
    # (EN name, UA name, EN place, UA place, tags)
    ('Aparthotel “Alberti”', 'Апартготель «Alberti»', 'Nice, France', 'Ніцца, Франція', ['id', 'br']),
    ('Beauty Salon “So. Shell”', 'Б’юті-салон «So. Shell»', 'Kharkiv, Ukraine', 'Харків, Україна', ['id']),
    ('Cafe “Avec toi”', 'Кафе «Avec toi»', 'Nice, France', 'Ніцца, Франція', ['id', 'br']),
    ('Apartment “Azur Cap d’Ail”', 'Апартаменти «Azur Cap d’Ail»', 'Monaco', 'Монако', ['id']),
    ('Seaside residence “Villa Promenade”', 'Резиденція біля моря «Villa Promenade»', 'Nice, France', 'Ніцца, Франція', ['id']),
    ('Residence “French House”', 'Резиденція «French House»', 'Nice, France', 'Ніцца, Франція', ['id']),
    ('Hotel-Restaurant “Kharkov Palace”', 'Готель-ресторан «Kharkov Palace»', 'Kharkiv, Ukraine', 'Харків, Україна', ['id']),
    ('House for a large family', 'Будинок для великої родини', 'Riviera Village, Kyiv, Ukraine', 'Riviera Village, Київ, Україна', ['id']),
    ('Villa Botanica', 'Villa Botanica', 'Riviera Village, Kyiv, Ukraine', 'Riviera Village, Київ, Україна', ['br']),
    ('Framingham Dermatology', 'Framingham Dermatology', 'United States', 'США', ['br']),
    ('Atmosphere', 'Atmosphere', 'United States', 'США', ['br']),
]

T = {
    'en': dict(
        title='Portfolio — Oksana Panteleyko, Interior Architect',
        intro='A selection of interior and branding projects shaped with purpose and character.',
        desc='Each apartment is designed in a unique color palette and carries its own philosophy. Every space invites you to experience a different emotion.',
        tags={'id': 'Interior Design', 'br': 'Branding'},
        explore='Explore project', prev='Previous photo', next='Next photo',
        h2='Selected<br>Projects', home='index.html', other='portfolio-ua.html', me='portfolio.html',
    ),
    'ua': dict(
        title='Портфоліо — Оксана Пантелейко, архітектор інтер’єрів',
        intro='Добірка інтер’єрних і брендингових проєктів, створених із метою та характером.',
        desc='Кожні апартаменти мають власну колірну палітру й філософію. Кожен простір запрошує відчути іншу емоцію.',
        tags={'id': 'Дизайн інтер’єру', 'br': 'Брендинг'},
        explore='Дивитися проєкт', prev='Попереднє фото', next='Наступне фото',
        h2=None, home='ua.html', other='portfolio.html', me='portfolio-ua.html',
    ),
}

CSS = '''
<style>/* the header sits outside the page blocks so nothing scrolls over it; it keeps the hero's scale unit */
.header{--u:min(calc(100vw / 1920),calc(100vh / 1080));z-index:60!important}</style>
<style id="pf-css">
/* ===== Portfolio page ===== */
.pfx{--u:min(calc(100vw / 1920),calc(100vh / 1080));position:relative;z-index:2;background:#fff;color:var(--ink)}   /* the header sizes itself from --u, as in the hero */
.pfi{padding:calc(100px + clamp(48px,6.25vw,120px)) var(--pad) clamp(64px,6.25vw,120px);text-align:center}
.pfi .prj__title{position:relative!important;left:auto!important;top:auto!important;margin:0 auto calc(var(--u) * 150)}   /* the Portfolio script hangs below the box */
.pfi .prj__title{--u:calc(min(100vw - 32px,520px) / 700)}
@media (min-width:901px){.pfi .prj__title{--u:min(calc(100vw / 1920),1px)}}
.pfi__lead{max-width:30em;margin:clamp(40px,4.2vw,80px) auto 0;font:500 clamp(14px,1.05vw,20px)/1.4 var(--sans);text-transform:uppercase;letter-spacing:.02em;color:var(--ink);text-wrap:balance}
.pfl{padding:0 var(--pad) clamp(80px,6.25vw,120px)}
.pfp{display:grid;grid-template-columns:minmax(0,16%) 1fr;gap:0;padding:clamp(64px,6.25vw,120px) 0 clamp(40px,5.2vw,100px);border-top:1px solid var(--line)}
.pfp__n{font:400 clamp(40px,3.33vw,64px)/1.1 var(--serif);opacity:.4;font-variant-numeric:lining-nums}
.pfp__top{display:flex;justify-content:space-between;align-items:flex-end;gap:24px}
.pfp__top h2{margin:0;font:600 var(--h2)/1.1 var(--serif);letter-spacing:-.01em}
.pfp__loc{display:flex;align-items:center;gap:8px;flex:none;font:400 clamp(14px,1.05vw,20px)/1.4 var(--sans);white-space:nowrap}
.pfp__loc img{width:clamp(18px,1.25vw,24px);height:auto}
.pfp__desc{max-width:900px;margin:clamp(24px,2.6vw,48px) 0 0;font:400 clamp(14px,1.05vw,20px)/1.5 var(--sans);opacity:.7}
.pfp__bar{display:flex;justify-content:space-between;align-items:center;gap:16px;margin-top:clamp(20px,2.1vw,40px)}
.pfp__tags{display:flex;flex-wrap:wrap;gap:8px}
.pfp__tags span{padding:12px 20px;border-radius:300px;background:#F6F6F6;font:500 clamp(13px,.9vw,16px)/1.2 var(--sans);white-space:nowrap}
.pfp__arr{display:flex}
.pfp__arr button{width:54px;height:54px;display:grid;place-items:center;border:1px solid var(--ink);background:#fff;color:var(--ink);cursor:pointer;transition:background .3s,color .3s,opacity .3s}
.pfp__arr button+button{margin-left:-1px}
.pfp__arr button:hover{background:var(--ink);color:#fff}
.pfp__arr button:disabled{opacity:.3;pointer-events:none}
.pfp__arr svg{width:16px;height:16px}
.pfp__gal{margin-top:clamp(24px,2.3vw,44px);overflow:hidden;position:relative}
.pfp__badge{position:absolute;top:0;left:0;z-index:2;width:clamp(80px,6.6vw,124px);height:auto;padding:8px;background:#fff;box-shadow:inset 0 0 0 1px rgba(29,22,22,.18)}   /* SBID finalist badge pinned to the photo's top-left corner */
@media (max-width:900px){.pfp__badge{width:80px}}
.pfp__gal img.pfp__badge{scale:1!important;transform-origin:0 0}
.pfp__track{display:flex;gap:9px;transition:transform .8s var(--ease)}
.pfp__track img{display:block;height:clamp(300px,33.5vw,644px);width:auto;flex:none;object-fit:cover;background:#F1F1F1}
.pfp__track img:first-child{width:calc((100% - 9px) * .675)}
.pfp__track img:nth-child(2){width:calc((100% - 9px) * .325)}
.pfp .lnk{margin-top:clamp(24px,2.3vw,44px);display:inline-flex!important;width:clamp(200px,12vw,240px)!important;max-width:100%}   /* a short link, as in the design — not the full row */
@media (max-width:900px){
  .pfi{padding:calc(60px + 64px) var(--pad) 64px}
  .pfi__lead{margin-top:32px}
  .pfp{grid-template-columns:1fr;padding:56px 0 64px}
  .pfp__n{font-size:28px;margin-bottom:8px}
  .pfp__top{flex-direction:column;align-items:flex-start;gap:16px}
  .pfp__desc{margin-top:20px}
  .pfp__bar{margin-top:20px;align-items:flex-end;flex-wrap:wrap;row-gap:12px}
  .pfp__arr{margin-left:auto}
  .pfx{overflow-x:clip}   /* nothing may push the page sideways on narrow phones */
  .pfp__tags span{padding:10px 16px}
  .pfp__arr button{width:46px;height:46px}
  .pfp__gal{margin-top:24px;margin-right:calc(var(--pad) * -1)}
  .pfp__track img,.pfp__track img:first-child,.pfp__track img:nth-child(2){width:min(86%,560px);height:min(62vw,420px);aspect-ratio:auto;object-fit:cover}
}
/* ---- entrance: the first screen builds itself in when the page opens ---- */
/* like the home hero: the title's letters rise out of a blur one by one, then "Portfolio" is written left to right */
.pfi .prj__title h2 .ch{display:inline-block;opacity:0;transform:translateY(.4em);filter:blur(6px)}
.pf-in .pfi .prj__title h2 .ch{animation:ch .9s var(--ease) forwards;animation-delay:calc(.15s + var(--i) * .045s)}
.pfi .prj__pf{-webkit-mask:linear-gradient(90deg,#000 42%,transparent 58%) 100% 0/320% 100% no-repeat,var(--m-portfolio-script) center/contain no-repeat;mask:linear-gradient(90deg,#000 42%,transparent 58%) 100% 0/320% 100% no-repeat,var(--m-portfolio-script) center/contain no-repeat;-webkit-mask-composite:source-in;mask-composite:intersect}
.pf-in .pfi .prj__pf{animation:pfWrite 1.9s cubic-bezier(.45,.05,.35,1) .95s forwards}
@keyframes pfWrite{to{-webkit-mask-position:0 0,center;mask-position:0 0,center}}
.pfi__lead{opacity:0;translate:0 18px;transition:opacity 1s var(--ease) 2s,translate 1s var(--ease) 2s}
.pfl>.pfp:first-child{border-top-color:transparent;background:linear-gradient(var(--line),var(--line)) 0 0/0 1px no-repeat;transition:background-size 1.4s var(--ease) 2.2s}
.pf-in .pfi__lead{opacity:1;translate:0 0}
.pf-in .pfl>.pfp:first-child{background-size:100% 1px}
/* ---- projects: each one rises in as it reaches the screen, its parts one after another ---- */
.pfp>*,.pfp__body>*{opacity:0;translate:0 32px;transition:opacity .9s var(--ease),translate .9s var(--ease)}
.pfp__n{transition-delay:0s}
.pfp__top{transition-delay:.08s!important}.pfp__desc{transition-delay:.16s!important}.pfp__bar{transition-delay:.24s!important}
.pfp__gal{translate:0 0!important;clip-path:inset(12% 0 0 0);transition:opacity .9s var(--ease) .3s,clip-path 1.3s var(--ease) .3s!important}
.pfp__gal img{scale:1.08;transition:scale 1.8s var(--ease) .3s}
.pfp .lnk{transition-delay:.5s!important}
.pfp.in>*,.pfp.in .pfp__body>*{opacity:1;translate:0 0}
.pfp.in>.pfp__n{opacity:.5}   /* the number stays half-transparent after it appears */
.pfp.in .pfp__gal{clip-path:inset(0 0 0 0)}
.pfp.in .pfp__gal img{scale:1}
@media (prefers-reduced-motion:reduce){.pfi *,.pfp *,.pfp{transition:none!important;clip-path:none!important;opacity:1!important;translate:none!important;scale:none!important}}

/* ===== first screen: project thumbnails orbit the title, a line of project names runs along the bottom ===== */
.pfi{position:relative;min-height:100vh;min-height:100svh;display:flex;flex-direction:column;justify-content:center;align-items:center;overflow:hidden;padding-bottom:calc(clamp(64px,6.25vw,120px) + 40px)!important}
.pfi>.prj__title,.pfi__lead{position:relative;z-index:3}
.pfi__lead{z-index:5;text-shadow:0 0 14px #fff,0 0 6px #fff,0 0 2px #fff}   /* stays readable when a thumbnail passes behind it */
.pfo{position:absolute;inset:0;z-index:4;pointer-events:none;--tw:clamp(74px,8.4vw,160px)}
.pfo a{position:absolute;left:0;top:0;width:var(--tw);aspect-ratio:4/5;pointer-events:auto;will-change:transform,opacity,filter;opacity:0;cursor:pointer}
.pfo a.back{z-index:-2}
.pfo img{width:100%;height:100%;object-fit:cover;display:block;box-shadow:0 18px 40px -18px rgba(29,22,22,.45);transition:transform .5s var(--ease)}
.pfo a span{position:absolute;left:50%;top:calc(100% + 10px);translate:-50% 6px;white-space:nowrap;font:500 13px/1.2 var(--sans);letter-spacing:.04em;text-transform:uppercase;color:var(--ink);opacity:0;transition:opacity .35s,translate .35s var(--ease)}
.pfo a:hover img{transform:scale(1.12)}
.pfo a:hover span{opacity:1;translate:-50% 0}
.pfo.back-layer{z-index:1}
.pfm{position:absolute;left:0;right:0;bottom:clamp(24px,3vw,48px);z-index:3;overflow:hidden;border-top:1px solid var(--line);border-bottom:1px solid var(--line);padding:14px 0;opacity:0;transition:opacity 1.2s var(--ease) 2.6s;-webkit-mask:linear-gradient(90deg,transparent,#000 8%,#000 92%,transparent);mask:linear-gradient(90deg,transparent,#000 8%,#000 92%,transparent)}
.pf-in .pfm{opacity:1}
.pfm__t{display:flex;width:max-content;animation:pfm 60s linear infinite}
.pfm__t span{display:flex;align-items:center;gap:18px;padding-right:18px;font:500 clamp(13px,.85vw,16px)/1 var(--sans);letter-spacing:.06em;text-transform:uppercase;white-space:nowrap;color:var(--ink)}
.pfm__t span i{font-style:normal;color:#8a8a8a}
.pfm__t span b{font-weight:400;font-size:1.4em;line-height:0;color:#b0d3eb}
.pfm:hover .pfm__t{animation-play-state:paused}
@keyframes pfm{to{transform:translateX(-50%)}}
@media (max-width:900px){.pfo{--tw:64px}.pfo a span{display:none}.pfi{padding-bottom:110px!important}}
@media (prefers-reduced-motion:reduce){.pfm__t{animation:none}}
</style>
'''

JS = '''
<script>
/* entrance of the first screen, then projects appear one after another as they scroll in */
/* split the title into letters, keeping the line break, as the hero name does */
document.querySelectorAll('.pfi .prj__title h2').forEach(h=>{let i=0;h.innerHTML=h.innerHTML.split(/<br\\s*\\/?>/i).map(l=>l.trim().split(' ').map(w=>'<span style="white-space:nowrap">'+[...w].map(c=>`<span class="ch" style="--i:${i++}">${c}</span>`).join('')+'</span>').join(' ')).join('<br>')});
requestAnimationFrame(()=>requestAnimationFrame(()=>document.body.classList.add('pf-in')));
(()=>{const ps=[...document.querySelectorAll('.pfp')];
  const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}}),{threshold:.12,rootMargin:'0px 0px -8% 0px'});
  ps.forEach(p=>io.observe(p))})();

/* orbit: thumbnails travel a tilted ellipse round the title — near ones big and sharp in front, far ones small, soft and behind the title.
   The mouse slows and tilts it; scrolling down flings the thumbnails outwards and fades them as the list comes up. */
(()=>{const box=document.querySelector('.pfo'),hero=document.querySelector('.pfi');if(!box)return;
  const back=box.cloneNode(false);back.className='pfo back-layer';hero.insertBefore(back,hero.firstChild);
  const A=[...box.children],N=A.length,reduce=matchMedia('(prefers-reduced-motion:reduce)').matches;
  let rot=0,spd=1,spdT=1,mx=0,my=0,tx=0,ty=0,t0=performance.now(),last=t0;
  hero.addEventListener('pointermove',e=>{if(e.pointerType==='touch')return;const r=hero.getBoundingClientRect();mx=(e.clientX-r.left)/r.width-.5;my=(e.clientY-r.top)/r.height-.5;spdT=.35});
  hero.addEventListener('pointerleave',()=>{mx=my=0;spdT=1});
  A.forEach(a=>{a.addEventListener('pointerenter',()=>spdT=0);a.addEventListener('pointerleave',()=>spdT=.35)});
  const tick=now=>{requestAnimationFrame(tick);const r=hero.getBoundingClientRect();if(r.bottom<0)return;
    const dt=Math.min(50,now-last);last=now;spd+=(spdT-spd)*.05;if(!reduce)rot+=dt*.00011*spd;
    tx+=(mx-tx)*.05;ty+=(my-ty)*.05;
    const W=r.width,H=r.height,mob=W<=900,t=box.querySelector('h2')||hero.querySelector('.prj__title'),tr=t.getBoundingClientRect();
    const cx=W/2,cy=tr.top-r.top+tr.height*.62,sc=Math.min(1,Math.max(0,-r.top/(H*.7)));   /* scroll progress */
    const Rx=(mob?W*.42:Math.min(W*.4,780))*(1+sc*.9),Ry=(mob?H*.34:Math.min(H*.3,330))*(1+sc*.9),tilt=-.13+ty*.12;
    const intro=Math.min(1,Math.max(0,(now-t0-1900)/1400));
    A.forEach((a,i)=>{const th=rot+i*2*Math.PI/N+tx*.6,z=Math.sin(th),x0=Math.cos(th)*Rx,y0=z*Ry,
      x=cx+x0*Math.cos(tilt)-y0*Math.sin(tilt),y=cy+x0*Math.sin(tilt)+y0*Math.cos(tilt),d=(z+1)/2,s=(.55+.6*d)*(.6+.4*intro),
      w=a.offsetWidth,h=a.offsetHeight,front=z>-.05;
      if(front!==(a.parentNode===box))(front?box:back).appendChild(a);
      a.style.transform=`translate(${(x-w/2).toFixed(1)}px,${(y-h/2).toFixed(1)}px) scale(${s.toFixed(3)})`;
      a.style.opacity=((.45+.55*d)*intro*(1-sc*1.3)).toFixed(3);a.style.filter=d<.45?`blur(${((.45-d)*6).toFixed(1)}px)`:'none';a.style.zIndex=Math.round(d*100)})};
  requestAnimationFrame(tick)})();
/* portfolio: the arrows slide each project's photos */
document.querySelectorAll('.pfp').forEach(p=>{const t=p.querySelector('.pfp__track'),[pv,nx]=p.querySelectorAll('.pfp__arr button');let i=0;
  const go=k=>{const im=[...t.children],max=Math.max(0,im.length-1);i=Math.max(0,Math.min(max,k));
    const off=i?im[i].offsetLeft-0:0;const lim=Math.max(0,t.scrollWidth-t.parentElement.clientWidth);t.style.transform=`translateX(${-Math.min(off,lim)}px)`;pv.disabled=i===0;nx.disabled=Math.min(off,lim)>=lim&&i>0||lim===0};
  pv.addEventListener('click',()=>go(i-1));nx.addEventListener('click',()=>go(i+1));addEventListener('resize',()=>go(i));go(0)});
</script>
'''

ARROW = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.2"><path d="M{a}"/></svg>'


def project(n, p, L):
    t = T[L]
    name = p[0] if L == 'en' else p[1]
    place = p[2] if L == 'en' else p[3]
    tags = ''.join(f'<span>{t["tags"][k]}</span>' for k in p[4])
    alt = html.escape(name, quote=True)
    badge = f'<img class="pfp__badge" src="assets/sbid-finalist-{SBID[n]}.png" alt="SBID International Design Awards {SBID[n]} Finalist">' if n in SBID else ''
    return f'''
  <article class="pfp" id="p{n:02d}">
    <div class="pfp__n">{n:02d}</div>
    <div class="pfp__body">
      <div class="pfp__top"><h2>{name}</h2><span class="pfp__loc"><img src="assets/icon-pin.svg" alt="">{place}</span></div>
      <p class="pfp__desc">{t["desc"]}</p>
      <div class="pfp__bar"><div class="pfp__tags">{tags}</div><div class="pfp__arr"><button type="button" aria-label="{t["prev"]}">{ARROW.format(a="13 8H3M7 4L3 8l4 4")}</button><button type="button" aria-label="{t["next"]}">{ARROW.format(a="3 8h10M9 4l4 4-4 4")}</button></div></div>
      <div class="pfp__gal">{badge}<div class="pfp__track"><img src="assets/pf/{n:02d}a.webp?v=2" alt="{alt}" loading="lazy"><img src="assets/pf/{n:02d}b.webp?v=2" alt="{alt}" loading="lazy"></div></div>
      <a class="lnk" href="{(("alberti.html" if L=="en" else "alberti-ua.html") if n==1 else "#")}">{t["explore"]} <i></i></a>
    </div>
  </article>'''


def build(L, src, out):
    t = T[L]
    s = (ROOT / src).read_text(encoding='utf-8')
    # header out of the hero
    hdr = re.search(r'<header class="header">.*?</header>', s, re.S).group(0)
    start = s.index('<section class="hero" id="top">')
    end = s.index('<section class="cta cta2" id="request">')
    # keep a comment marker so the CSS/JS stay in place
    lockup = re.search(r'<div class="prj__title prj__title--sel">.*?</span></div>', s, re.S).group(0)
    orbit = ''.join(f'<a href="#p{i+1:02d}" tabindex="-1"><img src="assets/pf/o{i+1:02d}.webp?v=2" alt=""><span>{html.escape(p[0] if L=="en" else p[1])}</span></a>' for i, p in enumerate(PROJECTS))
    marq = ''.join(f'<span>{html.escape(p[0] if L=="en" else p[1])} <i>{html.escape(p[2] if L=="en" else p[3])}</i><b>·</b></span>' for p in PROJECTS)
    body = f'''{hdr}
<section class="pfx" id="top">
  <div class="pfi" id="portfolio">
    {lockup}
    <p class="pfi__lead">{t["intro"]}</p>
    <div class="pfo" aria-hidden="true">{orbit}</div>
    <div class="pfm" aria-hidden="true"><div class="pfm__t">{marq}{marq}</div></div>
  </div>
  <div class="pfl">{''.join(project(i + 1, p, L) for i, p in enumerate(PROJECTS))}
  </div>
</section>

'''
    # the main-page sections stay in the page, hidden and without images, so the shared scripts find what they expect
    stub = s[start:end].replace('id="top"', 'id="top-main"')
    stub = re.sub(r'(<img\b[^>]*?)\ssrc="[^"]*"', r'\1', stub)   # images keep their tags but load nothing
    stub = re.sub(r'<header class="header">.*?</header>', '', stub, flags=re.S)
    body += '<div class="pf-stub" hidden aria-hidden="true">' + stub + '</div>\n'
    s = s[:start] + body + s[end:]
    # the globe script belongs to the Locations block, which this page does not have
    s = re.sub(r'<script type="module">\s*/\* Project locations:.*?</script>', '', s, count=1, flags=re.S)
    # language switch and links back to the main page
    s = s.replace(f'href="{T["ua" if L=="en" else "en"]["home"]}"', f'href="{t["other"]}"', 1) if False else s
    s = re.sub(r'<a href="(ua\.html|index\.html)"( class="lang__on")? lang="uk"', lambda m: f'<a href="portfolio-ua.html"{m.group(2) or ""} lang="uk"', s)
    s = re.sub(r'<a href="(ua\.html|index\.html)"( class="lang__on")? lang="en"', lambda m: f'<a href="portfolio.html"{m.group(2) or ""} lang="en"', s)
    keep = {'#top', '#request', '#contacts', '#portfolio'}
    s = re.sub(r'href="(#[a-z][\w-]*)"', lambda m: m.group(0) if m.group(1) in keep or re.fullmatch(r'#p\d\d', m.group(1)) else f'href="{t["home"]}{m.group(1)}"', s)
    # inner page: no preloader on a normal visit; a quiet dark screen with the logo only if loading takes long
    s = s.replace('<body class="preloading">', '<body>', 1)
    s = s.replace("if(reduce){finish();writeTitle();return}", "if(reduce||window.__noPre){if(!window.__noPre)finish();writeTitle();return}", 1)
    s = s.replace('<div class="pre" id="pre"', '<script>window.__noPre=true</script>\n<div class="pre" id="pre" style="display:none"', 1)
    s = s.replace('</body>', """<script>
/* slow connection only: show the dark logo screen after 0.7 s, fade it out when the page has loaded */
(()=>{const pre=document.getElementById('pre');if(!pre)return;
  const t=setTimeout(()=>{if(document.readyState==='complete')return;const a=pre.querySelector('.pre__art');if(a)a.removeAttribute('mask');pre.style.display=''},700);
  const done=()=>{clearTimeout(t);if(pre.style.display==='none'){pre.remove();return}pre.animate([{opacity:1},{opacity:0}],{duration:500,easing:'ease',fill:'forwards'}).onfinish=()=>pre.remove()};
  document.readyState==='complete'?done():addEventListener('load',done)})();
</script>
</body>""", 1)
    s = re.sub(r'<title>.*?</title>', f'<title>{t["title"]}</title>', s, count=1, flags=re.S)
    s = s.replace('</head>', CSS + '</head>', 1)
    s = s.replace('</body>', JS + '</body>', 1)
    (ROOT / out).write_text(s, encoding='utf-8')
    print(out, 'written')


# the UA main page must link to the UA portfolio (build_ua.py copies the EN link)
ua = ROOT / 'ua.html'
ua.write_text(ua.read_text(encoding='utf-8').replace('<a class="lnk prj__all" href="portfolio.html">', '<a class="lnk prj__all" href="portfolio-ua.html">'), encoding='utf-8')

build('en', 'index.html', 'portfolio.html')
build('ua', 'ua.html', 'portfolio-ua.html')
