#!/usr/bin/env python3
"""Build the Consultations page from the main pages (run after build_ua.py).

consultations.html    <- index.html (EN shell)
consultations-ua.html <- ua.html    (UA shell)

Content follows the Figma frame «Consultations» (node 1362:2559), restyled to match
the home page: same fonts, colours, labels, buttons, blue star bullets. The page reuses
the home page's About, Testimonials, request form, contacts and footer.
"""
import re, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
STAR = '<svg class="cn-star" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 1c.9 6.3 4.7 10.1 11 11-6.3.9-10.1 4.7-11 11-.9-6.3-4.7-10.1-11-11C7.3 11.1 11.1 7.3 12 1z"/></svg>'

T = {
 'en': dict(
  title='Individual Consultations — Oksana Panteleyko, Interior Architect',
  h1='Individual<br>Consultations',
  lead='Consultations with an interior designer for people who buy, open, build, or live in a space. Start with a free Diagnostic Session.',
  hero_btn='Get a free Diagnostic Session',
  who_h='Who it’s for', see='See details',
  who=['I invest in<br>real estate', 'I own<br>a business', 'I own<br>a home', 'I’m an interior<br>designer'],
  how_h='How it works',
  how=[('Request', 'Send a request or message me on WhatsApp.'), ('Session', 'Get a free 20-minute diagnostic session.'),
       ('Plan', 'Receive a plan and price tailored to you.'), ('Result', 'Leave with clear answers and next steps.')],
  for_h='This is for you if:', get_h='What you get:', res_h='The result:', ways_h='Ways to work together:',
  aud=[
   dict(id='investors', t='Real estate investors', s='Know if a property will pay off before you invest.',
        f=['You’re looking at a property and aren’t sure it’s worth buying;', 'You’re afraid of wasting your budget on a renovation that won’t pay off;', 'You can’t see the hidden risks, like layout, utilities, or restrictions.'],
        g=['An assessment of the property’s commercial potential;', 'A list of hidden risks;', 'A plan: what to change and what to leave alone.'],
        r='Confidence that your money will come back, and a higher property value with minimal spending.',
        w=[('One-time consultation', 'Property review and answers.'), ('Consultation package', 'Support up to your purchase decision.'), ('Personal guidance', 'From evaluation to finished project.')],
        b='Evaluate my property'),
   dict(id='business', t='Business owners', s='A space that supports your brand and attracts your kind of customers.',
        f=['You’ve changed your concept, but your space looks the same.', 'You’re opening a new location and need one consistent style.', 'Your renovation is underway, but something feels off.'],
        g=['A clear idea of what your concept should be.', 'A review of your current project.', 'Budget and quality control, plus a plan from idea to finished space.'],
        r='A space that reflects your brand and earns back what you invest in the renovation.',
        w=[('One-time consultation', 'A specific question or stage.'), ('Project audit', 'A check of your plans and estimate.'), ('Renovation support', 'From concept to handover.')],
        b='Talk about my business space'),
   dict(id='homeowners', t='Homeowners', s='A home that’s comfortable to live in, with no budget surprises.',
        f=['You bought an apartment or home and don’t know where to start.', 'You’re worried about overpaying or getting the layout wrong.', 'Your renovation is underway, but results aren’t what you expected.'],
        g=['An assessment of the layout and the space’s potential.', 'A check of your plans, estimate, and contractors.', 'A plan and budget: where to save and where not to.'],
        r='A space that fits the way you live, without expensive mistakes.',
        w=[('One-time consultation', 'Answers to your questions.'), ('Project audit', 'A check of your plans and estimate.'), ('Project support', 'Oversight of key stages.')],
        b='Get advice on my home'),
  ],
  des=dict(id='designers', t='Interior designers', s='Become a client magnet: a package of 3 strategy sessions.',
        f=['You don’t have clients in Europe yet.', 'You don’t know how to get noticed in a new country.', 'You can’t raise your rates and keep taking projects you don’t enjoy.'],
        r=['A strong portfolio.', 'A steady stream of clients.', 'Rates that match your experience.'],
        ses=[('Session 1', 'Portfolio and resume', 'Made appealing to the European market.'), ('Session 2', 'Social media', 'Adapted to what European clients expect.'), ('Session 3', 'Finding clients', 'Who to contact, what to write, where to find projects.')],
        price='$500', price_s='For the 3-session package', online='Online', plan='Payment plan available', b='Get the package'),
  fmt_h='Formats and pricing',
  fmt=[('Online', 'WhatsApp, Zoom, Google Meet'), ('In person in Nice, France', '37 Promenade des Anglais, 06000 Nice'), ('On-site visit', 'Anywhere in the world. The client covers airfare.')],
  note=['Every project differs in size and depth, so we set the format and price after the Diagnostic Session.', 'The one exception is the designer package at $500.', 'The Diagnostic Session is free and comes with no obligation.'],
  ext_k='For business', ext_h='Additional services',
  ext=[dict(k='Turnkey rebranding', t='“Full transformation”', p='When a business needs a full refresh — not a single renovation or a new logo — I bring together a team of specialists who run the whole process turnkey:',
            l=['Interior renovation', 'Branding', 'Website development'], p2='You get one coherent result where the space, the visual identity and the online presence speak the same language — without coordinating several contractors yourself.'),
       dict(k='Business consulting', t='Team building and management', p='For businesses opening or growing a hotel, restaurant or other venue:',
            l=['Selecting specialists for your team', 'Hotel launch consulting', 'How to run a hotel or restaurant', 'Working with the venue’s manager'], p2='')],
  ext_b='Discuss collaboration',
  faq_h='Frequently asked<br>questions',
  faq=[('How much does a consultation cost?', 'The price depends on the scope and depth of your request. We set the format and price after a short, free diagnostic session.'),
       ('How long does a consultation take?', 'The diagnostic session takes about 20 minutes. A full consultation usually lasts 60–90 minutes, depending on the format.'),
       ('Online or in person?', 'Both. Online via WhatsApp, Zoom or Google Meet; in person in Nice; or an on-site visit anywhere in the world.'),
       ('What should I prepare beforehand?', 'Plans or floor layouts, photos of the space, your estimate if you have one, and a short list of questions. Anything you have helps.'),
       ('Can I ask about something that isn’t listed?', 'Of course. Tell me about your situation and I’ll suggest the format that fits.')],
  me='consultations.html', other='consultations-ua.html', home='index.html',
 ),
 'ua': dict(
  title='Індивідуальні консультації — Оксана Пантелейко, архітектор інтер’єрів',
  h1='Індивідуальні<br>консультації',
  lead='Консультації дизайнера інтер’єру для тих, хто купує, відкриває, будує чи живе у просторі. Почніть з безкоштовної діагностичної сесії.',
  hero_btn='Безкоштовна діагностична сесія',
  who_h='Для кого', see='Детальніше',
  who=['Я інвестую<br>в нерухомість', 'У мене<br>бізнес', 'Я власник<br>житла', 'Я дизайнер<br>інтер’єру'],
  how_h='Як це працює',
  how=[('Заявка', 'Залиште заявку або напишіть мені у WhatsApp.'), ('Сесія', 'Безкоштовна 20-хвилинна діагностична сесія.'),
       ('План', 'План і ціна, підібрані саме під Вас.'), ('Результат', 'Чіткі відповіді та наступні кроки.')],
  for_h='Це для Вас, якщо:', get_h='Що Ви отримаєте:', res_h='Результат:', ways_h='Формати співпраці:',
  aud=[
   dict(id='investors', t='Інвесторам у нерухомість', s='Дізнайтеся, чи окупиться об’єкт, ще до інвестиції.',
        f=['Ви розглядаєте об’єкт і не впевнені, що його варто купувати;', 'Боїтеся витратити бюджет на ремонт, який не окупиться;', 'Не бачите прихованих ризиків: планування, комунікацій чи обмежень.'],
        g=['Оцінку комерційного потенціалу об’єкта;', 'Перелік прихованих ризиків;', 'План: що змінити, а що лишити як є.'],
        r='Впевненість, що гроші повернуться, і вища вартість об’єкта за мінімальних витрат.',
        w=[('Разова консультація', 'Огляд об’єкта і відповіді.'), ('Пакет консультацій', 'Супровід до рішення про купівлю.'), ('Персональний супровід', 'Від оцінки до готового проєкту.')],
        b='Оцінити мій об’єкт'),
   dict(id='business', t='Власникам бізнесу', s='Простір, що підтримує Ваш бренд і приваблює саме Ваших клієнтів.',
        f=['Ви змінили концепцію, а простір лишився тим самим.', 'Відкриваєте нову локацію і потрібен єдиний стиль.', 'Ремонт уже йде, але щось не так.'],
        g=['Чітке розуміння, якою має бути концепція.', 'Аналіз Вашого поточного проєкту.', 'Контроль бюджету і якості та план від ідеї до готового простору.'],
        r='Простір, який відображає Ваш бренд і повертає вкладене в ремонт.',
        w=[('Разова консультація', 'Конкретне питання чи етап.'), ('Аудит проєкту', 'Перевірка планів і кошторису.'), ('Супровід реновації', 'Від концепції до здачі.')],
        b='Обговорити мій бізнес-простір'),
   dict(id='homeowners', t='Власникам житла', s='Дім, у якому комфортно жити, — без сюрпризів у бюджеті.',
        f=['Ви купили квартиру чи будинок і не знаєте, з чого почати.', 'Боїтеся переплатити або помилитися з плануванням.', 'Ремонт уже йде, але результат не такий, як очікували.'],
        g=['Оцінку планування і потенціалу простору.', 'Перевірку планів, кошторису й підрядників.', 'План і бюджет: де можна заощадити, а де ні.'],
        r='Простір під Ваш спосіб життя — без дорогих помилок.',
        w=[('Разова консультація', 'Відповіді на Ваші питання.'), ('Аудит проєкту', 'Перевірка планів і кошторису.'), ('Супровід проєкту', 'Контроль ключових етапів.')],
        b='Порада щодо мого житла'),
  ],
  des=dict(id='designers', t='Дизайнерам інтер’єру', s='Станьте магнітом для клієнтів: пакет із 3 стратегічних сесій.',
        f=['У Вас ще немає клієнтів у Європі.', 'Не знаєте, як заявити про себе в новій країні.', 'Не можете підняти ціни й берете проєкти, які не подобаються.'],
        r=['Сильне портфоліо.', 'Стабільний потік клієнтів.', 'Ціни, що відповідають Вашому досвіду.'],
        ses=[('Сесія 1', 'Портфоліо і резюме', 'Привабливі для європейського ринку.'), ('Сесія 2', 'Соцмережі', 'Під очікування європейських клієнтів.'), ('Сесія 3', 'Пошук клієнтів', 'Кому писати, що писати, де шукати проєкти.')],
        price='$500', price_s='За пакет із 3 сесій', online='Онлайн', plan='Можлива оплата частинами', b='Отримати пакет'),
  fmt_h='Формати та вартість',
  fmt=[('Онлайн', 'WhatsApp, Zoom, Google Meet'), ('Особисто в Ніцці, Франція', '37 Promenade des Anglais, 06000 Nice'), ('Виїзд на об’єкт', 'Будь-де у світі. Переліт оплачує клієнт.')],
  note=['Кожен проєкт різний за масштабом і глибиною, тому формат і ціну визначаємо після діагностичної сесії.', 'Єдиний виняток — пакет для дизайнерів за $500.', 'Діагностична сесія безкоштовна й ні до чого не зобов’язує.'],
  ext_k='Для бізнесу', ext_h='Додаткові послуги',
  ext=[dict(k='Ребрендинг під ключ', t='«Повна трансформація»', p='Якщо бізнесу потрібне повне оновлення — а не окремий ремонт чи новий логотип — я збираю команду фахівців, яка проведе весь процес під ключ:',
            l=['Реновація інтер’єру', 'Брендинг', 'Розробка сайту'], p2='Ви отримуєте цілісний результат, де простір, візуальна ідентичність і цифрова присутність говорять однією мовою — без потреби самостійно координувати кількох підрядників.'),
       dict(k='Консультування бізнесу', t='Підбір команди та управління', p='Для бізнесу, який відкриває або розвиває готель, ресторан чи інший об’єкт:',
            l=['Підбір спеціалістів у команду', 'Консультації із запуску готелю', 'Як управляти готелем чи рестораном', 'Робота з керуючим об’єкта'], p2='')],
  ext_b='Обговорити співпрацю',
  faq_h='Часті питання',
  faq=[('Скільки коштує консультація?', 'Вартість залежить від масштабу та глибини запиту. Формат і ціну визначаємо після короткої безкоштовної діагностичної зустрічі.'),
       ('Скільки триває консультація?', 'Діагностична сесія триває близько 20 хвилин. Повна консультація — зазвичай 60–90 хвилин, залежно від формату.'),
       ('Консультація онлайн чи офлайн?', 'Обидва варіанти. Онлайн — у WhatsApp, Zoom чи Google Meet; особисто — у Ніцці; або виїзд на об’єкт будь-де у світі.'),
       ('Що потрібно підготувати перед консультацією?', 'Плани або обміри, фото простору, кошторис, якщо він є, і короткий список питань. Усе, що маєте, допоможе.'),
       ('Чи можна звернутись з питанням, якого немає у списку?', 'Звісно. Розкажіть про свою ситуацію — і я запропоную формат, який підійде.')],
  me='consultations-ua.html', other='consultations.html', home='ua.html',
 ),
}

