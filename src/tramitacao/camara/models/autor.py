from pydantic import BaseModel


class Autor(BaseModel):
    uri: str
    nome: str
    codTipo: int
    tipo: str
    ordemAssinatura: int
    proponente: int
