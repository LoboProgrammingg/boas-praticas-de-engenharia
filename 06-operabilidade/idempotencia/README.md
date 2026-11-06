# Idempotência e Idempotency-Key

> "A request method is considered 'idempotent' if the intended effect on the server of
> multiple identical requests with that method is the same as the effect for a single such
> request."
> RFC 9110, seção 9.2.2

| | |
|---|---|
| **Origem** | Semântica HTTP (RFC 9110); chaves de idempotência popularizadas por APIs de pagamento; cabeçalho `Idempotency-Key` em rascunho no IETF |
| **Resolve** | O reenvio de uma requisição cuja resposta se perdeu duplica o efeito (cobrança em dobro, pedido duplicado) |
| **Em uma frase** | Faça com que repetir a mesma operação tenha o mesmo efeito de executá-la uma vez |

## O problema

Uma rede perde a resposta, não a requisição. Em [`ruim.py`](ruim.py), o servidor cobrou e o
cliente, sem saber, repete: o [teste](test_idempotencia.py) mostra **duas cobranças**. Um
timeout não diz que o efeito não aconteceu. A AWS resume: "a timeout or failure doesn't
necessarily mean that side effects haven't happened", e APIs com efeitos colaterais "aren't
safe to retry unless they provide idempotency".

Isso é o que torna [retries](../timeouts-retries-backoff/README.md) perigosos para
operações que criam recursos ou movimentam dinheiro.

## A solução

### 1. Métodos HTTP

Pela RFC 9110, `PUT`, `DELETE` e os métodos seguros (`GET`, `HEAD`, `OPTIONS`, `TRACE`) são
idempotentes. `POST` (e `PATCH`) **não** são. O próprio RFC diz que um cliente não deve
repetir automaticamente uma requisição não idempotente. Desenhe a API para que o que for
natural seja idempotente (`PUT /pedidos/{id}` em vez de `POST /pedidos`).

### 2. Chave de idempotência

Quando a operação é um `POST` que cria algo, o cliente envia uma chave única (um UUID) no
cabeçalho `Idempotency-Key`. Em [`bom.py`](bom.py), o servidor:

| Situação | Resposta |
|---|---|
| chave nova | executa, guarda o resultado associado à chave |
| mesma chave, mesmo payload, já concluída | **devolve o resultado guardado**, sem cobrar de novo |
| mesma chave, payload diferente | `ChaveReutilizadaError` (HTTP 422 no rascunho) |
| mesma chave, primeira requisição ainda em andamento | `EmProcessamentoError` (HTTP 409) |
| execução falhou | libera a chave; um novo envio pode tentar de novo |

O teste cobre cada linha, inclusive 32 requisições concorrentes com a mesma chave em
threads: exatamente uma cobrança. O *fingerprint* do payload (hash do corpo) é o que
distingue "reenvio legítimo" de "reutilização indevida da chave".

Em produção, o registro é uma tabela com `UNIQUE(idempotency_key)` e prazo de expiração,
gravada **na mesma transação** que o efeito; um dicionário em memória não sobrevive a
reinício nem a vários processos.

## Status do `Idempotency-Key`: ainda é rascunho

O cabeçalho `Idempotency-Key` está descrito em um **Internet-Draft** do grupo HTTPAPI do
IETF, **não em uma RFC**. Na consulta de **2026-11-06**, a versão vigente era
`draft-ietf-httpapi-idempotency-key-header-08`, de 22 de outubro de 2026, com o estado
"Active Internet-Draft", status pretendido *Standards Track* e expiração em 25 de abril de
2027. Rascunhos podem mudar ou expirar; confira a página do
[datatracker](https://datatracker.ietf.org/doc/draft-ietf-httpapi-idempotency-key-header/)
antes de citar como padrão. Pontos do rascunho usados aqui:

- o valor é um *Structured Header* do tipo string; recomenda-se um UUID ou identificador
  aleatório similar;
- a chave não deve ser reutilizada com outro payload; chave ausente em operação que a exige:
  `400`; payload diferente: `422`; requisição original ainda em andamento: `409`;
- a política de expiração da chave deve ser definida e documentada pelo servidor.

Na prática, o cabeçalho já existe em APIs reais: a seção "Implementation Status" do
rascunho lista implementações existentes, como a do Stripe, e elas podem variar em nome e
semântica em relação ao rascunho.

## Quando não aplicar

- **Operações naturalmente idempotentes** (`PUT` do estado final, `DELETE`, leituras) não
  precisam de chave.
- **Efeitos em sistemas que você não controla** (e-mail, SMS) não ficam idempotentes só
  porque você guardou uma chave: a deduplicação precisa existir no destino, ou o seu lado
  precisa registrar o envio antes de executar.
- **Chave sem expiração** faz o registro crescer sem fim; defina TTL.
- **Não use como substituto de modelagem.** Às vezes a solução é uma restrição de unicidade
  de negócio (um pagamento por pedido), não uma chave do cliente.

## Relações

- [Timeouts, retries e backoff](../timeouts-retries-backoff/README.md): o retry só é seguro
  com operações idempotentes.
- Eventos entregues "pelo menos uma vez" ([CQRS](../../03-arquitetura/cqrs/README.md),
  filas) pedem consumidores idempotentes.
- Erros dessa API devem seguir [Problem Details](../../07-design-de-api/problem-details/README.md).

## Referências

- RFC 9110, [*HTTP Semantics*, seção 9.2.2: Idempotent Methods](https://www.rfc-editor.org/rfc/rfc9110.html#name-idempotent-methods).
- IETF HTTPAPI WG, [*The Idempotency-Key HTTP Header Field* (Internet-Draft)](https://datatracker.ietf.org/doc/draft-ietf-httpapi-idempotency-key-header/); versão 08 em [texto](https://www.ietf.org/archive/id/draft-ietf-httpapi-idempotency-key-header-08.html).
- Marc Brooker, [*Timeouts, retries, and backoff with jitter*](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/), AWS Builders' Library, 2019.
- Stripe, [*Idempotent requests*](https://docs.stripe.com/api/idempotent_requests).
