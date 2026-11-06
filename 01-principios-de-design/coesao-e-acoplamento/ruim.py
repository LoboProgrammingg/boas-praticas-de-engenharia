"""Baixa coesão e alto acoplamento: uma classe ``Utils`` com tudo que não coube em outro lugar.

* Baixa coesão: formatar CPF, enviar SMS e calcular frete não têm nada em comum.
* Alto acoplamento: ``enviar_sms`` escreve num estado global, então todo código que
  usa ``Utils`` depende, sem saber, do mesmo estado compartilhado.
"""

from decimal import Decimal

SMS_ENVIADOS: list[tuple[str, str]] = []


class Utils:
    @staticmethod
    def formatar_cpf(numero: str) -> str:
        return f"{numero[:3]}.{numero[3:6]}.{numero[6:9]}-{numero[9:]}"

    @staticmethod
    def enviar_sms(telefone: str, mensagem: str) -> None:
        SMS_ENVIADOS.append((telefone, mensagem))

    @staticmethod
    def calcular_frete(distancia_em_km: int) -> Decimal:
        return Decimal("10") + Decimal("0.5") * distancia_em_km
