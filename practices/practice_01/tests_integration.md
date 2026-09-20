# Integration-проверки

| Связь компонентов | Что может сломаться | Как воспроизводим | Ожидаемый результат | Evidence |
|---|---|---|---|---|
| FastAPI ↔ ReviewService | Успешный путь не соответствует контракту OUT-1 | POST /api/reviews с валидным JSON `{ diff: "..." }` длиной ≤ 20k; LLM-заглушка возвращает корректный объект | 200 OK; тело JSON: `summary: str`, `risks: list (0..3) с полями file, line, evidence, risk`, `checks: list[str]` | OUT-1 правило; ADR «Решение»; app/api.py (контракт ответа) |
| FastAPI ↔ ReviewService | Отсутствует поле `diff` | POST /api/reviews без поля `diff` | 422 Unprocessable Entity от валидации; LLM не вызывается | Валидация FastAPI/Pydantic; API-1 ограничение применяется до LLM; ADR «Решение» |
| FastAPI ↔ ReviewService | Неверный тип `diff` (не строка) | POST /api/reviews с `{ diff: 123 }` | 422 Unprocessable Entity; сообщение о типе; LLM не вызывается | Контракт входа; OUT-1 неприменим; ADR «Решение» |
| FastAPI ↔ ReviewService | Превышение длины diff | POST /api/reviews с `diff` длиной 20001 | 413 Request Entity Too Large; LLM не вызывается | API-1 правило; ADR «Решение» |
| ReviewService ↔ LLM-адаптер | Таймаут LLM ≥ 10s | LLM-заглушка спит >10s | 504 Gateway Timeout; тело `{ error: "LLM timeout" }` | REL-1; ADR «Маппинг ошибок LLM → HTTP» |
| ReviewService ↔ LLM-адаптер | Сетевая/5xx ошибка LLM | LLM-заглушка бросает исключение, имитирующее 5xx/NetworkError | 502 Bad Gateway; тело `{ error: "LLM unavailable" }` | REL-1; ADR «Маппинг ошибок LLM → HTTP» |
| ReviewService ↔ LLM-адаптер | Внутренняя ошибка адаптера | LLM-заглушка бросает произвольное исключение | 500 Internal Server Error; тело `{ error: "Internal error" }` | REL-1; ADR «Маппинг ошибок LLM → HTTP» |
| FastAPI ↔ Логи | Нарушение OBS-1 (утечка diff/prompt/response в логи) | Выполнить запрос и собрать логи (caplog); сценарии: успешный, 422, 413, ошибки LLM | В логах есть только `request_id`, длительность, статус; отсутствуют `diff`, `prompt`, `response` | OBS-1 правило; ADR «Политика логирования (OBS-1)» |
| FastAPI ↔ ReviewService ↔ LLM-адаптер | Ненужные вызовы LLM при 422/413 | Счётчик вызовов LLM-заглушки; отправить запросы без `diff` и с длиной >20k | Счётчик вызовов не увеличивается (LLM не зовётся) | API-1; корректная валидация входа до внешних вызовов; ADR «Решение» |

## Как использовали AI

 - Для чего: Расширить интеграционные проверки под ADR (OUT-1, API-1, REL-1, OBS-1) и убрать двусмысленности кодов/тел
 - Тип промпта: master prompt
 - Строка в [`prompts.md`](prompts.md): P1-02
 - Что проверили и исправили сами: Добавили точные статусы/тела 504/502/500, проверки OBS-1 и отсутствие вызова LLM при 422/413
