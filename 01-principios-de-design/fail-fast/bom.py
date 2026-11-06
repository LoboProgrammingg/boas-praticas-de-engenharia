"""Fail fast: valida na borda e falha na hora, com mensagem que aponta a causa.

Só o *ausente* tem padrão explícito e documentado. Valor presente e inválido nunca
é adivinhado.
"""

from collections.abc import Mapping

PORTA_PADRAO = 8080


class ConfiguracaoInvalidaError(ValueError):
    pass


def ler_porta(ambiente: Mapping[str, str]) -> int:
    bruto = ambiente.get("PORT")
    if bruto is None:
        return PORTA_PADRAO
    try:
        porta = int(bruto)
    except ValueError as erro:
        raise ConfiguracaoInvalidaError(f"PORT deve ser um inteiro, recebido {bruto!r}") from erro
    if not 1 <= porta <= 65535:
        raise ConfiguracaoInvalidaError(f"PORT fora do intervalo 1-65535: {porta}")
    return porta
