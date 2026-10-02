"""Командная оболочка StudyOS. Ходит только в syscalls."""

from src.syscalls import (
    sys_login,
    sys_logout,
    sys_whoami,
    sys_create_file,
    sys_list_files,
    sys_ps,
    sys_logs,
)


def prompt(current_user):
    return f"{current_user}@studyos:~$ "


def run(input_fn=input, output_fn=print):
    current_user = "guest"
    while True:
        try:
            line = input_fn(prompt(current_user))
        except EOFError:
            break
        if line is None:
            break
        cmd = line.strip()
        if not cmd:
            continue
        if cmd == "exit":
            break
        if cmd == "whoami":
            output_fn(sys_whoami(current_user))
        elif cmd == "login":
            login = input_fn("login: ").strip()
            password = input_fn("password: ").strip()
            if sys_login(login, password, current_user):
                current_user = login
                output_fn(f"Вы вошли как {login}")
            else:
                output_fn("Ошибка входа")
        elif cmd == "logout":
            if sys_logout(current_user):
                current_user = "guest"
                output_fn("Сессия завершена")
        elif cmd == "create":
            path = input_fn("path: ").strip()
            content = input_fn("content: ").strip()
            fid = sys_create_file(path, content, current_user)
            output_fn(f"Создан файл с id={fid}")
        elif cmd == "ls":
            files = sys_list_files("/", current_user)
            for item in files:
                output_fn(item)
        elif cmd == "ps":
            processes = sys_ps(current_user)
            for item in processes:
                output_fn(item)
        elif cmd == "logs":
            rows = sys_logs(10, current_user)
            for item in rows:
                output_fn(item)
        else:
            output_fn(f"Неизвестная команда: {cmd}")


if __name__ == "__main__":
    run()
