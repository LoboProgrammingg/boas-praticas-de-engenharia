"""Funções que dizem o que fazem, no nível de abstração do chamador.

* Um formato por função; o único booleano restante é nomeado na chamada.
* O desconto devolve valores novos (retorno, não argumento de saída).
"""

from collections.abc import Sequence
from decimal import Decimal


def exportar_csv(linhas: Sequence[Sequence[str]], *, com_cabecalho: bool = True) -> str:
    return _juntar(linhas, ",", com_cabecalho)


def exportar_tabela(linhas: Sequence[Sequence[str]], *, com_cabecalho: bool = True) -> str:
    return _juntar(linhas, " | ", com_cabecalho)


def precos_com_desconto(precos: Sequence[Decimal], percentual: Decimal) -> tuple[Decimal, ...]:
    return tuple(preco * (1 - percentual / 100) for preco in precos)


def _juntar(linhas: Sequence[Sequence[str]], separador: str, com_cabecalho: bool) -> str:
    selecionadas = linhas if com_cabecalho else linhas[1:]
    return "\n".join(separador.join(linha) for linha in selecionadas)
