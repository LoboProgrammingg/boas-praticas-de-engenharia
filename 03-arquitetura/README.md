# 03. Arquitetura

Arquitetura é o conjunto de decisões difíceis de mudar depois. Esta seção cobre como
separar a regra de negócio da infraestrutura, como dividir o domínio, quando distribuir o
sistema e como registrar as decisões. Em todas, o tom é o mesmo: comece simples e pague
cada camada de complexidade só quando o problema a justificar.

| Tópico | O que ensina | Exemplo executável |
|---|---|---|
| [Camadas, Hexagonal, Onion e Clean](camadas-hexagonal-clean/README.md) | A Dependency Rule: dependências de código apontam para a regra de negócio. Notas históricas de cada variante | `ruim.py`, `bom.py`, teste |
| [DDD estratégico](ddd/README.md) | Bounded Context, Ubiquitous Language e Context Map; padrões táticos no repositório [DDD-Structure](https://github.com/LoboProgrammingg/DDD-Structure) | `ruim.py`, `bom.py`, teste |
| [CQRS](cqrs/README.md) | Um modelo para escrever e outro para ler, e por que a maioria dos sistemas não precisa | `ruim.py`, `bom.py`, teste |
| [Monólito modular × microsserviços](monolito-modular-vs-microsservicos/README.md) | *Monolith First* e o *Microservice Premium* | `ruim.py`, `bom.py`, teste |
| [Twelve-Factor App](twelve-factor/README.md) | Os doze fatores; configuração no ambiente, validada na inicialização | `ruim.py`, `bom.py`, teste |
| [ADRs](adrs/README.md) | Registros curtos de decisões de arquitetura (formato de Nygard), com um exemplo completo | [ADR de exemplo](adrs/0001-usar-postgresql-como-fila-de-jobs.md) |

## Como ler

1. Comece por **camadas, hexagonal e clean**: é a base das demais.
2. **DDD estratégico** diz *onde* ficam as fronteiras; **monólito modular** diz *como*
   mantê-las em um só processo.
3. **CQRS** e **microsserviços** são escolhas com custo real; leia as seções "Quando não
   aplicar" antes de adotar.
4. Registre cada decisão importante como **ADR**.

## Convenção

Cada tópico com código segue o padrão do repositório: `README.md` (definição, problema,
solução, quando não aplicar, relações e referências), `ruim.py` (o problema), `bom.py` (a
solução) e `test_<tópico>.py`, que demonstra a falha da versão ruim e prova a boa. Rode
tudo com `uv run pytest 03-arquitetura`.
