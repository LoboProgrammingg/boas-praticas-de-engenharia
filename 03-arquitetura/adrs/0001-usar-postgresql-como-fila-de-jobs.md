# ADR 1: Usar PostgreSQL como fila de jobs

- **Status:** aceita
- **Data:** 2026-11-06

## Contexto

O sistema precisa executar tarefas em segundo plano: enviar e-mails de confirmação,
gerar relatórios e reprocessar webhooks. O volume atual é de cerca de 2 mil jobs por dia,
com picos de algumas dezenas por minuto. A equipe tem três pessoas e já opera um banco
PostgreSQL gerenciado; não opera nenhum outro serviço com estado.

Duas forças estão em tensão:

- um broker dedicado (por exemplo, Redis ou RabbitMQ) oferece melhor vazão e semântica de
  fila nativa, mas é mais um serviço para monitorar, fazer backup e manter disponível;
- os jobs precisam ser criados **na mesma transação** que altera os dados de negócio. Com um
  broker externo, é preciso resolver o problema de "gravou no banco mas não enfileirou" (ou
  o inverso) com um padrão adicional, como o outbox.

## Decisão

Vamos usar uma tabela `jobs` no PostgreSQL como fila, com consumo por
`SELECT ... FOR UPDATE SKIP LOCKED`. Os jobs são inseridos na mesma transação que a mudança
de negócio que os origina. Cada job tem uma chave de idempotência, e os consumidores devem
ser seguros para reexecução.

## Consequências

Positivas:

- enfileirar e gravar o dado de negócio é atômico, sem outbox;
- nenhum serviço novo para operar, monitorar ou fazer backup;
- a fila é consultável com SQL, o que facilita depuração.

Negativas:

- a vazão tem teto bem abaixo de um broker dedicado; acima de algumas centenas de jobs por
  segundo, a fila passa a competir com o tráfego transacional do mesmo banco;
- jobs concluídos acumulam linhas e exigem rotina de limpeza e acompanhamento de *bloat*;
- não há *backpressure* nem roteamento sofisticado prontos; o que precisarmos, construímos.

Riscos e gatilhos de revisão:

- reavaliar esta decisão se a vazão sustentada passar de 100 jobs por segundo ou se o
  atraso da fila afetar a latência do banco principal. Nesse caso, a mudança para um
  broker deve gerar uma nova ADR que **substitui** esta (esta passa a "substituída").
