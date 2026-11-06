# A07:2025 Authentication Failures (JWT)

| | |
|---|---|
| **Categoria** | [A07:2025 Authentication Failures](https://owasp.org/Top10/2025/A07_2025-Authentication_Failures/) |
| **Norma** | [RFC 8725](https://www.rfc-editor.org/rfc/rfc8725) (JWT Best Current Practices) |
| **Resolve** | Tokens forjados, algoritmo escolhido pelo atacante, token de outro serviço aceito |
| **Em uma frase** | Quem verifica decide o algoritmo e as claims; o token nunca decide |

## O problema

[`vulneravel.py`](vulneravel.py) chama `jwt.decode(token, options={"verify_signature": False})`.
Um JWT é só JSON codificado em base64: sem verificar a assinatura, qualquer pessoa escreve
`{"sub": "admin"}`. Os testes forjam um token `alg: none` e outro assinado com uma chave
aleatória; os dois passam.

Variante clássica: `algorithms=jwt.get_unverified_header(token)["alg"]`. Deixar o header (controlado
pelo atacante) ditar o algoritmo reabre *algorithm confusion* e `none`.

## A solução

[`seguro.py`](seguro.py), com PyJWT:

| Controle | Como |
|---|---|
| Algoritmo | `algorithms=["HS256"]`, lista fixa no verificador |
| Expiração | `exp` obrigatório e validade curta (15 min) |
| Destinatário | `aud` conferido contra a audiência esperada |
| Emissor | `iss` conferido contra o emissor esperado |
| Claims obrigatórias | `options={"require": ["exp", "iat", "sub", "aud", "iss"]}` |
| Relógio | `leeway` de poucos segundos, nunca minutos |
| Falha | `jwt.InvalidTokenError` vira `TokenInvalidoError`, sem detalhe para o cliente |

Os testes cobrem: token legítimo, sem assinatura, chave errada, algoritmo fora da lista (HS384),
expirado, `aud`/`iss` errados e cada claim obrigatória ausente. A chave é gerada em tempo de
execução (`secrets.token_bytes(64)`); em produção ela vem do ambiente ou de um vault.

## Regras que o exemplo não mostra

- **Uma chave, um algoritmo.** Não misture HS256 e RS256 no mesmo verificador (*key confusion*).
  Para vários serviços, prefira assinatura assimétrica (ES256, EdDSA) e distribua só a chave pública.
- **JWT é assinado, não criptografado**: não ponha dado sensível no payload
  ([doc do FastAPI](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/)).
- **Nunca em `localStorage`**: qualquer XSS lê. Detalhes e alternativas em
  [`autenticacao-e-autorizacao/`](../../autenticacao-e-autorizacao/README.md).
- Revogação: JWT de acesso curto + refresh token rotativo, com detecção de reuso.
- Força bruta: limite por (IP + identificador) e por conta, com backoff; resposta idêntica para
  usuário inexistente e senha errada.
- MFA: o NIST SP 800-63B-4 exige que o AAL2 **ofereça** uma opção resistente a phishing; na prática,
  passkeys (WebAuthn/FIDO2).

## Referências

- [OWASP A07:2025](https://owasp.org/Top10/2025/A07_2025-Authentication_Failures/)
- [RFC 8725: JWT BCP](https://www.rfc-editor.org/rfc/rfc8725)
- [PyJWT](https://pyjwt.readthedocs.io/en/stable/)
- [Session Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html)
