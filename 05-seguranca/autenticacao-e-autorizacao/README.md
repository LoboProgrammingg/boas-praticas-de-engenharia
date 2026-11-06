# Autenticação e autorização

| | |
|---|---|
| **Fontes** | [RFC 9700](https://www.rfc-editor.org/rfc/rfc9700) (OAuth 2.0 Security BCP), [RFC 8725](https://www.rfc-editor.org/rfc/rfc8725) (JWT BCP), [NIST SP 800-63B-4](https://pages.nist.gov/800-63-4/sp800-63b.html) |
| **Em uma frase** | Autenticação prova quem é; autorização, centralizada e negando por padrão, decide o que pode |

## OAuth 2.0 hoje: RFC 9700, não OAuth 2.1

O OAuth 2.1 (`draft-ietf-oauth-v2-1`) **ainda é um Internet-Draft**: o
[datatracker](https://datatracker.ietf.org/doc/draft-ietf-oauth-v2-1/) mostra a revisão -17, ativa, atualizada em outubro de 2026.
Não o cite como padrão. O que vale hoje é o **RFC 9700** (BCP 240, janeiro de 2025):

| Tema | Exigência (RFC 9700) |
|---|---|
| PKCE | Clientes públicos **MUST** usar PKCE; authorization servers MUST suportá-lo (§2.1.1) |
| Método | `S256` é o único método que não expõe o verifier no request de autorização; `plain` não |
| Refresh token (cliente público) | **MUST** ser *sender-constrained* (mTLS, DPoP) **ou** usar **rotação** (§2.2.2, §4.14) |
| Rotação | Token usado é invalidado; reuso de token já invalidado revoga o token ativo |
| Vida útil | Refresh token expira por inatividade; pode ser revogado em troca de senha ou logout |

### PKCE S256 em Python

A transformação do [RFC 7636 §4.2](https://www.rfc-editor.org/rfc/rfc7636) é
`BASE64URL(SHA256(ASCII(code_verifier)))`, com `code_verifier` de 43 a 128 caracteres (§4.1):

```python
import base64
import hashlib
import secrets

code_verifier = secrets.token_urlsafe(64)  # 86 caracteres, dentro de 43..128
code_challenge = (
    base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode("ascii")).digest())
    .rstrip(b"=")
    .decode("ascii")
)
# envie code_challenge + code_challenge_method=S256 na autorização;
# envie code_verifier somente na troca do code por token.
```

### Rotação de refresh token com detecção de reuso (esqueleto)

Ilustrativo, não executado (depende de repositório e banco do seu projeto):

```python
async def refresh(db, apresentado: str) -> ParDeTokens:
    linha = await repo.buscar_refresh_por_hash(db, sha256(apresentado))
    if linha is None or linha.expira_em < agora():
        raise NaoAutorizado()
    if linha.usado_em is not None:  # reuso: provável roubo
        await repo.revogar_familia(db, linha.familia_id)  # derruba toda a cadeia
        raise NaoAutorizado()
    await repo.marcar_usado(db, linha.id)
    return await emitir_par(db, linha.usuario_id, familia_id=linha.familia_id)
```

Guarde apenas o **hash** do refresh token no banco.

## Senhas: o que mudou no NIST SP 800-63B-4

Publicado em 2025-08-26, substitui a SP 800-63B
([senhas](https://pages.nist.gov/800-63-4/sp800-63b/authenticators/)):

| Regra | Detalhe |
|---|---|
| Tamanho mínimo | **15 caracteres** se a senha é o fator único; 8 se faz parte de MFA |
| Tamanho máximo | Permitir pelo menos 64 (SHOULD) |
| Caracteres | Aceitar ASCII imprimível, espaço e Unicode (cada code point conta como um caractere) |
| Composição | **Proibido** impor regras de composição (maiúscula, número, símbolo): levam a `Password1!` |
| Blocklist | Obrigatória: senhas comuns e vazadas |
| Resistência a phishing | Senha **não** é resistente a phishing; o AAL2 deve **oferecer** uma opção que seja (passkeys/WebAuthn) |
| Ataque online | Mitigado com *rate limiting* |

Armazenamento: Argon2id, ver [A04](../owasp-top-10-2025/a04-falhas-criptograficas/README.md).
Não verifiquei nesta pesquisa as regras do NIST sobre SMS/OTP via PSTN nem sobre troca periódica de
senha; consulte o texto normativo antes de afirmar.

## Onde guardar o token

| Opção | Veredito |
|---|---|
| `localStorage` / `sessionStorage` | **Nunca.** Qualquer XSS lê o token |
| Cookie `HttpOnly; Secure; SameSite=Lax`, sem `Domain=` | Padrão para web first-party: o JavaScript não toca no token |
| Access token curto (5 a 15 min) em memória + refresh rotativo em cookie `HttpOnly` | Bom para SPA com API separada |
| Mobile (Flutter) | Keychain/Keystore via armazenamento seguro do SO. Não pesquisei MASVS/MASTG nesta rodada |

```python
response.set_cookie(
    "refresh_token",
    token,
    max_age=60 * 60 * 24 * 14,
    path="/auth",
    httponly=True,
    secure=True,
    samesite="lax",
)
```

Com cookie, volta a haver CSRF: use a proteção do framework, `SameSite` como defesa em profundidade e
nunca mude estado via `GET` ([CSRF Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html)).
Para a verificação do JWT em si, ver [A07](../owasp-top-10-2025/a07-falhas-de-autenticacao/README.md).

## Autorização: policy engine em vez de `if role == "admin"`

### O problema

[`vulneravel.py`](vulneravel.py) decide com `usuario.role == "admin"`. Três falhas num só padrão:
a regra é copiada por endpoint (e diverge), compara string solta (`"Admin"` falha) e **esquece o
tenant**: o teste mostra um admin da empresa A excluindo a fatura da empresa B.

### A solução

[`seguro.py`](seguro.py) é um policy engine pequeno (uma classe e duas regras):

- Um único ponto de decisão, `PoliticaDeAcesso.pode(usuario, acao, recurso)`.
- Regras são funções pequenas e componíveis (`tem_papel("admin")`, `eh_dono`); a política é uma
  tabela `acao -> regras`, legível numa revisão.
- O **tenant é checado antes de qualquer regra**: nenhuma regra futura consegue esquecê-lo.
- **Nega por padrão**: ação desconhecida, lista de regras vazia e regra que lança exceção resultam em negado.
- `exigir(...)` levanta `AcessoNegadoError` com `status_http = 404`, para não revelar a existência do recurso.

Em FastAPI, o `exigir` entra como dependência (`Depends`) do endpoint, uma única vez, em vez de um `if`
em cada handler. O teste [`test_politica.py`](test_politica.py) cobre cada propriedade acima.

### Quando adotar um engine externo

Este exemplo cobre RBAC + dono + tenant. Quando as regras passarem a depender de muitos atributos,
relacionamentos (compartilhamento, hierarquias) ou precisarem ser editadas fora do deploy, avalie um
engine dedicado (Casbin, OPA/Rego, Cerbos, OpenFGA e similares). Não comparei esses projetos aqui:
cite-os como candidatos e avalie no momento da escolha.

## Referências

- [RFC 9700](https://www.rfc-editor.org/rfc/rfc9700), [RFC 7636](https://www.rfc-editor.org/rfc/rfc7636), [RFC 8725](https://www.rfc-editor.org/rfc/rfc8725)
- [OAuth 2.1 (draft)](https://datatracker.ietf.org/doc/draft-ietf-oauth-v2-1/)
- [NIST SP 800-63B-4](https://pages.nist.gov/800-63-4/sp800-63b.html)
- [OWASP Authorization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html)
- [OWASP Session Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html)
