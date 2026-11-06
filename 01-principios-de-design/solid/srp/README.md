# SRP: Princípio da Responsabilidade Única

> "Um módulo deve ter uma, e apenas uma, razão para mudar."
> Robert C. Martin

| | |
|---|---|
| **Origem** | Robert C. Martin, fim dos anos 1990, a partir das ideias de coesão (Constantine, DeMarco) e de *information hiding* (Parnas, 1972) |
| **Resolve** | Classes que mudam por motivos diferentes e quebram em cascata a cada alteração |
| **Em uma frase** | Agrupe o que muda pelo mesmo motivo; separe o que muda por motivos diferentes |

## O problema

"Razão para mudar" é, na prática, **quem pede a mudança**. Em [`ruim.py`](ruim.py), a
classe `Fatura` atende três pessoas: o financeiro (regra de preço), quem cuida do banco
(esquema da tabela) e o marketing (texto do e-mail). Qualquer um deles pode quebrar o
trabalho dos outros, e até para testar um cálculo é preciso uma conexão de banco.

## A solução

Em [`bom.py`](bom.py), cada responsabilidade vira um módulo:

| Módulo | Muda quando... |
|---|---|
| `Fatura` (dataclass imutável) | a regra de cálculo muda |
| `RepositorioDeFaturas` / `RepositorioSqlite` | o armazenamento muda |
| `formatar_email` | a comunicação com o cliente muda |

O teste [`test_srp.py`](test_srp.py) prova a diferença: o total é calculado sem
infraestrutura, a persistência é trocável e o texto do e-mail muda sem tocar na regra.

## Quando não aplicar

- **Não fragmente por fragmentar.** Dezenas de classes de um método com interfaces rasas
  pioram a leitura; John Ousterhout chama isso de *shallow modules*, e o próprio Martin
  admite que limites rígidos de tamanho nunca foram absolutos
  ([debate Ousterhout × Martin](https://github.com/johnousterhout/aposd-vs-clean-code)).
- **Scripts e protótipos** de vida curta não têm "várias razões para mudar" ainda.
- Separe quando a segunda razão de mudança **aparecer de verdade**, não quando for imaginada (YAGNI).

## Relações

- É a forma operacional de **alta coesão** e de **Separação de Responsabilidades**.
- Habilita **DIP**: o repositório vira uma porta (`Protocol`) que o domínio usa sem conhecer o banco.
- Em tensão com **KISS** quando levado ao extremo.

## Referências

- Robert C. Martin, [*The Single Responsibility Principle*](https://blog.cleancoder.com/uncle-bob/2014/05/08/SingleReponsibilityPrinciple.html), 2014.
- David Parnas, *On the Criteria To Be Used in Decomposing Systems into Modules*, CACM, 1972.
- John Ousterhout e Robert C. Martin, [*A Philosophy of Software Design* vs *Clean Code*](https://github.com/johnousterhout/aposd-vs-clean-code), 2024–2025.
