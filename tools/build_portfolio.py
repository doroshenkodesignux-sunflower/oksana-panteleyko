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

PROJECTS = [
    # (EN name, UA name, EN place, UA place, tags)
    ('Aparthotel “Alberti”', 'Апартготель «Alberti»', 'Nice, France', 'Ніцца, Франція', ['id', 'br']),
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
<style id="pf-css">
/* ===== Portfolio page ===== */
.pfx{--u:min(calc(100vw / 1920),calc(100vh / 1080));background:#fff;color:var(--ink)}   /* the header sizes itself from --u, as in the hero */
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
.pfp__desc{max-width:900px;margin:clamp(20px,2.1vw,40px) 0 0;font:400 clamp(14px,1.05vw,20px)/1.5 var(--sans);opacity:.7}
.pfp__bar{display:flex;justify-content:space-between;align-items:center;gap:16px;margin-top:clamp(20px,2.1vw,40px)}
.pfp__tags{display:flex;flex-wrap:wrap;gap:8px}
.pfp__tags span{padding:12px 20px;border-radius:300px;background:#F6F6F6;font:500 clamp(13px,.9vw,16px)/1.2 var(--sans);white-space:nowrap}
.pfp__arr{display:flex}
.pfp__arr button{width:54px;height:54px;display:grid;place-items:center;border:1px solid var(--ink);background:#fff;color:var(--ink);cursor:pointer;transition:background .3s,color .3s,opacity .3s}
.pfp__arr button+button{margin-left:-1px}
.pfp__arr button:hover{background:var(--ink);color:#fff}
.pfp__arr button:disabled{opacity:.3;pointer-events:none}
.pfp__arr svg{width:16px;height:16px}
.pfp__gal{margin-top:clamp(24px,2.3vw,44px);overflow:hidden}
.pfp__track{display:flex;gap:9px;transition:transform .8s var(--ease)}
.pfp__track img{display:block;height:clamp(300px,33.5vw,644px);width:auto;flex:none;object-fit:cover;background:#F1F1F1}
.pfp__track img:first-child{width:calc((100% - 9px) * .675)}
.pfp__track img:nth-child(2){width:calc((100% - 9px) * .325)}
.pfp .lnk{margin-top:clamp(24px,2.3vw,44px)}
@media (max-width:900px){
  .pfi{padding:calc(60px + 64px) var(--pad) 64px}
  .pfi__lead{margin-top:32px}
  .pfp{grid-template-columns:1fr;padding:56px 0 64px}
  .pfp__n{font-size:40px;margin-bottom:8px}
  .pfp__top{flex-direction:column;align-items:flex-start;gap:12px}
  .pfp__desc{margin-top:16px}
  .pfp__bar{margin-top:20px;align-items:flex-end}
  .pfp__tags span{padding:10px 16px}
  .pfp__arr button{width:46px;height:46px}
  .pfp__gal{margin-top:24px;margin-right:calc(var(--pad) * -1)}
  .pfp__track img{height:auto;aspect-ratio:4/3}
  .pfp__track img:first-child,.pfp__track img:nth-child(2){width:86%}
  .pfp__track img:nth-child(2){aspect-ratio:auto;object-fit:cover}
}
</style>
'''

JS = '''
<script>
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
    return f'''
  <article class="pfp rv">
    <div class="pfp__n">{n:02d}</div>
    <div class="pfp__body">
      <div class="pfp__top"><h2>{name}</h2><span class="pfp__loc"><img src="assets/icon-pin.svg" alt="">{place}</span></div>
      <p class="pfp__desc">{t["desc"]}</p>
      <div class="pfp__bar"><div class="pfp__tags">{tags}</div><div class="pfp__arr"><button type="button" aria-label="{t["prev"]}">{ARROW.format(a="13 8H3M7 4L3 8l4 4")}</button><button type="button" aria-label="{t["next"]}">{ARROW.format(a="3 8h10M9 4l4 4-4 4")}</button></div></div>
      <div class="pfp__gal"><div class="pfp__track"><img src="assets/pf/{n:02d}a.webp" alt="{alt}" loading="lazy"><img src="assets/pf/{n:02d}b.webp" alt="{alt}" loading="lazy"></div></div>
      <a class="lnk" href="#">{t["explore"]} <i></i></a>
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
    body = f'''<section class="pfx" id="top">
  {hdr}
  <div class="pfi" id="portfolio">
    {lockup}
    <p class="pfi__lead">{t["intro"]}</p>
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
    s = re.sub(r'href="(#[a-z][\w-]*)"', lambda m: m.group(0) if m.group(1) in keep else f'href="{t["home"]}{m.group(1)}"', s)
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
