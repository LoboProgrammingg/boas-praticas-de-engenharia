# Timeouts, retries e backoff com jitter

> "When failures are caused by overload or contention, backing off often doesn't help as
> much as it seems like it should. This is because of correlation. If all the failed calls
> back off to the same time, they cause contention or overload again when they are
> retried. Our solution is jitter."
> Marc Brooker, AWS Builders' Library

| | |
|---|---|
| **Origem** | Marc Brooker, *Exponential Backoff And Jitter* (AWS, 2015) e *Timeouts, retries, and backoff with jitter* (AWS Builders' Library, 2019) |
| **Resolve** | Clientes pendurados em chamadas sem timeout e tempestades de retry sincronizadas que impedem o servidor de se recuperar |
| **Em uma frase** | Dê timeout a toda chamada remota; repita só falhas transitórias de operações idempotentes, com espera exponencial aleatória e limite |

## O problema

Em [`ruim.py`](ruim.py), `com_retry`:

- repete **qualquer** exceção, até um `ValueError` (bug ou validação), cinco vezes;
- espera `2 ** tentativa` segundos, igual para todo mundo: o
  [teste](test_timeouts_retries_backoff.py) com 100 clientes mostra que todos têm
  exatamente a mesma agenda `[1, 2, 4]`. Quando o servidor cai e volta, os cem clientes
  chegam **juntos** nos mesmos instantes e o derrubam de novo (*thundering herd*);
- não dá timeout à operação: uma chamada que nunca responde prende o cliente (e seus
  recursos: threads, conexões, memória) indefinidamente;
- repete operações que mudam estado sem proteção contra duplicidade (ver
  [idempotência](../idempotencia/README.md)).

## A solução

Em [`bom.py`](bom.py), quatro regras:

| Regra | Como |
|---|---|
| **Timeout em toda chamada** | cada tentativa recebe `timeout` e deve respeitá-lo |
| **Backoff exponencial com teto** | espera máxima = `min(teto, base * 2**tentativa)`: 0,1 s, 0,2 s, 0,4 s... até 2 s |
| **Jitter** | a espera é sorteada em `[0, máximo]` ("full jitter"), espalhando os clientes no tempo |
| **Só o que faz sentido repetir** | apenas `FalhaTransitoriaError`, e só se `idempotente=True`; erro permanente sobe imediatamente |

O jitter da AWS tem variações (*Full*, *Equal*, *Decorrelated*). Brooker mostra em
simulação que todas reduzem muito o trabalho comparadas a backoff sem jitter; "Equal" é a
pior das jitteradas, e a escolha entre "Full" e "Decorrelated" é menos clara. Este exemplo
usa *Full Jitter*, o mais simples.

O teste prova cada regra com `dormir` e `sorteio` injetados (nenhum teste dorme de
verdade): as esperas de clientes com sementes diferentes são diferentes; a espera nunca
passa do teto exponencial nem do `teto`; o erro permanente é tentado uma vez; a operação
não idempotente é tentada uma vez; ao esgotar as tentativas, o erro original é propagado.

### Onde repetir

A AWS alerta que retries em várias camadas se multiplicam. Em uma pilha de cinco serviços
com três tentativas em cada camada, a carga no banco sobe 243 vezes (3⁵) quando ele começa
a falhar, tornando a recuperação improvável. Repetir na camada mais alta desperdiça trabalho já feito;
repetir em todas multiplica a carga. Decida **uma** camada responsável por repetir, e limite o
total (por exemplo, com um orçamento de retries, como o *token bucket* que a AWS descreve).

## Quando não aplicar

- **Erros permanentes** (4xx de validação, 401, 404): repetir não muda o resultado.
- **Operações com efeito colateral sem chave de idempotência**: um timeout não significa
  que o efeito não ocorreu. A AWS: APIs com efeitos colaterais "aren't safe to retry unless
  they provide idempotency".
- **Servidor já sobrecarregado**: mais tentativas pioram a carga. Combine com
  [circuit breaker](../circuit-breaker/README.md) ou com um orçamento de retries.
- **Usuário esperando em interface**: o total de esperas deve caber no orçamento de tempo
  da requisição; às vezes é melhor falhar rápido e
  [degradar](../degradacao-elegante/README.md).
- Em produção, prefira biblioteca madura em vez de reimplementar (por exemplo, `tenacity`
  em Python); confira o que já existe no lockfile do projeto.

## Relações

- [Idempotência](../idempotencia/README.md): o que torna o retry seguro.
- [Circuit breaker](../circuit-breaker/README.md): para de chamar quando a falha persiste.
  A AWS observa que breakers introduzem comportamento modal difícil de testar e prefere
  limitar retries localmente; os dois são ferramentas com custos diferentes.
- [Degradação elegante](../degradacao-elegante/README.md): o que fazer quando as tentativas
  acabam.

## Referências

- Marc Brooker, [*Timeouts, retries, and backoff with jitter*](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/), AWS Builders' Library, 2019.
- Marc Brooker, [*Exponential Backoff And Jitter*](https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/), AWS Architecture Blog, 2015.
