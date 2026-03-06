### Project Structure

```text
github-stats-cards/
├── api/
│   ├── github_stats.py      # Ядро — генерация всех 4 типов SVG-карточек
│   │                         #   ├── generate_stats_card()    — статистика профиля
│   │                         #   ├── generate_streak_card()   — стрики
│   │                         #   ├── generate_graph_card()    — тепловая карта
│   │                         #   └── generate_views_card()    — счётчик просмотров
│   │                         #   + 7 тем, иконки, ранговая система
│   │
│   └── stats_index.py        # Flask-роуты: /stats, /streak, /graph, /views, /themes
│                              #   + получение данных с GitHub API (если есть токен)
│                              #   + fallback на детерминированные демо-данные
│
├── stats_index.html           # Интерактивный playground (UI для настройки карточек)
│
├── vercel.json                # Конфиг маршрутов для Vercel деплоя
│
└── sample_*.svg               # Примеры сгенерированных карточек (для превью)
    ├── sample_stats.svg
    ├── sample_streak.svg
    ├── sample_graph.svg
    └── sample_views.svg
```
