"""SQLite connection and schema setup."""

import sqlite3
from pathlib import Path


APP_DIR = Path(__file__).resolve().parents[1]
DATABASE_PATH = APP_DIR / "stockflow.db"
SCHEMA_PATH = Path(__file__).with_name("schema.sql")


def get_connection() -> sqlite3.Connection:
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def initialize_database() -> None:
    schema_sql = SCHEMA_PATH.read_text()

    with get_connection() as connection:
        connection.executescript(schema_sql)