PLUS = ' <span class="plus"></span>'


def ul(items):
    return '<ul class="cn-list">' + ''.join(f'<li>{STAR}<span>{x}</span></li>' for x in items) + '</ul>'


def audience(n, a, t, tint):
    ways = ''.join(f'<div class="cn-way"><h4>{h}</h4><p>{p}</p></div>' for h, p in a['w'])
    return f'''<section class="cn cn-aud{' cn--tint' if tint else ''}" id="{a['id']}">
  <div class="cn-head rv"><p class="cn-n">{n:02d}</p><h2 class="cn-h2">{a['t']}</h2><p class="cn-sub">{a['s']}</p></div>
  <div class="cn-photo rv"><img src="assets/consult/room.webp" alt="" loading="lazy"></div>
  <div class="cn-two">
    <div class="cn-box rv"><h3 class="cn-h3">{t['for_h']}</h3>{ul(a['f'])}</div>
    <div class="cn-box rv" style="--d:.1s"><h3 class="cn-h3">{t['get_h']}</h3>{ul(a['g'])}</div>
  </div>
  <div class="cn-result rv"><h3 class="cn-h3">{t['res_h']}</h3><p>{a['r']}</p></div>
  <h3 class="cn-ways-h rv">{t['ways_h']}</h3>
  <div class="cn-ways rv">{ways}</div>
  <div class="cn-cta rv"><a class="btn btn--ink" href="#request">{a['b']}{PLUS}</a></div>
</section>'''


