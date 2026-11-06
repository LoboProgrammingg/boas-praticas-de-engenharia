# YAGNI: You Aren't Gonna Need It

> "You Aren't Gonna Need It."
> Mantra de Extreme Programming

| | |
|---|---|
| **Origem** | Extreme Programming, em conversa entre Kent Beck e Chet Hendrickson no projeto C3; ligado à prática de *Simple Design* |
| **Resolve** | Funcionalidade construída para um futuro presumido que nunca chega, ou chega diferente |
| **Em uma frase** | Não construa agora capacidade que ninguém precisa agora |

## O problema

Martin Fowler chama de *presumptive feature* o recurso feito por antecipação e aponta
quatro custos: **construir** (esforço de algo que pode ficar sem uso), **adiar** (valor
perdido por não fazer outra coisa antes), **carregar** (a complexidade extra atrapalha
toda mudança seguinte) e **reparar** (o recurso foi feito sobre um entendimento que
ficou velho).

Em [`ruim.py`](ruim.py) há interface de gateway, registro e fábrica para suportar "N
gateways", mas existe um só. Até para cobrar R$ 10,00 é preciso registrar o gateway
antes, ou a chamada falha com `KeyError`.

## A solução

[`bom.py`](bom.py) tem uma função concreta, `cobrar`, e continua validando a entrada.
Quando o segundo gateway for real, extrai-se a interface a partir de dois casos
concretos, e não de um palpite. O [`teste`](test_yagni.py) mostra a cerimônia da versão
ruim e a validação que a versão boa mantém.

## Quando não aplicar

Fowler delimita o que YAGNI **não** cobre:

- **Práticas que tornam o software fácil de mudar**: testes automatizados, integração
  contínua, refatoração, nomes claros. Sem elas, YAGNI vira dívida.
- **Saúde do código.** YAGNI não é desculpa para deixar o código apodrecer.
- **Decisões caras de reverter**, como o formato de uma API pública: a Google exige
  paginação desde a primeira versão porque adicioná-la depois é uma mudança incompatível
  ([AIP-158](https://google.aip.dev/158)). Aqui vale analisar antes.

## Relações

- Aliado de [KISS](../kiss/README.md) e de [DRY/AHA](../dry-e-aha/README.md) (Rule of Three).
- Em tensão com OCP e com [DIP](../solid/dip/README.md) quando as abstrações são criadas sem uma segunda implementação.
- Complementa "revela intenção, sem duplicação, menos elementos" das regras de Beck.

## Referências

- Martin Fowler, [*Yagni*](https://martinfowler.com/bliki/Yagni.html), 2015.
- Martin Fowler, [*Beck Design Rules*](https://martinfowler.com/bliki/BeckDesignRules.html), 2015.
- Google, [AIP-158: Paginação](https://google.aip.dev/158).
