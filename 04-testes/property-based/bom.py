"""Compressão por repetição com uma representação sem ambiguidade.

Em vez de uma string, o código é uma sequência de pares ``(caractere, contagem)``. Não há
análise de texto para errar, e a propriedade ``decodificar(codificar(x)) == x`` vale para
qualquer entrada.
"""

type Codigo = list[tuple[str, int]]


def codificar(texto: str) -> Codigo:
    codigo: Codigo = []
    for caractere in texto:
        if codigo and codigo[-1][0] == caractere:
            codigo[-1] = (caractere, codigo[-1][1] + 1)
        else:
            codigo.append((caractere, 1))
    return codigo


def decodificar(codigo: Codigo) -> str:
    return "".join(caractere * contagem for caractere, contagem in codigo)
