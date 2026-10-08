#!/usr/bin/env python3
"""Збирає стенд concept/concept.html — стиль «Ніжна» у ділі й з чого він складається.

Запуск:  python3 concept/stand.py

Стилі стенду — concept/stand.css, скрипт вбудовує їх у сторінку. Значення беруться
лише з tokens.css: кольори, розміри й шкала — через змінні, таблиця контрасту —
з contrast.py, іконки — токени --icon-*, які пише icons.py. Нова іконка в розмітці
без токена зупиняє збирання.

Дані Плану — з wireframes/plan.html, plan-card.html і microcopy.md (колонка «стало»).
Сторінку руками не правити: зміни — тут або в stand.css, потім перезібрати.
"""
import html
from pathlib import Path

import contrast as CT

HERE = Path(__file__).parent
OUT = HERE / 'concept.html'


USED_ICONS = set()


def ic(name, style, cls='i'):
    # Іконка — порожній span із маскою: форма з токена --icon-<назва> у tokens.css, колір — currentColor
    USED_ICONS.add(name)
    return f'<span class="{cls} ic-{name}" aria-hidden="true"></span>'


def e(t):
    return html.escape(t, quote=False)


UNV = '[не вивірено рецензентом]'

# Дані — wireframes/plan.html, plan-card.html, microcopy.md (колонка «стало»)
ITEMS = [
    dict(k='gyn', layer='base', icon='stethoscope', name='Огляд у гінеколога', state='overdue',
         meta='раз на рік · був до 14 червня 2026', freq='раз на рік', stub=('був до', '14 червня 2026'),
         desc='Розмова раз на рік про те, що змінилось: цикл, контрацепція, скарги. Це не те саме, що скринінг — окремі обстеження призначають за потреби. Це розмова, а не обов’язковий огляд на кріслі — про те, що тебе турбує, можна просто спитати.',
         when='Раз на рік · востаннє 14 червня 2025', cost='Безкоштовно за програмою медичних гарантій',
         basis='Рекомендовано всім жінкам твого віку. Не залежить від твоїх відповідей — це базовий шар.',
         conf='Доказова база: настанова професійної спільноти, не скринінгова рекомендація з рівнем доказовості.',
         src='ACOG, Well-Woman Visit · рівень доказовості не застосовується · переглянуто 2024', unv=UNV,
         acts=[('check-square', 'Позначити пройденим', True), ('calendar-add', 'Запланувати', False)]),
    dict(k='dent', layer='base', icon='smile-circle', name='Огляд у стоматолога', state='done',
         meta='раз на рік · наступний до березня 2027', freq='раз на рік', stub=('наступний до', 'березня 2027'),
         desc='Профілактичний огляд і чистка. Потрібен, навіть коли нічого не болить.',
         when='Раз на рік · пройдено 12 березня 2026', cost='Платно',
         basis='Рекомендовано всім дорослим. Не залежить від твоїх відповідей — це базовий шар.',
         conf='Доказова база: стоматологічні настанови.',
         src='Стоматологічні настанови', unv='[джерело уточнюється · не вивірено рецензентом]',
         acts=[('pen', 'Змінити відмітку', False), ('calendar-add', 'Запланувати', False)]),
    dict(k='bp', layer='risk', icon='heart-pulse', name='Вимірювання тиску', state='none',
         meta='раз на 3–5 років; з 40 — раз на рік', freq='раз на 3–5 років; з 40 — раз на рік', stub=('', '—'),
         desc='Кілька хвилин на прийомі або вдома тонометром. Підвищений тиск роками не дає симптомів.',
         when='Раз на 3–5 років, поки тиск нормальний; з 40 — раз на рік · дата наступного з’явиться після першої відмітки',
         cost='Безкоштовно за програмою медичних гарантій', basis='Через твій вік — 36 років.',
         conf='Рекомендовано всім дорослим, доказів високої якості.',
         src='USPSTF, Hypertension in Adults: Screening · рівень A · переглянуто 2021', unv=UNV,
         acts=[('check-square', 'Позначити пройденим', True), ('calendar-add', 'Запланувати', False)]),
    dict(k='cyto', layer='risk', icon='test-tube', name='Цитологія з ВПЛ-тестом', state='done',
         meta='раз на 5 років · наступна до березня 2028', freq='раз на 5 років', stub=('наступна до', 'березня 2028'),
         desc='Мазок із шийки матки. Шукає зміни клітин до того, як вони стануть проблемою.',
         when='Раз на 5 років · пройдено навесні 2023 — приблизна дата, рахуємо від 1 березня',
         cost='Безкоштовно за програмою медичних гарантій', basis='Через твій вік — 36 років.',
         conf='Рекомендовано всім жінкам 21–65 років, доказів високої якості.',
         src='USPSTF, Cervical Cancer: Screening · рівень A · переглянуто 2018', unv=UNV,
         acts=[('pen', 'Змінити відмітку', False), ('calendar-add', 'Запланувати', False)]),
]
OWN = dict(k='tsh', layer='own', icon='notes', name='ТТГ', state='done',
           meta='твій пункт · раз на рік — так сказала лікарка', freq='твій пункт · раз на рік — так сказала лікарка',
           stub=('пройдено', '20 березня 2026'), mark='Додано до списку · 14 березня 2026',
           when='Раз на рік — так сказала лікарка · пройдено 20 березня 2026',
           acts=[('pen', 'Змінити відмітку', False), ('calendar-add', 'Запланувати', False)])
