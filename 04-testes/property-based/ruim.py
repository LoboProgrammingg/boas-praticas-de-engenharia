"""Compressão por repetição (run-length) com um defeito que exemplos não pegam.

``codificar("aaabcc")`` vira ``"3a1b2c"``. A decodificação lê a contagem com um único
dígito, então quebra com 10 ou mais repetições e com dígitos no texto original. Os três
exemplos clássicos passam.
"""


def codificar(texto: str) -> str:
    saida: list[str] = []
    indice = 0
    while indice < len(texto):
        fim = indice
        while fim < len(texto) and texto[fim] == texto[indice]:
            fim += 1
        saida.append(f"{fim - indice}{texto[indice]}")
        indice = fim
    return "".join(saida)


def decodificar(codigo: str) -> str:
    return "".join(int(codigo[i]) * codigo[i + 1] for i in range(0, len(codigo), 2))
