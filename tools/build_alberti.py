#!/usr/bin/env python3
"""Build the Alberti project page from the main pages (run after build_ua.py).

alberti.html    <- index.html (EN shell)
alberti-ua.html <- ua.html    (UA shell)

Layout follows the Figma frame «Страница Проекта - Alberty» (1920 wide); photo
positions below are the frame's own pixel coordinates, scaled with --u on desktop
and stacked on phones. The page reuses the main page's request blocks,
testimonials, contacts and footer.
"""
import re, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent

T = {
    'en': dict(
        title='Aparthotel “Alberti” — Oksana Panteleyko, Interior Architect',
        big='Alberti', t1='“Alberti”', t2='Apart hotel',
        desc='Each apartment is designed in a unique color palette and carries its own philosophy. Every space invites you to experience a different emotion.',
        place='Nice, France',
        role_k='My role', role='Interior Designer<br>Art Director',
        task_k='Task', res_k='Result',
        task='Each apartment is designed in a unique color palette and carries its own philosophy. Every space invites you to experience a different emotion.',
        res='Each apartment is designed in a unique color palette and carries its own philosophy. Every space invites you to experience a different emotion.',
        area='Total area', rooms='Rooms', year='Year',
        h_int='Interior design', h_br='Branding',
        cap={'ek': 'Entrance + Kitchen', 'k': 'Kitchen', 'b1': 'Bedroom 1', 'b2': 'Bedroom 2', 'lr': 'Living room', 'lr2': 'Living room 2',
             'r1': 'Room 1', 'cu': 'Close-up', 'mask': 'Eye mask for sleeping', 'keys': 'Room keys', 'logo': 'Logo',
             'bc': 'Business cards', 'wl': 'Welcome letter', 'sk': 'Facade sketch'},
        brtext='Each apartment is designed in a unique color palette and carries its own philosophy. Every space invites you to experience a different emotion.',
        me='alberti.html', other='alberti-ua.html', home='index.html',
    ),
    'ua': dict(
        title='Апартготель «Alberti» — Оксана Пантелейко, архітектор інтер’єрів',
        big='Alberti', t1='«Alberti»', t2='Апарт-готель',
        desc='Кожні апартаменти мають власну колірну палітру й філософію. Кожен простір запрошує відчути іншу емоцію.',
        place='Ніцца, Франція',
        role_k='Моя роль', role='Дизайнер інтер’єру<br>Арт-директор',
        task_k='Завдання', res_k='Результат',
        task='Кожні апартаменти мають власну колірну палітру й філософію. Кожен простір запрошує відчути іншу емоцію.',
        res='Кожні апартаменти мають власну колірну палітру й філософію. Кожен простір запрошує відчути іншу емоцію.',
        area='Загальна площа', rooms='Кімнат', year='Рік',
        h_int='Дизайн інтер’єру', h_br='Брендинг',
        cap={'ek': 'Передпокій + кухня', 'k': 'Кухня', 'b1': 'Спальня 1', 'b2': 'Спальня 2', 'lr': 'Вітальня', 'lr2': 'Вітальня 2',
             'r1': 'Кімната 1', 'cu': 'Деталі', 'mask': 'Маска для сну', 'keys': 'Ключі від номера', 'logo': 'Логотип',
             'bc': 'Візитівки', 'wl': 'Вітальний лист', 'sk': 'Ескіз фасаду'},
        brtext='Кожні апартаменти мають власну колірну палітру й філософію. Кожен простір запрошує відчути іншу емоцію.',
        me='alberti-ua.html', other='alberti.html', home='ua.html',
    ),
}

# (file, x, y, w, h, caption key) — Figma pixels, y relative to the gallery top
INTERIOR_TOP = 4680
INTERIOR = [
    ('i01', 48, 4680, 600, 648, 'ek'), ('i02', 656, 4680, 1216, 1312, 'k'),
    ('i03', 48, 6128, 600, 808, 'b1'), ('i04', 656, 6128, 1216, 808, 'lr'),
    ('i05', 48, 7080, 1216, 1304, 'r1'), ('i06', 1272, 7736, 600, 648, 'cu'),
    ('i07', 48, 8528, 600, 800, 'b1'), ('i08', 656, 8528, 1216, 800, 'lr'),
    ('i09', 664, 9472, 592, 648, 'b2'), ('i10', 1272, 9472, 600, 640, 'lr2'),
    ('i11', 48, 10256, 1824, 1008, 'k'),
    ('i12', 48, 11408, 1216, 800, 'lr'), ('i13', 1272, 11408, 600, 800, 'b1'),
    ('sketch', 51, 12356, 1818, 1074, None),
]
INTERIOR_END = 13430
BRAND_TOP = 14040
BRAND = [
    ('b01', 48, 14040, 600, 648, 'cu'), ('b02', 656, 14040, 1216, 1304, 'mask'),
    ('b03', 48, 15488, 600, 640, 'keys'), ('b04', 656, 15488, 600, 640, 'mask'),
    ('b05', 48, 16264, 1216, 1312, 'r1'), ('b06', 1272, 16928, 600, 640, 'logo'),
    ('b07', 48, 17712, 600, 648, 'bc'), ('b08', 664, 17712, 600, 648, 'wl'),
    ('b09', 664, 18504, 1200, 768, 'bc'),
    ('b10', 48, 19424, 1824, 1080, None),
]
BRAND_END = 20504