EXCL = [
    ('Мамографія',
     'Розглянули і не включили у твій чекап: мамографію не рекомендують до 40 років без обтяженої сімейної історії. За твоїми відповідями раку грудей у мами, сестри чи доньки не було.',
     'з 40 років, раз на 2 роки. Якщо рак грудей виявлять у мами, сестри чи доньки — обговори з лікарем, чи варто почати раніше.',
     'USPSTF, Breast Cancer: Screening · рівень B (для 40–74 років) · переглянуто 2024'),
    ('УЗД органів малого таза як скринінг раку яєчників',
     'Розглянули і не включили у твій чекап: жінкам без симптомів і без спадкового ризику скринінг раку яєчників не рекомендують — він частіше призводить до зайвих втручань, ніж знаходить хворобу вчасно.',
     'як скринінг — не з’явиться. Якщо є симптоми або відома мутація BRCA, це вже не чекап, а окрема розмова з лікарем.',
     'USPSTF, Ovarian Cancer: Screening · рівень D — рекомендація проти скринінгу · переглянуто 2018'),
    ('Низькодозова КТ легень',
     'Розглянули і не включили у твій чекап: скринінг раку легень роблять з 50 до 80 років тим, хто курив щонайменше 20 пачко-років і курить досі або кинув менш ніж 15 років тому. Тобі 36, і за твоїми відповідями стаж менший.',
     'найімовірніше, ні — ти кинула, і до 50 мине більше ніж 15 років. Якщо почнеш курити знову, план перерахується.',
     'USPSTF, Lung Cancer: Screening · рівень B · переглянуто 2021'),
]
STATE = {'overdue': ('danger-circle', 'прострочено'), 'none': ('clock-circle', 'не позначено'),
         'scheduled': ('calendar-mark', 'заплановано'), 'done': ('check-circle', 'пройдено')}
STATE_EX = {'overdue': 'раз на рік · був до 14 червня 2026', 'none': 'дата наступного з’явиться після першої відмітки',
            'scheduled': 'раз на рік · 15 жовтня 2026, у твоєму календарі', 'done': 'раз на рік · наступний до березня 2027'}
LAYERS = {'base': ('Базовий шар', 'показано всім · ACOG, стоматологічні настанови'),
          'risk': ('Ризик-орієнтовані скринінги', 'за віком і анамнезом · USPSTF, з рівнем доказовості')}


BADGE = {'gyn': 'pink', 'dent': 'peach', 'bp': 'lilac', 'cyto': 'mint', 'tsh': 'grey'}


def state_mark(v, st, state, compact=False):
    icn, word = STATE[state]
    return f'<span class="stt s-{state}">{ic(icn, st)}<span>{word}</span></span>'


def acts_html(it, st):
    return '<div class="acts">' + ''.join(
        f'<button type="button" class="btn{" pri" if p else ""}">{ic(n, st)}{e(t)}</button>' for n, t, p in it['acts']) + '</div>'


def tags(parts, unv):
    t = ''.join(f'<span class="tag">{e(p)}</span>' for p in parts)
    if unv:
        t += f'<span class="tag unv">{e(unv)}</span>'
    return f'<span class="tags">{t}</span>' if t else ''


def frow(icon, st, label, main, sub='', extra='', tail=''):
    return (f'<li class="fr"><span class="fic">{ic(icon, st)}</span><div class="fb"><span class="fl">{e(label)}</span>'
            f'<span class="fv">{e(main)}</span>{f"<span class=fs>{e(sub)}</span>" if sub else ""}'
            f'{f"<span class=fx2>{e(extra)}</span>" if extra else ""}{tail}</div></li>')


def full_html(it, v, st):
    if it['layer'] == 'own':
        main, _, sub = it['when'].partition(' · ')
        return (f'<div class="full"><p class="mark">{e(it["mark"])}</p>'
                f'<ul class="fx">{frow("calendar", st, "Коли", main, sub)}</ul>{acts_html(it, st)}</div>')
    when_main, _, when_sub = it['when'].partition(' · ')
    b = it['basis']
    i = b.find('. ')
    basis_main, basis_sub = (b[:i + 1], b[i + 2:]) if i > 0 else (b, '')
    src = it['src'].split(' · ')
    unv = it['unv'].strip('[]')
    rows = (frow('calendar', st, 'Коли', when_main, when_sub)
            + frow('wallet-money', st, 'Вартість', it['cost'])
            + frow('user-heart', st, 'Чому в плані', basis_main, basis_sub, it['conf'])
            + frow('document-text', st, 'Джерело', src[0], '', '', tags(src[1:], f'[{unv}]')))
    return f'<div class="full"><p class="desc">{e(it["desc"])}</p><ul class="fx">{rows}</ul>{acts_html(it, st)}</div>'


