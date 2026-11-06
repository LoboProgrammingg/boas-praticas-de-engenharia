# Composição sobre herança

> "Favor object composition over class inheritance."
> Gamma, Helm, Johnson e Vlissides, *Design Patterns*, 1994

| | |
|---|---|
| **Origem** | Máxima do livro *Design Patterns* (GoF, 1994), que trata herança e composição como técnicas que "trabalham de mãos dadas" |
| **Resolve** | Hierarquias rígidas, criadas só para reaproveitar código, que se multiplicam a cada combinação de comportamentos |
| **Em uma frase** | Para reaproveitar comportamento, monte objetos que se encaixam; reserve a herança para relações "é-um" estáveis |

## O problema

Em [`ruim.py`](ruim.py), a lógica de reenvio nasceu em `NotificadorSmtpComReenvio`, uma
subclasse. O SMS não herda de SMTP, então não tem como ganhar reenvio sem outra
subclasse com o laço copiado. Se depois vier "reenvio com registro", são mais classes
(SMTP+registro, SMS+registro, SMTP+reenvio+registro...). A herança fixou o
comportamento em tempo de escrita e o amarrou a uma classe-pai.

## A solução

Em [`bom.py`](bom.py), `ComReenvio` e `ComRegistro` são decoradores: recebem qualquer
`Notificador` (um `Protocol` de um método) e têm a mesma interface. A combinação sai da
montagem:

```python
notificador = ComRegistro(ComReenvio(NotificadorSms()), registro)
```

O [`teste`](test_composicao_sobre_heranca.py) dá reenvio ao SMS sem tocar em uma linha
dele, respeita o limite de tentativas e empilha comportamentos. Até o simulador de falhas
usado pelos dois canais é compartilhado por composição.

## Quando não aplicar

- **Herança continua certa** para relações "é-um" estáveis e compatíveis com o contrato
  da classe-pai (LSP): hierarquias de exceção, classes base de frameworks que pedem
  subclasse.
- A Wikipedia registra que muitos problemas fáceis com herança ficam difíceis só com
  composição (encaminhar dezenas de métodos à mão, por exemplo).
- Não crie um `Protocol` e três decoradores para um comportamento usado em um lugar
  só ([YAGNI](../yagni/README.md)). No exemplo, o reenvio real também precisaria de
  espera crescente entre tentativas e de operação idempotente.

## Relações

- Exige o contrato de [LSP](../solid/lsp/README.md) bem definido: o decorador é substituível pelo objeto interno.
- Habilita [DIP](../solid/dip/README.md) e OCP: novos comportamentos entram sem alterar as classes existentes.
- Compare com [Lei de Demeter](../lei-de-demeter/README.md): objetos compostos escondem a estrutura interna.

## Referências

- [Wikipedia: Composition over inheritance](https://en.wikipedia.org/wiki/Composition_over_inheritance).
- Gamma, Helm, Johnson, Vlissides, *Design Patterns: Elements of Reusable Object-Oriented Software*, Addison-Wesley, 1994 (a máxima é o segundo princípio de design da introdução).
- Brandon Rhodes, [*The Composition Over Inheritance Principle*](https://python-patterns.guide/gang-of-four/composition-over-inheritance/), com a discussão aplicada a Python.
