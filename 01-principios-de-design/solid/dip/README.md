# DIP: Princípio da Inversão de Dependência

> "Módulos de alto nível não devem depender de módulos de baixo nível. Ambos devem
> depender de abstrações."
> Robert C. Martin

| | |
|---|---|
| **Origem** | Robert C. Martin, *The Dependency Inversion Principle*, C++ Report (junho de 1996) |
| **Resolve** | Regras de negócio presas a detalhes (relógio, banco, HTTP) e, por isso, difíceis de testar e de trocar |
| **Em uma frase** | A política declara o que precisa; o detalhe se adapta e é injetado de fora |

## O problema

Em [`ruim.py`](ruim.py), `Cupom.esta_expirado` chama `datetime.now()` por conta
própria. A regra é simples, mas o teste fica refém da data em que roda: não há como
verificar a borda "um minuto antes de expirar" sem manipular o relógio do sistema ou
fazer monkeypatch.

## A solução

Em [`bom.py`](bom.py), a regra depende de uma **porta** (`Relogio`, um `Protocol`).
Em produção entra o `RelogioDoSistema`; no teste, um `RelogioFixo` torna as duas bordas
determinísticas. A dependência foi **invertida**: o detalhe (relógio real) é que se
adapta ao contrato definido pela regra.

## Quando não aplicar

- Não abstraia o que é estável e local (`math`, `Decimal`, `timedelta`). Uma interface
  com uma única implementação para sempre é indireção sem retorno.
- Abstraia o que é **não determinístico** (tempo, aleatoriedade), **externo** (banco,
  rede, filas) ou **variável** entre ambientes.

## Relações

- É a **Dependency Rule** da Clean Architecture e o coração de Ports & Adapters (seção 03, Arquitetura).
- Interfaces pequenas (**ISP**) tornam as portas fáceis de implementar.
- Habilita **dublês de teste** sem mocks de módulo.

## Referências

- Robert C. Martin, *The Dependency Inversion Principle*, C++ Report, 1996.
- Robert C. Martin, [*The Clean Architecture*](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html), 2012.
