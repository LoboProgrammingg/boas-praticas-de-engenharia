# Property-based testing

> "With Hypothesis, you write tests which should pass for all inputs in whatever range you
> describe, and let Hypothesis randomly choose which of those inputs to check, including
> edge cases you might not have thought about."
> Documentação do Hypothesis

| | |
|---|---|
| **Origem** | QuickCheck (Koen Claessen e John Hughes, ICFP 2000); em Python, a biblioteca [Hypothesis](https://hypothesis.readthedocs.io/) |
| **Resolve** | Testes por exemplos que só cobrem os casos em que o autor pensou |
| **Em uma frase** | Descreva uma **propriedade** que vale para toda entrada válida e deixe a biblioteca procurar um contraexemplo |

## O problema

Em [`ruim.py`](ruim.py), `codificar`/`decodificar` implementam compressão por repetição
(`"aaabcc"` ↔ `"3a1b2c"`). Os três exemplos clássicos passam, e o código parece correto.
Mas a decodificação lê a contagem com **um dígito**, então `"a" * 10` (código `"10a"`)
quebra. O autor não pensou em 10 repetições, e testes por exemplos só encontram o que o
autor imaginou.

## A solução

Troque "para esta entrada, esta saída" por "para **toda** entrada, esta propriedade". Em
[`test_property_based.py`](test_property_based.py):

```python
@given(TEXTOS_COM_REPETICOES)  # textos feitos de trechos repetidos, de 1 a 15 vezes
def ida_e_volta(texto: str) -> None:
    assert decodificar(codificar(texto)) == texto
```

O Hypothesis gera centenas de textos, inclusive os de borda, e, ao achar uma falha,
**reduz** (*shrinking*) o contraexemplo ao menor possível (aqui, `"aaaaaaaaaa"`, dez letras
iguais). Na versão ruim, a propriedade falha; em [`bom.py`](bom.py), que usa pares
`(caractere, contagem)` em vez de texto para o código, ela vale.

Famílias de propriedades úteis:

| Tipo | Exemplo |
|---|---|
| **Ida e volta** (round-trip) | `decodificar(codificar(x)) == x`; serializar e desserializar |
| **Invariante** | `len(codificar(x)) <= len(x)`; saída sempre ordenada; saldo nunca negativo |
| **Idempotência** | normalizar duas vezes é o mesmo que uma |
| **Oráculo** | comparar uma implementação otimizada com uma simples e óbvia |
| **Metamórfica** | a relação entre duas entradas, não o valor exato (ex.: inverter e ordenar) |

Pontos práticos:

- **Reprodutibilidade.** Falhas do Hypothesis são salvas num banco local para reexecução.
  Nos testes deste repositório usamos `settings(database=None, derandomize=True)` para que a
  execução seja determinística e não escreva em disco.
- **Estratégia certa importa.** Com texto totalmente aleatório, dez repetições seguidas
  raramente aparecem; `TEXTOS_COM_REPETICOES` gera de propósito trechos repetidos. O
  Hypothesis procura, mas você aponta onde olhar.
- **Estratégias do domínio.** Construa geradores (`st.builds`, `st.sampled_from`) que só
  produzem entradas válidas do seu domínio, em vez de filtrar entradas aleatórias.
- **Combine com exemplos.** O contraexemplo reduzido vira um teste de regressão por
  exemplo (`@example(...)` ou um teste normal).

## Quando não aplicar

- **Sem propriedade clara.** Se o único jeito de dizer o resultado esperado é repetir a
  implementação dentro do teste, o teste não ajuda; use exemplos.
- **Testes lentos ou com efeitos externos** (rede, banco real): centenas de execuções por
  teste ficam caras. Limite `max_examples` ou use propriedades sobre a parte pura.
- **Não substitui exemplos.** Exemplos documentam comportamentos específicos de negócio;
  propriedades procuram o que ninguém previu.

## Relações

- Um bom ponto de partida é o contraexemplo que um [TDD](../tdd/README.md) revela, como
  "a soma das parcelas é o total".
- Mede-se a força de uma suíte (por exemplos ou propriedades) com
  [mutation testing](../mutation/README.md).
- Em TypeScript, a biblioteca equivalente é a `fast-check`; não é usada neste repositório.

## Referências

- Documentação do [Hypothesis](https://hypothesis.readthedocs.io/en/latest/) (incluindo "What you can generate and how").
- Koen Claessen e John Hughes, [*QuickCheck: a lightweight tool for random testing of Haskell programs*](https://doi.org/10.1145/351240.351266), ICFP 2000.