def summary_html(it, v, st):
    chev = ic('round-alt-arrow-down', st, 'i chev')
    return (f'<span class="badge b-{BADGE[it["k"]]}">{ic(it["icon"], st, "i ex")}</span>'
            f'<span class="what"><h4 class="nm">{e(it["name"])}</h4><span class="meta">{e(it["meta"])}</span>'
            f'{state_mark(v, st, it["state"])}</span>{chev}')


def item_html(it, v, st, open_=False, group=None):
    nm = f' name="{group}"' if group else ''
    op = ' open' if open_ else ''
    own = ' own' if it['layer'] == 'own' else ''
    return (f'<li class="item s-{it["state"]}{own}"><details{nm}{op}><summary>{summary_html(it, v, st)}</summary>'
            f'{full_html(it, v, st)}</details></li>')


def excl_html(v, st):
    arts = ''
    for n, r, c, s in EXCL:
        lead, _, rest = r.partition(': ')
        parts = s.split(' · ')
        arts += (f'<article class="ex-it"><h4>{e(n)}</h4><p class="why"><b>{e(lead)}:</b> {e(rest)}</p>'
                 f'<div class="cond"><span class="fic">{ic("calendar-mark", st)}</span><div class="fb"><span class="fl">З’явиться у твоєму плані</span><p>{e(c[0].upper() + c[1:])}</p></div></div>'
                 f'<p class="srcl">{ic("document-text", st, "i fi")}<span><b>{e(parts[0])}</b>{tags(parts[1:], UNV)}</span></p></article>')
    return (f'<section class="excl"><details><summary><span class="ex-h"><h3>Розглянули і не включили у твій чекап — 3 обстеження</h3>'
            f'<span class="hint">Мамографія, УЗД органів малого таза як скринінг раку яєчників, низькодозова КТ легень. Ми перевірили їх саме для твого випадку.</span></span>'
            f'{ic("round-alt-arrow-down", st, "i chev")}</summary><div class="ex-body">{arts}'
            f'<div class="gate"><p>Лікар призначив те, чого тут немає?</p><button type="button" class="btn">{ic("magnifer", st)}Знайти обстеження</button></div>'
            f'</div></details></section>')


def phone(v, st, label, open_gyn, uid):
    group = None
    by = {'base': [], 'risk': []}
    for it in ITEMS:
        by[it['layer']].append(it)
    secs = ''
    for lk in ('base', 'risk'):
        t, srcs = LAYERS[lk]
        lis = ''.join(item_html(it, v, st, open_=(open_gyn and it['k'] == 'gyn'), group=group) for it in by[lk])
        secs += (f'<section class="layer l-{lk}"><h3 class="lh"><span class="lsrc">{srcs}</span><span class="tab">{t}</span></h3>'
                 f'<ul class="items">{lis}</ul></section>')
    own = (f'<section class="layer l-own"><h3 class="lh"><span class="tab">Твої пункти</span></h3>'
           f'<p class="own-lead">Ми їх не оцінювали: джерела, рівня доказовості й слова «рекомендовано» тут немає. Ми тримаємо їх поруч, щоб усе було в одному місці.</p>'
           f'<ul class="items">{item_html(OWN, v, st, group=group)}</ul></section>')
    filt = ('<div class="filter" role="group" aria-label="Показати пункти за станом">'
            '<button type="button" aria-pressed="true">Усі · 5</button><button type="button" aria-pressed="false">Зараз · 2</button>'
            '<button type="button" aria-pressed="false">Пройдено · 3</button></div>')
    head = (f'<header class="ph"><h3 class="pt">План</h3><p class="pu">Оновлено 23 вересня 2026 · порахований за твоїми відповідями</p>'
            f'{filt}</header>')
    foot = (f'<footer class="disc"><p>Prevently — інформаційно-освітній продукт, а не медичний виріб. Це не діагноз і не призначення. '
            f'Остаточні рішення про обстеження ухвалює лікар разом із тобою.</p><div class="acts">'
            f'<button type="button" class="btn">{ic("download-minimalistic", st)}Завантажити PDF</button>'
            f'<button type="button" class="btn">{ic("history", st)}Пройдене</button></div></footer>')
    CUR = ' class="on" aria-current="page"'
    nav = ''.join(f'<li><a href="#"{CUR if i == 0 else ""}>{ic(n, st)}<span>{t}</span></a></li>'
                  for i, (n, t) in enumerate([('clipboard-list', 'План'), ('notebook-minimalistic', 'Мої відповіді'), ('info-circle', 'Про підхід')]))
    sbar = ('<div class="sbar" aria-hidden="true"><span class="clock">9:41</span><span class="sig">'
            '<svg viewBox="0 0 18 12"><rect x="0" y="8" width="3" height="4" rx="1"/><rect x="5" y="5.5" width="3" height="6.5" rx="1"/><rect x="10" y="3" width="3" height="9" rx="1"/><rect x="15" y="0" width="3" height="12" rx="1"/></svg>'
            '<svg viewBox="0 0 26 12"><rect x="0.5" y="0.5" width="22" height="11" rx="3" fill="none" stroke="currentColor" opacity=".45"/><rect x="2.5" y="2.5" width="16" height="7" rx="1.6"/><rect x="23.5" y="4" width="2" height="4" rx="1" opacity=".45"/></svg>'
            '</span></div>')
    return (f'<div class="device" role="region" aria-label="{label}"><div class="sa">{sbar}<div class="scroll">{head}{secs}'
            f'{excl_html(v, st)}{own}{foot}</div><nav class="tabbar" aria-label="Основна навігація · {label}"><ul>{nav}</ul></nav>'
            f'<span class="home" aria-hidden="true"></span></div></div>')


