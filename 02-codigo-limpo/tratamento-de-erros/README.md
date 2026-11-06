# Tratamento de erros

> "Errors should never pass silently. Unless explicitly silenced."
> PEP 20, *The Zen of Python*

| | |
|---|---|
| **Origem** | Capítulo de tratamento de erros de *Clean Code* (Martin, 2008): exceções em vez de códigos de retorno |
| **Resolve** | Falhas que passam despercebidas como valor mágico (`-1`, `None`) ou que são engolidas, perdendo causa e contexto |
| **Em uma frase** | Falhe com uma exceção tipada que carregue o contexto, e nunca descarte a causa |

## O problema

Em [`ruim.py`](ruim.py):

- `sacar` devolve `-1` quando falta saldo. Quem esquece de checar soma `-1` ao total e
  segue adiante: o [`teste`](test_tratamento_de_erros.py) mostra `30 + (-1) = 29`
  como "total sacado" de uma conta que só tinha 100 e recusou 500.
- `ler_valor` troca qualquer erro por `None`. Quem recebe não sabe se o texto estava
  vazio, com vírgula ou corrompido.

## A solução

Em [`bom.py`](bom.py):

| Prática | Onde |
|---|---|
| Exceção tipada, com os dados da falha | `SaldoInsuficienteError(saldo, valor)` |
| O estado não muda quando a operação falha | `Conta.sacar` valida antes de debitar |
| Traduzir o erro técnico em erro do domínio sem perder a causa | `raise ValorInvalidoError(...) from erro` |
| Nome do erro termina em `Error` | convenção do Python e regra do linter |

O erro interrompe o fluxo por padrão; ninguém precisa lembrar de checar nada.

## Quando não aplicar

- **Falhas esperadas e frequentes** (um campo de formulário vazio, um item que pode não
  existir) são fluxo normal. Devolver `None` ou um tipo de resultado (`Ok`/`Erro`) é
  legítimo, desde que o tipo obrigue a tratar a ausência. O ponto é que o erro não passe
  *sem o chamador saber*.
- **Não capture `Exception` para "ficar seguro".** Capture o erro específico, no lugar
  onde há o que fazer a respeito. Na fronteira (job, handler HTTP), registre e traduza.
- **Não use exceção como fluxo de controle comum** num laço quente: é caro e confuso.
- Em lote, uma entrada inválida não deve derrubar o processo todo
  ([fail fast](../../01-principios-de-design/fail-fast/README.md): falhe no núcleo,
  degrade na borda).
- Não exponha detalhes internos nem dados sensíveis (CPF, token, senha) na mensagem
  de erro nem nos logs.

## Relações

- [Fail fast](../../01-principios-de-design/fail-fast/README.md): erro detectado perto da causa.
- [Funções](../funcoes/README.md): uma função que devolve o resultado *ou* levanta o erro
  não precisa de código de retorno.
- Em [nomes](../nomes/README.md), o nome da exceção (`SaldoInsuficienteError`) já conta o que houve.

## Referências

- Robert C. Martin, *Clean Code*, Prentice Hall, 2008, capítulo 7.
- [PEP 20, *The Zen of Python*](https://peps.python.org/pep-0020/).
- Python, [exceções embutidas e hierarquia](https://docs.python.org/3/library/exceptions.html) e [a instrução `raise ... from`](https://docs.python.org/3/reference/simple_stmts.html#the-raise-statement).
- Jim Shore, [*Fail Fast*](https://martinfowler.com/ieeeSoftware/failFast.pdf), IEEE Software, 2004.
