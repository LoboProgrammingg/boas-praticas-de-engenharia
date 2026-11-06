# Observabilidade: traces, métricas e logs com OpenTelemetry

> "Observability lets you understand a system from the outside by letting you ask questions
> about that system without knowing its inner workings."
> OpenTelemetry, *Observability primer*

| | |
|---|---|
| **Origem** | Conceito de teoria de controle adotado em engenharia de software; padronizado pelo projeto OpenTelemetry (CNCF) |
| **Resolve** | Sistemas que falham de formas imprevistas e que só se investigam adicionando código novo e reimplantando |
| **Em uma frase** | Emita sinais correlacionados (traces, métricas, logs) ricos o bastante para responder a perguntas que você ainda não sabe fazer |

## O problema

Em [`ruim.py`](ruim.py), `cobrar` escreve `"iniciando cobrança"` e `"erro ao cobrar"`. Com
três requisições intercaladas, o log tem três linhas iguais; não dá para saber qual
cobrança falhou, quanto demorou ou quantas falharam no total. Monitorar só o que já se
sabe que pode quebrar (um *dashboard* de CPU) não ajuda com o "unknown unknown".

O primer do OpenTelemetry diz que uma aplicação está bem instrumentada quando você não
precisa adicionar mais instrumentação para investigar um problema. E lembra que "um
sistema pode estar 100% no ar" e ainda assim ser inútil para o usuário: por isso medir do
ponto de vista dele (SLIs) importa mais que medir só a máquina.

## A solução

Os sinais do OpenTelemetry:

| Sinal | O que registra | Pergunta que responde |
|---|---|---|
| **Traces** | o caminho de uma requisição entre componentes, como uma árvore de *spans* | Onde o tempo foi gasto? Qual chamada falhou? |
| **Metrics** | medições agregadas em tempo de execução (contadores, histogramas) | Quantas falhas por minuto? Qual o p99 de latência? |
| **Logs** | o registro de um evento pontual | O que exatamente aconteceu nesta requisição? |
| **Baggage** | contexto que viaja com a requisição entre serviços | Quem é o cliente / qual o tenant ao longo do caminho? |

O que torna os sinais úteis é a **correlação**: o mesmo `trace_id` aparece no trace e
no log, de modo que você sai de "a latência subiu" para "esta requisição específica" e
para "esta linha de log".

[`bom.py`](bom.py) é um modelo mínimo, **sem dependências**, desses conceitos:

- `Telemetria.span` abre spans aninhados com `contextvars`, mantendo `trace_id`, `span_id`,
  pai e duração;
- `Telemetria.contar` incrementa uma métrica;
- `FiltroDeTrace` injeta o `trace_id` ativo em cada registro de log.

O [`test_observabilidade.py`](test_observabilidade.py) prova que spans filhos compartilham o
trace e apontam para o pai, que cada requisição tem o seu trace, e que o log produzido
dentro de um span carrega o mesmo `trace_id` (e o de fora, não). Ele usa relógio e gerador
de ids falsos, então é determinístico.

> **Em produção, use o SDK do OpenTelemetry**, não este modelo. Ele traz a propagação de
> contexto entre processos (W3C Trace Context), instrumentação automática de frameworks e
> exportadores padronizados (OTLP). O exemplo existe para mostrar *o que* os sinais são, não
> para substituí-los.

### O que medir

O livro de SRE do Google distingue monitoramento *white-box* (métricas internas e logs) de
*black-box* (o comportamento externo, como o usuário vê) e sugere começar pelos **quatro
sinais dourados**: latência, tráfego, erros e saturação.

## Quando não aplicar

- **Aplicação pequena, de um processo só**: logs estruturados
  ([logs estruturados](../logs-estruturados/README.md)) e algumas métricas bastam; traces
  distribuídos pagam-se quando há várias chamadas entre serviços.
- **Alta cardinalidade em métricas.** Não use `user_id` como rótulo de métrica; isso é papel
  de trace e log. Rótulos ilimitados explodem custo e memória.
- **Observabilidade tem custo** (armazenamento, rede, CPU). Amostre traces e defina retenção.
- **Não registre dados pessoais** em atributos de span ou de log.

## Relações

- Os logs fazem parte do conjunto: [logs estruturados](../logs-estruturados/README.md).
- Alertas de um [circuit breaker](../circuit-breaker/README.md) aberto e de
  [degradação](../degradacao-elegante/README.md) dependem desses sinais.
- Fator XI do [12-Factor](../../03-arquitetura/twelve-factor/README.md): logs como fluxo de eventos.

## Referências

- OpenTelemetry, [*Observability primer*](https://opentelemetry.io/docs/concepts/observability-primer/).
- OpenTelemetry, [*Signals*](https://opentelemetry.io/docs/concepts/signals/).
- Google SRE Book, [*Monitoring Distributed Systems*](https://sre.google/sre-book/monitoring-distributed-systems/).
- W3C, [*Trace Context*](https://www.w3.org/TR/trace-context/).