ST = 'bold-duotone'
TOK = CT.read_tokens()
CSS = (HERE / 'stand.css').read_text(encoding='utf-8')


def hx(token):
    v = TOK[token]
    return v.upper() if v.startswith('#') else v


A1 = '1 · Спокійний, не тривожний'
A2 = '2 · Сканується одним поглядом'
A3 = '3 · Підписаний, не анонімний'
A4 = '4 · Як застосунок, не як сайт'
A5 = '5 · З характером, не лабораторія'
ANCH = 'concept.md#атрибути'

COLORS = [
    ('Основний — рожевий', 'Колір продукту й дій. Ніша «жіноче здоров’я» має вгадуватися з першого погляду — рішення 07.10.', [
        (['--color-primary'], 'Рожевий', 'іконки в картці, знак продукту', A5),
        (['--color-primary-strong'], 'Рожевий для дій', 'основна кнопка, активний фільтр і вкладка', A4),
        (['--color-primary-text'], 'Рожевий для тексту', 'посилання, текст другорядної кнопки', A4),
        (['--color-primary-soft'], 'Рожеве тло', 'наведення на другорядну кнопку', A1),
    ]),
    ('Акцентний — персиковий', 'Живе лише у фоні: градієнт «рожевий і персиковий» замість суцільного рожевого.', [
        (['--color-accent'], 'Персиковий', 'лівий верхній кут градієнта', A1),
        (['--pink-blush'], 'Рожевий градієнта', 'правий верхній кут градієнта', A1),
        (['--color-page'], 'Фон сторінки', 'низ градієнта', A1),
    ]),
    ('Нейтральні', 'Текст на білому, ієрархію тримають вага шрифту, підписи й роздільники — без рожевих підкладок.', [
        (['--color-surface'], 'Білий', 'картки й текстові блоки', A1),
        (['--color-text'], 'Текст', 'назви, головне в рядку', A2),
        (['--color-text-muted'], 'Текст-2', 'пояснення, мета-рядок', A2),
        (['--color-text-label'], 'Підписи', '«Коли», «Вартість», «Чому в плані», «Джерело»', A3),
        (['--color-divider'], 'Роздільник', 'лінії між рядками фактів', A2),
        (['--color-border-dashed'], 'Пунктир', '«твій пункт» і «не вивірено рецензентом»', A3),
    ]),
    ('Значки обстежень', 'Свій пастельний значок у кожного обстеження, як ілюстровані бейджі Airbnb.', [
        (['--badge-pink-bg', '--badge-pink-fg'], 'Рожевий', 'гінеколог', A2),
        (['--badge-peach-bg', '--badge-peach-fg'], 'Персиковий', 'стоматолог', A2),
        (['--badge-lilac-bg', '--badge-lilac-fg'], 'Бузковий', 'тиск', A2),
        (['--badge-mint-bg', '--badge-mint-fg'], 'М’ятний', 'аналізи', A2),
        (['--badge-grey-bg', '--badge-grey-fg'], 'Сірий', 'твій пункт — не наша рекомендація', A3),
    ]),
    ('Кольори станів', 'Колір лише там, де треба діяти, і завжди разом зі словом та іконкою.', [
        (['--color-error', '--color-error-text', '--color-error-bg'], 'Помилка', 'алерт тривожного симптому над планом, помилки', 'безпекова межа з брифу: найсильніший колір системи'),
        (['--color-overdue', '--color-overdue-text', '--color-overdue-bg'], 'Прострочено', 'мітка з тлом — єдине, що «горить» у плані', A1),
        (['--color-success', '--color-success-text', '--color-success-bg'], 'Успіх', 'галочка «пройдено», повідомлення про успіх', A1),
        (['--color-neutral-state', '--color-neutral-state-text'], 'Нейтральний стан', '«не позначено», «заплановано», слово «пройдено»', A1),
    ]),
]

SCALE = ['--pink-50', '--pink-100', '--pink-200', '--pink-300', '--pink-500', '--pink-600', '--pink-700', '--pink-800']

