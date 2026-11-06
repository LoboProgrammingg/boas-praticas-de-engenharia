"""Funções com argumentos que escondem a intenção.

* ``exportar(linhas, True, False)``: o que significam os dois booleanos? Trocá-los
  continua válido e muda o resultado sem nenhum erro.
* ``aplicar_desconto`` devolve ``None`` e altera a lista do chamador (argumento de
  saída), então quem já guardou os preços originais os perde.
"""

from decimal import Decimal


def exportar(linhas: list[list[str]], csv: bool, cabecalho: bool) -> str:
    separador = "," if csv else " | "
    saida = [separador.join(linha) for linha in linhas]
    if not cabecalho:
        saida = saida[1:]
    return "\n".join(saida)


def aplicar_desconto(precos: list[Decimal], percentual: Decimal) -> None:
    for posicao, preco in enumerate(precos):
        precos[posicao] = preco * (1 - percentual / 100)