def gallery(items, top, end, t, extra=''):
    figs = []
    for f, x, y, w, h, cap in items:
        alt = t['cap'][cap] if cap else ('Aparthotel Alberti' if f != 'sketch' else t['cap']['sk'])
        cls = ' alb-fig--sketch' if f == 'sketch' else ''
        figs.append(f'<figure class="alb-fig{cls}" style="--x:{x};--y:{y - top};--w:{w};--h:{h}">'
                    f'<div class="alb-fig__img"><img src="assets/alberti/{f}.webp" alt="{alt}" loading="lazy"></div>'
                    + (f'<figcaption>{t["cap"][cap]}</figcaption>' if cap else '') + '</figure>')
    return f'<div class="alb-gal" style="--H:{end - top}">' + ''.join(figs) + extra + '</div>'


CSS = '''
<style id="alb-css">
/* ===== Alberti project page — 1920 Figma frame, scaled by --u on desktop ===== */
.alb{--u:calc(100vw / 1920);background:#fff;color:var(--ink);position:relative;z-index:2}
.alb-hero{position:relative;height:calc(var(--u) * 1080);overflow:hidden}
.alb-hero__big{position:absolute;left:50%;top:calc(var(--u) * 330);translate:-50% 0;margin:0;font:400 calc(var(--u) * 520)/1 var(--serif);letter-spacing:-.02em;text-transform:uppercase;color:#333;white-space:nowrap}
.alb-hero__img{position:absolute;left:calc(var(--u) * 670);top:calc(var(--u) * 175);width:calc(var(--u) * 579);height:calc(var(--u) * 829);object-fit:cover;z-index:1}
.alb-head{text-align:center;padding:calc(var(--u) * 190) var(--pad) calc(var(--u) * 140)}
.alb-head h1{margin:0;font:400 calc(var(--u) * 110)/1 var(--serif);text-transform:uppercase;letter-spacing:-.01em;color:var(--ink)}
.alb-head__script{display:block;margin:calc(var(--u) * -40) auto 0;width:calc(var(--u) * 944);aspect-ratio:944/250;background:var(--accent);-webkit-mask:url(assets/alberti/script-interior-design.png) center/contain no-repeat;mask:url(assets/alberti/script-interior-design.png) center/contain no-repeat}
.alb-head__desc{max-width:34em;margin:calc(var(--u) * 60) auto 0;font:400 clamp(16px,.95vw,18px)/1.5 var(--sans);text-wrap:balance}
.alb-head__place{margin:calc(var(--u) * 120) 0 0;font:600 clamp(16px,1.05vw,20px)/1.2 var(--sans);text-transform:uppercase;letter-spacing:.02em;color:#5B8DB8}
.alb-wide{display:block;width:100%;height:auto;aspect-ratio:16/9;object-fit:cover}
.alb-info{display:grid;grid-template-columns:1fr 1fr;margin:0 var(--pad);border-top:1px solid #D7E6F2;border-bottom:1px solid #D7E6F2}
.alb-info>div{padding:calc(var(--u) * 60) 0 calc(var(--u) * 100)}
.alb-info>div:nth-child(2n){border-left:1px solid #D7E6F2;padding-left:calc(var(--u) * 50)}
.alb-info>div:nth-child(n+3){border-top:1px solid #D7E6F2}
.alb-k{margin:0 0 calc(var(--u) * 40);font:700 16px/1.2 var(--sans);text-transform:uppercase;letter-spacing:.04em;color:#5B8DB8}
.alb-v{margin:0;max-width:22em;font:400 clamp(16px,1.25vw,24px)/1.45 var(--sans)}
.alb-stats{display:grid;grid-template-columns:repeat(2,max-content);gap:calc(var(--u) * 40) calc(var(--u) * 80)}
.alb-stats b{display:block;font:400 calc(var(--u) * 150)/1 var(--serif);color:#7FB0D8;font-variant-numeric:lining-nums}
.alb-stats b sup{font-size:.45em;vertical-align:.9em}
.alb-stats span{display:block;margin-top:12px;font:400 16px/1.2 var(--sans);opacity:.7}
.alb-h2{margin:0;padding:calc(var(--u) * 160) var(--pad) calc(var(--u) * 110);text-align:center;font:400 var(--h2)/1.1 var(--serif);text-transform:uppercase;letter-spacing:-.01em}
.alb-gal{position:relative;height:calc(var(--u) * var(--H))}
.alb-fig{position:absolute;margin:0;left:calc(var(--u) * var(--x));top:calc(var(--u) * var(--y));width:calc(var(--u) * var(--w))}
.alb-fig__img{height:calc(var(--u) * var(--h));overflow:hidden;background:#F2F2F2}
.alb-fig__img img{display:block;width:100%;height:100%;object-fit:cover;transition:scale 1.2s var(--ease)}
.alb-fig:hover .alb-fig__img img{scale:1.03}
.alb-fig figcaption{margin-top:calc(var(--u) * 16);font:400 16px/1.3 var(--sans);opacity:.8}
.alb-fig--sketch .alb-fig__img{background:#fff;outline:1px solid #E3E3E3}
.alb-fig--sketch img{object-fit:contain}
.alb-brtext{position:absolute;left:calc(var(--u) * 1272);top:calc(var(--u) * 2030);width:calc(var(--u) * 560);margin:0;font:400 16px/1.5 var(--sans)}
/* reveal */
.alb-fig,.alb-info>div,.alb-h2,.alb-brtext{opacity:0;translate:0 40px;transition:opacity 1s var(--ease),translate 1s var(--ease)}
.alb-fig.in,.alb-info>div.in,.alb-h2.in,.alb-brtext.in{opacity:1;translate:0 0}
.alb-hero__big .ch{display:inline-block;opacity:0;transform:translateY(.25em);filter:blur(8px)}
.alb-in .alb-hero__big .ch{animation:ch 1s var(--ease) forwards;animation-delay:calc(.2s + var(--i) * .06s)}
.alb-hero__img{clip-path:inset(100% 0 0 0);transition:clip-path 1.4s cubic-bezier(.65,0,.35,1) .1s}
.alb-in .alb-hero__img{clip-path:inset(0 0 0 0)}
@media (max-width:900px){
  .alb{--u:calc(100vw / 390)}
  .alb-hero{height:calc(60px + var(--u) * 370)}
  .alb-hero__big{top:calc(60px + var(--u) * 150);font-size:calc(var(--u) * 112)}
  .alb-hero__img{left:calc(50% - var(--u) * 105);top:calc(60px + var(--u) * 40);width:calc(var(--u) * 210);height:calc(var(--u) * 300)}
  .alb-head{padding:56px 16px 56px}
  .alb-head h1{font-size:clamp(34px,10vw,48px)}
  .alb-head__script{width:min(86vw,420px);margin-top:-14px}
  .alb-head__desc{margin-top:24px}
  .alb-head__place{margin-top:32px}
  .alb-wide{aspect-ratio:4/3}
  .alb-info{grid-template-columns:1fr;margin:0 16px}
  .alb-info>div{padding:28px 0 32px}
  .alb-info>div:nth-child(2n){border-left:0;padding-left:0}
  .alb-info>div+div{border-top:1px solid #D7E6F2}
  .alb-k{margin-bottom:16px}
  .alb-stats{gap:24px 48px}
  .alb-stats b{font-size:64px}
  .alb-h2{padding:72px 16px 32px}
  .alb-gal{height:auto;display:flex;flex-direction:column;gap:28px;padding:0 16px}
  .alb-fig{position:static;width:auto}
  .alb-fig__img{height:auto;aspect-ratio:var(--w)/var(--h)}
  .alb-fig figcaption{margin-top:8px}
  .alb-brtext{position:static;width:auto}
}
@media (prefers-reduced-motion:reduce){.alb *{transition:none!important;animation:none!important;opacity:1!important;translate:none!important;clip-path:none!important;filter:none!important;transform:none!important}}
</style>
'''