TYPE = [
    ('--text-48', 'Nunito 900', 'Ніжна', 'заголовок стенду'),
    ('--text-34', 'Nunito 800', 'План', 'заголовок екрана'),
    ('--text-28', 'Nunito 900', 'Кольори', 'заголовок розділу'),
    ('--text-20', 'Nunito 700', 'Базовий шар', 'заголовок шару'),
    ('--text-17', 'Nunito 800', 'Огляд у гінеколога', 'назва обстеження'),
    ('--text-15', 'Nunito Sans 400–700', 'Раз на рік', 'основний текст, кнопки, значення фактів'),
    ('--text-14', 'Nunito Sans 400', 'востаннє 14 червня 2025', 'пояснення під головним'),
    ('--text-13', 'Nunito Sans 400–700', 'раз на рік · був до 14 червня 2026', 'мета-рядок, мітка стану'),
    ('--text-12', 'Nunito 700', 'Коли', 'підписи полів, мітки, нижнє меню'),
]
TYPE_FAMILY = {'--text-48': 'display', '--text-34': 'display', '--text-28': 'display', '--text-20': 'display', '--text-17': 'display', '--text-12': 'display'}
TYPE_WEIGHT = {'--text-48': '--weight-black', '--text-34': '--weight-heavy', '--text-28': '--weight-black', '--text-20': '--weight-heavy',
               '--text-17': '--weight-heavy', '--text-15': '--weight-regular', '--text-14': '--weight-regular', '--text-13': '--weight-regular', '--text-12': '--weight-bold'}

ICONS_G = [
    ('Нижнє меню', '', [('clipboard-list', 'План'), ('notebook-minimalistic', 'Мої відповіді'), ('info-circle', 'Про підхід')]),
    ('Обстеження', 'badge', [('stethoscope', 'гінеколог', 'pink'), ('smile-circle', 'стоматолог', 'peach'), ('heart-pulse', 'тиск', 'lilac'), ('test-tube', 'аналізи', 'mint'), ('notes', 'твій пункт', 'grey')]),
    ('Статуси обстеження', 'st', [('danger-circle', 'прострочено', 'overdue'), ('clock-circle', 'не позначено', 'none'), ('calendar-mark', 'заплановано', 'scheduled'), ('check-circle', 'пройдено', 'done')]),
    ('Кнопки', '', [('check-square', 'Позначити пройденим'), ('calendar-add', 'Запланувати'), ('pen', 'Змінити відмітку'), ('download-minimalistic', 'Завантажити PDF'), ('history', 'Пройдене'), ('magnifer', 'Знайти обстеження')]),
    ('Стани екрана', 'sys', [('danger-triangle', 'тривожний симптом', 'error'), ('restart', 'спробувати ще раз', 'muted'), ('hourglass', 'рахуємо план', 'muted'), ('inbox', 'порожньо', 'muted'), ('shield-warning', 'не вивірено рецензентом', 'muted'), ('info-circle', 'підказка', 'muted')]),
]

SCHED = dict(ITEMS[0], state='scheduled', meta='раз на рік · 15 жовтня 2026, у твоєму календарі',
             when='Раз на рік · востаннє 14 червня 2025 · заплановано на 15 жовтня 2026',
             acts=[('check-square', 'Позначити пройденим', True), ('calendar-mark', 'Змінити дату', False)])


def colors_html():
    out = ''
    for title, sub, rows in COLORS:
        lis = ''
        for toks, name, use, attr in rows:
            if len(toks) == 1:
                sw = f'<span class="chip" style="background:var({toks[0]})"></span>'
            else:
                sw = '<span class="chips3">' + ''.join(f'<span style="background:var({t})"></span>' for t in toks) + '</span>'
            codes = ' · '.join(f'{hx(t)} <code>{t}</code>' for t in toks)
            attr_html = f'З атрибута <a href="{ANCH}">{e(attr)}</a>' if attr[0].isdigit() else e(attr[0].upper() + attr[1:])
            lis += (f'<li>{sw}<span><span class="sw-name">{e(name)}</span><span class="sw-code">{codes}</span>'
                    f'<span class="sw-use">{e(use)}</span><span class="sw-attr">{attr_html}</span></span></li>')
        out += f'<div class="panel"><h3>{e(title)}</h3><p class="small">{e(sub)}</p><ul class="sw-grid">{lis}</ul></div>'
    scale = ''.join(f'<li><span class="chip" style="background:var({t})"></span><b>{t.split("-")[-1]}</b>{hx(t)}</li>' for t in SCALE)
    out += f'<div class="panel"><h3>Відтінки рожевого</h3><p class="small">#C15182 з білим дає 4,4:1 — замало для тексту на кнопці, тому кнопка — 600, текст посилань — 700, натиснута кнопка — 800.</p><ul class="scale">{scale}</ul></div>'
    return out


