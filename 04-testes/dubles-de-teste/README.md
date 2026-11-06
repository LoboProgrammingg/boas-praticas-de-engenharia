# Dublês de teste (Test Doubles)

> "Test Double is a generic term for any case where you replace a production object for
> testing purposes."
> Martin Fowler, *Test Double*, a partir do vocabulário de Gerard Meszaros

| | |
|---|---|
| **Origem** | Gerard Meszaros, *xUnit Test Patterns* (2007); resumo de Martin Fowler (2006) |
| **Resolve** | Testes lentos, não determinísticos ou frágeis por dependerem de banco, rede, relógio e e-mail reais |
| **Em uma frase** | Troque a dependência real por um objeto de teste do tipo certo, e prefira **fakes** a mocks de interação |

## O problema

Em [`ruim.py`](ruim.py), o repositório real teve o método renomeado de `adicionar` para
`salvar`, e o caso de uso `Cadastrar` ainda chama `adicionar`. O teste usa `Mock()`, que
aceita qualquer chamada, e confere que `adicionar` foi chamado: **verde**. Com o repositório
real, o mesmo código levanta `AttributeError`. O teste duplica a implementação e nunca a
confrontou com a realidade; os dois testes de [`test_dubles_de_teste.py`](test_dubles_de_teste.py)
que mostram o problema rodam lado a lado.

Fowler, em *Mocks Aren't Stubs*, descreve dois estilos: o **clássico**, que verifica o
**estado** depois da ação, e o **mockista**, que verifica as **interações** (quem chamou o
quê). O segundo acopla o teste à implementação: refatorações que preservam o comportamento
quebram o teste.

## A solução

A taxonomia de Meszaros, com um exemplo de cada tipo em [`bom.py`](bom.py):

| Tipo | O que é | Em `bom.py` |
|---|---|---|
| **Dummy** | preenche um parâmetro que nunca é usado | `NotificadorNulo` |
| **Stub** | devolve respostas prontas | `RelogioFixo` |
| **Fake** | implementação funcional com atalho (ex.: banco em memória) | `RepositorioEmMemoria` |
| **Spy** | stub que também registra as chamadas | `NotificadorEspiao` |
| **Mock** | tem expectativas pré-programadas e falha se chamado diferente | `create_autospec` sobre a porta |

Orientações:

1. **Prefira Fake a Mock de interação.** O fake tem comportamento real (rejeita e-mail
   duplicado, devolve o que foi salvo); o teste verifica o **resultado**, não o roteiro de
   chamadas, e sobrevive a refatorações.
2. **Use Stub para o que é não determinístico**, como relógio e gerador de id: o teste
   deixa de depender da hora do dia.
3. **Use Spy ou Mock para efeitos que são o ponto**, como "o e-mail de boas-vindas foi
   enviado". Aí a interação é o comportamento observável.
4. **Dublês tipados contra uma porta.** O dublê implementa o `Protocol`, de modo que
   `mypy --strict` acusa a renomeação do exemplo ruim. Quando precisar de `Mock`, use
   `create_autospec(Porta, instance=True)`: ele recusa métodos que a porta não tem.
5. **Dublês não substituem integração.** Garanta que o fake e a implementação real se
   comportam igual com [testes de contrato](../testes-de-contrato/README.md), e mantenha
   alguns testes com a dependência real.

## Quando não aplicar

- **Não duble o que você controla e é barato.** Objetos de valor e funções puras entram no
  teste de verdade. Dublar tudo produz testes que só verificam os próprios dublês.
- **Não duble tipos que você não possui** (ex.: o cliente HTTP de uma biblioteca) diretamente
  nos testes do domínio: crie uma porta sua e duble a porta.
- **Mocks de interação** são legítimos quando a interação é o requisito; evite-os para
  verificar passos internos.

## Relações

- Portas pequenas (DIP) são o que permite trocar o real pelo dublê:
  [`../../03-arquitetura/camadas-hexagonal-clean`](../../03-arquitetura/camadas-hexagonal-clean/README.md).
- A fase *Arrange* de [AAA](../aaa-given-when-then/README.md) é onde os dublês são montados.
- O fake e o real devem concordar: [testes de contrato](../testes-de-contrato/README.md).

## Referências

- Martin Fowler, [*Test Double*](https://martinfowler.com/bliki/TestDouble.html), 2006.
- Martin Fowler, [*Mocks Aren't Stubs*](https://martinfowler.com/articles/mocksArentStubs.html), 2007.
- Gerard Meszaros, *xUnit Test Patterns: Refactoring Test Code*, Addison-Wesley, 2007.
- Python, [`unittest.mock.create_autospec`](https://docs.python.org/3/library/unittest.mock.html#unittest.mock.create_autospec).
