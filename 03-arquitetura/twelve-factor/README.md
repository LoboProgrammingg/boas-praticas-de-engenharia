# The Twelve-Factor App

> "A litmus test for whether an app has all config correctly factored out of the code is
> whether the codebase could be made open source at any moment, without compromising any
> credentials."
> Adam Wiggins, *The Twelve-Factor App*, fator III

| | |
|---|---|
| **Origem** | Adam Wiggins e a equipe do Heroku, [12factor.net](https://12factor.net/) |
| **Resolve** | Aplicações difíceis de implantar, escalar e portar entre ambientes (diferenças entre dev e prod, configuração presa ao código) |
| **Em uma frase** | Doze regras para apps de serviço (SaaS) que sobem igual em qualquer ambiente de nuvem e escalam sem mudar a arquitetura |

## O problema

Em [`ruim.py`](ruim.py), a URL do banco (com a senha de produção) e a chave de API são
constantes no código. Trocar de ambiente é editar código; o segredo vai parar no
repositório; e o teste do "código aberto a qualquer momento" falha de cara.

## A solução

Os doze fatores, conforme a introdução e as páginas oficiais:

| # | Fator | Ideia |
|---|---|---|
| I | Codebase | uma base de código versionada, vários deploys |
| II | Dependencies | declare e isole as dependências (`pyproject.toml` + lockfile) |
| III | Config | configuração no ambiente, separada do código |
| IV | Backing services | banco, fila e cache são recursos anexados, trocáveis por URL |
| V | Build, release, run | estágios separados; release imutável |
| VI | Processes | processos sem estado; o estado fica em serviço de apoio |
| VII | Port binding | o app exporta o serviço ao escutar uma porta |
| VIII | Concurrency | escale por processos (horizontalmente) |
| IX | Disposability | inicia rápido e encerra com elegância |
| X | Dev/prod parity | mantenha dev, staging e produção o mais parecidos possível |
| XI | Logs | trate logs como fluxo de eventos em `stdout` |
| XII | Admin processes | tarefas administrativas rodam como processos pontuais, com o mesmo código |

Este exemplo executável cobre o **fator III**. Em [`bom.py`](bom.py), `Config.do_ambiente`
lê um mapeamento de variáveis (`os.environ` em produção) e valida com Pydantic: tipos
corretos, obrigatórias presentes, falha na inicialização se algo estiver errado, e a chave
de API como `SecretStr`, que não aparece em `repr` nem em log. O teste
[`test_twelve_factor.py`](test_twelve_factor.py) prova cada uma dessas propriedades usando
um `dict` como ambiente, sem tocar no `os.environ` real.

O fator **XI** (logs como fluxo de eventos para `stdout`) está desenvolvido em
[`../../06-operabilidade/logs-estruturados`](../../06-operabilidade/logs-estruturados/README.md).

## Quando não aplicar

- **O 12-Factor descreve apps de serviço em nuvem**, não bibliotecas, ferramentas de linha
  de comando ou aplicativos de desktop e mobile. Tome-o como checklist, não como lei.
- **Variáveis de ambiente não são cofre.** Elas resolvem a separação entre código e
  configuração; segredos de alto valor pedem também um gerenciador de segredos e rotação.
- **Config granular.** O texto oficial pede variáveis independentes, não agrupadas em
  "ambientes" (`APP_ENV=prod` que liga dez comportamentos). Prefira uma variável por decisão.

## Relações

- Fator IV (backing services) é a mesma ideia de portas e adaptadores:
  [`../camadas-hexagonal-clean`](../camadas-hexagonal-clean/README.md).
- Fator VI (processos sem estado) e IX (descartabilidade) pedem
  [idempotência](../../06-operabilidade/idempotencia/README.md) e retries seguros.
- Fator XI: [logs estruturados](../../06-operabilidade/logs-estruturados/README.md) e
  [observabilidade](../../06-operabilidade/observabilidade/README.md).

## Referências

- Adam Wiggins, [*The Twelve-Factor App*](https://12factor.net/).
- [III. Config](https://12factor.net/config) e [XI. Logs](https://12factor.net/logs).
- Documentação do Pydantic sobre [`SecretStr`](https://docs.pydantic.dev/latest/api/types/#pydantic.types.SecretStr).