def type_html():
    rows = ''
    for tok, face, sample, use in TYPE:
        fam = 'var(--font-display)' if TYPE_FAMILY.get(tok) else 'var(--font-text)'
        rows += (f'<tr><th scope="row"><code>{tok}</code><br>{TOK[tok]}</th><td>{e(face)}</td>'
                 f'<td style="font:var({TYPE_WEIGHT[tok]}) var({tok})/var(--leading-snug) {fam}">{e(sample)}</td><td>{e(use)}</td></tr>')
    return (f'<div class="pair"><div class="panel"><p class="small">Заголовки, назви, підписи · <code>--font-display</code></p>'
            f'<p class="spec-d">Nunito</p><p class="spec-t" style="font-family:var(--font-display);font-weight:var(--weight-heavy)">Огляд у гінеколога · Розглянули і не включили</p>'
            f'<p class="small">Округлий гротеск: м’який, але читається на ходу. Ваги 700–900.</p></div>'
            f'<div class="panel"><p class="small">Текст, дати, кнопки · <code>--font-text</code></p><p class="spec-d" style="font-family:var(--font-text)">Nunito Sans</p>'
            f'<p class="spec-t">Кілька хвилин на прийомі або вдома тонометром. 14 червня 2026 · рівень A · 2021</p>'
            f'<p class="small">Та сама родина без заокруглень — для довгого тексту й цифр. Ваги 400–700.</p></div></div>'
            f'<div class="panel"><h3>Шкала розмірів</h3><div class="tw"><table><thead><tr><th>Токен</th><th>Шрифт і вага</th><th>Як виглядає</th><th>Де</th></tr></thead>'
            f'<tbody>{rows}</tbody></table></div></div>')


def shape_html():
    radii = [('--radius-xs', 'мітки в таблицях стенду'), ('--radius-sm', 'вкладки меню'), ('--radius-md', 'плитки палітри'),
             ('--radius-lg', 'картки, блоки плану'), ('--radius-pill', 'кнопки, фільтр, мітки'), ('--radius-round', 'значки обстежень')]
    rad = ''.join(f'<figure><span class="rbox" style="border-radius:var({t})"></span><b><code>{t}</code></b>{TOK[t]} · {e(u)}</figure>' for t, u in radii)
    sh = [('--shadow-card', 'картки й блоки'), ('--shadow-raised', 'наведення на основну кнопку, перемикач'), ('--shadow-hairline', 'тонка рамка плиток')]
    sha = ''.join(f'<figure><span class="sbox" style="box-shadow:var({t})"></span><b><code>{t}</code></b>{e(u)}</figure>' for t, u in sh)
    sp = ['--space-hair', '--space-1', '--space-2', '--space-3', '--space-4', '--space-5', '--space-6', '--space-8', '--space-10', '--space-12', '--space-16', '--space-20']
    spu = {'--space-1': 'між іконкою й словом', '--space-2': 'між мітками, у фільтрі', '--space-3': 'між картками, між рядками фактів',
           '--space-4': 'внутрішній відступ картки', '--space-6': 'відступ панелі', '--space-16': 'між розділами стенду'}
    spa = ''.join(f'<li><span><code>{t}</code> · {TOK[t]}</span><span class="sp-row"><i style="width:var({t})"></i><span class="small">{e(spu.get(t, ""))}</span></span></li>' for t in sp)
    return (f'<div class="panel"><h3>Радіуси</h3><div class="shape-row">{rad}</div></div>'
            f'<div class="panel"><h3>Тіні</h3><p class="small">Тінь лише одна робоча — у картки. Вона тепла й коротка: картка лежить на градієнті, а не висить над ним.</p><div class="shape-row">{sha}</div></div>'
            f'<div class="panel"><h3>Відступи</h3><p class="small">Крок 4 px. Тісно всередині групи, просторо між групами.</p><ul class="spacing">{spa}</ul></div>')


def icons_html():
    out = ''
    for title, kind, items in ICONS_G:
        lis = ''
        for it in items:
            n, label = it[0], it[1]
            if kind == 'badge':
                lis += f'<li><span class="badge b-{it[2]}">{ic(n, ST)}</span>{e(label)}</li>'
            elif kind == 'st':
                lis += f'<li class="st-{it[2]}">{ic(n, ST)}{e(label)}</li>'
            elif kind == 'sys':
                lis += f'<li class="sys-{it[2]}">{ic(n, ST)}{e(label)}</li>'
            else:
                lis += f'<li>{ic(n, ST)}{e(label)}</li>'
        out += f'<div class="panel"><h3>{e(title)}</h3><ul class="ic-list">{lis}</ul></div>'
    return f'<div class="ic-groups">{out}</div>'


def buttons_html():
    kinds = [('pri', 'Основна', 'check-square', 'Позначити пройденим'), ('', 'Другорядна', 'calendar-add', 'Запланувати'), ('txt', 'Текстова', 'magnifer', 'Знайти обстеження')]
    states = [('', 'Звичайна'), ('is-hover', 'Наведення'), ('is-active', 'Натиснута'), ('is-focus', 'Фокус'), ('disabled', 'Вимкнена')]
    cells = '<span></span>' + ''.join(f'<span class="hd">{name}</span>' for _, name, _, _ in kinds)
    for cls, sname in states:
        cells += f'<span class="hd">{sname}</span>'
        for k, name, icon, label in kinds:
            dis = ' disabled' if cls == 'disabled' else ''
            c = ' '.join(x for x in ['btn', k, cls if cls != 'disabled' else ''] if x)
            cells += f'<span><button type="button" class="{c}"{dis} tabindex="-1">{ic(icon, ST)}{e(label)}</button></span>'
    return f'<div class="btn-matrix">{cells}</div>'