def designers(t):
    d = t['des']
    ses = ''.join(f'<div class="cn-ses rv"><p class="cn-ses__k">{k}</p><h4 class="cn-h3">{h}</h4><p>{p}</p></div>' for k, h, p in d['ses'])
    return f'''<section class="cn cn-aud cn--dark" id="{d['id']}" data-dark>
  <div class="cn-head rv"><p class="cn-n">04</p><h2 class="cn-h2">{d['t']}</h2><p class="cn-sub">{d['s']}</p></div>
  <div class="cn-photo rv"><img src="assets/consult/room.webp" alt="" loading="lazy"></div>
  <div class="cn-two">
    <div class="cn-box rv"><h3 class="cn-h3">{t['for_h']}</h3>{ul(d['f'])}</div>
    <div class="cn-box rv" style="--d:.1s"><h3 class="cn-h3">{t['res_h']}</h3>{ul(d['r'])}</div>
  </div>
  <div class="cn-sesgrid">{ses}
    <div class="cn-price rv"><div class="cn-price__top"><b>{d['price']}</b><span>{d['online']}</span></div>
      <div class="cn-price__row"><span>{d['price_s']}</span><span class="cn-ok">✓ {d['plan']}</span></div>
      <a class="btn btn--light cn-price__btn" href="#request">{d['b']}{PLUS}</a></div>
  </div>
</section>'''


def page_html(t):
    who = ''.join(f'<a class="cn-who rv" style="--d:{i*.08:.2f}s" href="#{a}"><h3>{w}</h3><span class="lnk cn-who__lnk">{t["see"]} <i></i></span></a>'
                  for i, (w, a) in enumerate(zip(t['who'], ['investors', 'business', 'homeowners', 'designers'])))
    how = ''.join(f'<div class="cn-step rv" style="--d:{i*.1:.1f}s"><span class="cn-step__n">{i+1}</span><h3>{h}</h3><p>{p}</p></div>' for i, (h, p) in enumerate(t['how']))
    fmt = ''.join(f'<div class="cn-way"><h4>{h}</h4><p>{p}</p></div>' for h, p in t['fmt'])
    ext = ''.join(f'''<div class="cn-ext rv"><p class="cn-ext__k">{e['k']}</p><h3 class="cn-h3">{e['t']}</h3><p>{e['p']}</p>
      <ul class="cn-dash">{''.join(f'<li>{x}</li>' for x in e['l'])}</ul>{f'<p>{e["p2"]}</p>' if e['p2'] else ''}
      <a class="btn btn--light" href="#request">{t['ext_b']}{PLUS}</a></div>''' for e in t['ext'])
    faq = ''.join(f'<details class="cn-faq__i"{" open" if i == 0 else ""}><summary>{q}<i></i></summary><p>{a}</p></details>' for i, (q, a) in enumerate(t['faq']))
    auds = ''.join(audience(i + 1, a, t, i % 2 == 1) for i, a in enumerate(t['aud']))
    return f'''<section class="cn cn-hero" id="top-c">
  <img class="cn-hero__img" src="assets/consult/room.webp" alt="">
  <div class="cn-hero__in">
    <h1 class="cn-hero__h">{t['h1']}</h1>
    <div class="cn-hero__side"><a class="btn btn--light" href="#request">{t['hero_btn']}{PLUS}</a><p>{t['lead']}</p></div>
  </div>
</section>
<section class="cn cn-whosec"><h2 class="cn-h2 rv">{t['who_h']}</h2><div class="cn-whogrid">{who}</div></section>
<section class="cn cn--tint cn-howsec"><h2 class="cn-h2 rv">{t['how_h']}</h2><div class="cn-steps">{how}</div></section>
{auds}
{designers(t)}
<section class="cn cn-fmt"><h2 class="cn-h2 rv">{t['fmt_h']}</h2><div class="cn-ways cn-ways--tint rv">{fmt}</div>
  <div class="cn-note rv"><p>{t['note'][0]}</p><p><b>{t['note'][1]}</b></p><p>{t['note'][2]}</p></div></section>
'''


def page_html_after(t):
    ext = ''.join(f'''<div class="cn-ext rv"><p class="cn-ext__k">{e['k']}</p><h3 class="cn-h3">{e['t']}</h3><p>{e['p']}</p>
      <ul class="cn-dash">{''.join(f'<li>{x}</li>' for x in e['l'])}</ul>{f'<p>{e["p2"]}</p>' if e['p2'] else ''}
      <a class="btn btn--light" href="#request">{t['ext_b']}{PLUS}</a></div>''' for e in t['ext'])
    faq = ''.join(f'<details class="cn-faq__i"{" open" if i == 0 else ""}><summary>{q}<i></i></summary><p>{a}</p></details>' for i, (q, a) in enumerate(t['faq']))
    return f'''<section class="cn cn--dark cn-extsec" data-dark><div class="cn-head rv"><p class="cn-n">{t['ext_k']}</p><h2 class="cn-h2">{t['ext_h']}</h2></div><div class="cn-two">{ext}</div></section>
<section class="cn cn-faq"><h2 class="cn-h2 rv">{t['faq_h']}</h2><div class="cn-faq__list rv">{faq}</div></section>
'''


