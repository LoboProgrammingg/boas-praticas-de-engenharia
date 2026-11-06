# 06. Operabilidade

Em sistemas distribuídos, falhas parciais são normais: a rede perde respostas, um serviço
fica lento, uma dependência cai. Esta seção reúne os padrões que mantêm um sistema
funcionando e diagnosticável nessas condições. Eles se combinam: **timeout curto, retry
limitado com jitter, só para operações idempotentes, circuit breaker para não insistir, e
um fallback explícito e observável**.

| Tópico | O que ensina | Exemplo executável |
|---|---|---|
| [Observabilidade](observabilidade/README.md) | Traces, métricas e logs correlacionados (OpenTelemetry) | `ruim.py`, `bom.py`, teste |
| [Logs estruturados](logs-estruturados/README.md) | Um evento por linha, em JSON, sem dados pessoais | `ruim.py`, `bom.py`, teste |
| [Timeouts, retries e backoff](timeouts-retries-backoff/README.md) | Backoff exponencial com jitter; quando **não** repetir | `ruim.py`, `bom.py`, teste |
| [Circuit breaker](circuit-breaker/README.md) | Parar de chamar um fornecedor que está falhando | `ruim.py`, `bom.py`, teste |
| [Idempotência](idempotencia/README.md) | `Idempotency-Key` e retries sem efeito duplicado | `ruim.py`, `bom.py`, teste |
| [Degradação elegante](degradacao-elegante/README.md) | Entregar uma versão reduzida em vez de um erro | `ruim.py`, `bom.py`, teste |

## Como as peças se encaixam

```mermaid
flowchart LR
    Chamada["Chamada remota"] --> Timeout["Timeout"]
    Timeout --> Retry["Retry com jitter<br/>(só idempotente)"]
    Retry --> Breaker["Circuit breaker"]
    Breaker -->|aberto ou esgotado| Fallback["Degradação elegante"]
    Breaker -. "sinais" .-> Obs["Logs + métricas + traces"]
    Fallback -. "sinais" .-> Obs
```

A composição é uma síntese: cada fonte descreve uma peça (AWS Builders' Library para
timeout, retry e jitter; Fowler para o circuit breaker; o livro de SRE para degradação). A
ordem acima é uma orientação, não um padrão normativo, e cada peça tem custos e momentos em
que **não** deve ser usada, descritos na seção "Quando não aplicar" de cada página.

## Convenção

Os exemplos seguem o padrão do repositório (`ruim.py`, `bom.py`, `test_<tópico>.py`) e são
determinísticos: relógios, `sleep` e geradores aleatórios são injetados, então nenhum teste
espera de verdade. Rode com `uv run pytest 06-operabilidade`.
