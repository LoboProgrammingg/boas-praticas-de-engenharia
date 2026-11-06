# DRY e AHA: duplicação de conhecimento versus abstração apressada

> "Every piece of knowledge must have a single, unambiguous, authoritative representation within a system."
> Andrew Hunt e David Thomas, *The Pragmatic Programmer*

| | |
|---|---|
| **Origem** | DRY: Hunt e Thomas, *The Pragmatic Programmer*. A crítica vem de Sandi Metz (*The Wrong Abstraction*, 2016) e de Kent C. Dodds (*AHA Programming*, 2020) |
| **Resolve** | A mesma regra de negócio espalhada, que muda num lugar e fica velha nos outros |
| **Em uma frase** | Elimine a duplicação de *conhecimento*, não a de *texto*; na dúvida, espere a terceira ocorrência |

## O problema

DRY trata de **conhecimento**, não de linhas parecidas, e há dois erros opostos.

1. **Duplicar a regra.** Em [`ruim.py`](ruim.py), `total_do_checkout` e `total_da_fatura`
   escrevem a alíquota `1.17` cada uma. Quando a alíquota mudar, alguém corrige uma e
   esquece a outra.
2. **Fundir o que só parece igual.** `renderizar(usuario, admin=, compacto=, para_email=)`
   junta perfil na tela e assinatura de e-mail numa função com três flags. São oito
   combinações, e algumas nem fazem sentido: `compacto=True` com `para_email=True`
   ignora o `compacto` em silêncio.

Sandi Metz descreve o ciclo: alguém extrai a abstração, um requisito "quase igual"
chega, ganha um parâmetro e um `if`, e o processo se repete até a função ficar
incompreensível. Para ela, duplicação custa muito menos do que a abstração errada.

## A solução

Em [`bom.py`](bom.py):

| Caso | Tratamento |
|---|---|
| Mesma regra de negócio | Uma constante (`ALIQUOTA_ICMS`) e uma função (`com_icms`); mudar a alíquota é mudar uma linha |
| Casos parecidos por acaso | Duas funções pequenas (`renderizar_perfil`, `renderizar_assinatura_de_email`) que evoluem sem se afetar |

O [`teste`](test_dry_e_aha.py) troca a alíquota num único ponto e vê os dois totais
mudarem, e mostra as combinações de flags da versão ruim.

**Regra prática (Rule of Three).** Duplique uma vez, abstraia na terceira ocorrência.
Dodds chama essa postura de AHA (*Avoid Hasty Abstractions*): DRY é bom, mas não
dogma, e o oposto (WET, escrever tudo duas vezes) também não é. A Rule of Three costuma
ser creditada a Don Roberts e divulgada no livro *Refactoring* (informação de fonte
secundária, ver [Wikipedia](https://en.wikipedia.org/wiki/Rule_of_three_(computer_programming))).

## Quando não aplicar

- **Duplicação acidental.** Dois trechos iguais hoje, mas que mudam por motivos
  diferentes, devem continuar separados.
- **Entre serviços ou contextos.** Uma biblioteca compartilhada acopla todos os
  consumidores; às vezes copiar é mais barato do que sincronizar versões.
- **Testes.** Um pouco de repetição deixa o teste legível sem navegar por helpers.
- Na ordem de Beck, "sem duplicação" fica *abaixo* de "revela intenção".

## Relações

- Em tensão com [coesão e acoplamento](../coesao-e-acoplamento/README.md): abstração
  compartilhada cria acoplamento entre quem a usa.
- Em tensão com OCP e com [KISS](../kiss/README.md); aliado de [YAGNI](../yagni/README.md).
- Caso particular citado por Meyer, o *Single Choice Principle*: só um módulo conhece a
  lista exaustiva de alternativas.

## Referências

- [Wikipedia: Don't repeat yourself](https://en.wikipedia.org/wiki/Don%27t_repeat_yourself), com a definição de Hunt e Thomas.
- Sandi Metz, [*The Wrong Abstraction*](https://sandimetz.com/blog/2016/1/20/the-wrong-abstraction), 2016.
- Kent C. Dodds, [*AHA Programming*](https://kentcdodds.com/blog/aha-programming), 2020.
- Martin Fowler, [*Beck Design Rules*](https://martinfowler.com/bliki/BeckDesignRules.html), 2015.