CSS = '''
<style>.header{--u:min(calc(100vw / 1920),calc(100vh / 1080));z-index:60!important}</style>
<style id="cn-css">
/* ===== Consultations page — home-page fonts, colours and buttons ===== */
.cn{position:relative;z-index:2;background:#fff;color:var(--ink);padding:clamp(80px,7.8vw,150px) var(--pad)}
.cn--tint{background:#EEF2F5}
.cn--dark{background:#1D1616;color:#fff}
.cn-h2{margin:0;text-align:center;font:400 var(--h2)/1.1 var(--serif);text-transform:uppercase;letter-spacing:-.01em}
.cn-h3{margin:0;font:400 clamp(24px,1.9vw,36px)/1.15 var(--serif);text-transform:uppercase;letter-spacing:-.01em}
.cn-head{text-align:center;margin-bottom:clamp(40px,4.2vw,80px)}
.cn-n{margin:0 0 14px;font:500 16px/1 var(--sans);letter-spacing:.06em;text-transform:uppercase;opacity:.55}
.cn-sub{margin:16px auto 0;max-width:36em;font:400 clamp(16px,1.05vw,20px)/1.45 var(--sans);opacity:.75}
.cn-star{flex:none;width:18px;height:18px;margin-top:3px;fill:#8FB8D2}
.cn--dark .cn-star{fill:#fff}
/* hero */
.cn-hero{padding:0;height:100vh;height:100svh;min-height:560px;overflow:hidden;color:#fff}
.cn-hero__img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:50% 62%}
.cn-hero::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(29,22,22,.18) 0%,rgba(29,22,22,0) 30%,rgba(29,22,22,.45) 100%)}
.cn-hero__in{position:absolute;z-index:1;left:var(--pad);right:var(--pad);bottom:clamp(40px,4.2vw,80px);display:flex;justify-content:space-between;align-items:flex-end;gap:40px}
.cn-hero__h{margin:0;font:400 clamp(44px,5.2vw,100px)/1 var(--serif);text-transform:uppercase;letter-spacing:-.01em}
.cn-hero__side{max-width:420px;display:flex;flex-direction:column;gap:20px}
.cn-hero__side p{margin:0;font:400 16px/1.5 var(--sans)}
/* who */
.cn-whogrid{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-top:clamp(40px,4.2vw,80px)}
.cn-who{display:flex;flex-direction:column;justify-content:space-between;gap:48px;min-height:clamp(200px,13vw,250px);padding:clamp(20px,1.6vw,32px);background:#EEF2F5;color:var(--ink);text-decoration:none;transition:background .4s}
.cn-who:hover{background:#E1EBF4}
.cn-who h3{margin:0;font:400 clamp(24px,1.7vw,32px)/1.15 var(--serif);text-transform:uppercase}
/* the card's link is the site's plus-link; hovering the whole card plays its hover */
.cn-who__lnk{align-self:stretch;font-weight:600;font-size:clamp(12px,.833vw,16px);line-height:1.5;padding-bottom:clamp(9px,.62vw,12px)}   /* same as the home page's plus-links */
.cn-who__lnk i{width:clamp(10px,.708vw,13.6px);height:clamp(10px,.708vw,13.6px)}
.cn-who:hover .lnk i{transform:rotate(90deg)}
.cn-who:hover .lnk .roll>span:first-child{transform:translateY(-110%)}
.cn-who:hover .lnk .roll>span+span{transform:none}
.cn-who:hover .lnk::after{animation:lineRedraw .9s cubic-bezier(.77,0,.18,1)}
/* how */
.cn-steps{display:grid;grid-template-columns:1fr 1fr 1fr auto;gap:24px;margin-top:clamp(40px,4.2vw,80px);position:relative}   /* the last step sits at the right edge, so the row spans the full width */
.cn-steps::before{content:"";position:absolute;left:20px;right:var(--lineR,20px);top:20px;border-top:1px dashed #8FB8D2}   /* ends at the 4th circle (set by script) */
.cn-step{position:relative}
.cn-step__n{display:grid;place-items:center;width:40px;height:40px;border-radius:50%;background:#1D1616;color:#fff;font:600 16px/1 var(--sans)}
.cn-step h3{margin:28px 0 12px;font:400 clamp(24px,1.9vw,36px)/1.1 var(--serif);text-transform:uppercase}
.cn-step p{margin:0;max-width:16em;font:400 16px/1.5 var(--sans);opacity:.8;text-wrap:balance}
/* audience blocks */
.cn-photo{height:clamp(260px,28vw,540px);overflow:hidden}
.cn-photo img{width:100%;height:100%;object-fit:cover;object-position:50% 62%}
.cn-two{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:12px}
.cn-box{padding:clamp(24px,2vw,40px);border:1px solid var(--line);background:#fff}
.cn--tint .cn-box{border-color:transparent}
.cn--dark .cn-box{background:transparent;border-color:rgba(255,255,255,.18)}
.cn-list{list-style:none;margin:24px 0 0;padding:0;display:grid;gap:14px}
.cn-list li{display:flex;gap:12px;font:400 clamp(16px,1.05vw,20px)/1.45 var(--sans)}
.cn-result{margin-top:12px;padding:clamp(24px,2vw,40px);background:#1D1616;color:#fff}
.cn-result p{margin:14px 0 0;font:400 clamp(16px,1.05vw,20px)/1.45 var(--sans)}
.cn-ways-h{margin:clamp(56px,4.2vw,80px) 0 0;text-align:center;font:400 clamp(26px,2vw,40px)/1.1 var(--serif);text-transform:uppercase}
.cn-ways{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-top:clamp(28px,2.1vw,40px)}
.cn-way{padding:clamp(24px,1.6vw,32px);border:1px solid var(--line);background:#fff}
.cn--tint .cn-way{border-color:transparent}
.cn-ways--tint .cn-way{background:#EEF2F5;border-color:transparent}
.cn-way h4{margin:0;font:600 16px/1.3 var(--sans);text-transform:uppercase;letter-spacing:.02em}
.cn-way p{margin:12px 0 0;font:400 16px/1.5 var(--sans);opacity:.8}
.cn-cta{display:flex;justify-content:center;margin-top:clamp(40px,3.1vw,60px)}
.cn-cta .btn{width:auto;min-width:320px}
/* designers */
.cn-sesgrid{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:12px}
.cn-ses{padding:clamp(24px,2vw,40px);background:#F4F2F0;color:var(--ink)}
.cn-ses__k{margin:0 0 28px;font:600 16px/1 var(--sans)}
.cn-ses p:last-child{margin:14px 0 0;font:400 16px/1.5 var(--sans);opacity:.8}
.cn-price{display:flex;flex-direction:column;gap:12px;padding:clamp(24px,2vw,40px);border:1px solid rgba(255,255,255,.18)}
.cn-price__top{display:flex;justify-content:space-between;align-items:baseline}
.cn-price__top b{font:400 clamp(40px,3.1vw,60px)/1 var(--serif)}
.cn-price__top span,.cn-price__row{font:400 16px/1.4 var(--sans)}
.cn-price__row{display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap;opacity:.9}
.cn-price__btn{margin-top:auto}
/* formats */
.cn-note{margin:clamp(40px,3.1vw,60px) 0 0;padding-left:20px;border-left:2px solid #1D1616;font:400 clamp(16px,1.05vw,20px)/1.5 var(--sans)}
.cn-note p{margin:0 0 10px}
/* extra services */
.cn-ext{display:flex;flex-direction:column;gap:18px;padding:clamp(28px,2.6vw,48px);background:rgba(255,255,255,.06)}
.cn-ext__k{margin:0;font:500 16px/1 var(--sans);text-transform:uppercase;letter-spacing:.04em;opacity:.7}
.cn-ext p{margin:0;font:400 16px/1.55 var(--sans);opacity:.85}
.cn-dash{margin:0;padding:0;list-style:none;font:400 clamp(16px,1.05vw,20px)/1.6 var(--sans)}
.cn-dash li::before{content:"— "}
.cn-ext .btn{margin-top:auto;align-self:flex-start;width:auto;min-width:280px}
/* faq */
.cn-faq{display:grid;grid-template-columns:1fr 1fr;gap:40px}
.cn-faq .cn-h2{text-align:left}
.cn-faq__list{display:grid;gap:8px}
.cn-faq__i{background:#EEF2F5;transition:background .3s ease}
.cn-faq__i[open]{background:#D6E6F2}   /* the open question stands out in the site's light blue */
.cn-faq__i p{overflow:hidden}
.cn-faq__i summary{list-style:none;display:flex;justify-content:space-between;align-items:center;gap:20px;padding:22px 24px;cursor:pointer;font:500 clamp(16px,1.05vw,20px)/1.35 var(--sans)}
.cn-faq__i summary::-webkit-details-marker{display:none}
.cn-faq__i summary i{position:relative;flex:none;width:16px;height:16px}
.cn-faq__i summary i::before,.cn-faq__i summary i::after{content:"";position:absolute;left:0;right:0;top:50%;border-top:1.5px solid currentColor;transition:rotate .35s var(--ease)}
.cn-faq__i summary i::after{rotate:90deg}
.cn-faq__i[open] summary i::after{rotate:0deg}
.cn-faq__i p{margin:0;padding:0 24px 24px;font:400 16px/1.55 var(--sans);opacity:.85}
/* photo of Oksana right before the About block */
.cn-me{padding:0;height:clamp(420px,46vw,880px);overflow:hidden}
.cn-me img{display:block;width:100%;height:100%;object-fit:cover;object-position:50% 22%}
@media (max-width:900px){.cn-me{height:auto;aspect-ratio:4/5}.cn-me img{object-position:50% 30%}}
/* light buttons keep the home page's soft light-blue glow under the cursor (no override) */
/* white buttons on dark blocks: the home page's light-blue fill spreading from the cursor */
.cn--dark .btn--light::before,.cn-hero .btn--light::before{display:block!important;opacity:1!important;background:#84B7DB!important;clip-path:circle(0% at var(--ex,50%) var(--ey,50%));transition:clip-path .7s cubic-bezier(.65,0,.35,1)}
.cn--dark .btn--light,.cn-hero .btn--light{transition:color .45s ease}
.cn--dark .btn--light:hover,.cn-hero .btn--light:hover{color:#fff!important}   /* text turns white on the blue fill, as on the home page */
.cn--dark .btn--light:hover::before,.cn-hero .btn--light:hover::before{clip-path:circle(150% at var(--ex,50%) var(--ey,50%))}
@media (max-width:900px){
  .cn{padding:80px 16px}
  .cn-hero{padding:0}
  .cn-hero__in{flex-direction:column;align-items:flex-start;left:16px;right:16px;bottom:32px;gap:24px}
  .cn-hero__h{font-size:clamp(36px,11vw,52px)}
  .cn-whogrid{grid-template-columns:1fr 1fr;gap:8px}
  .cn-who{min-height:170px;gap:24px;padding:18px}
  .cn-who h3{font-size:clamp(18px,5vw,24px)}
  .cn-steps{grid-template-columns:1fr 1fr;gap:40px 16px}
  .cn-steps::before{display:none}
  .cn-two,.cn-ways,.cn-sesgrid,.cn-faq{grid-template-columns:1fr}
  .cn-photo{height:62vw}
  .cn-cta .btn,.cn-ext .btn{min-width:0;width:100%}
  .cn-faq{gap:32px}
}
@media (max-width:420px){.cn-whogrid{grid-template-columns:1fr}.cn-who{min-height:0}}
</style>
'''



