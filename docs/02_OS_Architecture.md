# Архитектура ОС

## 1. Состав модулей

- shell.py — командная оболочка, читает команды пользователя
- syscalls.py — системные вызовы, интерфейс между оболочкой и ядром
- kernel.py — ядро, обрабатывает вызовы и координирует подсистемы
- scheduler.py — планировщик, управляет процессами
- memory.py — управление памятью
- fs.py — файловая система, работает с файлами
- auth.py — аутентификация и права доступа
- db.py — работа с SQLite

Зависимости только сверху вниз: оболочка не обращается к базе напрямую, ядро координирует подсистемы, подсистемы пишут в SQLite через db.py.

## 2. Системные вызовы

```text
sys_login(login: str, password: str) -> bool
sys_logout() -> bool
sys_whoami() -> str
sys_create_file(path: str, content: str) -> int
sys_read_file(path: str) -> str
sys_delete_file(path: str) -> bool
sys_list_files(path: str) -> list
sys_exec(name: str) -> int
sys_ps() -> list
sys_kill(pid: int) -> bool
sys_mem_alloc(size: int) -> int
sys_logs(limit: int) -> list
sys_shutdown() -> bool
```

Оболочка вызывает только эти функции. Реализация на занятии — заглушки с записью в syscalls_log.

## 3. Контракты системных вызовов

### sys_create_file(path, content) -> int

- предусловие: пользователь авторизован
- постусловие: файл создан, возвращён его id
- побочный эффект: запись в syscalls_log

### sys_login(login, password) -> bool

- предусловие: пара login/password передана, сессия ещё не обязана существовать
- постусловие: при верных учётных данных возвращено True и текущий пользователь установлен вызывающей стороной; при неверных — False, пользователь не меняется
- побочный эффект: запись в syscalls_log (args = login, пароль в лог не пишется)

### sys_kill(pid) -> bool

- предусловие: пользователь авторизован, pid указывает на существующий процесс, вызывающий — владелец или имеет роль, которой разрешено завершать чужие процессы
- постусловие: процесс переведён в состояние terminated, возвращено True; если процесса нет или прав недостаточно — False
- побочный эффект: запись в syscalls_log; освобождение памяти процесса делегируется memory.py

## 4. Структуры данных

```python
process = {
    "pid": 0,
    "name": "",
    "state": "ready",
    "owner": "",
    "memory": 0,
    "created_at": "",
}
```

```python
file = {
    "id": 0,
    "path": "",
    "content": "",
    "owner": "",
    "created_at": "",
}
```

```python
user = {
    "id": 0,
    "login": "",
    "password_hash": "",
    "role": "user",
}
```

```python
log = {
    "id": 0,
    "syscall_name": "",
    "args": "",
    "user": "",
    "status": "",
    "timestamp": "",
}
```
