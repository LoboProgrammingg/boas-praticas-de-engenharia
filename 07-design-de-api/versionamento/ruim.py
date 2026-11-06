"""Mudança incompatível feita no lugar: quem integrou antes quebra sem aviso.

O campo ``name`` virou ``full_name`` e o saldo (``balance``) deixou de ser um inteiro em
centavos para virar um objeto. Todo cliente que já lia ``name`` e somava o saldo passa a
falhar no mesmo instante em que o servidor é implantado.
"""


def obter_cliente(cliente_id: str) -> dict[str, object]:
    return {
        "id": cliente_id,
        "full_name": "Ana Souza",
        "balance": {"amount": 1000, "currency": "BRL"},
    }