# ===================== v2: editorial redesign (placeholders until Oksana sends materials) =====================
X = {
 'en': dict(cta='Book a Free Diagnostic Session', trust=['18 years of practice', '120+ projects', 'SBID Awards finalist'],
            kicker='Interior consultations', reply='I reply within 24 hours',
            wa='Write on WhatsApp', before='Today', after='After the consultation',
            menu_h='Formats and pricing', menu_note='Prices are indicative; the final format and price are set after the free diagnostic.',
            menu=[('Free Diagnostic Session', '20 minutes · online', 'Free'), ('One-time consultation', '60–90 minutes · online or in Nice', 'from €250'),
                  ('Project audit', 'Plans, estimate and contractors reviewed', 'from €600'), ('Personal guidance', 'From evaluation to the finished space', 'on request'),
                  ('Designer package', '3 strategy sessions · online', '$500')],
            where=['Online — WhatsApp, Zoom, Google Meet', 'In person — 37 Promenade des Anglais, Nice', 'On site — anywhere in the world'],
            ways_short='Formats'),
 'ua': dict(cta='Записатися на безкоштовну діагностику', trust=['18 років практики', '120+ проєктів', 'Фіналіст SBID Awards'],
            kicker='Консультації дизайнера інтер’єру', reply='Відповім протягом 24 годин',
            wa='Написати у WhatsApp', before='Зараз', after='Після консультації',
            menu_h='Формати та вартість', menu_note='Ціни орієнтовні; остаточний формат і вартість визначаємо після безкоштовної діагностики.',
            menu=[('Безкоштовна діагностична сесія', '20 хвилин · онлайн', 'Безкоштовно'), ('Разова консультація', '60–90 хвилин · онлайн або в Ніцці', 'від €250'),
                  ('Аудит проєкту', 'Перевірка планів, кошторису й підрядників', 'від €600'), ('Персональний супровід', 'Від оцінки до готового простору', 'за запитом'),
                  ('Пакет для дизайнерів', '3 стратегічні сесії · онлайн', '$500')],
            where=['Онлайн — WhatsApp, Zoom, Google Meet', 'Особисто — 37 Promenade des Anglais, Ніцца', 'Виїзд на об’єкт — будь-де у світі'],
            ways_short='Формати'),
}
PHOTOS = {'investors': 'pf/05a.webp', 'business': 'pf/06a.webp', 'homeowners': 'renovation.webp', 'designers': 'services.jpg'}
ARROW = '<svg class="cn-arr" viewBox="0 0 40 12" aria-hidden="true"><path d="M0 6h38M32 1l6 5-6 5" fill="none" stroke="currentColor" stroke-width="1.2"/></svg>'


def cta_btn(L, cls='btn--ink'):
    return f'<a class="btn {cls}" href="#request">{X[L]["cta"]}{PLUS}</a>'


def audience(n, a, t, tint, L='en'):
    x = X[L]
    ways = ''.join(f'<li><b>{h}</b><span>{p}</span></li>' for h, p in a['w'])
    return f'''<section class="cn cn-aud{' cn--tint' if tint else ''}" id="{a['id']}">
  <div class="cn-aud__side">
    <div class="cn-aud__stick">
      <p class="cn-aud__n rv">{n:02d}</p>
      <h2 class="cn-aud__t rv">{a['t']}</h2>
      <p class="cn-sub rv">{a['s']}</p>
      <div class="cn-aud__img rv"><img src="assets/{PHOTOS[a['id']]}" alt="" loading="lazy"></div>
    </div>
  </div>
  <div class="cn-aud__main">
    <div class="cn-ba rv">
      <div class="cn-ba__col"><p class="cn-k">{x['before']}</p>{ul(a['f'])}</div>
      {ARROW}
      <div class="cn-ba__col cn-ba__col--after"><p class="cn-k">{x['after']}</p>{ul(a['g'])}</div>
    </div>
    <p class="cn-quote rv">{a['r']}</p>
    <div class="cn-formats rv"><p class="cn-k">{x['ways_short']}</p><ul>{ways}</ul></div>
    <div class="cn-cta rv">{cta_btn(L)}</div>
  </div>
</section>'''


def designers(t, L='en'):
    d, x = t['des'], X[L]
    ses = ''.join(f'<li class="rv"><span class="cn-ses__k">{k}</span><b>{h}</b><span>{p}</span></li>' for k, h, p in d['ses'])
    return f'''<section class="cn cn-aud cn--dark" id="{d['id']}" data-dark>
  <div class="cn-aud__side">
    <div class="cn-aud__stick">
      <p class="cn-aud__n rv">04</p>
      <h2 class="cn-aud__t rv">{d['t']}</h2>
      <p class="cn-sub rv">{d['s']}</p>
      <div class="cn-aud__img rv"><img src="assets/{PHOTOS['designers']}" alt="" loading="lazy"></div>
    </div>
  </div>
  <div class="cn-aud__main">
    <div class="cn-ba rv">
      <div class="cn-ba__col"><p class="cn-k">{x['before']}</p>{ul(d['f'])}</div>
      {ARROW}
      <div class="cn-ba__col cn-ba__col--after"><p class="cn-k">{x['after']}</p>{ul(d['r'])}</div>
    </div>
    <ol class="cn-sessions">{ses}</ol>
    <div class="cn-pack rv"><div><b>{d['price']}</b><span>{d['price_s']} · {d['online']} · {d['plan']}</span></div>{cta_btn(L, 'btn--light')}</div>
  </div>
</section>'''


def page_html(t, L='en'):
    x = X[L]
    ids = ['investors', 'business', 'homeowners', 'designers']
    who = ''.join(f'<a class="cn-row rv" href="#{a}" data-img="assets/{PHOTOS[a]}"><span class="cn-row__n">{i+1:02d}</span><span class="cn-row__t">{w.replace("<br>", " ")}</span><span class="cn-row__go">{ARROW}</span></a>'
                  for i, (w, a) in enumerate(zip(t['who'], ids)))
    how = ''.join(f'<div class="cn-step rv" style="--d:{i*.1:.1f}s"><span class="cn-step__n">{i+1}</span><h3>{h}</h3><p>{p}</p></div>' for i, (h, p) in enumerate(t['how']))
    auds = ''.join(audience(i + 1, a, t, i % 2 == 1, L) for i, a in enumerate(t['aud']))
    menu = ''.join(f'<li class="rv"><span class="cn-menu__t">{h}</span><span class="cn-menu__d">{d}</span><span class="cn-menu__dots"></span><span class="cn-menu__p">{pr}</span></li>' for h, d, pr in x['menu'])
    trust = ''.join(f'<li>{s}</li>' for s in x['trust'])
    return f'''<section class="cn cn-hero2" id="top-c">
  <div class="cn-hero2__txt">
    <p class="cn-k load" style="--d:.2s">{x['kicker']}</p>
    <h1 class="cn-hero2__h">{t['h1']}</h1>
    <span class="cn-hero2__sign" role="img" aria-label="Oksana Panteleyko"></span>
    <p class="cn-hero2__lead load" style="--d:.9s">{t['lead']}</p>
    <div class="cn-hero2__act load" style="--d:1.05s">{cta_btn(L)}</div>
    <ul class="cn-trust load" style="--d:1.2s">{trust}</ul>
  </div>
  <div class="cn-hero2__img"><img src="assets/consult-cafe.jpg" alt=""></div>
</section>
<section class="cn cn-whosec"><h2 class="cn-h2 rv">{t['who_h']}</h2><nav class="cn-rows">{who}</nav><img class="cn-float" alt="" aria-hidden="true"></section>
<section class="cn cn--tint cn-howsec"><h2 class="cn-h2 rv">{t['how_h']}</h2><div class="cn-steps">{how}</div></section>
{auds}
{designers(t, L)}
<section class="cn cn-menusec"><h2 class="cn-h2 rv">{x['menu_h']}</h2>
  <ul class="cn-menu">{menu}</ul>
  <ul class="cn-where rv">{''.join(f'<li>{w}</li>' for w in x['where'])}</ul>
  <p class="cn-menu__note rv">{x['menu_note']}</p>
  <div class="cn-cta rv">{cta_btn(L)}</div>
</section>
'''