def excl_solo():
    n, r, c, s = EXCL[0]
    lead, _, rest = r.partition(': ')
    parts = s.split(' · ')
    return (f'<div class="excl-solo"><article class="ex-it"><h4>{e(n)}</h4><p class="why"><b>{e(lead)}:</b> {e(rest)}</p>'
            f'<div class="cond"><span class="fic">{ic("calendar-mark", ST)}</span><div class="fb"><span class="fl">З’явиться у твоєму плані</span><p>{e(c[0].upper() + c[1:])}</p></div></div>'
            f'<p class="srcl">{ic("document-text", ST)}<span><b>{e(parts[0])}</b>{tags(parts[1:], UNV)}</span></p></article></div>')


def contrast_html():
    rows = ''
    for r in CT.rows(TOK):
        kind = {'text': 'текст', 'large': 'великий текст', 'graphic': 'іконка'}[r['kind']]
        res = '<span class="ok">так</span>' if r['ok'] else '<span class="no">ні</span>'
        ratio_s = ('%.2f' % r['ratio']).replace('.', ',')
        rows += (f'<tr><td><span class="dot" style="background:var({r["fg"]})"></span>{r["fg_hex"]}<br><code>{r["fg"]}</code></td>'
                 f'<td><span class="dot" style="background:var({r["bg"]})"></span>{r["bg_hex"]}<br><code>{r["bg"]}</code></td>'
                 f'<td>{ratio_s}:1</td><td>{str(r["need"]).replace(".", ",")}:1 · {kind}</td><td>{res}</td><td>{e(r["where"])}</td></tr>')
    total = len(CT.rows(TOK)); ok = sum(1 for r in CT.rows(TOK) if r['ok'])
    return (f'<div class="panel"><p class="small">Пораховано скриптом <code>concept/contrast.py</code> зі значень у <code>tokens.css</code>: {ok} із {total} пар проходять WCAG 2.2 AA. '
            f'Поріг для тексту — 4,5:1, для іконок і графіки — 3:1.</p><div class="tw"><table><thead><tr><th>Текст</th><th>Фон</th><th>Коефіцієнт</th><th>Поріг</th><th>Проходить</th><th>Де</th></tr></thead>'
            f'<tbody>{rows}</tbody></table></div></div>')


states_cards = ''.join(item_html(it, 'n', ST) for it in [ITEMS[0], ITEMS[2], SCHED, ITEMS[1], OWN])

