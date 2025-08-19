from importlib import resources
import json

from .autor import Autor
from .proposicao import Proposicao
from .proposicoes import Proposicoes
from .tipo_autor import add_tipo_autor
from .tipo_proposicao import add_tipo_proposicao
from .tramitacao import Tramitacao

__all__ = [
    "Autor",
    "Proposicao",
    "Proposicoes",
    "Tramitacao",
]


with resources.open_text('tramitacao.camara.data', 'tipo_proposicao.json') as f:
    data = json.load(f)

    for tipo_data in data:
        add_tipo_proposicao(tipo_data)


with resources.open_text('tramitacao.camara.data', 'tipo_autor.json') as f:
    data = json.load(f)

    for tipo_autor in data:
        add_tipo_autor(tipo_autor)
