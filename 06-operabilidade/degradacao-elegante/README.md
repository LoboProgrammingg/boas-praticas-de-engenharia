# Degradação elegante (graceful degradation)

> "Graceful degradation takes the concept of load shedding one step further by reducing the
> amount of work that needs to be performed. In some applications, it's possible to
> significantly decrease the amount of work or time needed by decreasing the quality of
> responses."
> Google SRE Book, *Addressing Cascading Failures*

| | |
|---|---|
| **Origem** | Prática de engenharia de confiabilidade; descrita no livro de SRE do Google (*Addressing Cascading Failures* e *Handling Overload*) |
| **Resolve** | Uma dependência não essencial falha e derruba uma funcionalidade inteira que poderia continuar funcionando de forma reduzida |
| **Em uma frase** | Quando uma parte falha, entregue uma versão reduzida e honesta do resultado em vez de um erro, e deixe isso visível |

## O problema

Em [`ruim.py`](ruim.py), as recomendações são um enfeite da página inicial, mas
`pagina_inicial` propaga a exceção do serviço de recomendação. O usuário não vê a página
só porque o enfeite falhou: um problema pequeno vira indisponibilidade.

O erro oposto também existe: `except Exception: pass`, que engole tudo. A página "funciona",
mas ninguém sabe que está degradada, e bugs de verdade ficam escondidos. O Zen do Python
resume: "Errors should never pass silently. Unless explicitly silenced."

## A solução

Decida de antemão **o que é essencial e o que é opcional**, e defina a alternativa para o
que é opcional. Em [`bom.py`](bom.py), `PaginaInicial.montar`:

1. chama o recomendador;
2. se falhar com um erro **esperado** (`DependenciaIndisponivelError`), usa a melhor alternativa, na
   ordem: **(a)** as últimas recomendações boas daquele usuário (defasadas, mas
   personalizadas) e **(b)** uma lista de itens populares;
3. devolve `degradada=True` para a camada acima poder sinalizar isso (um selo, outro
   cache, outro TTL);
4. emite um log `recomendacoes_degradadas` com o motivo, para que a degradação seja
   **observável** (alerta, métrica, painel);
5. deixa passar qualquer outro erro: um `TypeError` é bug e deve aparecer.

O [`test_degradacao_elegante.py`](test_degradacao_elegante.py) cobre as cinco situações.

Estratégias comuns de degradação:

| Estratégia | Exemplo |
|---|---|
| Cache defasado (*stale*) | mostrar o último catálogo conhecido |
| Resposta genérica | itens populares no lugar de personalizados |
| Funcionalidade reduzida | buscar em um subconjunto, ou ranking mais simples |
| Desligar o opcional | esconder o bloco de recomendações |
| Enfileirar para depois | aceitar o pedido e processar o resto de forma assíncrona |

Segundo o livro de SRE, degradar é "servir resultados de menor qualidade e mais baratos de
calcular" quando o sistema está sob carga ou com partes fora do ar. Ela é a resposta
natural a um [circuit breaker](../circuit-breaker/README.md) aberto: o `DependenciaIndisponivelError`
do exemplo é exatamente o que o chamador converteria de `CircuitoAbertoError` ou de um
timeout.

## Quando não aplicar

- **Dependência essencial.** Se o dado é parte do contrato (saldo da conta, preço no
  checkout), um valor defasado ou genérico pode ser pior que um erro. Falhe de forma clara.
  Cobrança, por exemplo, nunca deve "degradar" para uma cobrança aproximada.
- **Degradação silenciosa.** Se o fallback não é logado nem medido, você passa a operar
  em modo degradado sem saber. Meça quanto tempo está em fallback.
- **Fallback sem teste.** O caminho alternativo raramente executa em produção e costuma
  quebrar justamente quando necessário; exercite-o (como nos testes deste exemplo, ou com
  injeção de falhas).
- **Cuidado com o cache velho** de dados sensíveis (permissões, preços): a defasagem tem que
  ser aceitável para o negócio, e deve haver limite de idade.

*Observação sobre fontes:* o livro de SRE trata a degradação no contexto de carga e falha
em cascata; o exemplo daqui, com cache defasado e itens populares, é uma aplicação
ilustrativa do conceito, não uma receita extraída de uma fonte única.

## Relações

- [Circuit breaker](../circuit-breaker/README.md) decide quando parar de chamar; a
  degradação decide o que responder.
- [Timeouts e retries](../timeouts-retries-backoff/README.md): o fallback entra quando as
  tentativas acabam.
- [Logs estruturados](../logs-estruturados/README.md) e [observabilidade](../observabilidade/README.md)
  tornam a degradação visível.

## Referências

- Google SRE Book, [*Addressing Cascading Failures*](https://sre.google/sre-book/addressing-cascading-failures/) (seção Load Shedding and Graceful Degradation).
- Google SRE Book, [*Handling Overload*](https://sre.google/sre-book/handling-overload/).
- Tim Peters, [PEP 20: The Zen of Python](https://peps.python.org/pep-0020/).
