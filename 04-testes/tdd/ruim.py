"""Código escrito "no olho", sem um teste que forçasse a pergunta difícil.

``parcelar`` divide um valor em centavos em ``n`` parcelas iguais. Para 100 em 3 parcelas
devolve 33 + 33 + 33 = 99: um centavo some.
"""


def parcelar(total_em_centavos: int, parcelas: int) -> list[int]:
    return [total_em_centavos // parcelas] * parcelas
