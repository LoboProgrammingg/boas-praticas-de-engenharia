# Comentários

> O nome diz o *quê*; o comentário diz o *porquê*.
> Síntese da recomendação comum aos dois lados do debate

| | |
|---|---|
| **Origem** | Capítulo de comentários de *Clean Code* (Martin, 2008); contraponto em *A Philosophy of Software Design* (Ousterhout, 2018) e no debate público de 2024–2025 |
| **Resolve** | Comentários que repetem o código, que ficam velhos e passam a mentir, e código morto comentado |
| **Em uma frase** | Escreva o que o código não consegue dizer: a razão, a restrição, o contrato |

## O problema

Em [`ruim.py`](ruim.py):

```python
# retorna o valor com 10% de desconto
resultado = valor  # atribui o valor ao resultado
if valor < 5:  # se o valor for menor que 5
    resultado = Decimal(5)  # resultado recebe 5
# resultado = resultado * Decimal("0.9")
```

Três problemas: comentários que só repetem a linha; um comentário que **mente**
(fala em 10% de desconto que o código não aplica, e o [`teste`](test_comentarios.py) prova
isso); e uma linha de código morto comentada. Ninguém sabe por que o piso é 5.

## A solução

Em [`bom.py`](bom.py):

- O comentário vive onde está a **razão**: o gateway recusa cobranças abaixo de R$ 5,00,
  por isso a constante `VALOR_MINIMO_DO_GATEWAY` existe;
- o *quê* é do código e dos nomes (`max(valor, VALOR_MINIMO_DO_GATEWAY)`);
- a *docstring* documenta o contrato público da função.

Código antigo não vai em comentário: o controle de versão guarda o histórico.

## Onde os dois lados concordam, e onde não

No debate de 2024–2025, John Ousterhout considera comentários "cruciais" (para
abstração e para informação que o código não expressa) e quer mais. Martin os chama de
"mal necessário", diz ser contra os gratuitos e não contra todos, e só confia neles depois
de conferir com o código. **Concordam** que APIs públicas precisam de comentário de
interface. O recado prático é o mesmo: comentário bom diz o que o código não diz.

## Quando não aplicar

- **Não use comentário para consertar nome ruim.** Primeiro renomeie
  ([nomes](../nomes/README.md)); comente o que sobrar.
- **Não comente o óbvio**, mas também não corte comentário só porque "bom código se explica":
  restrições externas, decisões e armadilhas não estão no código.
- Comentários velhos são pior que nenhum: revise-os junto com a mudança de código.
- Docstrings de API pública (PEP 257) são documentação, não ruído.

## Relações

- [Nomes](../nomes/README.md) bons dispensam comentários do tipo *quê*.
- Decisões de arquitetura longas pertencem a um registro de decisões (ADR), não a um comentário.
- Em [funções](../funcoes/README.md), a intenção também aparece no nome da função extraída.

## Referências

- Robert C. Martin, *Clean Code*, Prentice Hall, 2008, capítulo 4.
- John Ousterhout e Robert C. Martin, [debate *APOSD* vs *Clean Code*](https://github.com/johnousterhout/aposd-vs-clean-code), seção de comentários, 2024–2025.
- [PEP 257, *Docstring Conventions*](https://peps.python.org/pep-0257/).
- Martin Fowler, [*Code As Documentation*](https://martinfowler.com/bliki/CodeAsDocumentation.html).
