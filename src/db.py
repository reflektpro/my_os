"""Минимальный доступ к SQLite учебной ОС."""

import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "db", "os.sqlite")


def init_db(conn):
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS syscalls_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            syscall_name TEXT,
            args TEXT,
            user TEXT,
            status TEXT,
            timestamp TEXT DEFAULT (datetime('now'))
        )
        """
    )
    conn.commit()


def get_connection():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    # Каталог db лежит на FUSE: delete-журнал и posix-lock дают disk I/O error.
    conn = sqlite3.connect(f"file:{DB_PATH}?nolock=1", uri=True, timeout=10)
    conn.execute("PRAGMA journal_mode=MEMORY")
    conn.execute("PRAGMA synchronous=OFF")
    init_db(conn)
    return conn
