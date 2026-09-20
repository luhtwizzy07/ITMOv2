# E2E-проверки

| Сценарий пользователя | Предусловия | Действие | Наблюдаемый результат | Evidence |
|---|---|---|---|---|
| Успешный путь по OUT-1 | Валидный JSON `{ diff: "..." }`, длина ≤ 20 000, LLM-заглушка в режиме ok | POST /api/reviews | 200 OK; тело содержит `summary:str`, `risks:list` (0..3 объектов с полями file,line,evidence,risk), `checks:list[str]` | OUT-1 (context.md); ADR «Решение» |
| Отсутствует diff | JSON без поля `diff` | POST /api/reviews | 422 Unprocessable Entity; LLM не вызывается | Вход: `diff` — обязательная строка (context.md); product_management.md (422); ADR «Решение» |
| Неверный тип diff | JSON `{ diff: 123 }` | POST /api/reviews | 422 Unprocessable Entity; LLM не вызывается | Вход: `diff` — строка (context.md); product_management.md |
| Граничный: ровно 20 000 | Строка `diff` длиной 20 000 | POST /api/reviews | 200 OK (допустимо по лимиту) | API-1 (context.md): «длиннее 20 000 → 413» |
| Граничный: 20 001 | Строка `diff` длиной 20 001 | POST /api/reviews | 413 Request Entity Too Large; LLM не вызывается | API-1 (context.md); ADR «Решение» |
| Таймаут LLM | LLM-заглушка спит ≥ 10s | POST /api/reviews | 504 Gateway Timeout; тело `{ error: "LLM timeout" }` | REL-1 (context.md); ADR «Маппинг ошибок LLM → HTTP» |
| Сетевая/5xx ошибка LLM | LLM-заглушка бросает сетевую/5xx ошибку | POST /api/reviews | 502 Bad Gateway; тело `{ error: "LLM unavailable" }` | REL-1; ADR «Маппинг ошибок LLM → HTTP» |
| Внутренняя ошибка адаптера | LLM-заглушка бросает произвольное исключение | POST /api/reviews | 500 Internal Server Error; тело `{ error: "Internal error" }` | REL-1; ADR «Маппинг ошибок LLM → HTTP» |
| OBS-1: политика логирования | Настроен сбор логов тестом (caplog); выполнить любой успешный и ошибочный сценарий | POST /api/reviews | В логах есть только `request_id`, длительность, статус; отсутствуют `diff`, `prompt`, `response` | OBS-1 (context.md); ADR «Политика логирования (OBS-1)» |

## Как использовали AI

 - Для чего: Сформулировать полный набор end-to-end сценариев по OUT-1/API-1/REL-1/OBS-1 согласно ADR
 - Тип промпта: master prompt
 - Строка в [`prompts.md`](prompts.md): P1-02
 - Что проверили и исправили сами: Добавили граничные случаи 20 000/20 001, точные коды/тела 504/502/500, проверки 422 (нет/неверный тип diff) и OBS-1
