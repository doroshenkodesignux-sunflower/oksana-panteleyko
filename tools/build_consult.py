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
        g=['An assessment of the property’s potential as a hotel, restaurant, spa, or cafe;', 'A list of hidden risks;', 'A plan: what to change and what to leave alone.'],
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
            l=['interior renovation', 'branding', 'website development'], p2='You get one coherent result where the space, the visual identity and the online presence speak the same language — without coordinating several contractors yourself.'),
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
        g=['Оцінку потенціалу об’єкта як готелю, ресторану, SPA чи кафе;', 'Перелік прихованих ризиків;', 'План: що змінити, а що лишити як є.'],
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
            l=['реновація інтер’єру', 'брендинг', 'розробка сайту'], p2='Ви отримуєте цілісний результат, де простір, візуальна ідентичність і цифрова присутність говорять однією мовою — без потреби самостійно координувати кількох підрядників.'),
       dict(k='Консультування бізнесу', t='Підбір команди та управління', p='Для бізнесу, який відкриває або розвиває готель, ресторан чи інший об’єкт:',
            l=['Підбір спеціалістів у команду', 'Консультації із запуску готелю', 'Як управляти готелем чи рестораном', 'Робота з керуючим об’єкта'], p2='')],
  ext_b='Обговорити співпрацю',
  faq_h='Питання, які<br>запитують найчастіше',
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
    who = ''.join(f'<a class="cn-who rv" style="--d:{i*.08:.2f}s" href="#{a}"><h3>{w}</h3><span class="cn-who__more">{t["see"]}<i>→</i></span></a>'
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
.cn-who__more{display:flex;justify-content:space-between;padding-bottom:10px;border-bottom:1px solid var(--ink);font:500 16px/1 var(--sans)}
.cn-who__more i{font-style:normal;transition:translate .4s var(--ease)}.cn-who:hover .cn-who__more i{translate:6px 0}
/* how */
.cn-steps{display:grid;grid-template-columns:repeat(4,1fr);gap:24px;margin-top:clamp(40px,4.2vw,80px);position:relative}
.cn-steps::before{content:"";position:absolute;left:20px;right:12%;top:20px;border-top:1px dashed #8FB8D2}
.cn-step{position:relative}
.cn-step__n{display:grid;place-items:center;width:40px;height:40px;border-radius:50%;background:#1D1616;color:#fff;font:600 16px/1 var(--sans)}
.cn-step h3{margin:28px 0 12px;font:400 clamp(24px,1.9vw,36px)/1.1 var(--serif);text-transform:uppercase}
.cn-step p{margin:0;max-width:16em;font:400 16px/1.5 var(--sans);opacity:.8}
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
.cn-faq__i{background:#EEF2F5}
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
/* light buttons: the same blue fill from the cursor as the home page's buttons */
.cn .btn--light::before{display:block!important;opacity:1;background:#84B7DB;clip-path:circle(0% at var(--ex,50%) var(--ey,50%));transition:clip-path .7s cubic-bezier(.65,0,.35,1)}
.cn .btn--light:hover::before{clip-path:circle(150% at var(--ex,50%) var(--ey,50%))}
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


def build(L, src, out):
    t = T[L]
    s = (ROOT / src).read_text(encoding='utf-8')
    hdr = re.search(r'<header class="header">.*?</header>', s, re.S).group(0)
    start = s.index('<section class="hero" id="top">')
    end = s.index('<section class="cta cta2" id="request">')
    mid = s[start:end]
    about = re.search(r'<section class="abx" id="about">.*?</section>', mid, re.S).group(0)
    tst = re.search(r'<section class="tst" id="testimonials">.*?</section>', mid, re.S).group(0)
    stub = mid.replace(about, '').replace(tst, '').replace('id="top"', 'id="top-main"')
    stub = re.sub(r'(<img\b[^>]*?)\ssrc="[^"]*"', r'\1', stub)
    stub = re.sub(r'<header class="header">.*?</header>', '', stub, flags=re.S)
    body = (hdr + '\n<div id="top"></div>\n' + page_html(t) + f'<section class="cn cn-me" aria-hidden="true"><img src="assets/consult/oksana-sbid.webp" alt="" loading="lazy"></section>\n' + about + '\n' + tst + '\n' + page_html_after(t)
            + '<div class="pf-stub" hidden aria-hidden="true">' + stub + '</div>\n')
    s = s[:start] + body + s[end:]
    s = re.sub(r'(<img src=")[^"]*(" alt="" id="cta2Img">)', r'\1assets/consult/room.webp\2', s, count=1)
    s = re.sub(r'<script type="module">\s*/\* Project locations:.*?</script>', '', s, count=1, flags=re.S)
    s = re.sub(r'<a href="(ua\.html|index\.html)"( class="lang__on")? lang="uk"', lambda m: f'<a href="consultations-ua.html"{m.group(2) or ""} lang="uk"', s)
    s = re.sub(r'<a href="(ua\.html|index\.html)"( class="lang__on")? lang="en"', lambda m: f'<a href="consultations.html"{m.group(2) or ""} lang="en"', s)
    keep = {'#top', '#request', '#contacts', '#about', '#testimonials', '#investors', '#business', '#homeowners', '#designers'}
    s = re.sub(r'href="(#[a-z][\w-]*)"', lambda m: m.group(0) if m.group(1) in keep else f'href="{t["home"]}{m.group(1)}"', s)
    s = s.replace('<body class="preloading">', '<body>', 1)
    s = s.replace("if(reduce){finish();writeTitle();return}", "if(reduce||window.__noPre){if(!window.__noPre)finish();writeTitle();return}", 1)
    s = s.replace('<div class="pre" id="pre"', '<script>window.__noPre=true</script>\n<div class="pre" id="pre" style="display:none"', 1)
    s = s.replace('</body>', """<script>
(()=>{const pre=document.getElementById('pre');if(!pre)return;
  const t=setTimeout(()=>{if(document.readyState==='complete')return;const a=pre.querySelector('.pre__art');if(a)a.removeAttribute('mask');pre.style.display=''},700);
  const done=()=>{clearTimeout(t);if(pre.style.display==='none'){pre.remove();return}pre.animate([{opacity:1},{opacity:0}],{duration:500,easing:'ease',fill:'forwards'}).onfinish=()=>pre.remove()};
  document.readyState==='complete'?done():addEventListener('load',done)})();
/* on this page the request forms start with «Consultation» picked */
document.querySelectorAll('.cta__chips input[value="Consultation"]').forEach(i=>{i.checked=true;i.dispatchEvent(new Event('change',{bubbles:true}))});
/* FAQ: one answer open at a time */
document.querySelectorAll('.cn-faq__i').forEach(d=>d.addEventListener('toggle',()=>{if(d.open)document.querySelectorAll('.cn-faq__i').forEach(o=>{if(o!==d)o.open=false})}));
/* anything already scrolled past is shown (safety for the shared reveal) */
addEventListener('scroll',()=>document.querySelectorAll('.cn .rv:not(.in)').forEach(el=>{if(el.getBoundingClientRect().top<innerHeight*.94)el.classList.add('in')}),{passive:true});
</script>
</body>""", 1)
    s = re.sub(r'<title>.*?</title>', f'<title>{t["title"]}</title>', s, count=1, flags=re.S)
    s = s.replace('</head>', CSS + '</head>', 1)
    (ROOT / out).write_text(s, encoding='utf-8')
    print(out, 'written')


build('en', 'index.html', 'consultations.html')
build('ua', 'ua.html', 'consultations-ua.html')
