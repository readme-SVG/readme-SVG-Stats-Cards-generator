# README Custom Badge Generator

Serverless генератор SVG-баджей для README, профилей GitHub и документации с упором на максимальную кастомизацию.

## Что умеет

- Генерирует баджи через endpoint `/badge`.
- Поддерживает стили: `flat`, `flat-square`, `for-the-badge`, `plastic`, `social`, `rounded`, `pill`, `outline`, `soft`.
- Поддерживает размеры: `xs`, `sm`, `md`, `lg`, `xl` + точная настройка через `scale`.
- Поддерживает темы: `dark`, `light`, `neon`, `sunset`, `terminal`.
- Дает выбор цветов через палитру в UI, color picker и ручной HEX.
- Имеет пресеты и каталог возможностей через `/catalog`.

## Быстрый старт

```bash
git clone https://github.com/<your-user>/readme-SVG-Stats-Cards-generator.git
cd readme-SVG-Stats-Cards-generator
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 api/stats_index.py
```

Откройте `http://127.0.0.1:5000`.

## API

### `GET /badge`

Основные параметры:

- `label` — левая часть (`build`)
- `value` — правая часть (`passing`)
- `icon` — `star|heart|check|fire|bolt|rocket|code|build|docs|none`
- `style` — `flat|flat-square|for-the-badge|plastic|social|rounded|pill|outline|soft`
- `size` — `xs|sm|md|lg|xl`
- `scale` — float `0.7..2.0`
- `theme` — `dark|light|neon|sunset|terminal`
- `label_bg`, `value_bg`, `label_color`, `value_color`, `border_color` — HEX
- `border_radius` — `0..999`
- `gradient` — `true|false` (для `plastic`)
- `uppercase` — `true|false`
- `compact` — `true|false`
- `preset` — `build|coverage|release|docs|quality`

Пример:

```text
/badge?preset=release&label=deploy&value=prod&style=for-the-badge&icon=rocket&theme=sunset&size=lg
```

### `GET /catalog`

Возвращает JSON с темами, стилями, размерами, иконками, цветовой палитрой и пресетами.

### `GET /health`

Проверка доступности сервиса.

## Встраивание в README

```md
![build](https://your-domain.vercel.app/badge?label=build&value=passing&icon=check&theme=terminal&size=md)
```

```md
![release](https://your-domain.vercel.app/badge?label=release&value=v2.1.0&style=pill&theme=neon&size=xl&scale=1.1)
```

## Локальные примеры

```bash
python3 scripts/refresh_sample_svgs.py
```

Файлы появятся в `sample_*.svg/`.

## Deploy на Vercel

```bash
vercel
```

## Лицензия

`GPL-3.0`, см. `LICENSE`.