JS = '''
<script>
/* Alberti page: hero letters + photo reveal on open, then blocks rise in as they scroll into view */
document.querySelectorAll('.alb-hero__big').forEach(h=>{let i=0;h.innerHTML=[...h.textContent].map(c=>`<span class="ch" style="--i:${i++}">${c}</span>`).join('')});
requestAnimationFrame(()=>requestAnimationFrame(()=>document.body.classList.add('alb-in')));
(()=>{const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}}),{threshold:.08,rootMargin:'0px 0px -6% 0px'});
  document.querySelectorAll('.alb-fig,.alb-info>div,.alb-h2,.alb-brtext').forEach(el=>io.observe(el))})();
</script>
'''


def build(L, src, out):
    t = T[L]
    s = (ROOT / src).read_text(encoding='utf-8')
    hdr = re.search(r'<header class="header">.*?</header>', s, re.S).group(0)
    start = s.index('<section class="hero" id="top">')
    end = s.index('<section class="cta cta2" id="request">')
    mid = s[start:end]
    contact = re.search(r'<section class="cta" id="contact">.*?</section>', mid, re.S).group(0)
    contact = re.sub(r'(<img src=")[^"]*(" alt="" id="ctaImg">)', r'\1assets/alberti/wide.webp\2', contact)
    tst = re.search(r'<section class="tst" id="testimonials">.*?</section>', mid, re.S).group(0)
    stub = mid.replace(contact, '').replace(tst, '').replace('id="top"', 'id="top-main"')
    stub = re.sub(r'(<img\b[^>]*?)\ssrc="[^"]*"', r'\1', stub)
    stub = re.sub(r'<header class="header">.*?</header>', '', stub, flags=re.S)

    top = f'''<section class="alb" id="top">
  {hdr}
  <div class="alb-hero"><p class="alb-hero__big" aria-hidden="true">{t["big"]}</p><img class="alb-hero__img" src="assets/alberti/hero.webp" alt="{t["t1"]}"></div>
  <div class="alb-head">
    <h1>{t["t1"]}<br>{t["t2"]}</h1>
    <span class="alb-head__script" role="img" aria-label="Interior Design"></span>
    <p class="alb-head__desc">{t["desc"]}</p>
    <p class="alb-head__place">{t["place"]}</p>
  </div>
  <img class="alb-wide" src="assets/alberti/wide.webp" alt="{t["t1"]}">
  <div class="alb-info">
    <div><p class="alb-k">{t["role_k"]}</p><p class="alb-v">{t["role"]}</p></div>
    <div><p class="alb-k">{t["task_k"]}</p><p class="alb-v">{t["task"]}</p></div>
    <div><div class="alb-stats"><div><b>328m<sup>2</sup></b><span>{t["area"]}</span></div><div><b>5</b><span>{t["rooms"]}</span></div><div><b>2024</b><span>{t["year"]}</span></div></div></div>
    <div><p class="alb-k">{t["res_k"]}</p><p class="alb-v">{t["res"]}</p></div>
  </div>
  <h2 class="alb-h2">{t["h_int"]}</h2>
  {gallery(INTERIOR, INTERIOR_TOP, INTERIOR_END, t)}
  <div style="height:calc(var(--u) * 160)"></div>
</section>
{contact}
<section class="alb alb--br">
  <h2 class="alb-h2">{t["h_br"]}</h2>
  {gallery(BRAND, BRAND_TOP, BRAND_END, t, f'<p class="alb-brtext">{t["brtext"]}</p>')}
  <div style="height:calc(var(--u) * 160)"></div>
</section>
{tst}
<div class="pf-stub" hidden aria-hidden="true">{stub}</div>
'''
    s = s[:start] + top + s[end:]
    s = re.sub(r'<script type="module">\s*/\* Project locations:.*?</script>', '', s, count=1, flags=re.S)
    s = re.sub(r'<a href="(ua\.html|index\.html)"( class="lang__on")? lang="uk"', lambda m: f'<a href="alberti-ua.html"{m.group(2) or ""} lang="uk"', s)
    s = re.sub(r'<a href="(ua\.html|index\.html)"( class="lang__on")? lang="en"', lambda m: f'<a href="alberti.html"{m.group(2) or ""} lang="en"', s)
    keep = {'#top', '#request', '#contacts', '#contact', '#testimonials'}
    s = re.sub(r'href="(#[a-z][\w-]*)"', lambda m: m.group(0) if m.group(1) in keep else f'href="{t["home"]}{m.group(1)}"', s)
    # inner page: no preloader unless loading is slow (same as the portfolio page)
    s = s.replace('<body class="preloading">', '<body>', 1)
    s = s.replace("if(reduce){finish();writeTitle();return}", "if(reduce||window.__noPre){if(!window.__noPre)finish();writeTitle();return}", 1)
    s = s.replace('<div class="pre" id="pre"', '<script>window.__noPre=true</script>\n<div class="pre" id="pre" style="display:none"', 1)
    s = s.replace('</body>', """<script>
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


build('en', 'index.html', 'alberti.html')
build('ua', 'ua.html', 'alberti-ua.html')
