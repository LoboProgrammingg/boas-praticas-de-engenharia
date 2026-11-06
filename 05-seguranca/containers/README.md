# Containers

| | |
|---|---|
| **Fontes** | [CIS Docker Benchmark](https://www.cisecurity.org/benchmark/docker), [Docker: build best practices](https://docs.docker.com/build/building/best-practices/), [OWASP Docker Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Docker_Security_Cheat_Sheet.html) |
| **Resolve** | Imagem inchada, rodando como root, com segredo embutido e sem limites de runtime |
| **Em uma frase** | Imagem mínima e reconstruída, processo sem privilégios, rootfs somente leitura, nenhuma capability que você não usa |

## Antes e depois

| Arquivo | Papel |
|---|---|
| [`Dockerfile.vulneravel`](Dockerfile.vulneravel) | Anti-exemplo, com cada defeito anotado com o controle CIS que ele viola |
| [`Dockerfile.seguro`](Dockerfile.seguro) | Multi-stage, não-root, sem segredos, com `HEALTHCHECK` |

Ambos passam em `docker build --check` (sintaxe e lint do BuildKit). O seguro pressupõe um
`requirements.txt` com hashes e o pacote em `app/`; nenhum dos dois foi construído por completo aqui,
porque o projeto de aplicação não faz parte deste repositório.

### O que o Dockerfile seguro faz

| Controle | Como | CIS Docker Benchmark v1.8.0 |
|---|---|---|
| Multi-stage | Estágio `build` instala dependências; a imagem final copia só o venv, sem compiladores | 4.3 |
| Base mínima e confiável | `python:3.12-slim`, fixada por digest em produção (`--build-arg BASE=...@sha256:<digest>`) | 4.2 |
| Usuário não-root | `useradd --system --uid 10001` + `USER 10001` | 4.1 |
| `COPY`, não `ADD` | | 4.9 |
| Sem segredos na imagem | Nenhum `ENV`/`ARG` com credencial; segredo em runtime ou `RUN --mount=type=secret` | 4.10 |
| Hashes nas dependências | `pip install --require-hashes` | 4.11 |
| Healthcheck | `HEALTHCHECK` chamando `/health` | 4.6 |

Segundo a documentação do Docker, também vale usar **duas bases** (build e produção, sem ferramentas
de debug), reconstruir as imagens com frequência e usar `docker build --pull` para receber patches da base.

### Runtime endurecido (docker compose)

Os itens do CIS de runtime que mais pesam, no mesmo desenho API + Worker com a mesma imagem
(troque só o `command`):

```yaml
services:
  api:
    image: ghcr.io/org/app@sha256:<digest>
    read_only: true                          # CIS 5.13: rootfs somente leitura
    tmpfs: ["/tmp"]                          # único lugar gravável
    cap_drop: ["ALL"]                        # CIS 5.4: sem capabilities
    security_opt: ["no-new-privileges:true"] # CIS 5.26
    mem_limit: 512m                          # CIS 5.11
    pids_limit: 200                          # CIS 5.29
    env_file: [.env]                         # segredos injetados em runtime, fora da imagem
    ports: ["127.0.0.1:8000:8000"]           # CIS 5.14: interface específica
    # NUNCA: privileged: true (5.5); montar /var/run/docker.sock (5.32)
```

Postgres e Redis ficam só na rede interna do compose (sem `ports:`), Redis com senha ou ACL.

## Scan de imagem com Trivy

Cada flag foi conferida na documentação do Trivy: `--severity`, `--ignore-unfixed` e `--exit-code`
(por padrão o Trivy sai com código 0 mesmo havendo achados; `--exit-code 1` faz o pipeline falhar).

```bash
trivy image --severity HIGH,CRITICAL --ignore-unfixed --exit-code 1 ghcr.io/org/app@sha256:<digest>
```

`--ignore-unfixed` esconde vulnerabilidades sem correção disponível, o que reduz ruído; registre
essa decisão. O Trivy também verifica misconfiguration de Dockerfile e IaC (`--scanners misconfig`).
Rode o scan no CI e **de novo periodicamente** em imagens já publicadas: o banco de vulnerabilidades muda
depois do build.

## CIS Docker Benchmark: qual versão?

Há um conflito de versão que não consegui resolver com fonte aberta:

- A numeração acima vem do **v1.8.0 (2025-07-24)**, lido num espelho em PDF do benchmark.
- A página do CIS lista **Docker (1.9.0)** como versão recente, mas o download é restrito a membros.

Os números das seções podem mudar entre versões. Confirme a vigente com o CIS antes de citar
um item numa auditoria; trate a numeração desta página como referência do v1.8.0.

## Checklist

- [ ] Base mínima fixada por digest e reconstruída com frequência.
- [ ] Multi-stage; sem compiladores nem ferramentas de debug na imagem final.
- [ ] `USER` não-root; `HEALTHCHECK`; `COPY` em vez de `ADD`.
- [ ] Nenhum segredo em `ENV`, `ARG`, `COPY` ou camada; `.dockerignore` exclui `.env` e `.git`.
- [ ] `read_only`, `cap_drop: [ALL]`, `no-new-privileges`, limites de memória e PIDs.
- [ ] Sem `privileged`, sem `docker.sock` montado, portas só em `127.0.0.1` quando possível.
- [ ] Scan no CI (Trivy) com `--exit-code`, e proveniência/assinatura ([`supply-chain/`](../supply-chain/README.md)).

## Referências

- [CIS Docker Benchmark](https://www.cisecurity.org/benchmark/docker)
- [Docker: build best practices](https://docs.docker.com/build/building/best-practices/)
- [OWASP Docker Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Docker_Security_Cheat_Sheet.html)
- [Trivy: container image](https://trivy.dev/latest/docs/target/container_image/), [filtering](https://trivy.dev/latest/docs/configuration/filtering/), [exit code](https://trivy.dev/latest/docs/configuration/others/)
