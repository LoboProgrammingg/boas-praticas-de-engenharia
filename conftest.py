"""Fixture compartilhada: carrega um exemplo (ex.: ``bom.py``) da pasta do próprio teste.

Cada tópico tem arquivos com o mesmo nome (``ruim.py``, ``bom.py``). Carregar por
caminho, com um nome de módulo único, evita colisões entre pastas.
"""

import importlib.util
import sys
from collections.abc import Callable
from pathlib import Path
from types import ModuleType

import pytest

RAIZ = Path(__file__).parent

type CarregarExemplo = Callable[[str], ModuleType]


@pytest.fixture
def exemplo(request: pytest.FixtureRequest) -> CarregarExemplo:
    pasta = request.path.parent

    def carregar(arquivo: str) -> ModuleType:
        caminho = pasta / arquivo
        partes = caminho.relative_to(RAIZ).with_suffix("").parts
        nome = "exemplo_" + "_".join(partes).replace("-", "_")
        spec = importlib.util.spec_from_file_location(nome, caminho)
        if spec is None or spec.loader is None:
            raise ImportError(f"Não foi possível carregar {caminho}")
        modulo = importlib.util.module_from_spec(spec)
        sys.modules[nome] = modulo
        spec.loader.exec_module(modulo)
        return modulo

    return carregar
