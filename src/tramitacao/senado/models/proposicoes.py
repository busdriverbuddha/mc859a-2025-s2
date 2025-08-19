from pydantic import BaseModel

from .proposicao import Proposicao


class Proposicoes(BaseModel):
    items: list[Proposicao]
