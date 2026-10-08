# Практика и ДЗ №4: Notify Mini

Продолжение учебного сервиса из практики №3 в отдельной копии. Данные хранятся
в памяти процесса. Фича A — отсортированный независимый список подписчиков;
фича B — отписка с нормализацией имени и идемпотентным результатом.

## Запуск

Python 3.10+; проверенная среда — Python 3.13.7, OpenCode 1.18.31,
Ollama 0.35.1, локальная модель itmo-agent на базе qwen3.5:4b.

```sh
cd practices/practice_04/lab
make setup
make test
make mcp-proof
```

Код сервиса использует только стандартную библиотеку. `requirements.txt`
устанавливает официальный MCP SDK для MCP-сервера и интеграционных проверок.
API key не нужен. Для запуска сохранённых запросов OpenCode нужен доступный
в Ollama `itmo-agent`; модель можно создать по материалам практики №3:

```sh
# из корня учебного репозитория
ollama create itmo-agent -f practices/practice_03/lab/Modelfile.agent
cd practices/practice_04/lab
opencode mcp list
opencode --agent build
```

Здесь поддерживается **OpenCode 1.18.31**. Слайды используют 2.0.20:
конфигурация MCP и hook намеренно адаптированы к установленной версии.
Для этого проекта MCP находится непосредственно в `mcp.notify_checks`,
а hook использует `tool.execute.after`. Не переносить этот конфиг в 2.x
без миграции. Статус MCP connected ещё не доказывает вызов инструмента.

## Файлы

- `service.py`, `tests/` — сервис и проверки поведения, skill и MCP.
- `AGENTS.md`, `docs/requirements.md`, `docs/style-guide.md` — правила и контракт.
- `.opencode/skills/notify-tdd/` — собственный skill с ресурсом и исполняемым gate.
- `.opencode/plugins/check-after-edit.js` — автоматическая проверка после правки.
- `scripts/check.sh`, `scripts/check.py` — общий runner; профили baseline/a/b/all.
- `mcp_server.py`, `opencode.json` — собственный stdio MCP и подключение агента.
- `scripts/prove_mcp.py` — реальные вызовы MCP официальным клиентом.
- `REPORT.md`, `evidence/` — соответствие условиям и подтверждения выполнения.
- `docs/HANDOFF.md` — контекст для новой сессии.
- `reflection.md` — наблюдения по фактическому ходу работы.

## Что дают подключения

Правила сохраняют контракт и границы маленькой задачи. Skill проверяет смысл
RED/GREEN: ImportError, skip и нулевой набор тестов не считаются полезным RED.
MCP даёт модели один проверяемый интерфейс проверок вместо произвольной shell
команды. Hook возвращает результат runner в вывод инструмента записи, чтобы
агент увидел последствия изменения сразу. Один собственный MCP используется
и в среде практики, и в ДЗ; лишние подключения для количества не добавлены.

## Источники интерфейсов

- [Условия работы](../README.md) и слайды `../presentation.pdf`.
- [OpenCode: skills](https://opencode.ai/docs/skills/).
- [OpenCode: plugins](https://opencode.ai/docs/plugins/).
- [OpenCode: MCP](https://opencode.ai/docs/mcp-servers/).
- [Официальный Python MCP SDK, линия 1.x](https://github.com/modelcontextprotocol/python-sdk/tree/v1.x).
