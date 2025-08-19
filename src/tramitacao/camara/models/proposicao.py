from pydantic import BaseModel, computed_field, ValidationError

from .autor import Autor
from .tipo_proposicao import TipoProposicaoRef, TIPOS_BY_COD
from .tramitacao import Tramitacao


class Proposicao(BaseModel):
    id: int
    uri: str
    siglaTipo: str
    codTipo: int
    numero: int | None = None
    ano: int
    ementa: str
    autores: list[Autor] = []
    tramitacoes: list[Tramitacao] = []

    @computed_field(return_type=TipoProposicaoRef)
    @property
    def tipo(self) -> TipoProposicaoRef:
        try:
            ref = TIPOS_BY_COD[self.codTipo]
        except KeyError:
            raise ValidationError([{
                "type": "value_error",
                "loc": ("codTipo",),
                "msg": f"Tipo desconhecido: {self.codTipo}"
            }], Proposicao)
        # Optional safety: ensure sigla matches known cod
        if ref.sigla != self.siglaTipo:
            # you can allow it (data can be messy) or raise
            pass
        return ref

    def __str__(self):
        return f"Proposição Câmara: {self.siglaTipo} {self.numero}/{self.ano}"
