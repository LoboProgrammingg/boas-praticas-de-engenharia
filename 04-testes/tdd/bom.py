"""Resultado de um ciclo de TDD (veja o README): a soma das parcelas é sempre o total.

O teste que falhou primeiro foi ``soma_das_parcelas == total``. Ele forçou a decisão de
design: distribuir o resto, um centavo por parcela, nas primeiras parcelas.
"""


def parcelar(total_em_centavos: int, parcelas: int) -> list[int]:
    if parcelas <= 0:
        raise ValueError("parcelas deve ser positivo")
    base, resto = divmod(total_em_centavos, parcelas)
    return [base + 1 if indice < resto else base for indice in range(parcelas)]
