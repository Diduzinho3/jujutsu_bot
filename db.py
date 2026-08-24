import sqlite3

from config import DATABASE_PATH


def get_connection() -> sqlite3.Connection:
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db() -> None:
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS fichas (
                user_id INTEGER PRIMARY KEY,
                vida_atual INTEGER NOT NULL,
                vida_max INTEGER NOT NULL,
                ce_atual INTEGER NOT NULL,
                ce_max INTEGER NOT NULL,
                reforco_nivel INTEGER NOT NULL,
                reforco_xp INTEGER NOT NULL,
                controle_nivel INTEGER NOT NULL,
                controle_xp INTEGER NOT NULL,
                tecnica_nivel INTEGER NOT NULL,
                tecnica_xp INTEGER NOT NULL,
                rct_nivel INTEGER NOT NULL,
                rct_xp INTEGER NOT NULL,
                barreira_nivel INTEGER NOT NULL,
                barreira_xp INTEGER NOT NULL
            )
            """
        )
