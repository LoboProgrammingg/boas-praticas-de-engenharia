# Alta coesão e baixo acoplamento

> Mantenha junto o que muda junto; mantenha separado, e ligado por interfaces estreitas, o que muda por motivos diferentes.
> Síntese dos conceitos

| | |
|---|---|
| **Origem** | Larry Constantine, final dos anos 1960 (*Structured Design*); publicado em Stevens, Myers e Constantine, *Structured Design*, IBM Systems Journal, 1974 |
| **Resolve** | Módulos "faz-tudo" e dependências ocultas, onde uma mudança local se espalha pelo sistema |
| **Em uma frase** | Coesão mede o quanto as partes de um módulo pertencem juntas; acoplamento mede o quanto módulos dependem uns dos outros |

## O problema

Em [`ruim.py`](ruim.py), `Utils` agrupa `formatar_cpf`, `enviar_sms` e `calcular_frete`.
As três não têm nada em comum, o que a literatura chama de **coesão coincidental**, a
pior forma. E `enviar_sms` grava numa lista global: quem usa `Utils` para avisar uma
entrega e quem usa para uma promoção do marketing compartilham o mesmo estado sem saber.
É acoplamento por estado global.

## A solução

[`bom.py`](bom.py) separa por conceito e injeta as dependências:

| Unidade | Coesão |
|---|---|
| `Cpf` | tudo sobre documento: valida no construtor e formata |
| `TabelaDeFrete` | tudo sobre preço de entrega, com parâmetros nos dados |
| `ServicoDeSms` | recebe um `CanalDeSms` (porta de um método), sem estado global |

O [`teste`](test_coesao_e_acoplamento.py) confirma que cada serviço de SMS usa o seu
canal e não vê o do vizinho, e que a versão ruim mistura três assuntos num namespace.

**Escala da coesão** (pior para melhor, segundo a classificação clássica): coincidental,
lógica, temporal, procedural, comunicacional, sequencial e funcional. O alvo é a
funcional: todas as partes contribuem para uma tarefa bem definida.

## Quando não aplicar

- **Acoplamento zero não existe**: módulos precisam conversar. O objetivo é depender de
  contratos pequenos e estáveis, não de nada.
- **Não fragmente em busca de coesão perfeita.** Dez classes de um método, sem
  identidade própria, só trocam acoplamento visível por indireção
  ([Ousterhout](https://github.com/johnousterhout/aposd-vs-clean-code) chama isso de
  módulos rasos).
- Duplicar um trecho pequeno pode ser melhor do que criar uma dependência compartilhada
  ([DRY/AHA](../dry-e-aha/README.md)).

## Relações

- [SRP](../solid/srp/README.md) é a coesão aplicada: uma razão para mudar.
- [Separação de responsabilidades](../separacao-de-responsabilidades/README.md) é o meio de obtê-la.
- [Lei de Demeter](../lei-de-demeter/README.md) e [DIP](../solid/dip/README.md) reduzem acoplamento.
- GRASP, catálogo de Craig Larman em *Applying UML and Patterns*, lista *Low Coupling* e *High Cohesion* entre seus padrões.

## Referências

- [Wikipedia: Cohesion](https://en.wikipedia.org/wiki/Cohesion_(computer_science)) e [Coupling](https://en.wikipedia.org/wiki/Coupling_(computer_programming)).
- W. P. Stevens, G. J. Myers, L. L. Constantine, *Structured Design*, IBM Systems Journal, 1974.
- [Wikipedia: GRASP](https://en.wikipedia.org/wiki/GRASP_(object-oriented_design)).
- Robert C. Martin, [*The Single Responsibility Principle*](https://blog.cleancoder.com/uncle-bob/2014/05/08/SingleReponsibilityPrinciple.html), 2014.
