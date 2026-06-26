# Инструкции для всех агентов этого проекта

## Память — обязательно при старте

Прочитай эти файлы перед любой работой:

1. `/home/primero/.claude/projects/-home-primero-Python-python-codes-other-test-tasks-test-speeder/memory/AGENTS.md` — протокол работы с памятью, префиксы файлов, правила, откуда брать
2. `/home/primero/.claude/projects/-home-primero-Python-python-codes-other-test-tasks-test-speeder/memory/project_state.md` — живой статус проекта, архитектура, ключевые решения
3. `/home/primero/.claude/projects/-home-primero-Python-python-codes-other-test-tasks-test-speeder/memory/feedback_code_style.md` — правила стиля кода, обязательны

Полный индекс памяти: `memory/MEMORY.md` (загружается автоматически)

## Правила памяти (кратко)

- `MEMORY.md` и общие файлы — только **Edit**, никогда **Write**
- Личные файлы — только с **твоим префиксом** (main_, review_, qa_, ...). Чужие — только читать
- `project_state.md` — обновляй только **свою секцию** через Edit
- Если твоей секции нет — добавь через Edit в конец

## Проект

CLI-скрипт замерятель скорости интернета.
Принимает URL, делает 10 последовательных async-запросов, выводит скорость в МБ/с.

Рабочая директория: `/home/primero/Python/python_codes/other/test_tasks/test_speeder`
Референсный проект (паттерны кода): `/home/primero/Python/python_codes/langgraph/1_lang`
