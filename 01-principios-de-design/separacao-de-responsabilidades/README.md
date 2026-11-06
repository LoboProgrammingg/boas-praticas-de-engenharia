# Separação de Responsabilidades (Separation of Concerns)

> Cada preocupação do sistema deve poder ser entendida, testada e mudada isoladamente.
> Síntese do princípio

| | |
|---|---|
| **Origem** | Edsger Dijkstra, *On the role of scientific thought*, 1974 (a expressão *separation of concerns*), com raízes no *information hiding* de Parnas (1972) |
| **Resolve** | Funções e módulos em que leitura, regra, formato e infraestrutura se misturam, e uma mudança em um afeta os outros |
| **Em uma frase** | Separe o que muda por motivos diferentes em partes que se encaixam por interfaces pequenas |

## O problema

Em [`ruim.py`](ruim.py), `relatorio(caminho)` abre um arquivo, interpreta o CSV, soma e
imprime, tudo junto. Para testar só a soma é preciso criar um arquivo em disco e capturar
a saída padrão, e trocar o formato do relatório obriga a mexer no código que lê o CSV.

A Wikipedia lembra que a separação pode seguir eixos diferentes: por tempo, por
qualidade, por visão ou por tamanho (modularidade). Camadas (apresentação, regra,
persistência) são só um deles.

## A solução

Em [`bom.py`](bom.py) há uma função por preocupação:

| Função | Preocupação |
|---|---|
| `ler_vendas` | interpretar o texto de entrada |
| `totais_por_produto` | regra de cálculo, pura |
| `formatar_relatorio` | apresentação |
| `gerar_relatorio` | a casca que junta as três |

O [`teste`](test_separacao_de_responsabilidades.py) exercita o cálculo sem disco nem
`print`, e troca o formato sem tocar na leitura.

## Quando não aplicar

- **Não confunda separar com fragmentar.** Cada divisão cria uma interface a manter.
  John Ousterhout alerta para módulos rasos, com interface quase tão complexa quanto a
  implementação ([debate Ousterhout × Martin](https://github.com/johnousterhout/aposd-vs-clean-code)).
- **Scripts curtos** de uso único não pagam o custo da separação.
- Separe quando a segunda razão de mudança aparecer, não quando for imaginada.

## Relações

- [SRP](../solid/srp/README.md) é a aplicação do princípio a classes e módulos: uma razão para mudar.
- Pede [alta coesão e baixo acoplamento](../coesao-e-acoplamento/README.md).
- Dá base à *clean architecture* e à arquitetura hexagonal (separar regra de infraestrutura).

## Referências

- [Wikipedia: Separation of concerns](https://en.wikipedia.org/wiki/Separation_of_concerns).
- Robert C. Martin, [*The Single Responsibility Principle*](https://blog.cleancoder.com/uncle-bob/2014/05/08/SingleReponsibilityPrinciple.html), 2014, com o histórico (Parnas 1972, Dijkstra 1974).
- John Ousterhout e Robert C. Martin, [*A Philosophy of Software Design* vs *Clean Code*](https://github.com/johnousterhout/aposd-vs-clean-code), 2024–2025.
