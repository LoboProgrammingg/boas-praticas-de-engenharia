# 01. Princípios de design

Princípios de design são **heurísticas para controlar o custo de mudança**, não leis.
Quase todos têm um contrapeso: DRY tem a abstração errada, SRP tem a fragmentação
excessiva, composição tem os casos em que a herança é a resposta certa. Por isso cada
tópico aqui traz um exemplo ruim, um bom, um teste que prova a diferença e uma seção
**Quando não aplicar**.

Cada pasta tem `README.md` (definição, fonte, relações), `ruim.py`, `bom.py` e um
`test_*.py` que exercita as duas versões.

## Índice

### SOLID

| Princípio | Em uma frase | Exemplo |
|---|---|---|
| SRP | Um módulo, uma razão para mudar | [`solid/srp/`](solid/srp/README.md) |
| OCP | Estenda sem modificar o que já funciona | [`solid/ocp/`](solid/ocp/) |
| LSP | Um subtipo substitui o tipo base sem surpresas | [`solid/lsp/`](solid/lsp/) |
| ISP | Interfaces pequenas, por cliente | [`solid/isp/`](solid/isp/) |
| DIP | Dependa de abstrações, não de implementações | [`solid/dip/`](solid/dip/) |

### Demais princípios

| Princípio | Em uma frase | Exemplo |
|---|---|---|
| [KISS](kiss/README.md) | Entre duas soluções, a de menos peças móveis | [`kiss/`](kiss/) |
| [DRY e AHA](dry-e-aha/README.md) | Elimine duplicação de conhecimento, não de texto | [`dry-e-aha/`](dry-e-aha/) |
| [YAGNI](yagni/README.md) | Não construa o que ninguém precisa agora | [`yagni/`](yagni/) |
| [Separação de responsabilidades](separacao-de-responsabilidades/README.md) | Preocupações diferentes, partes diferentes | [`separacao-de-responsabilidades/`](separacao-de-responsabilidades/) |
| [Lei de Demeter](lei-de-demeter/README.md) | Fale com amigos imediatos, não com a cadeia | [`lei-de-demeter/`](lei-de-demeter/) |
| [Composição sobre herança](composicao-sobre-heranca/README.md) | Monte comportamento em vez de herdá-lo | [`composicao-sobre-heranca/`](composicao-sobre-heranca/) |
| [Tell, Don't Ask](tell-dont-ask/README.md) | Diga ao objeto o que fazer; ele decide como | [`tell-dont-ask/`](tell-dont-ask/) |
| [CQS](cqs/README.md) | Perguntar não pode mudar a resposta | [`cqs/`](cqs/) |
| [Fail fast](fail-fast/README.md) | Falhe perto da causa, com mensagem clara | [`fail-fast/`](fail-fast/) |
| [Imutabilidade](imutabilidade/README.md) | Em vez de alterar, devolva um valor novo | [`imutabilidade/`](imutabilidade/) |
| [Coesão e acoplamento](coesao-e-acoplamento/README.md) | Junte o que muda junto; separe o resto | [`coesao-e-acoplamento/`](coesao-e-acoplamento/) |

## Matriz de relações e conflitos

Os princípios não formam uma lista de regras que se somam. Eles se reforçam e também
se contradizem. Conhecer os pares em tensão evita aplicar um deles até o absurdo.

| Princípio | Reforça | Tensão ou conflito |
|---|---|---|
| SRP | Coesão, separação de responsabilidades, testabilidade | Fragmentação excessiva (Ousterhout), módulos rasos |
| OCP | DIP, LSP | YAGNI, KISS (extensão prevista e nunca usada) |
| LSP | Composição, contratos | Herança só por conveniência |
| ISP, DIP | Arquitetura hexagonal, testes com fakes | Interfaces com uma única implementação |
| DRY | Fonte única da verdade | AHA e Rule of Three; acoplamento por abstração compartilhada |
| YAGNI | KISS, *Simple Design* do XP | Decisões caras de reverter (API pública, paginação) |
| Demeter, Tell Don't Ask | Encapsulamento, baixo acoplamento | DTOs, interfaces fluentes, excesso de delegação (Middle Man) |
| CQS | Funções puras, imutabilidade | `pop()`, operações atômicas (`INSERT ... RETURNING`) |
| Fail fast | Menor surpresa, validação na borda | Resiliência e degradação elegante |
| Composição | DIP, OCP | Casos em que herança estável é mais simples |
| Imutabilidade | CQS, funções puras | Desempenho em laços quentes e estruturas grandes |

## Como desempatar

Os conflitos acima se agrupam em três famílias:

1. **Reduzir duplicação** (DRY, OCP);
2. **Reduzir indireção e complexidade** (KISS, YAGNI, AHA);
3. **Proteger contra mudança** (SRP, DIP, Demeter).

Quando duas famílias discordam, a ordem das regras de design simples de Kent Beck
([Fowler, 2015](https://martinfowler.com/bliki/BeckDesignRules.html)) serve de desempate:

1. passa nos testes;
2. revela a intenção;
3. não tem duplicação;
4. tem o menor número de elementos.

E use o critério de **mudança real observada**: proteja-se contra a mudança que já
aconteceu duas vezes, não contra a que você imagina.

O erro mais comum é tratar o princípio como métrica (linhas por função, uma classe por
responsabilidade, zero duplicação) em vez de ferramenta. Os próprios John Ousterhout e
Robert C. Martin concordam, no [debate público](https://github.com/johnousterhout/aposd-vs-clean-code)
de 2024–2025, que decomposição excessiva e limites numéricos arbitrários são riscos.

## Próximo passo

[02. Código limpo](../02-codigo-limpo/README.md): nomes, funções, comentários e
tratamento de erros, os princípios aplicados à escrita do dia a dia.
