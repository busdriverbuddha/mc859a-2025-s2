from datetime import datetime

from pydantic import BaseModel


class Proposicao(BaseModel):
    id: int
    codigoMateria: int
    identificacao: str
    apelido: str | None = None
    objetivo: str | None = None
    casaIdentificadora: str
    enteIdentificador: str
    tipoConteudo: str
    ementa: str
    tipoDocumento: str
    dataApresentacao: datetime
    autoria: str
    tramitando: str
    dataDeLiberacao: datetime | None = None
    siglaTipoDeliberacao: str | None = None
    normaGerada: str | None = None
    urlDocumento: str | None = None
