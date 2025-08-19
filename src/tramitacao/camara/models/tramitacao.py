from pydantic import BaseModel
from datetime import datetime


class Tramitacao(BaseModel):
    dataHora: datetime
    sequencia: int
    siglaOrgao: str
    uriOrgao: str
    uriUltimoRelator: str | None = None
    regime: str | None = None
    descricaoTramitacao: str
    codTipoTramitacao: int
    descricaoSituacao: str | None = None
    codSituacao: int | None = None
    despacho: str
    url: str | None = None
    ambito: str
    apreciacao: str
