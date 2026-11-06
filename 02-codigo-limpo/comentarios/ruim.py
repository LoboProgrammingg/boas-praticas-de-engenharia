"""Comentários que repetem o código, comentário que mente e código morto comentado."""

from decimal import Decimal


def valor_cobravel(valor: Decimal) -> Decimal:
    # retorna o valor com 10% de desconto
    resultado = valor  # atribui o valor ao resultado
    if valor < 5:  # se o valor for menor que 5
        resultado = Decimal(5)  # resultado recebe 5
    # resultado = resultado * Decimal("0.9")
    return resultado
