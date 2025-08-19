from importlib import resources
import json

from .proposicao import Proposicao
from .proposicoes import Proposicoes
from .tipo_proposicao import add_tipo
from .tramitacao import Tramitacao

__all__ = [
    "Proposicao",
    "Proposicoes",
    "Tramitacao",
]


with resources.open_text('tramitacao.camara.data', 'tipo_proposicao.json') as f:
    data = json.load(f)

    for tipo_data in data["dados"]:
        add_tipo(tipo_data)
