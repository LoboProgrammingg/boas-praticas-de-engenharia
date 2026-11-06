# SOLID

Cinco princípios de design orientado a objetos reunidos por Robert C. Martin no artigo
*Design Principles and Design Patterns* (2000). O acrônimo foi cunhado depois, por
Michael Feathers.

| Princípio | Ideia central | Sinal de violação |
|---|---|---|
| [SRP](srp/) Responsabilidade Única | Um motivo para mudar | Classe alterada por pedidos de áreas diferentes |
| [OCP](ocp/) Aberto/Fechado | Estender sem modificar | Cadeia de `if/elif` que cresce a cada requisito |
| [LSP](lsp/) Substituição de Liskov | Subtipo cumpre o contrato do tipo base | `NotImplementedError` ou `isinstance` no cliente |
| [ISP](isp/) Segregação de Interfaces | Interfaces pequenas, por cliente | Implementações vazias de métodos obrigatórios |
| [DIP](dip/) Inversão de Dependência | Política depende de abstração | Regra de negócio instanciando banco, relógio ou HTTP |

SOLID é um meio para reduzir o custo de mudança, não um fim. Cada tópico traz também
**quando não aplicar**: abstrações prematuras custam mais do que a duplicação que evitam.

## Referências

- Robert C. Martin, *Design Principles and Design Patterns*, 2000.
- [SOLID](https://en.wikipedia.org/wiki/SOLID), Wikipedia (histórico).
