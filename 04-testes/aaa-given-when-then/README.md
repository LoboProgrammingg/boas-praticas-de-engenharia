# AAA e Given-When-Then

> "The given part describes the state of the world before you begin the behavior you're
> specifying... The when section is that behavior that you're specifying... Finally the then
> section describes the changes you expect due to the specified behavior."
> Martin Fowler, *Given When Then*

| | |
|---|---|
| **Origem** | AAA (*Arrange, Act, Assert*): Bill Wake, 2001. Given-When-Then: Daniel Terhorst-North e Chris Matts (BDD), com crédito a Ivan Moore |
| **Resolve** | Testes longos e embaralhados, em que não se vê o que está sendo preparado, exercitado e verificado |
| **Em uma frase** | Todo teste tem três fases visíveis: preparar o cenário, executar **uma** ação, verificar o resultado |

## O problema

Um teste ilegível mistura preparação, ação e verificação em dezenas de linhas, verifica dez
coisas, e o nome (`test_carrinho_1`) não diz qual comportamento quebrou. Quando falha, o
primeiro trabalho é decifrar o teste:

```python
def test_carrinho():
    c = Carrinho()
    c.adicionar(Decimal(60))
    c.adicionar(Decimal(40))
    assert c.total() == 100
    c.aplicar_cupom(Decimal(10))
    assert c.total() == 90
    with pytest.raises(ValueError):
        c.adicionar(Decimal(0))
    assert len(c.itens) == 2
```

São três comportamentos no mesmo teste (total, cupom, validação) e ações e verificações
intercaladas: se a segunda verificação falha, as outras nem rodam.

## A solução

| Fase AAA | Fase BDD | O que faz |
|---|---|---|
| **Arrange** | **Given** | monta o estado inicial (objetos, fixtures, dublês) |
| **Act** | **When** | executa o comportamento sob teste, idealmente **uma** chamada |
| **Assert** | **Then** | verifica o resultado ou o efeito observável |

Fowler descreve Given-When-Then como reformulação do padrão *Four-Phase Test* (setup,
exercise, verify, teardown): *given* são as pré-condições, *when* é o comportamento e
*then* são as mudanças esperadas.

Regras de bolso, todas demonstradas em
[`test_aaa_given_when_then.py`](test_aaa_given_when_then.py):

- **Um teste por comportamento, não por método.** `total()` aparece em três testes,
  um para cada comportamento (vazio, soma, cupom).
- **O nome descreve o comportamento**, em linguagem de domínio:
  `test_dado_dois_itens_quando_aplica_cupom_de_10_por_cento_entao_total_cai_10_por_cento`.
  Quando falha, o nome já diz o que quebrou.
- **Arrange compartilhado vai para fixtures**, e o corpo do teste fica só com o que é
  específico dele (`carrinho_com_dois_itens`).
- **Variações do mesmo comportamento** usam `parametrize`, não `for` dentro do teste: cada
  caso falha e é reportado separadamente.
- **Verifique o efeito, não a implementação.** No caso de erro, o teste também confirma que
  o estado não mudou.
- Linhas em branco (ou comentários `# Arrange`, `# Act`, `# Assert`, usados no primeiro
  exemplo) separam as fases. Se o teste não cabe em três blocos, provavelmente testa mais de
  um comportamento.

## Quando não aplicar

- **Não é uma cerimônia.** Um teste de duas linhas não precisa de comentário em cada fase.
- **Um `when` com várias chamadas é válido** se o comportamento é uma sequência (ex.:
  adicionar, remover, e o total volta a zero); o que importa é que haja uma única
  *razão* para o teste falhar.
- **BDD completo** (arquivos Gherkin com cenários para o negócio) é uma prática maior que
  só o formato Given-When-Then; sem a conversa com o negócio, o ganho some.

## Relações

- Os dublês preparados no *Arrange*: [dublês de teste](../dubles-de-teste/README.md).
- O ciclo [TDD](../tdd/README.md) produz testes neste formato.
- Muitos exemplos de uma regra podem virar uma propriedade em
  [property-based testing](../property-based/README.md).

## Referências

- Martin Fowler, [*Given When Then*](https://martinfowler.com/bliki/GivenWhenThen.html), 2013.
- Bill Wake, [*3A: Arrange, Act, Assert*](https://xp123.com/3a-arrange-act-assert/), 2011.
- Documentação do pytest sobre [fixtures](https://docs.pytest.org/en/stable/how-to/fixtures.html) e [parametrização](https://docs.pytest.org/en/stable/how-to/parametrize.html).
