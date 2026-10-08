#!/usr/bin/env python3
"""Іконки Solar Bold Duotone як токени в concept/tokens.css.

Запуск:  python3 concept/icons.py

Бере SVG з Iconify API і переписує в tokens.css блок між позначками
«Іконки: початок» і «Іконки: кінець». Кожна іконка — змінна --icon-<назва>
зі значенням url("data:image/svg+xml,…"). На сторінці її малює mask-image:
форма береться з файлу, колір — із ролі, тож одна іконка фарбується будь-яким
токеном. Напівпрозорий шар «duotone» маска зберігає.

Щоб додати іконку — допишіть її в ICONS і запустіть скрипт знову.
"""
import json
import re
import urllib.request
from pathlib import Path
from urllib.parse import quote

TOKENS = Path(__file__).with_name('tokens.css')
STYLE = 'bold-duotone'
START = '  /* ── Іконки: початок · згенеровано concept/icons.py, руками не правити ── */'
END = '  /* ── Іконки: кінець ── */'

# (назва в Solar, де трапляється)
ICONS = [
    ('stethoscope', 'обстеження: гінеколог'),
    ('smile-circle', 'обстеження: стоматолог'),
    ('heart-pulse', 'обстеження: тиск'),
    ('test-tube', 'обстеження: аналізи'),
    ('notes', 'обстеження: твій пункт'),
    ('danger-circle', 'стан: прострочено'),
    ('clock-circle', 'стан: не позначено'),
    ('calendar-mark', 'стан: заплановано; найближча дата'),
    ('check-circle', 'стан: пройдено'),
    ('calendar', 'факт: коли'),
    ('wallet-money', 'факт: вартість'),
    ('user-heart', 'факт: чому в плані'),
    ('document-text', 'факт: джерело'),
    ('check-square', 'дія: позначити пройденим'),
    ('calendar-add', 'дія: запланувати'),
    ('pen', 'дія: змінити відмітку'),
    ('magnifer', 'дія: знайти обстеження'),
    ('download-minimalistic', 'дія: завантажити PDF'),
    ('history', 'дія: пройдене'),
    ('restart', 'дія: спробувати ще раз'),
    ('folder-open', 'дія: копія твоїх даних'),
    ('clipboard-add', 'дія: додати до списку'),
    ('arrow-left', 'дія: назад у питаннях'),
    ('arrow-right', 'дія: далі у питаннях'),
    ('upload-minimalistic', 'дія: відновити з копії'),
    ('trash-bin-minimalistic', 'дія: видалити файл, видалити всі дані'),
    ('clipboard-list', 'меню: план'),
    ('notebook-minimalistic', 'меню: мої відповіді; пройти опитувальник заново'),
    ('info-circle', 'меню: про підхід; підказка'),
    ('round-alt-arrow-down', 'розкрити: картку, «не включили», джерело'),
    ('clipboard-remove', 'екран: план не порахувався, Пройдене не відкрилося'),
    ('hourglass', 'екран: рахуємо план'),
    ('hand-heart', 'екран: знак продукту на Вході й у PDF'),
    ('shield-check', 'обіцянка: відповіді тільки на цьому пристрої'),
    ('checklist-minimalistic', 'пошук: розглянули і не включили'),
    ('minus-circle', 'пошук: не оцінюємо для чекапів'),
    ('danger-triangle', 'алерт тривожного симптому'),
    ('inbox', 'стенд: порожньо'),
    ('shield-warning', 'стенд: не вивірено рецензентом'),
]


def fetch(names):
    url = f'https://api.iconify.design/solar.json?icons={",".join(f"{n}-{STYLE}" for n in names)}'
    req = urllib.request.Request(url, headers={'User-Agent': 'curl/8.4.0'})
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.load(r)
    missing = data.get('not_found', [])
    if missing:
        raise SystemExit(f'Немає в Solar: {", ".join(missing)}')
    return data['icons']


def data_uri(body):
    svg = f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'>{body}</svg>"
    svg = re.sub(r'\s+', ' ', svg.replace('"', "'"))
    return 'url("data:image/svg+xml,' + quote(svg, safe=" '=:/,.-_()") + '")'


def main():
    bodies = fetch([n for n, _ in ICONS])
    lines = [START, '  /* Solar Bold Duotone · 480 Design · CC BY 4.0 */']
    for name, where in ICONS:
        lines.append(f'  /* {where} */')
        lines.append(f'  --icon-{name}: {data_uri(bodies[f"{name}-{STYLE}"]["body"])};')
    lines.append(END)
    block = '\n'.join(lines)

    css = TOKENS.read_text(encoding='utf-8')
    if START in css:
        css = re.sub(re.escape(START) + r'.*?' + re.escape(END), lambda _: block, css, flags=re.S)
    else:
        css = css.rstrip().removesuffix('}').rstrip() + '\n\n' + block + '\n}\n'
    TOKENS.write_text(css, encoding='utf-8')
    print(f'{len(ICONS)} іконок → {TOKENS.name}')


if __name__ == '__main__':
    main()
