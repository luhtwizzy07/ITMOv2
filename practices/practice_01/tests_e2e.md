# E2E-проверки

| Сценарий пользователя | Предусловия | Действие | Наблюдаемый результат | Evidence |
|---|---|---|---|---|
| Позитивный | Валидный JSON { diff: "..." }, длина ≤ 20k | POST /api/reviews | 200 OK, тело { summary, risks (≤3), checks } | OUT-1 правило |
| Негативный | JSON без diff | POST /api/reviews | 422 Unprocessable Entity | app/api.py:35-38 (нет модели) |
| Граничный | diff длиной 20 001 | POST /api/reviews | 413 Request Entity Too Large | API-1 правило |

## Как использовали AI

 - Для чего: Сформулировать end-to-end сценарии по контракту OUT-1
 - Тип промпта: master prompt
 - Строка в [`prompts.md`](prompts.md): P1-02
 - Что проверили и исправили сами: Уточнили ожидаемые коды и структуру ответа
