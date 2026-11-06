"""Erros HTTP no formato Problem Details (RFC 9457), ``application/problem+json``.

Membros padrão: ``type``, ``status``, ``title``, ``detail``, ``instance``. Extensões
específicas do tipo de problema (``balance``, ``errors``...) ficam ao lado deles. O
``status`` do corpo é igual ao status HTTP real. Erros inesperados viram um 500 genérico,
sem detalhes internos.
"""

from dataclasses import dataclass, field
from http import HTTPStatus

TIPO_PADRAO = "about:blank"
MEDIA_TYPE = "application/problem+json"


@dataclass(frozen=True, slots=True)
class Resposta:
    status: int
    cabecalhos: dict[str, str] = field(default_factory=dict)
    corpo: dict[str, object] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class Problema:
    status: int
    tipo: str = TIPO_PADRAO
    titulo: str | None = None
    detalhe: str | None = None
    instancia: str | None = None
    extensoes: dict[str, object] = field(default_factory=dict)

    def como_resposta(self) -> Resposta:
        titulo = self.titulo
        if titulo is None and self.tipo == TIPO_PADRAO:
            titulo = HTTPStatus(self.status).phrase
        padrao: dict[str, object] = {
            "type": self.tipo,
            "title": titulo,
            "status": self.status,
            "detail": self.detalhe,
            "instance": self.instancia,
        }
        corpo = {**self.extensoes, **{k: v for k, v in padrao.items() if v is not None}}
        return Resposta(self.status, {"Content-Type": MEDIA_TYPE}, corpo)


class SaldoInsuficienteError(Exception):
    def __init__(self, saldo: int, necessario: int) -> None:
        super().__init__("saldo insuficiente")
        self.saldo = saldo
        self.necessario = necessario


class DadosInvalidosError(Exception):
    def __init__(self, campo: str, mensagem: str) -> None:
        super().__init__(mensagem)
        self.campo = campo
        self.mensagem = mensagem


def tratar(erro: Exception, instancia: str) -> Resposta:
    if isinstance(erro, SaldoInsuficienteError):
        return Problema(
            status=403,
            tipo="https://api.exemplo.com/problemas/saldo-insuficiente",
            titulo="Saldo insuficiente.",
            detalhe=f"Seu saldo é {erro.saldo}, mas a operação custa {erro.necessario}.",
            instancia=instancia,
            extensoes={"balance": erro.saldo},
        ).como_resposta()
    if isinstance(erro, DadosInvalidosError):
        return Problema(
            status=422,
            tipo="https://api.exemplo.com/problemas/validacao",
            titulo="Os dados enviados são inválidos.",
            instancia=instancia,
            extensoes={"errors": [{"detail": erro.mensagem, "pointer": f"#/{erro.campo}"}]},
        ).como_resposta()
    return Problema(status=500, instancia=instancia).como_resposta()
