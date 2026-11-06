# A03:2025 Software Supply Chain Failures

[OWASP A03:2025](https://owasp.org/Top10/2025/A03_2025-Software_Supply_Chain_Failures/) amplia a antiga
"Vulnerable and Outdated Components" para **toda a cadeia**: dependências, sistemas de build e
distribuição. Segundo a página da categoria, 50% dos respondentes da pesquisa da comunidade a
colocaram em primeiro lugar; poucos CVEs mapeados, mas a maior incidência média e os maiores
scores médios de exploração e impacto.

O conteúdo prático está em [`supply-chain/`](../../supply-chain/README.md) (SLSA, Sigstore, SBOM,
lockfiles, cooldown, Actions) e [`containers/`](../../containers/README.md). Este é o resumo de revisão.

## Checklist

**Dependências**

- [ ] Lockfile versionado e instalação reprodutível em CI (`uv sync --locked`, `npm ci`).
- [ ] Scanner de vulnerabilidades no CI (`pip-audit`, `npm audit`, `osv-scanner`) e atualização automatizada (Dependabot/Renovate).
- [ ] **Cooldown** de versões novas (Dependabot `cooldown`, e no gerenciador: `exclude-newer` no uv, `min-release-age` no npm) para reduzir o risco de pacote malicioso recém-publicado.
- [ ] Scripts de instalação de terceiros desabilitados por padrão em CI (`npm ci --ignore-scripts`).

**Build e pipeline**

- [ ] Actions fixadas por **SHA de commit**; `permissions:` mínimas; `persist-credentials: false`.
- [ ] Nenhum `${{ github.event.* }}` interpolado em `run:`; cuidado com `pull_request_target`.
- [ ] Deploy por **OIDC**, sem chave de nuvem de longa duração.

**Distribuição**

- [ ] Imagens e artefatos assinados (Sigstore/cosign) e com proveniência (SLSA).
- [ ] SBOM gerado por release.
- [ ] Publicação em registries por *trusted publishing*, sem token de longa duração no CI.

## Por que importa

Em setembro de 2025 o worm "Shai-Hulud" se propagou entre pacotes npm via contas de mantenedores
comprometidas e scripts `postinstall`, roubando segredos; o GitHub removeu mais de 500 pacotes
([GitHub Blog](https://github.blog/security/supply-chain-security/our-plan-for-a-more-secure-npm-supply-chain/)).

## Referências

- [OWASP A03:2025](https://owasp.org/Top10/2025/A03_2025-Software_Supply_Chain_Failures/)
- [SLSA v1.2](https://slsa.dev/spec/)
- [OpenSSF Scorecard: checks](https://github.com/ossf/scorecard/blob/main/docs/checks.md)
