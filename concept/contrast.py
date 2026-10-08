#!/usr/bin/env python3
"""Контраст пар «текст / фон» з concept/tokens.css за WCAG 2.2.

Запуск:  python3 concept/contrast.py          — таблиця в Markdown
         python3 concept/contrast.py --json   — те саме для збирання стенду

Пороги: звичайний текст 4,5:1, великий текст (від 24 px або від 19 px жирним) 3:1,
іконки й графіка 3:1. Скрипт завершується з кодом 1, якщо хоч одна пара не проходить.
"""
import json
import re
import sys
from pathlib import Path

TOKENS = Path(__file__).with_name('tokens.css')

# (колір тексту, колір фону, тип, де трапляється)
PAIRS = [
    ('--color-text', '--color-surface', 'text', 'Основний текст на картці'),
    ('--color-text-muted', '--color-surface', 'text', 'Пояснення, мета-рядок, нижнє меню'),
    ('--color-text-label', '--color-surface', 'text', 'Підписи: «Коли», «Джерело», «З’явиться у твоєму плані»'),
    ('--color-text', '--color-page', 'text', 'Заголовок екрана на фоні'),
    ('--color-text-muted', '--color-page', 'text', 'Пояснення під заголовком екрана й секції'),
    ('--color-text', '--peach-200', 'text', 'Текст на найтемнішій точці градієнта'),
    ('--color-text-muted', '--peach-200', 'text', 'Мета-рядок на персиковій точці градієнта'),
    ('--color-text-muted', '--pink-blush', 'text', 'Мета-рядок на рожевій точці градієнта'),
    ('--color-on-primary', '--color-primary-strong', 'text', 'Основна кнопка, активний фільтр'),
    ('--color-on-primary', '--color-primary-pressed', 'text', 'Основна кнопка натиснута'),
    ('--color-primary-text', '--color-surface', 'text', 'Другорядна кнопка, посилання'),
    ('--color-primary-text', '--color-primary-soft', 'text', 'Другорядна кнопка під курсором'),
    ('--color-primary-text', '--color-primary-soft-pressed', 'text', 'Другорядна кнопка натиснута'),
    ('--color-text', '--color-primary-soft', 'text', 'Кнопка фільтра під курсором, вибраний варіант відповіді'),
    ('--color-primary-strong', '--color-surface', 'text', 'Активна вкладка нижнього меню'),
    ('--color-overdue-text', '--color-overdue-bg', 'text', 'Мітка «прострочено»'),
    ('--color-neutral-state-text', '--color-surface', 'text', 'Мітки «не позначено», «заплановано», «пройдено»'),
    ('--color-success-text', '--color-success-bg', 'text', 'Повідомлення про успіх'),
    ('--color-error-text', '--color-error-bg', 'text', 'Помилка, алерт тривожного симптому'),
    ('--color-on-primary', '--color-error', 'text', 'Смуга алерту тривожного симптому: заголовок і значок'),
    ('--color-primary', '--color-surface', 'graphic', 'Іконка в розгорнутій картці'),
    ('--color-primary', '--badge-pink-bg', 'graphic', 'Іконка факту в колі, значок «план не порахувався»'),
    ('--color-neutral-state', '--color-surface', 'graphic', 'Іконка «не позначено», «заплановано»'),
    ('--color-overdue', '--color-overdue-bg', 'graphic', 'Іконка «прострочено», значок попередження'),
    ('--color-overdue', '--color-surface', 'graphic', 'Іконка «прострочено» в рядку відмітки'),
    ('--color-text-muted', '--badge-grey-bg', 'graphic', 'Значок екрана «не відкрилося»'),
    ('--color-success', '--color-surface', 'graphic', 'Галочка «пройдено»'),
    ('--badge-pink-fg', '--badge-pink-bg', 'graphic', 'Значок гінеколога'),
    ('--badge-peach-fg', '--badge-peach-bg', 'graphic', 'Значок стоматолога'),
    ('--badge-lilac-fg', '--badge-lilac-bg', 'graphic', 'Значок тиску'),
    ('--badge-mint-fg', '--badge-mint-bg', 'graphic', 'Значок аналізів'),
    ('--badge-grey-fg', '--badge-grey-bg', 'graphic', 'Значок твого пункту'),
    ('--color-text-muted', '--color-surface-soft', 'text', 'Адресний рядок браузера в макеті екрана'),
    ('--color-text-muted', '--color-primary-soft', 'text', 'Підпис на місці прев’ю файлу'),
    ('--color-primary', '--color-primary-soft', 'graphic', 'Іконка документа на місці прев’ю файлу'),
    ('--color-border-input', '--color-surface', 'graphic', 'Рамка поля вводу, кнопка «Видалити»'),
    ('--color-border-input', '--color-page', 'graphic', 'Рамка поля вводу на фоні екрана'),
    ('--color-primary-strong', '--color-primary-soft', 'graphic', 'Рамка й позначка вибраного варіанта відповіді'),
    ('--color-primary-strong', '--color-primary-soft-pressed', 'graphic', 'Заповнена частина прогресу опитувальника'),
    ('--color-primary', '--color-page', 'graphic', 'Щит біля обіцянки «тільки на цьому пристрої»'),
    ('--color-primary-text', '--color-page', 'text', 'Посилання в тексті секції на фоні екрана'),
]
THRESHOLD = {'text': 4.5, 'large': 3.0, 'graphic': 3.0}


def read_tokens(path=TOKENS):
    css = path.read_text(encoding='utf-8')
    raw = dict(re.findall(r'(--[\w-]+)\s*:\s*([^;]+);', css))

    def resolve(name, depth=0):
        value = raw[name].strip()
        m = re.fullmatch(r'var\((--[\w-]+)\)', value)
        return resolve(m.group(1), depth + 1) if m and depth < 10 else value
    return {k: resolve(k) for k in raw}


def luminance(hex_color):
    h = hex_color.lstrip('#')
    channels = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    lin = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in channels]
    return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]


def ratio(fg, bg):
    a, b = sorted((luminance(fg), luminance(bg)), reverse=True)
    return (a + 0.05) / (b + 0.05)


def rows(tokens=None):
    tokens = tokens or read_tokens()
    out = []
    for fg, bg, kind, where in PAIRS:
        r = ratio(tokens[fg], tokens[bg])
        need = THRESHOLD[kind]
        out.append(dict(fg=fg, fg_hex=tokens[fg].upper(), bg=bg, bg_hex=tokens[bg].upper(), kind=kind,
                        ratio=round(r, 2), need=need, ok=r >= need, where=where))
    return out


def main():
    data = rows()
    if '--json' in sys.argv:
        print(json.dumps(data, ensure_ascii=False, indent=1))
    else:
        print('| Текст | Фон | Коефіцієнт | Поріг AA | Проходить | Де |')
        print('|---|---|---|---|---|---|')
        for r in data:
            mark = 'так' if r['ok'] else '**ні**'
            ratio_s = f"{r['ratio']:.2f}".replace('.', ',')
            need_s = f"{r['need']}".replace('.', ',')
            print(f"| `{r['fg_hex']}` {r['fg']} | `{r['bg_hex']}` {r['bg']} | "
                  f"{ratio_s}:1 | {need_s}:1 | {mark} | {r['where']} |")
    sys.exit(0 if all(r['ok'] for r in data) else 1)


if __name__ == '__main__':
    main()
