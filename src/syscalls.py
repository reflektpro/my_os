"""Системные вызовы StudyOS. На этом занятии — заглушки с журналированием."""

from src.db import get_connection


def log_syscall(name, args="", user="system", status="OK"):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO syscalls_log (syscall_name, args, user, status) VALUES (?, ?, ?, ?)",
        (name, args, user, status),
    )
    conn.commit()
    conn.close()


def sys_login(login, password, current_user="guest"):
    log_syscall("sys_login", args=login, user=current_user)
    return True


def sys_logout(current_user="guest"):
    log_syscall("sys_logout", user=current_user)
    return True


def sys_whoami(current_user="guest"):
    log_syscall("sys_whoami", user=current_user)
    return current_user


def sys_create_file(path, content, current_user="guest"):
    log_syscall("sys_create_file", args=path, user=current_user)
    return 1


def sys_read_file(path, current_user="guest"):
    log_syscall("sys_read_file", args=path, user=current_user)
    return ""


def sys_delete_file(path, current_user="guest"):
    log_syscall("sys_delete_file", args=path, user=current_user)
    return True


def sys_list_files(path, current_user="guest"):
    log_syscall("sys_list_files", args=path, user=current_user)
    return []


def sys_exec(name, current_user="guest"):
    log_syscall("sys_exec", args=name, user=current_user)
    return 42


def sys_ps(current_user="guest"):
    log_syscall("sys_ps", user=current_user)
    return []


def sys_kill(pid, current_user="guest"):
    log_syscall("sys_kill", args=str(pid), user=current_user)
    return True


def sys_mem_alloc(size, current_user="guest"):
    log_syscall("sys_mem_alloc", args=str(size), user=current_user)
    return size


def sys_logs(limit=10, current_user="guest"):
    log_syscall("sys_logs", args=str(limit), user=current_user)
    return []


def sys_shutdown(current_user="guest"):
    log_syscall("sys_shutdown", user=current_user)
    return True


if __name__ == "__main__":
    print(sys_login("admin", "secret"))
    print(sys_whoami("admin"))
    print(sys_create_file("/test.txt", "hello", "admin"))
    print(sys_ps("admin"))
