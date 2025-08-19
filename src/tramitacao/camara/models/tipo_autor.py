from enum import StrEnum
from pydantic import BaseModel
from typing import Dict, List


# --- Families (coarse but practical buckets) -------------------------------

class AutorFamilia(StrEnum):
    PARLAMENTAR = "parlamentar"            # Deputado(a), Senador(a)
    COMISSAO = "comissao"                  # Comissões (permanente, especial, CPI, mista, GT, subcomissão)
    ORGAO_INSTITUCIONAL = "orgao_institucional"  # Órgãos da CD/SF + Executivo/Judiciário/Procuradorias/Secretarias
    PARTIDARIO = "partidario"              # Partido, Bloco
    LIDERANCA = "lideranca"                # Liderança, Bancada (+ entradas históricas como "LIDERANÇA DO PMDB")
    ARTICULACAO = "articulacao_politica"   # Governo/Maioria/Minoria (na CD/CN)
    PLENARIO = "plenario"                  # Plenário Virtual (CD/CN)
    SOCIEDADE_CIVIL = "sociedade_civil"
    GABINETE = "gabinete_parlamentar"
    IMPORTACAO = "importacao"              # Importação de proposições inativas (técnico)
    OUTROS = "outros"


class TipoAutorRef(BaseModel):
    cod: int
    sigla: str = ""          # dataset traz vazio; mantemos por simetria
    nome: str
    descricao: str | None = None
    familia: AutorFamilia = AutorFamilia.OUTROS


TIPOS_AUTOR_BY_COD: Dict[int, TipoAutorRef] = {}
TIPOS_AUTOR_BY_NOME: Dict[str, List[TipoAutorRef]] = {}  # nome normalizado -> many


# --- Loader ----------------------------------------------------------------

def add_tipo_autor(item: dict):
    ref = TipoAutorRef(
        **item,
        familia=infer_autor_familia(int(item["cod"]), item.get("nome", ""))
    )
    TIPOS_AUTOR_BY_COD.setdefault(ref.cod, ref)
    key = normalize_nome(ref.nome)
    TIPOS_AUTOR_BY_NOME.setdefault(key, []).append(ref)


def bulk_load_tipos_autor(items: List[dict]):
    for it in items:
        add_tipo_autor(it)


# --- Classifier ------------------------------------------------------------

def infer_autor_familia(cod: int, nome: str) -> AutorFamilia:
    n = normalize_nome(nome)

    # 1) Exact codes first (most reliable)
    if cod in {10000, 20000}:                        # Deputado(a), Senador(a)
        return AutorFamilia.PARLAMENTAR
    if cod in {101, 81009}:                          # Partido Político
        return AutorFamilia.PARTIDARIO
    if cod in {102, 80000, 81000, 9000}:             # Bloco, Liderança, Bancada (+ histórica PMDB)
        return AutorFamilia.LIDERANCA
    if cod in {103, 104, 105, 106, 121, 122, 123, 124}:  # Governo/Maioria/Minoria (CD/CN)
        return AutorFamilia.ARTICULACAO
    if cod in {26, 27, 81001}:                        # Plenário Virtual
        return AutorFamilia.PLENARIO
    if cod == 70000:
        return AutorFamilia.SOCIEDADE_CIVIL
    if cod == 81005:
        return AutorFamilia.GABINETE
    if cod == 1000:
        return AutorFamilia.IMPORTACAO
    if cod in {
        12000, 22000, 30000, 40000, 50000, 81006, 81007, 81008
    }:
        return AutorFamilia.ORGAO_INSTITUCIONAL

    # 2) Commission universe (codes commonly used + name heuristics)
    if cod in {
        1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 20, 21, 22, 25, 28, 110, 13000, 21000, 81002, 81003, 81004
    }:
        return AutorFamilia.COMISSAO
    if any(word in n for word in [
        "COMISSÃO", "SUBCOMISSÃO", "CPI", "COMISSÃO MISTA",
        "GRUPO DE TRABALHO", "GT"
    ]):
        return AutorFamilia.COMISSAO

    # 3) Institutional bodies by name (covers Procuradoria/Corregedoria/etc.)
    if any(word in n for word in [
        "ÓRGÃO", "PROCURADORIA", "CORREGEDORIA", "OUVIDORIA", "SECRETARIA"
    ]):
        return AutorFamilia.ORGAO_INSTITUCIONAL

    # 4) Fallbacks
    return AutorFamilia.OUTROS


def normalize_nome(nome: str) -> str:
    # robust uppercase & trimming; keep diacritics since we match by substrings in PT-BR
    return (nome or "").strip().upper()
