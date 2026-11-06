# Fail Fast

> "Errors should never pass silently. Unless explicitly silenced."
> PEP 20, *The Zen of Python*

| | |
|---|---|
| **Origem** | Jim Shore, *Fail Fast*, IEEE Software, 2004 |
| **Resolve** | Defeitos que aparecem longe da causa, horas depois, como comportamentos estranhos |
| **Em uma frase** | Detecte o problema no ponto onde ele nasce e falhe com uma mensagem que aponte a causa |

## O problema

Em [`ruim.py`](ruim.py), `porta()` envolve tudo em `try/except Exception` e devolve
`8080`. Um `PORT=80a` digitado errado em produção não derruba nada: o serviço sobe na
porta errada e o problema só aparece quando o balanceador não o encontra. Pior, a função
não distingue variável ausente de variável errada, e aceita `PORT=70000` e `PORT=-1`.

Shore observa que o contrário do que parece intuitivo é verdade: software que falha
imediata e visivelmente fica mais robusto, porque o defeito é achado perto da causa.

## A solução

Em [`bom.py`](bom.py), `ler_porta` recebe o ambiente como `Mapping` (fácil de testar):

- **ausente**: porta padrão explícita e documentada (`PORTA_PADRAO`);
- **presente e inválida**: `ConfiguracaoInvalidaError` com mensagem que cita `PORT` e o valor;
- a causa original é preservada com `raise ... from erro`.

O [`teste`](test_fail_fast.py) cobre os casos inválidos e os válidos.

## Quando não aplicar

- **Na fronteira de resiliência** (fluxo do usuário final, jobs em lote): fail fast no
  núcleo, tratamento e degradação elegante na borda. Não derrube o processo inteiro
  por um item inválido de um lote.
- Falhar rápido não é falhar feio: erros que chegam ao usuário precisam de mensagem
  tratada, sem expor detalhes internos.
- Um valor *ausente* pode ter padrão legítimo; o erro é adivinhar o que está *errado*.

## Relações

- Validar entrada na borda (Pydantic, Zod) é fail fast aplicado à entrada; ver também o
  texto de Alexis King, [*Parse, don't validate*](https://lexi-lambda.github.io/blog/2019/11/05/parse-don-t-validate/), 2019.
- Reforça o princípio da menor surpresa (POLA).
- Complementa [tratamento de erros](../../02-codigo-limpo/tratamento-de-erros/README.md): exceções tipadas, com contexto.

## Referências

- Jim Shore, [*Fail Fast*](https://martinfowler.com/ieeeSoftware/failFast.pdf), IEEE Software, 2004.
- [PEP 20, *The Zen of Python*](https://peps.python.org/pep-0020/).
- Alexis King, [*Parse, don't validate*](https://lexi-lambda.github.io/blog/2019/11/05/parse-don-t-validate/), 2019.
