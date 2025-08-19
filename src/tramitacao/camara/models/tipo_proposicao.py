from enum import StrEnum
from pydantic import BaseModel


class TipoFamilia(StrEnum):
    PROJETO = "projeto"       # PL, PLP, PEC, MPV, PDL/PDC, etc.
    EMENDA = "emenda"         # EMC, EMP, EML, EMR, ERD, ...
    REQUERIMENTO = "requerimento"  # REQ, RPD, DTQ, etc.
    PARECER = "parecer"       # PAR, PRL, PPP, RLF, ...
    MENSAGEM = "mensagem"     # MSC, MSG, MSF, ...
    DOCUMENTO = "documento"   # DOC, ATA, REL, ...
    OUTROS = "outros"


class TipoProposicaoRef(BaseModel):
    cod: int
    sigla: str
    nome: str
    descricao: str | None = None
    familia: TipoFamilia = TipoFamilia.OUTROS  # you can fill this via a small mapping


TIPOS_BY_COD: dict[int, TipoProposicaoRef] = {}
TIPOS_BY_SIGLA: dict[str, list[TipoProposicaoRef]] = {}  # note: sigla -> many


def add_tipo_proposicao(item: dict):
    ref = TipoProposicaoRef(**item, familia=infer_familia(item["sigla"]))
    TIPOS_BY_COD.setdefault(ref.cod, ref)
    TIPOS_BY_SIGLA.setdefault(ref.sigla, []).append(ref)


def infer_familia(sigla: str) -> TipoFamilia:
    s = sigla.upper()
    if s in {"PL", "PLP", "PLC", "PLS", "PLN", "PDL", "PDC", "PDS", "PRC", "PRN", "MPV"}:
        return TipoFamilia.PROJETO
    if s.startswith(("EM", "ERD", "EMA", "EMC", "EMP", "EMR", "EML", "ESP", "SSP", "SBE", "SBT")):
        return TipoFamilia.EMENDA
    if s in {"REQ", "RPD", "DTQ", "DTN", "DTS", "DVT", "RPD", "RPDR"}:
        return TipoFamilia.REQUERIMENTO
    if s in {"PAR", "PRL", "PPP", "PRR", "PRV", "PRLP", "PPR", "PEP", "PES", "PSS", "RLF", "RLP"}:
        return TipoFamilia.PARECER
    if s in {"MSC", "MSG", "MSF", "MTC", "MCN", "OFN", "OFS", "OF"}:
        return TipoFamilia.MENSAGEM
    if s in {"DOC", "ATA", "REL", "AV", "AVN", "AA"}:
        return TipoFamilia.DOCUMENTO

    return TipoFamilia.OUTROS
