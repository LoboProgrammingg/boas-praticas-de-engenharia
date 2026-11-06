# Checklist de novo repositório

## Apresentação

- [ ] README com: o que é, por que existe, como rodar, como testar, arquitetura e autor
- [ ] Descrição curta e de 5 a 20 *topics* na página do repositório
- [ ] Licença definida (`LICENSE`)
- [ ] Imagem de *social preview* (1280x640, menos de 1 MB)

## Comunidade

- [ ] `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md` e `SUPPORT.md`
- [ ] Modelos de issue (formulários) e de Pull Request
- [ ] `CODEOWNERS`

## Qualidade e segurança

- [ ] CI com lint, tipos e testes em todo PR
- [ ] Ruleset na branch principal: PR obrigatório, checks obrigatórios, sem force push
- [ ] Varredura de segredos (gitleaks) no CI e *push protection* ativo
- [ ] CodeQL e Dependabot habilitados
- [ ] Reporte privado de vulnerabilidades habilitado

## Fluxo

- [ ] Conventional Commits e merge por *squash*
- [ ] `CHANGELOG.md` e releases com SemVer
