from models.ficha import Ficha
from db import get_connection


def criar_ficha(ficha: Ficha) -> None:
    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO fichas (
                user_id, vida_atual, vida_max, ce_atual, ce_max,
                reforco_nivel, reforco_xp, controle_nivel, controle_xp,
                tecnica_nivel, tecnica_xp, rct_nivel, rct_xp,
                barreira_nivel, barreira_xp
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                ficha.user_id,
                ficha.vida_atual,
                ficha.vida_max,
                ficha.ce_atual,
                ficha.ce_max,
                ficha.reforco_nivel,
                ficha.reforco_xp,
                ficha.controle_nivel,
                ficha.controle_xp,
                ficha.tecnica_nivel,
                ficha.tecnica_xp,
                ficha.rct_nivel,
                ficha.rct_xp,
                ficha.barreira_nivel,
                ficha.barreira_xp,
            ),
        )


def buscar_ficha(user_id: int) -> Ficha | None:
    with get_connection() as connection:
        row = connection.execute(
            "SELECT * FROM fichas WHERE user_id = ?", (user_id,)
        ).fetchone()

    return Ficha(**dict(row)) if row else None


def salvar_ficha(ficha: Ficha) -> None:
    with get_connection() as connection:
        connection.execute(
            """
            UPDATE fichas SET
                vida_atual = ?, vida_max = ?, ce_atual = ?, ce_max = ?,
                reforco_nivel = ?, reforco_xp = ?,
                controle_nivel = ?, controle_xp = ?,
                tecnica_nivel = ?, tecnica_xp = ?, rct_nivel = ?, rct_xp = ?,
                barreira_nivel = ?, barreira_xp = ?
            WHERE user_id = ?
            """,
            (
                ficha.vida_atual,
                ficha.vida_max,
                ficha.ce_atual,
                ficha.ce_max,
                ficha.reforco_nivel,
                ficha.reforco_xp,
                ficha.controle_nivel,
                ficha.controle_xp,
                ficha.tecnica_nivel,
                ficha.tecnica_xp,
                ficha.rct_nivel,
                ficha.rct_xp,
                ficha.barreira_nivel,
                ficha.barreira_xp,
                ficha.user_id,
            ),
        )


def existe_ficha(user_id: int) -> bool:
    with get_connection() as connection:
        row = connection.execute(
            "SELECT 1 FROM fichas WHERE user_id = ?", (user_id,)
        ).fetchone()

    return row is not None
