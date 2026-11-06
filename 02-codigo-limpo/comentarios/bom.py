"""Comentários que dizem o *porquê*, e nomes que dizem o *quê*."""

from decimal import Decimal

# O gateway de pagamentos recusa cobranças abaixo de R$ 5,00 (regra do contrato
# com o fornecedor), então valores menores são elevados ao mínimo em vez de falhar
# no momento do pagamento.
VALOR_MINIMO_DO_GATEWAY = Decimal("5.00")


def valor_cobravel(valor: Decimal) -> Decimal:
    """Valor a enviar ao gateway: o próprio valor, nunca menos que o mínimo aceito."""
    return max(valor, VALOR_MINIMO_DO_GATEWAY)
