#!/usr/bin/env python3
"""Builds ua.html (Ukrainian) from index.html (English).

index.html stays the single source: after any change to the site run
    python3 tools/build_ua.py
and ua.html is regenerated. Every pair below is replaced in its exact context
(">text<", "'text'", attribute="text"...) so code, class names and map lookups
are never touched. The script stops with an error if a phrase is not found —
that means the English text changed and its translation needs updating here.
"""
import pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
src = (ROOT / 'index.html').read_text(encoding='utf-8')

# (english snippet, ukrainian snippet, how many times it must appear: 0 = at least once)
T = [
 # ---------- document ----------
 ('<html lang="en">', '<html lang="uk">', 1),
 ('<title>Oksana Panteleyko — Interior Architect</title>', '<title>Оксана Пантелейко — архітектор інтер’єрів</title>', 1),

 # ---------- language switch ----------
 ('<a href="ua.html" class="lang__on" lang="uk">UA</a><i></i><a href="index.html" lang="en" aria-current="true">EN</a>',
  '<a href="ua.html" lang="uk" aria-current="true">UA</a><i></i><a href="index.html" class="lang__on" lang="en">EN</a>', 0),
 ('aria-label="Language"', 'aria-label="Мова"', 0),

 # ---------- header / menu ----------
 ('>Based in Nice, France<', '>Ніцца, Франція<', 1),
 ('<b>Menu</b><b>Close</b>', '<b>Меню</b><b>Закрити</b>', 1),
 ('aria-label="Menu"', 'aria-label="Меню"', 0),
 ("'Close menu'", "'Закрити меню'", 0),
 ("'Menu'", "'Меню'", 0),
 ('>Home<', '>Головна<', 0),
 ('>Portfolio<', '>Портфоліо<', 0),
 ('>Services<', '>Послуги<', 0),
 ('>About me<', '>Про мене<', 0),
 ('>Consultation<', '>Консультація<', 0),
 ('>Awards<', '>Нагороди<', 0),
 ('>Testimonials<', '>Відгуки<', 0),
 ('>Contact me<', '>Контакти<', 0),
 ('<span>Phone</span>', '<span>Телефон</span>', 1),
 ('<span>Gmail</span>', '<span>Пошта</span>', 1),
 ('<span>Address</span>', '<span>Адреса</span>', 1),
 ('<b>Promenade des Anglais, Nice</b>', '<b>Promenade des Anglais, Ніцца</b>', 1),
 ('alt="Oksana Panteleyko at SBID Design Awards 2025"', 'alt="Оксана Пантелейко на SBID Design Awards 2025"', 1),

 # ---------- hero ----------
 ('alt="Oksana Panteleyko on a terrace in Nice"', 'alt="Оксана Пантелейко на терасі в Ніцці"', 1),
 ('<h1 class="hero__name" data-split>Oksana Panteleyko</h1>', '<h1 class="hero__name" data-split>Оксана Пантелейко</h1>', 1),
 ('<span>Strategist</span><span>•</span><span>Consultant</span>', '<span>Стратег</span><span>•</span><span>Консультант</span>', 1),
 ('<span>Spaces people love to be in —</span> <span>designed with care, planned to budget,</span> <span>and checked for risks before you invest.</span>',
  '<span>Простори, у яких хочеться бути, —</span> <span>створені з турботою, сплановані під бюджет</span> <span>і перевірені на ризики ще до інвестиції.</span>', 1),
 ('Discuss collaboration <span', 'Почати співпрацю <span', 1),
 ('View projects <span', 'Переглянути проєкти <span', 0),

 # ---------- about ----------
 ('<h2 class="abx__label rv">About me</h2>', '<h2 class="abx__label rv">Про мене</h2>', 1),
 ('For over 18 years I’ve been creating spaces where people feel at ease — and want to come back to. Each project starts with your main goal, not the decor, and is built to hold its value for years. I guide it from the first idea to the finished space.',
  'Понад 18 років я створюю простори, де людям легко й затишно — і куди хочеться повертатися. Кожен проєкт починається з Вашої головної мети, а не з декору, і створюється так, щоб зберігати цінність роками. Я веду його від першої ідеї до готового простору.', 1),
 ('<p>Years of<br class="mbr"> experience</p>', '<p>Років<br class="mbr"> досвіду</p>', 1),
 ('<p>SBID finalist<br class="mbr"> projects</p>', '<p>Проєкти<br class="mbr"> у фіналі SBID</p>', 1),
 ('<p>Countries with<br class="mbr"> projects</p>', '<p>Країн<br class="mbr"> із проєктами</p>', 1),
 ('<p>Completed<br class="mbr"> projects</p>', '<p>Завершених<br class="mbr"> проєктів</p>', 1),
 ('<p>SBID Accredited Design <br>Professional, London</p>', '<p>Акредитований спеціаліст <br>SBID, Лондон</p>', 1),
 ('<p>Finalist of the SBID London <br>Awards 2022 &amp; 2025.</p>', '<p>Фіналіст SBID London <br>Awards 2022 і 2025.</p>', 1),
 ('<p>Milano Business School — <br>HoReCa Segment.</p>', '<p>Milano Business School — <br>сегмент HoReCa.</p>', 1),
 ('Download CV <i></i>', 'Завантажити CV <i></i>', 1),
 ('>Download CV<', '>Завантажити CV<', 1),

 # ---------- projects ----------
 ('<h2>Selected<br>Projects</h2>', '<h2>Вибрані<br>проєкти</h2>', 0),
 ('View all projects <i>', 'Дивитися всі проєкти <i>', 0),
 ('Explore project <i>', 'Дивитися проєкт <i>', 0),
 ('<h3>Aparthotel “Alberti”</h3>', '<h3>Апартготель «Alberti»</h3>', 1),
 ('alt="Aparthotel “Alberti”"', 'alt="Апартготель «Alberti»"', 1),
 ('<h3>Cafe “Avec toi”</h3>', '<h3>Кафе «Avec toi»</h3>', 1),
 ('alt="Cafe “Avec toi”"', 'alt="Кафе «Avec toi»"', 1),
 ('<h3>Apartment “Azur Cap d’Ail”</h3>', '<h3>Апартаменти «Azur Cap d’Ail»</h3>', 1),
 ('alt="Apartment “Azur Cap d’Ail”"', 'alt="Апартаменти «Azur Cap d’Ail»"', 1),
 ('alt="">Nice, France<', 'alt="">Ніцца, Франція<', 0),
 ('Each apartment is designed in a unique color palette and carries its own philosophy. Every space invites you to experience a different emotion.',
  'Кожні апартаменти мають власну колірну гаму й філософію. Кожен простір дарує інші емоції.', 0),

 # ---------- who I work with ----------
 ('<h2 class="h2 rv">Who I work with</h2>', '<h2 class="h2 rv">З ким я працюю</h2>', 1),
 ('<h4>The challenge</h4>', '<h4>Ваш запит</h4>', 1),
 ('<h4>What you’ll get</h4>', '<h4>Що Ви отримаєте</h4>', 1),
 ("${c.cta||'Discuss my project'}", "${c.cta||'Обговорити проєкт'}", 1),
 ("t:'Property<br>Investors'", "t:'Інвестори<br>в нерухомість'", 1),
 ("t:'Business<br>Owners'", "t:'Власники<br>бізнесу'", 1),
 ("t:'Home<br>Owners'", "t:'Власники<br>житла'", 1),
 ("t:'Interior<br>Designers'", "t:'Дизайнери<br>інтер’єру'", 1),
 ("cta:'Learn more'", "cta:'Дізнатися більше'", 1),
 ("offer:['Become a client magnet','3 strategy sessions']", "offer:['Магніт для клієнтів','3 стратегічні сесії']", 1),
 ("tags:['Independent Assessment','Second Opinion','Risk Check','Design Audit','Project Review','Layout Review','Renovation Strategy']",
  "tags:['Незалежна оцінка','Друга думка','Аналіз ризиків','Дизайн-аудит','Рев’ю проєкту','Аналіз планування','Стратегія ремонту']", 1),
 ("[['hotel','Hospitality & Hotels'],['lotus','Wellness & Beauty'],['health','Healthcare Spaces'],['restaurant','Restaurants & Cafés']]",
  "[['hotel','Готелі'],['lotus','Б’юті & SPA'],['health','Медичні простори'],['restaurant','Ресторани й кафе']]", 1),
 ("tags:['Brand Space','Customer Journey','Zoning','Functionality','Renovation Plan','Budget Control']",
  "tags:['Простір бренду','Шлях клієнта','Зонування','Функціональність','План ремонту','Контроль бюджету']", 1),
 ("[['villa','Villas'],['apartment','Apartments'],['residence','Residences'],['penthouse','Penthouses']]",
  "[['villa','Вілла'],['apartment','Апартаменти'],['residence','Резиденція'],['penthouse','Пентхаус']]", 1),
 ("tags:['Personal Concept','Smart Layout','Calm Atmosphere','Natural Materials','Lighting Scenarios','Custom Furniture','Clever Storage','Budget Control']",
  "tags:['Персональна концепція','Продумане планування','Спокійна атмосфера','Натуральні матеріали','Сценарії освітлення','Меблі на замовлення','Розумне зберігання','Контроль бюджету']", 1),
 ("tags:['Portfolio & Resume','Social Media','Finding Clients']", "tags:['Портфоліо й резюме','Соцмережі','Пошук клієнтів']", 1),
 ("ch:'You’re about to buy a property — or already own one — but you’re not sure it will pay off, or which business would work best in it.'",
  "ch:'Ви плануєте купити нерухомість або вже маєте її, але не впевнені, чи вона окупиться і який бізнес найкраще в ній запрацює.'", 1),
 ("get:'I’ll give you an independent assessment of the property — its real potential, financial risks and payback — suggest the business that will work best there, from rentals to a café or a salon, and show you what to change to raise its value without unnecessary costs.'",
  "get:'Я дам незалежну оцінку об’єкта — його потенціалу, фінансових ризиків і окупності, — підкажу, який бізнес тут запрацює найкраще, і покажу, що змінити, щоб підвищити вартість без зайвих витрат.'", 1),
 ("ch:'Your space no longer reflects your business — or you’re opening something new and don’t know how to turn your brand into a space clients remember.'",
  "ch:'Ваш простір уже не відповідає рівню бізнесу — або Ви відкриваєте щось нове й не знаєте, як перетворити бренд на простір, який клієнти запам’ятають.'", 1),
 ("get:'I’ll design a space that sets you apart from competitors — where clients feel comfortable, stay longer and come back again.'",
  "get:'Я створю простір, який вирізнить Вас серед конкурентів, — де клієнтам комфортно, вони затримуються довше й повертаються знову.'", 1),
 ("ch:'You’re building a new home or refreshing the one you have, and you want it to feel truly yours — but don’t know where to start, or how to handle all the contractors along the way.'",
  "ch:'Ви будуєте новий дім або оновлюєте наявний і хочете, щоб він був по-справжньому Вашим, — але не знаєте, з чого почати і як упоратися з підрядниками.'", 1),
 ("get:'I’ll create a home made just for you — from a first concept to full support through the renovation, whatever you need — one you’ll love coming back to.'",
  "get:'Від концепції до повного супроводу ремонту я створю дім саме для Вас — дім, до якого хочеться повертатися.'", 1),
 ("ch:'You’re a talented designer, but clients come irregularly — mostly by word of mouth — and it’s hard to raise your fees or start over in a new country.'",
  "ch:'Ви талановитий дизайнер, але клієнти приходять нерегулярно — здебільшого за рекомендаціями, — і Вам складно підняти ціни чи почати заново в новій країні.'", 1),
 ("get:'In three strategy sessions, we’ll turn your portfolio and social media into tools that bring clients, set prices you feel confident about, and build a clear plan to win clients — at home or abroad.'",
  "get:'За три стратегічні сесії ми перетворимо Ваше портфоліо й соцмережі на інструменти, що приводять клієнтів, визначимо ціни, у яких Ви впевнені, і складемо чіткий план, як здобувати клієнтів — удома чи за кордоном.'", 1),

 # ---------- services ----------
 ('<h2 class="svc__title">Services</h2>', '<h2 class="svc__title">Послуги</h2>', 1),
 ("t:'Design Concept<br>& Planning'", "t:'Концепція<br>і планування'", 1),
 ("t:'Interior Design<br>& Renovation'", "t:'Дизайн інтер’єру<br>і реновація'", 1),
 ("t:'Expert<br>Consultations'", "t:'Експертні<br>консультації'", 1),
 ("t:'Brand & Space<br>Transformation'", "t:'Трансформація<br>бренду й простору'", 1),
 ("p:'Get a clear plan before you start. I shape the concept, layout and flow of your space around your goals — so every design and budget decision has a solid direction.'",
  "p:'Отримайте чіткий план ще до старту. Я формую концепцію, планування й логіку простору навколо Ваших цілей — щоб кожне рішення щодо дизайну й бюджету мало впевнений напрям.'", 1),
 ("tags:['Concept Development','Space Planning','Function','Atmosphere','Business Goals','Brand Through Space']",
  "tags:['Розробка концепції','Планування простору','Функція','Атмосфера','Бізнес-цілі','Бренд через простір']", 1),
 ("b:'Start with a concept'", "b:'Почати з концепції'", 1),
 ("p:'I design new interiors and renovate existing ones — homes, hotels, restaurants, salons and more — from concept to completion, with as much support as you need.'",
  "p:'Я проєктую нові інтер’єри й оновлюю наявні — житло, готелі, ресторани, салони та інше — від концепції до реалізації, із супроводом на Ваш запит.'", 1),
 ("tags:['Full Design Project','Technical Drawings','Materials & Finishes','Lighting','Furniture & Decor','Site Supervision']",
  "tags:['Повний дизайн-проєкт','Робочі креслення','Матеріали й оздоблення','Освітлення','Меблі й декор','Авторський нагляд']", 1),
 ("b:'Discuss my project'", "b:'Обговорити проєкт'", 1),
 ("p:'Not sure about a big design or property decision? Let’s talk it through. I’ll give you an honest view of the risks and options, so you can decide with confidence.'",
  "p:'Вагаєтеся щодо важливого рішення в дизайні чи нерухомості? Обговорімо його. Я чесно покажу ризики й можливості, щоб Ви ухвалили рішення впевнено.'", 1),
 ("tags:['Second Opinion','Design Audit','Project Review','Layout Review','Property Investment Check','Renovation Plan']",
  "tags:['Друга думка','Дизайн-аудит','Рев’ю проєкту','Аналіз планування','Перевірка інвестиції','План ремонту']", 1),
 ("b:'Book a consultation'", "b:'Замовити консультацію'", 1),
 ("p:'A full refresh, done turnkey: interior, brand identity and website, created together so your space and brand speak one language.<span class=\"svc__para\"></span>See more branding work at DiDi Brand Atelier.'",
  "p:'Повне оновлення під ключ: інтер’єр, айдентика бренду й сайт, створені разом, щоб простір і бренд говорили однією мовою.<span class=\"svc__para\"></span>Більше робіт із брендингу — на сайті DiDi Brand Atelier.'", 1),
 ("tags:['Interior Renovation','Branding','Website Design']", "tags:['Оновлення інтер’єру','Брендинг','Дизайн сайту']", 1),
 ("b2:'Explore DiDi Brand Atelier'", "b2:'Відкрити DiDi Brand Atelier'", 1),
 ("b:'Transform my brand'", "b:'Оновити мій бренд'", 1),

 # ---------- request forms ----------
 ('<h2>Leave a Request</h2>', '<h2>Залиште заявку</h2>', 0),
 ('<p>Leave your contact details and I’ll get back to you shortly to discuss your project or a consultation.</p>',
  '<p>Залиште свої контакти, і я зв’яжусь із Вами найближчим часом, щоб обговорити Ваш проєкт або консультацію.</p>', 0),
 ('<span>Name</span>', '<span>Ім’я</span>', 0),
 ('<span>Phone number</span>', '<span>Номер телефону</span>', 0),
 ('<legend>What can I help with?</legend>', '<legend>Чим я можу допомогти?</legend>', 0),
 ('<span>Concept</span>', '<span>Концепція</span>', 0),
 ('<span>Design<i class="cta__long"> &amp; Renovation</i></span>', '<span>Дизайн<i class="cta__long"> і реновація</i></span>', 0),
 ('<span>Consultation</span>', '<span>Консультація</span>', 0),
 ('<span>Rebranding</span>', '<span>Ребрендинг</span>', 0),
 ('<span>Not sure yet</span>', '<span>Ще не знаю</span>', 0),
 ('Submit a request <span', 'Надіслати заявку <span', 0),
 ('<h2>Thank you!</h2><p>Your request has been received.<br>I’ll get in touch with you shortly.</p>',
  '<h2>Дякую!</h2><p>Вашу заявку отримано.<br>Я зв’яжусь із Вами найближчим часом.</p>', 0),
 ('Back to home page <span', 'На головну <span', 0),
 ("'Required field'", "'Обов’язкове поле'", 0),
 ("'Enter a valid phone number'", "'Введіть коректний номер'", 0),
 ("'Enter a valid email'", "'Введіть коректний email'", 0),
 ("'Sending…'", "'Надсилаємо…'", 0),
 ("'The form is not connected yet — please write to hello@panteleyko.com.'", "'Форма ще не підключена — напишіть, будь ласка, на hello@panteleyko.com.'", 0),
 ("'Something went wrong — please try again or write to hello@panteleyko.com.'", "'Щось пішло не так — спробуйте ще раз або напишіть на hello@panteleyko.com.'", 0),

 # ---------- awards ----------
 ('aria-label="Awards and credentials"', 'aria-label="Нагороди й дипломи"', 1),
 ("s:'ApartHotel \"Alberti\"'", "s:'Апартготель «Alberti»'", 1),
 ("s:'Beauty Salon \"So. Shell\"'", "s:'Б’юті-салон «So. Shell»'", 1),
 ("s:'Beauty Salon \"SPA & Beauty\"'", "s:'Б’юті-салон «SPA & Beauty»'", 1),
 ("s:'Residence \"French House\"'", "s:'Резиденція «French House»'", 1),
 ("t:'Master of Architecture'", "t:'Магістр архітектури'", 1),
 ("s:'National University O.M. Beketov|Kharkiv, Ukraine'", "s:'ХНУМГ ім. О.М. Бекетова|Харків, Україна'", 1),
 ("t:'SBID Accredited Designer'", "t:'Акредитований дизайнер SBID'", 1),
 ("s:'The Society of British & International^Interior Design|London, UK'", "s:'The Society of British & International^Interior Design|Лондон, Велика Британія'", 1),
 ("s:'HoReCa · Project Design & Marketing|Milan, Italy'", "s:'HoReCa · дизайн і маркетинг|Мілан, Італія'", 1),

 # ---------- locations ----------
 ('<h2 class="loc__h">Project Locations</h2>', '<h2 class="loc__h">Локації проєктів</h2>', 1),
 ("n:\"Côte d'Azur\"", "n:'Лазурний берег'", 1),
 ("n:'Monaco'", "n:'Монако'", 1),
 ("n:'USA'", "n:'США'", 1),
 ("n:'UK'", "n:'Велика Британія'", 1),
 ("n:'Germany'", "n:'Німеччина'", 1),
 ("n:'Italy'", "n:'Італія'", 1),
 ("n:'Ukraine'", "n:'Україна'", 1),
 ("n:'Georgia'", "n:'Грузія'", 1),
 ("n:'Poland'", "n:'Польща'", 1),
 ("n:'Czechia'", "n:'Чехія'", 1),

 # ---------- approach ----------
 ("['Strategy first','I look at the full picture — how the space will be used, by whom and why — before choosing a single material.']",
  "['Спершу стратегія','Я бачу повну картину — як, ким і навіщо використовуватиметься простір — ще до вибору першого матеріалу.']", 1),
 ("['Design that works','Beautiful is only half the job. Every space I create is practical, easy to live or work in, and worth the investment.']",
  "['Дизайн, що працює','Красиво — це лише половина справи. Кожен мій простір практичний, зручний для життя чи роботи й вартий інвестицій.']", 1),
 ("['International experience','Projects in 10+ countries taught me to adapt to different markets, building rules and teams.']",
  "['Міжнародний досвід','Проєкти у 10+ країнах навчили мене адаптуватися до різних ринків, будівельних норм і команд.']", 1),
 ("['From concept to reality','I know construction, contractors, budgets and timelines, so ideas turn into real, finished spaces.']",
  "['Від концепції до реалізації','Я знаю будівництво, підрядників, бюджети й терміни, тож ідеї стають справжніми, завершеними просторами.']", 1),
 ("['Attention to detail','I care about materials, proportions and light — everything that shapes how a space feels.']",
  "['Увага до деталей','Мені важливі матеріали, пропорції та світло — усе, що визначає відчуття простору.']", 1),
 ("['Calm communication','My background in psychology helps me keep projects calm and clear, even when things get complicated.']",
  "['Спокійна комунікація','Психологічна освіта допомагає мені вести проєкти спокійно й зрозуміло, навіть коли все складно.']", 1),

 # ---------- testimonials (placeholders) ----------
 ('<span class="lockup__serif">My approach</span>', '<span class="lockup__serif">Мій підхід</span>', 1),
 ('Interior concept, space planning, FF&amp;E, renovation supervision and full branding. SBID&nbsp;Awards&nbsp;2025&nbsp;Finalist (Hotel&nbsp;Bedroom&nbsp;&amp;&nbsp;Suites&nbsp;Design).', 'Концепція інтер’єру, планування, комплектація, супровід реновації, повний брендинг; фіналіст SBID&nbsp;Awards&nbsp;2025 (Hotel&nbsp;Bedroom&nbsp;&amp;&nbsp;Suites&nbsp;Design).', 1),
 ('<h2 class="tst__label">Testimonials</h2>', '<h2 class="tst__label">Відгуки</h2>', 1),
 ('<p class="tst__prev">What my clients say</p>', '<p class="tst__prev">Що кажуть клієнти</p>', 1),
 ("['Owner,\\nBeauty Salon “So. Shell”','Oksana understood our brand from the very first meeting. She asked about our clients, our daily routine and the mood we wanted people to leave with — and then turned all of it into a space. The salon now feels exactly like us, and our clients notice it every single day.']",
  "['Власниця,\\nБ’юті-салон «So. Shell»','Оксана зрозуміла наш бренд з першої зустрічі. Вона розпитала про клієнтів, наш щоденний ритм і настрій, з яким люди мають від нас іти, — і перетворила все це на простір. Тепер салон відчувається саме нашим, і клієнти помічають це щодня.']", 1),
 ("['CEO,\\nAparthotel “Alberti”','We needed every apartment to have its own character without losing the feeling of one building. Oksana gave each room a story and still kept costs and timing under control. Guests now book specific apartments because of the interiors, and our reviews say it all.']",
  "['CEO,\\nАпартготель «Alberti»','Нам потрібно було, щоб кожні апартаменти мали свій характер, але будинок лишався цілісним. Оксана дала кожній кімнаті власну історію й при цьому тримала під контролем бюджет і терміни. Тепер гості бронюють конкретні апартаменти саме через інтер’єри, а відгуки говорять самі за себе.']", 1),
 ("['Private client,\\nResidence “French House”','Building a house is stressful, but she guided us through every decision with calm and clarity. She was honest about what was worth the money and what wasn’t. The result is beautiful, practical and was finished on time — we still can’t believe it.']",
  "['Приватний клієнт,\\nРезиденція «French House»','Будівництво будинку — це стрес, але Оксана спокійно й зрозуміло провела нас через кожне рішення. Вона чесно казала, що варте грошей, а що ні. Результат гарний, практичний і завершений вчасно — ми досі не віримо.']", 1),
 ("['Founder,\\nSPA & Beauty, Kharkiv Palace','We came for an interior and got a whole new identity: logo, style and a space that fits a five-star hotel. Oksana handled designers, suppliers and contractors so we didn’t have to. Our team loves working there, and guests ask who designed it.']",
  "['Засновниця,\\nSPA & Beauty, Kharkiv Palace','Ми прийшли по інтер’єр, а отримали цілісну нову айдентику: логотип, стиль і простір рівня п’ятизіркового готелю. Оксана сама працювала з дизайнерами, постачальниками й підрядниками. Команда любить там працювати, а гості питають, хто це створив.']", 1),
 ("['Investor,\\nCôte d’Azur apartment','Before buying, I asked Oksana to look at the property with me. In one visit she showed me the risks, the real potential and what the renovation would cost. That advice saved me money and helped me choose the right apartment.']",
  "['Інвестор,\\nАпартаменти на Лазурному березі','Перед купівлею я попросив Оксану подивитися об’єкт разом зі мною. За один візит вона показала ризики, реальний потенціал і вартість ремонту. Ця порада зберегла мені гроші й допомогла обрати правильні апартаменти.']", 1),

 # ---------- contacts ----------
 ('<p class="cts__eyebrow">Contacts</p>', '<p class="cts__eyebrow">Контакти</p>', 1),
 ('<p class="cts__lead">Get in touch to discuss your project, ideas <br>or collaboration opportunities.</p>',
  '<p class="cts__lead">Зв’яжіться зі мною, щоб обговорити проєкт,<br> ідеї або можливості співпраці.</p>', 1),
 ('<p class="cts__k">Address</p>', '<p class="cts__k">Адреса</p>', 1),
 ('<span class="nw">06000, Nice, France</span>', '<span class="nw">06000, Ніцца, Франція</span>', 1),
 ('<p class="cts__k">For collaborations</p>', '<p class="cts__k">Для співпраці</p>', 1),
 ('&amp;z=15&amp;hl=en&amp;output=embed', '&amp;z=15&amp;hl=uk&amp;output=embed', 1),
 ('title="Map: Promenade des Anglais, Nice"', 'title="Мапа: Promenade des Anglais, Ніцца"', 1),

 # ---------- footer & misc ----------
 ('aria-label="Panteleyko — back to top"', 'aria-label="Panteleyko — нагору"', 1),
 ('<p class="ftr__name" id="ftrName">Oksana Panteleyko</p>', '<p class="ftr__name" id="ftrName">Оксана Пантелейко</p>', 1),
 ('©2026 Oksana Panteleyko. All rights reserved.', '©2026 Оксана Пантелейко. Усі права захищено.', 1),
 ('<small>Website designed by</small>', '<small>Дизайн сайту</small>', 1),
 ('aria-label="Previous"', 'aria-label="Назад"', 0),
 ('aria-label="Next"', 'aria-label="Далі"', 0),
 ('aria-label="Back to top"', 'aria-label="Нагору"', 0),
 ('aria-label="Globe with project locations"', 'aria-label="Глобус із локаціями проєктів"', 0),
]

out, missing = src, []
# longest (most specific) phrases first, so short generic ones like '>About me<' never pre-empt them
for en, ua, n in sorted(T, key=lambda t: -len(t[0])):
    c = out.count(en)
    if c == 0 or (n and c != n):
        missing.append(f'  found {c}×, expected {n or "≥1"}: {en[:90]}')
        continue
    out = out.replace(en, ua)

# both pages point search engines to each other

# Ukrainian typography: short words (з, і, в, на, до…) never hang at the end of a line — glue them to the next word
import re
SHORT = r'(?:[взуіїйаоя]|та|на|до|за|по|не|що|як|із|зі|чи|ці|це|ми|ви|Ви|від|для|без|під|над|при)'
for _ in range(2):   # twice, so chains like «і з» are glued too
    out = re.sub(r'(?<=[\s>«(])(' + SHORT + r') (?=[^\s<])', '\\1\u00a0', out, flags=re.I)
# a dash never starts a line: glue it to the word before it
out = out.replace(' — ', '\u00a0— ')

if missing:
    print('Translation not applied (English text changed?):\n' + '\n'.join(missing))
    sys.exit(1)
(ROOT / 'ua.html').write_text(out, encoding='utf-8')
print(f'ua.html written ({len(T)} phrases)')