CSS += '''
<style id="cn-v2">
/* ===== v2 editorial layer ===== */
.cn-k{margin:0;font:600 16px/1.2 var(--sans);text-transform:uppercase;letter-spacing:.06em;color:#695845}
.cn--dark .cn-k{color:#B0D3EB}
/* hero: text left, portrait right */
.cn-hero2{display:grid;grid-template-columns:1.1fr .9fr;min-height:100vh;min-height:100svh;padding:0}
.cn-hero2__txt{display:flex;flex-direction:column;justify-content:flex-end;gap:24px;padding:calc(110px + 4vw) var(--pad) clamp(48px,5vw,96px)}
.cn-hero2__h{margin:0;font:400 clamp(52px,6.4vw,124px)/.95 var(--serif);text-transform:uppercase;letter-spacing:-.02em}
.cn-hero2__h .ch{display:inline-block;opacity:0;transform:translateY(.4em);filter:blur(6px);animation:ch .9s var(--ease) forwards;animation-delay:calc(.25s + var(--i) * .035s)}
.cn-hero2__sign{display:block;width:clamp(220px,20vw,380px);aspect-ratio:1024/720;margin:-1.2em 0 -.6em 30%;background:#8FB8D2;-webkit-mask:url(assets/about-signature.png) center/contain no-repeat;mask:url(assets/about-signature.png) center/contain no-repeat;clip-path:inset(0 100% 0 0);animation:cnSign 1.6s cubic-bezier(.65,0,.35,1) .7s forwards}
@keyframes cnSign{to{clip-path:inset(0 0 0 0)}}
.cn-hero2__lead{margin:0;max-width:30em;font:400 clamp(16px,1.15vw,22px)/1.5 var(--sans)}
.cn-hero2__act .btn{width:auto;min-width:340px}
.cn-trust{display:flex;flex-wrap:wrap;gap:8px 28px;margin:8px 0 0;padding:0;list-style:none;font:500 16px/1.3 var(--sans);opacity:.75}
.cn-trust li{display:flex;align-items:center;gap:10px}
.cn-trust li+li::before{content:"";width:5px;height:5px;border-radius:50%;background:#8FB8D2;margin-left:-18px}
.cn-hero2__img{position:relative;overflow:hidden}
.cn-hero2__img img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:50% 30%;scale:1.08;animation:cnZoom 2.4s cubic-bezier(.25,.1,.25,1) forwards}
@keyframes cnZoom{to{scale:1}}
/* who it's for: big editorial rows, a photo follows the cursor */
.cn-rows{margin-top:clamp(40px,4.2vw,80px);border-top:1px solid var(--line)}
.cn-row{display:grid;grid-template-columns:80px 1fr auto;align-items:center;gap:24px;padding:clamp(22px,2.2vw,40px) 0;border-bottom:1px solid var(--line);color:var(--ink);text-decoration:none;transition:padding .5s var(--ease),color .4s}
.cn-row__n{font:500 16px/1 var(--sans);opacity:.45}
.cn-row__t{font:400 clamp(30px,3.4vw,64px)/1 var(--serif);text-transform:uppercase;letter-spacing:-.01em}
.cn-row__go .cn-arr{width:44px;transition:translate .5s var(--ease)}
.cn-row:hover{padding-left:24px;color:#695845}
.cn-row:hover .cn-arr{translate:10px 0}
.cn-float{position:fixed;left:0;top:0;z-index:5;width:clamp(220px,18vw,340px);aspect-ratio:4/5;object-fit:cover;pointer-events:none;opacity:0;scale:.9;transition:opacity .35s ease,scale .45s var(--ease);will-change:transform}
.cn-float.on{opacity:1;scale:1}
/* how it works: the line draws as you scroll, circles light up in turn */
.cn-steps::before{transform-origin:0 50%;transform:scaleX(var(--p,0));border-top-style:solid!important;border-top-color:#1D1616!important}
.cn-steps::after{content:"";position:absolute;left:20px;right:var(--lineR,20px);top:20px;border-top:1px dashed #8FB8D2;z-index:-1}
.cn-step__n{background:#fff;color:#1D1616;box-shadow:inset 0 0 0 1px #1D1616;transition:background .4s,color .4s}
.cn-step.on .cn-step__n{background:#1D1616;color:#fff}
/* audiences: sticky side with number + photo, content on the right */
.cn-aud{display:grid;grid-template-columns:5fr 7fr;gap:clamp(40px,5vw,120px);align-items:start}
.cn-aud__stick{position:sticky;top:110px}
.cn-aud__n{margin:0;font:400 clamp(64px,7vw,140px)/.85 var(--serif);color:#8FB8D2}
.cn--dark .cn-aud__n{color:#B0D3EB}
.cn-aud__t{margin:16px 0 0;font:400 clamp(36px,3.4vw,64px)/1 var(--serif);text-transform:uppercase;letter-spacing:-.01em}
.cn-aud .cn-sub{margin:16px 0 0;text-align:left}
.cn-aud__img{margin-top:clamp(28px,2.6vw,48px);aspect-ratio:4/3;overflow:hidden}
.cn-aud__img img{width:100%;height:100%;object-fit:cover;scale:1.06;transition:scale 2.4s cubic-bezier(.25,.1,.25,1)}
.cn-aud__img.in img{scale:1}
.cn-aud__main{padding-top:clamp(8px,1vw,20px)}
.cn-ba{display:grid;grid-template-columns:1fr auto 1fr;gap:clamp(20px,2vw,40px);align-items:start}
.cn-ba .cn-arr{width:48px;margin-top:44px;color:#8FB8D2}
.cn-ba__col .cn-list{margin-top:20px}
.cn-ba__col:first-child .cn-list li{opacity:.7}
.cn-ba__col--after .cn-k{color:#1D1616}
.cn--dark .cn-ba__col--after .cn-k{color:#fff}
.cn-quote{margin:clamp(48px,4.2vw,80px) 0 0;padding-top:clamp(28px,2.6vw,48px);border-top:1px solid var(--line);font:400 clamp(28px,2.4vw,46px)/1.15 var(--serif);text-wrap:balance}
.cn--dark .cn-quote{border-color:rgba(255,255,255,.2)}
.cn-quote::before{content:"“";color:#8FB8D2}
.cn-quote::after{content:"”";color:#8FB8D2}
.cn-formats{margin-top:clamp(40px,3.6vw,64px)}
.cn-formats ul{margin:16px 0 0;padding:0;list-style:none;border-top:1px solid var(--line)}
.cn-formats li{display:grid;grid-template-columns:minmax(180px,.8fr) 1fr;gap:24px;padding:18px 0;border-bottom:1px solid var(--line);font:400 16px/1.5 var(--sans)}
.cn-formats li b{font-weight:600;text-transform:uppercase;letter-spacing:.02em}
.cn-formats li span{opacity:.75}
.cn-aud .cn-cta{justify-content:flex-start}
/* designers */
.cn-sessions{margin:clamp(40px,3.6vw,64px) 0 0;padding:0;list-style:none;border-top:1px solid rgba(255,255,255,.2)}
.cn-sessions li{display:grid;grid-template-columns:110px 1fr;gap:6px 24px;padding:22px 0;border-bottom:1px solid rgba(255,255,255,.2)}
.cn-sessions .cn-ses__k{grid-row:span 2;font:500 16px/1.3 var(--sans);color:#B0D3EB}
.cn-sessions b{font:400 clamp(24px,1.9vw,34px)/1.1 var(--serif);text-transform:uppercase}
.cn-sessions li>span:last-child{font:400 16px/1.5 var(--sans);opacity:.8}
.cn-pack{display:flex;justify-content:space-between;align-items:center;gap:24px;flex-wrap:wrap;margin-top:clamp(32px,3vw,56px)}
.cn-pack b{display:block;font:400 clamp(56px,4.6vw,88px)/1 var(--serif)}
.cn-pack span{font:400 16px/1.5 var(--sans);opacity:.8}
.cn-pack .btn{width:auto;min-width:340px}
/* pricing as a menu card */
.cn-menu{max-width:1100px;margin:clamp(40px,4.2vw,80px) auto 0;padding:0;list-style:none;border-top:1px solid var(--ink)}
.cn-menu li{display:grid;grid-template-columns:auto 1fr auto;grid-template-areas:"t dots p" "d d d";gap:6px 16px;align-items:baseline;padding:22px 0;border-bottom:1px solid var(--line)}
.cn-menu__t{grid-area:t;font:400 clamp(24px,1.9vw,36px)/1.1 var(--serif);text-transform:uppercase}
.cn-menu__dots{grid-area:dots;border-bottom:1px dotted rgba(29,22,22,.35);transform:translateY(-6px)}
.cn-menu__p{grid-area:p;font:600 clamp(16px,1.15vw,22px)/1 var(--sans);white-space:nowrap}
.cn-menu__d{grid-area:d;font:400 16px/1.5 var(--sans);opacity:.7}
.cn-menu li:first-child .cn-menu__p{color:#5B8DB8}
.cn-where{display:flex;flex-wrap:wrap;justify-content:center;gap:10px 32px;max-width:1100px;margin:32px auto 0;padding:0;list-style:none;font:400 16px/1.5 var(--sans)}
.cn-menu__note{max-width:1100px;margin:20px auto 0;text-align:center;font:400 16px/1.5 var(--sans);opacity:.6}
/* trust line inside the request card; sticky bar on phones */
.cta__head p.cn-reply{margin-top:4px!important}
.cn-cv{width:100%!important;max-width:420px;justify-self:start}
.cn-reply{margin:4px 0 0;font:500 14px/1.4 var(--sans);letter-spacing:.02em;color:#5B8DB8;text-align:center}
.cn-bar{display:none}
@media (max-width:900px){
  .cn-hero2{grid-template-columns:minmax(0,1fr);min-height:0}
  .cn-hero2__txt,.cn-aud__main,.cn-aud__side{min-width:0}
  .cn .btn{white-space:normal;height:auto;min-height:56px;padding-top:14px;padding-bottom:14px;text-align:left}
  .cn .btn .roll{line-height:1.3}
  .cn-trust li+li::before{display:none}
  .cn-hero2__img{order:-1;height:62svh;min-height:360px}
  .cn-hero2__txt{padding:32px 16px 56px;gap:18px}
  .cn-hero2__h{font-size:clamp(30px,9.6vw,56px)}
  .cn-hero2__sign{width:min(200px,52vw);margin:-.8em 0 -.4em 30%}
  .cn-hero2__act .btn{min-width:0;width:100%}
  .cn-trust{gap:6px 24px}
  .cn-row{grid-template-columns:36px 1fr auto;gap:12px}
  .cn-row__t{font-size:clamp(22px,6.4vw,32px)}
  .cn-row__go .cn-arr{width:28px}
  .cn-float{display:none}
  .cn-aud{grid-template-columns:1fr;gap:32px}
  .cn-aud__stick{position:static}
  .cn-aud__n{font-size:64px}
  .cn-ba{grid-template-columns:1fr;gap:28px}
  .cn-ba .cn-arr{margin:0;rotate:90deg;width:36px}
  .cn-formats li{grid-template-columns:1fr;gap:4px}
  .cn-sessions li{grid-template-columns:1fr}
  .cn-sessions .cn-ses__k{grid-row:auto}
  .cn-pack .btn{min-width:0;width:100%}
  .cn-menu li{grid-template-columns:minmax(0,1fr) auto;grid-template-areas:"t p" "d d"}
  .cn-menu__t{font-size:clamp(20px,6vw,26px)}
  .cn-menu__dots{display:none}
  .cn-where{flex-direction:column;align-items:center;gap:6px}
  .cn-bar{display:grid;grid-template-columns:1fr auto;gap:8px;position:fixed;left:12px;right:12px;bottom:12px;z-index:70;transform:translateY(140%);transition:transform .5s var(--ease)}
  .cn-bar.on{transform:none}
  .cn-bar a{display:flex;text-align:center;line-height:1.2;align-items:center;justify-content:center;height:52px;padding:0 18px;font:600 14px/1 var(--sans);text-transform:uppercase;letter-spacing:.02em;text-decoration:none}
  .cn-bar__go{background:#1D1616;color:#fff}
  .cn-bar__wa{background:#fff;color:#1D1616;box-shadow:0 6px 24px rgba(29,22,22,.18)}
  body:has(.cn-bar.on) .totop{bottom:76px!important}
}
</style>
'''

