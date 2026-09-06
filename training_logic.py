import random
from dataclasses import dataclass

from models.ficha import Ficha


@dataclass(frozen=True)
class ResultadoTreinamento:
    nome_atributo: str
    xp_ganho: int
    subiu_de_nivel: bool
    nivel_anterior: int
    nivel_atual: int
    xp_atual: int
    xp_necessario: int


ATRIBUTOS_TREINAVEIS = {
    "reforco": ("reforco_nivel", "reforco_xp", "Reforço"),
    "controle": ("controle_nivel", "controle_xp", "Controle"),
    "tecnica": ("tecnica_nivel", "tecnica_xp", "Técnica"),
    "rct": ("rct_nivel", "rct_xp", "Energia Reversa"),
    "barreira": ("barreira_nivel", "barreira_xp", "Barreira"),
}


def ganhar_xp() -> int:
    return random.randint(5, 12)


def calcular_level_up(nivel: int, xp: int) -> tuple[int, int, bool]:
    xp_necessario = nivel * 100

    if xp >= xp_necessario:
        return nivel + 1, xp - xp_necessario, True

    return nivel, xp, False


def treinar_atributo(ficha: Ficha, atributo: str) -> ResultadoTreinamento:
    nivel_field, xp_field, nome_atributo = ATRIBUTOS_TREINAVEIS[atributo]
    nivel_anterior = getattr(ficha, nivel_field)
    xp_ganho = ganhar_xp()
    xp_com_ganho = getattr(ficha, xp_field) + xp_ganho
    nivel_atual, xp_atual, subiu_de_nivel = calcular_level_up(
        nivel_anterior, xp_com_ganho
    )

    setattr(ficha, nivel_field, nivel_atual)
    setattr(ficha, xp_field, xp_atual)

    return ResultadoTreinamento(
        nome_atributo=nome_atributo,
        xp_ganho=xp_ganho,
        subiu_de_nivel=subiu_de_nivel,
        nivel_anterior=nivel_anterior,
        nivel_atual=nivel_atual,
        xp_atual=xp_atual,
        xp_necessario=nivel_atual * 100,
    )