doc = f'''<!DOCTYPE html>
<html lang="uk">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Ніжна — стенд стилю · Prevently</title>
<meta name="description" content="Стенд обраного напряму «Ніжна»: стиль у ділі, кольори з атрибутами, шрифти, форма, іконки Solar, три компоненти й контраст за WCAG AA.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400..900&family=Nunito+Sans:opsz,wght@6..12,400..800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="tokens.css">
<style>{CSS}</style>
</head>
<body>
<div class="wrap">
<header class="hero">
 <h1>Ніжна</h1>
 <p class="lead">Стенд обраного напряму. Угорі — стиль у ділі: План і розгорнута картка, кнопки, нижнє меню. Нижче — з чого він складається. Усі значення беруться з <a href="tokens.css">tokens.css</a>, і більше ніде не записані.</p>
 <ul class="toc"><li><a href="#live">У ділі</a></li><li><a href="#colors">Кольори</a></li><li><a href="#type">Шрифти</a></li><li><a href="#shape">Форма</a></li><li><a href="#icons">Іконки</a></li><li><a href="#components">Компоненти</a></li><li><a href="#contrast">Контраст</a></li></ul>
</header>
<main>
<section class="live" id="live" aria-labelledby="live-h"><h2 class="sr" id="live-h">Стиль у ділі</h2>
 <div class="phones">
  <figure>{phone('n', ST, 'План у стилі «Ніжна»', False, 's-1')}<figcaption>План: картки, фільтр, нижнє меню</figcaption></figure>
  <figure>{phone('n', ST, 'Розгорнута картка у стилі «Ніжна»', True, 's-2')}<figcaption>Розгорнута картка й кнопки дій</figcaption></figure>
 </div>
</section>

<section class="sec" id="colors" aria-labelledby="c-h"><h2 id="c-h">Кольори</h2>
 <p class="sub">Біля кожного кольору — з якого атрибута в <a href="concept.md#атрибути">concept.md</a> він випливає. Цифри атрибутів: 1 — спокійний, 2 — сканується, 3 — підписаний, 4 — як застосунок, 5 — з характером.</p>
 {colors_html()}
</section>

<section class="sec" id="type" aria-labelledby="t-h"><h2 id="t-h">Шрифти</h2>
 <p class="sub">Одна родина у двох характерах: Nunito для заголовків і назв, Nunito Sans для тексту й цифр. Шкала — дев’ять розмірів, нічого між ними.</p>
 {type_html()}
</section>

<section class="sec" id="shape" aria-labelledby="f-h"><h2 id="f-h">Форма</h2>
 <p class="sub">М’які великі радіуси на картках і повністю круглі кнопки та значки. Тінь одна й коротка, відступи кратні 4 px.</p>
 {shape_html()}
</section>

<section class="sec" id="icons" aria-labelledby="i-h"><h2 id="i-h">Іконки · Solar Bold Duotone</h2>
 <p class="sub">Один набір і один стиль на весь продукт. Колір іконки — з ролі: рожевий у меню й діях, пастельний значок в обстежень, колір стану в статусах.</p>
 {icons_html()}
</section>

<section class="sec" id="components" aria-labelledby="k-h"><h2 id="k-h">Компоненти</h2>
 <p class="sub">Три готові компоненти. Кожен зібраний тільки з токенів і поводиться однаково на всіх екранах.</p>
 <div class="panel"><h3>1. Кнопка дії</h3><p class="small">Основна — одна на картку, для головної дії. Другорядна — для решти дій. Текстова — для переходів і пошуку. Мінімальна висота — 44 px, щоб влучати пальцем.</p>{buttons_html()}</div>
 <div class="panel comp"><div><h3>2. Картка обстеження з позначкою стану</h3>
   <ol class="anat"><li><b>Значок</b> — пастельне коло з іконкою обстеження.</li><li><b>Назва</b> — Nunito 17, найсильніший текст картки.</li><li><b>Мета-рядок</b> — як часто і коли, сірим.</li><li><b>Позначка стану</b> — іконка й слово. Те, що треба зробити зараз («прострочено», «не позначено»), — у капсулі, як у лічильнику «Зараз»; колір і тло лише в «прострочено».</li><li><b>Знак розкриття</b> — кругла кнопка зі стрілкою; тап розгортає картку на місці, з усіма фактами й діями.</li><li><b>Твій пункт</b> — пунктирна рамка й сірий значок: це не наша рекомендація.</li></ol></div>
   <ul class="items cards-col">{states_cards}</ul></div>
 <div class="panel comp"><div><h3>3. Пояснення невключеного</h3>
   <p class="why-third"><b>Чому саме цей компонент.</b> «Чому цього немає» — половина продукту за брифом: без нього короткий план не відрізнити від недбалого. Він трапляється в Плані, у Пошуку обстеження і в PDF, тож має бути одним компонентом, а не трьома версіями.</p>
   <ol class="anat"><li><b>Назва обстеження.</b></li><li><b>Підстава</b> — «Розглянули і не включили у твій чекап:» жирним, далі причина.</li><li><b>«З’явиться у твоєму плані»</b> — коли й за якої умови воно стане потрібним; з іконкою календаря, як факт у картці.</li><li><b>Джерело</b> — назва настанови жирним, рівень і рік мітками, «не вивірено рецензентом» пунктиром.</li></ol>
   <p class="small">Наступний кандидат — алерт тривожного симптому: він єдиний носить колір помилки.</p></div>
   {excl_solo()}</div>
</section>

<section class="sec" id="contrast" aria-labelledby="x-h"><h2 id="x-h">Контраст</h2>
 <p class="sub">Кожна пара «текст / фон», яка трапляється в продукті, з коефіцієнтом за WCAG 2.2.</p>
 {contrast_html()}
</section>

</main>
<footer class="foot"><p>Вибір і всі напрями — <a href="concept.md#напрями">concept.md → Напрями</a>. Робоча сторінка напряму — <a href="nizhna.html">nizhna.html</a>. До чого можна повернутися: <a href="ridnyi.html">«Рідний»</a>, <a href="directions-round2.html#tablo">«Табло»</a>. Іконки <a href="https://icon-sets.iconify.design/solar/">Solar</a> від 480 Design, ліцензія CC BY 4.0. Шрифти — Google Fonts.</p></footer>
</div>
<script>
document.querySelectorAll('.filter').forEach(g => g.addEventListener('click', ev => {{
  const b = ev.target.closest('button'); if (!b) return;
  g.querySelectorAll('button').forEach(x => x.setAttribute('aria-pressed', String(x === b)));
}}));
document.querySelectorAll('.tabbar a').forEach(a => a.addEventListener('click', ev => ev.preventDefault()));
</script>
</body>
</html>
'''
missing = sorted(n for n in USED_ICONS if f'--icon-{n}' not in TOK)
assert not missing, f'немає токенів для іконок: {missing} — додай у concept/icons.py'
ICON_CSS = ''.join(f'.ic-{n}{{--i:var(--icon-{n})}}' for n in sorted(USED_ICONS))
doc = doc.replace('</style>', '/* Іконки: форма з токенів --icon-* */\n' + ICON_CSS + '\n</style>', 1)
OUT.write_text(doc, encoding='utf-8')
print('written', len(doc))
