# Checklist de code review

## Segurança

- [ ] Toda entrada externa é validada na borda (schema, tipos, tamanhos)
- [ ] Autorização verificada por recurso (não só autenticação); consultas filtram pelo dono ou tenant
- [ ] Nenhum segredo em código, teste, log ou mensagem de erro
- [ ] SQL parametrizado; nada de montar comandos com strings vindas do usuário
- [ ] Erros não vazam detalhes internos para o cliente

## Correção

- [ ] A regra de negócio faz o que a issue pede
- [ ] Bordas tratadas: vazio, nulo, limite, duplicado, concorrência
- [ ] Operações externas têm timeout; retries só em operações idempotentes

## Design

- [ ] O código está na camada certa (regra no domínio, orquestração na aplicação, I/O na infraestrutura)
- [ ] Nenhuma abstração criada para um único uso
- [ ] Dependências apontam para dentro (a regra não conhece o framework)

## Testes

- [ ] Há teste para o comportamento novo e para o bug corrigido
- [ ] O teste falharia se o código estivesse errado
- [ ] Testes são determinísticos (sem dependência de relógio, rede ou ordem)

## Legibilidade

- [ ] Nomes revelam intenção
- [ ] Comentários explicam o porquê, não o quê
- [ ] Commits e título do PR seguem Conventional Commits
