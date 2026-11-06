# ADRs: Architecture Decision Records

> "One of the hardest things to track during the life of a project is the motivation behind
> certain decisions."
> Michael Nygard, *Documenting Architecture Decisions*

| | |
|---|---|
| **Origem** | Michael Nygard, *Documenting Architecture Decisions*, 2011-11-15 |
| **Resolve** | Decisões de arquitetura cujo motivo ninguém mais lembra; quem chega depois só pode aceitar ou mudar "às cegas" |
| **Em uma frase** | Um arquivo curto e versionado por decisão significativa, com contexto, decisão e consequências |

## O problema

Decisões de arquitetura vivem na cabeça de quem estava na sala. Meses depois, o time novo
(ou você mesmo) vê, por exemplo, uma fila implementada em cima do banco e não sabe se foi
descuido ou escolha. Sem entender o motivo ou as consequências, diz Nygard, a pessoa tem só duas escolhas:
*blindly accept* a decisão, o que perpetua escolhas que o contexto já invalidou, ou
*blindly change* a decisão, o que pode desfazer algo que existia por um bom motivo. Documentos grandes não resolvem: os
que são grandes demais nunca são atualizados e ninguém os lê.

## A solução

Mantenha uma coleção de registros para decisões "arquiteturalmente significativas",
isto é, as que afetam estrutura, características não funcionais, dependências, interfaces
ou técnicas de construção. Cada ADR é um arquivo de texto curto, no repositório, no
formato de Nygard:

| Parte | O que contém |
|---|---|
| **Título** | frase nominal curta ("Usar PostgreSQL como fila de jobs") |
| **Contexto** | as forças em jogo (técnicas, políticas, sociais, do projeto), descritas com neutralidade e deixando as tensões claras |
| **Decisão** | a resposta a essas forças, em frases completas na voz ativa: "Vamos usar..." |
| **Status** | *proposta*, *aceita*, *depreciada* ou *substituída* (com referência à substituta) |
| **Consequências** | o contexto resultante, **todas** as consequências (positivas, negativas e neutras), não só as boas |

Regras de convivência recomendadas no mesmo texto:

- ADRs numerados em sequência, sem reutilizar números;
- uma decisão revertida não é apagada: continua no repositório, marcada como substituída;
- cada ADR com uma ou duas páginas, escrito como uma conversa com um futuro desenvolvedor.

Um exemplo completo está em [`0001-usar-postgresql-como-fila-de-jobs.md`](0001-usar-postgresql-como-fila-de-jobs.md).
Note como ele registra o que se perde (teto de vazão, limpeza de linhas) e **o gatilho que
reabriria a decisão**.

### Onde guardar

Nygard sugere `doc/arch/adr-NNN.md` no repositório do projeto, em Markdown ou outra
linguagem leve. Qualquer pasta previsível serve (`docs/adr/`), desde que fique ao lado do
código e passe pelo mesmo code review: assim a decisão e a mudança de código chegam
juntas.

## Quando não aplicar

- **Nem toda decisão é arquitetural.** Nome de variável e escolha de formatação não
  precisam de ADR. O critério é "custaria caro desfazer ou explicar depois?".
- **Projeto descartável ou de uma pessoa só, de vida curta**: o histórico do Git e o
  README bastam.
- **ADR não é design document.** Se o texto passa de duas páginas, a análise de
  alternativas provavelmente merece um documento próprio, ao qual o ADR aponta.
- Um ADR que ninguém lê porque está escondido numa wiki fora do repositório não ajuda.

## Relações

- As decisões de [monólito × microsserviços](../monolito-modular-vs-microsservicos/README.md),
  [CQRS](../cqrs/README.md) e do estilo de camadas
  ([`../camadas-hexagonal-clean`](../camadas-hexagonal-clean/README.md)) são os candidatos
  clássicos a ADR.
- É a mesma ideia de manter documentos pequenos e versionados com o código, aplicada à
  documentação em geral.

## Referências

- Michael Nygard, [*Documenting Architecture Decisions*](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions), 2011.
- [Architecture Decision Record (coleção de modelos e exemplos)](https://github.com/joelparkerhenderson/architecture-decision-record).
