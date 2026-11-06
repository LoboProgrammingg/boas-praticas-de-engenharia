# 07. Design de API

Uma API é um contrato difícil de mudar. Esta seção reúne as decisões que valem a pena tomar
no primeiro dia: descrever a API em um documento legível por máquina, padronizar os erros,
paginar de forma estável e planejar como ela vai evoluir.

| Tópico | O que ensina | Exemplo executável |
|---|---|---|
| [Problem Details (RFC 9457)](problem-details/README.md) | Erros HTTP no formato `application/problem+json` | `ruim.py`, `bom.py`, teste |
| [Paginação](paginacao/README.md) | Cursor (keyset) em vez de offset; AIP-158 | `ruim.py`, `bom.py`, teste |
| [Versionamento](versionamento/README.md) | O modelo do Stripe: versões por data e contas fixadas | `ruim.py`, `bom.py`, teste |
| [OpenAPI](openapi/README.md) | Spec gerada do código, verificada contra as respostas | `ruim.py`, `bom.py`, teste |

## O kit mínimo de uma API pública

1. **OpenAPI** como fonte única da descrição da API.
2. **Problem Details** para todos os erros.
3. **Paginação por cursor** em toda coleção, desde o início (acrescentá-la depois é uma
   mudança incompatível).
4. **Versionamento** planejado, com mudanças aditivas por padrão.
5. **`Idempotency-Key`** em operações que criam recursos (veja
   [idempotência](../06-operabilidade/idempotencia/README.md); o cabeçalho ainda é um
   rascunho do IETF).

## Convenção

Os exemplos seguem o padrão do repositório (`ruim.py`, `bom.py`, `test_<tópico>.py`), usam só
Python, a biblioteca padrão e o Pydantic (já presente no projeto), e simulam respostas HTTP
em processo, sem rede. Rode com `uv run pytest 07-design-de-api`.