V2_JS = '''<script>
/* v2: hero letters, cursor photo on the rows, step line drawn by scroll, sticky phone bar */
(()=>{const h=document.querySelector('.cn-hero2__h');if(h){let i=0;h.innerHTML=h.innerHTML.split(/<br\\s*\\/?>/i).map(l=>l.trim().split(' ').map(w=>'<span style="white-space:nowrap">'+[...w].map(c=>`<span class="ch" style="--i:${i++}">${c}</span>`).join('')+'</span>').join(' ')).join('<br>')}
  const fl=document.querySelector('.cn-float');let tx=0,ty=0,cx=0,cy=0,raf=0;
  const loop=()=>{cx+=(tx-cx)*.14;cy+=(ty-cy)*.14;fl.style.transform=`translate(${cx}px,${cy}px) translate(-50%,-55%)`;raf=requestAnimationFrame(loop)};
  document.querySelectorAll('.cn-row').forEach(r=>{r.addEventListener('mouseenter',e=>{fl.src=r.dataset.img;fl.classList.add('on');tx=cx=e.clientX;ty=cy=e.clientY;if(!raf)raf=requestAnimationFrame(loop)});
    r.addEventListener('mousemove',e=>{tx=e.clientX;ty=e.clientY});r.addEventListener('mouseleave',()=>{fl.classList.remove('on')})});
  const st=document.querySelector('.cn-steps'),steps=[...document.querySelectorAll('.cn-step')],bar=document.querySelector('.cn-bar'),inv=document.getElementById('investors'),req=document.getElementById('request');
  const onS=()=>{if(st){const r=st.getBoundingClientRect(),p=Math.min(1,Math.max(0,(innerHeight*.75-r.top)/(r.height+innerHeight*.25)));st.style.setProperty('--p',p.toFixed(3));
      const c=st.querySelectorAll('.cn-step__n'),L=r.width-parseFloat(getComputedStyle(st).getPropertyValue('--lineR')||20)-20;steps.forEach((s,k)=>{const x=c[k].getBoundingClientRect().left-r.left;s.classList.toggle('on',p*L+30>=x)})}
    if(bar&&inv&&req){const a=inv.getBoundingClientRect().top<innerHeight,b=req.getBoundingClientRect().top<innerHeight*.6;bar.classList.toggle('on',a&&!b)}};
  addEventListener('scroll',()=>requestAnimationFrame(onS),{passive:true});addEventListener('resize',onS);onS()})();
</script>'''

