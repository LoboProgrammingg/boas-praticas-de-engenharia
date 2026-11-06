# Nomes

> "Explicit is better than implicit."
> PEP 20, *The Zen of Python*

| | |
|---|---|
| **Origem** | Capítulo de nomes significativos de *Clean Code* (Martin, 2008); o conselho de nomes descritivos e consistentes é reconhecido como válido até pelos críticos do livro |
| **Resolve** | Código que só se entende lendo a implementação, e chamadas que compilam e rodam com argumentos trocados |
| **Em uma frase** | O nome diz o que a coisa é ou faz, em que unidade, e se tem efeito colateral |

## O problema

Em [`ruim.py`](ruim.py):

- `calc(d, r)` não diz o que calcula nem o que `d` e `r` são. Trocar os argumentos de
  lugar continua válido e devolve um número plausível, sem nenhum erro.
- `obter_usuario(id)` promete uma leitura, mas **cria** o usuário se ele não existe. O
  nome mente: quem chama para consultar altera o estado.

## A solução

Em [`bom.py`](bom.py):

| Antes | Depois | O que melhorou |
|---|---|---|
| `calc(d, r)` | `valor_composto_em_um_ano(*, principal, taxa_mensal)` | Intenção e papel de cada parâmetro; o `*` exige chamada nomeada, então não dá para trocar sem ver |
| `12` solto | `MESES_NO_ANO` | A constante tem nome |
| `obter_usuario` (que cria) | `buscar_usuario` (lê) e `obter_ou_criar_usuario` (avisa que escreve) | O nome conta o efeito |

O [`teste`](test_nomes.py) prova os dois defeitos da versão ruim e a recusa da chamada
posicional na boa.

Regras práticas: verbos para ações e substantivos para valores; uma palavra por conceito
(não misture `buscar`, `obter` e `pegar`); a unidade no nome quando o tipo não a diz
(`timeout_em_segundos`, ou melhor, um `timedelta`); nome do tamanho do escopo (`i` num
laço de três linhas está bem).

## Quando não aplicar

- **Nome longo demais** atrapalha tanto quanto o enigmático. Num escopo curto, `linha`
  vale mais que `linha_atual_do_arquivo_de_entrada`.
- **Vocabulário do domínio** vence a preferência pessoal. Se o negócio diz "fatura", não
  invente "nota de cobrança" (ver linguagem ubíqua, DDD).
- Não renomeie API pública só por gosto: renomear quebra quem usa. Faça com período de
  depreciação.

## Relações

- Um nome que descreve a intenção reduz a necessidade de [comentários](../comentarios/README.md).
- Nomes honestos sobre efeitos colaterais aplicam [CQS](../../01-principios-de-design/cqs/README.md).
- Parte da regra "revela a intenção" de Beck, que vem antes de "sem duplicação"
  ([Fowler, 2015](https://martinfowler.com/bliki/BeckDesignRules.html)).

## Referências

- Robert C. Martin, *Clean Code*, Prentice Hall, 2008, capítulo 2.
- qntm, [*It's probably time to stop recommending Clean Code*](https://qntm.org/clean), 2020, que reconhece como razoável o conselho de nomes.
- [PEP 8, *Style Guide for Python Code*](https://peps.python.org/pep-0008/), seção de convenções de nomes.
- Martin Fowler, [*Beck Design Rules*](https://martinfowler.com/bliki/BeckDesignRules.html), 2015.
