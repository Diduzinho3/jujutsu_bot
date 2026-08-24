from dataclasses import dataclass


@dataclass
class Ficha:
    user_id: int
    vida_atual: int
    vida_max: int
    ce_atual: int
    ce_max: int
    reforco_nivel: int
    reforco_xp: int
    controle_nivel: int
    controle_xp: int
    tecnica_nivel: int
    tecnica_xp: int
    rct_nivel: int
    rct_xp: int
    barreira_nivel: int
    barreira_xp: int