def build(L, src, out):
    t = T[L]
    s = (ROOT / src).read_text(encoding='utf-8')
    hdr = re.search(r'<header class="header">.*?</header>', s, re.S).group(0)
    start = s.index('<section class="hero" id="top">')
    end = s.index('<section class="cta cta2" id="request">')
    mid = s[start:end]
    about = re.search(r'<section class="abx" id="about">.*?</section>', mid, re.S).group(0)
    tst = re.search(r'<section class="tst" id="testimonials">.*?</section>', mid, re.S).group(0)
    about_src = about
    certs_m = re.search(r'<div class="certs" id="certs".*?</figure>\s*</div>\s*</div>', mid, re.S)
    if certs_m:   # the certificates viewer belongs to About; keep it outside the hidden stub
        mid = mid.replace(certs_m.group(0), '')
        about = about + '\n' + certs_m.group(0)
    about = re.sub(r'<a class="lnk abx__cv rv"([^>]*)>([^<]*?)\s*<i></i></a>', r'<a class="btn btn--ink abx__cv cn-cv rv"\1>\2 <span class="plus"></span></a>', about)
    stub = mid.replace(about_src, '').replace(tst, '').replace('id="top"', 'id="top-main"')
    stub = re.sub(r'(<img\b[^>]*?)\ssrc="[^"]*"', r'\1', stub)
    stub = re.sub(r'<header class="header">.*?</header>', '', stub, flags=re.S)
    body = (hdr + '\n<div id="top"></div>\n' + page_html(t, L) + f'<section class="cn cn-me" aria-hidden="true"><img src="assets/consult/oksana-sbid.webp" alt="" loading="lazy"></section>\n' + about + '\n' + tst + '\n' + page_html_after(t)
            + '<div class="pf-stub" hidden aria-hidden="true">' + stub + '</div>\n')
    s = s[:start] + body + s[end:]
    # request forms: the consultation wording from the design's closing block
    s = s.replace('Leave your contact details and I’ll get back to you shortly to discuss your project or a consultation.', 'I’ll look into your situation and suggest a solution.')
    # the form heading becomes the offer itself, so heading and line don't repeat each other
    s = s.replace('<h2>Leave a Request</h2>', '<h2>Book a Free Diagnostic Session</h2>')
    s = re.sub(r'<h2>Залиште заявку</h2>', '<h2>Запишіться на безкоштовну діагностику</h2>', s)
    s = re.sub(r'Залиште свої контакти,[^<]*?консультацію\.', 'Я\u00a0проаналізую Вашу ситуацію і\u00a0запропоную рішення.', s)
    s = re.sub(r'(<img src=")[^"]*(" alt="" id="cta2Img">)', r'\1assets/consult/room.webp\2', s, count=1)
    s = re.sub(r'<script type="module">\s*/\* Project locations:.*?</script>', '', s, count=1, flags=re.S)
    s = re.sub(r'<a href="(ua\.html|index\.html)"( class="lang__on")? lang="uk"', lambda m: f'<a href="consultations-ua.html"{m.group(2) or ""} lang="uk"', s)
    s = re.sub(r'<a href="(ua\.html|index\.html)"( class="lang__on")? lang="en"', lambda m: f'<a href="consultations.html"{m.group(2) or ""} lang="en"', s)
    keep = {'#top', '#request', '#contacts', '#about', '#testimonials', '#investors', '#business', '#homeowners', '#designers'}
    s = re.sub(r'href="(#[a-z][\w-]*)"', lambda m: m.group(0) if m.group(1) in keep else f'href="{t["home"]}{m.group(1)}"', s)
    s = s.replace('<body class="preloading">', '<body>', 1)
    s = s.replace("if(reduce){finish();writeTitle();return}", "if(reduce||window.__noPre){if(!window.__noPre)finish();writeTitle();return}", 1)
    s = s.replace('<div class="pre" id="pre"', '<script>window.__noPre=true;window.__toTopFrom="investors"</script>\n<div class="pre" id="pre" style="display:none"', 1)
    s = s.replace('</body>', """<script>
(()=>{const pre=document.getElementById('pre');if(!pre)return;
  const t=setTimeout(()=>{if(document.readyState==='complete')return;const a=pre.querySelector('.pre__art');if(a)a.removeAttribute('mask');pre.style.display=''},700);
  const done=()=>{clearTimeout(t);if(pre.style.display==='none'){pre.remove();return}pre.animate([{opacity:1},{opacity:0}],{duration:500,easing:'ease',fill:'forwards'}).onfinish=()=>pre.remove()};
  document.readyState==='complete'?done():addEventListener('load',done)})();
/* on this page the request forms start with «Consultation» picked */
document.querySelectorAll('.cta__chips input[value="Consultation"]').forEach(i=>{i.checked=true;i.dispatchEvent(new Event('change',{bubbles:true}))});
/* How it works: the dashed line stops at the centre of the last circle */
(()=>{const st=document.querySelector('.cn-steps');if(!st)return;const fit=()=>{const c=st.querySelectorAll('.cn-step__n'),r=st.getBoundingClientRect(),l=c[c.length-1].getBoundingClientRect();st.style.setProperty('--lineR',(r.right-(l.left+l.width/2))+'px')};addEventListener('resize',fit);addEventListener('load',fit);fit()})();
/* FAQ: one answer open at a time */
(()=>{const items=[...document.querySelectorAll('.cn-faq__i')],D=280,E='cubic-bezier(.25,.1,.25,1)';
  const close=d=>{const p=d.querySelector('p'),h=p.offsetHeight;p.animate([{height:h+'px',opacity:1},{height:'0px',opacity:0}],{duration:D,easing:E,fill:'forwards'});setTimeout(()=>{d.open=false;p.getAnimations().forEach(x=>x.cancel())},D)};
  const open=d=>{d.open=true;const p=d.querySelector('p'),h=p.offsetHeight;p.animate([{height:'0px',opacity:0},{height:h+'px',opacity:1}],{duration:D,easing:E})};
  items.forEach(d=>d.querySelector('summary').addEventListener('click',e=>{e.preventDefault();if(d.open){close(d)}else{items.forEach(o=>{if(o!==d&&o.open)close(o)});open(d)}}))})();
/* anything already scrolled past is shown (safety for the shared reveal) */
addEventListener('scroll',()=>document.querySelectorAll('.cn .rv:not(.in)').forEach(el=>{if(el.getBoundingClientRect().top<innerHeight*.94)el.classList.add('in')}),{passive:true});
</script>
</body>""", 1)
    s = re.sub(r'<title>.*?</title>', f'<title>{t["title"]}</title>', s, count=1, flags=re.S)
    s = s.replace('</head>', CSS + '</head>', 1)
    wa = (re.search(r'https://wa\.me/\d+', s) or [None])[0] or '#contacts'
    s = s.replace('</body>', f'<div class="cn-bar"><a class="cn-bar__go" href="#request">{X[L]["cta"]}</a><a class="cn-bar__wa" href="{wa}" target="_blank" rel="noopener">WhatsApp</a></div>\n' + V2_JS + '\n</body>', 1)
    s = re.sub(r'(<section class="cta cta2" id="request">.*?<div class="cta__head">\s*<h2>.*?</h2>\s*<p>.*?</p>)', lambda m: m.group(1) + f'<p class="cn-reply">{X[L]["reply"]}</p>', s, count=1, flags=re.S)
    (ROOT / out).write_text(s, encoding='utf-8')
    print(out, 'written')


build('en', 'index.html', 'consultations.html')
build('ua', 'ua.html', 'consultations-ua.html')
