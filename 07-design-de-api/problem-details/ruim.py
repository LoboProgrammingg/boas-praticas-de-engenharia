"""Erro como sucesso: status 200, formato inventado e detalhes internos expostos.

* Todo erro volta com ``200 OK``: caches, proxies, clientes HTTP genéricos e monitoramento
  tratam como sucesso.
* O formato ``{"error": ...}`` é próprio desta API; cada cliente precisa conhecê-lo.
* ``str(erro)`` pode conter SQL, caminhos de arquivo e nomes internos.
"""

from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class Resposta:
    status: int
    cabecalhos: dict[str, str] = field(default_factory=dict)
    corpo: dict[str, object] = field(default_factory=dict)


def tratar(erro: Exception) -> Resposta:
    return Resposta(200, {"Content-Type": "application/json"}, {"error": str(erro)})
