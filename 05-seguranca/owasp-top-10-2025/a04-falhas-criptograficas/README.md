# A04:2025 Cryptographic Failures (senhas)

| | |
|---|---|
| **Categoria** | [A04:2025 Cryptographic Failures](https://owasp.org/Top10/2025/A04_2025-Cryptographic_Failures/) |
| **CWE típico** | [CWE-916](https://cwe.mitre.org/data/definitions/916.html): hash de senha com esforço computacional insuficiente |
| **Resolve** | Vazamento de banco virando vazamento de senhas em texto |
| **Em uma frase** | Guarde senha com um hash lento, com sal e memória-dura (Argon2id), nunca com SHA-256 |

## O problema

[`vulneravel.py`](vulneravel.py) usa `hashlib.sha256(senha).hexdigest()`. SHA-256 foi feito para
ser **rápido**, e sem sal a mesma senha produz sempre o mesmo valor: o atacante com o banco
usa tabelas pré-computadas e testa bilhões de candidatas por segundo. O teste mostra o
determinismo (mesma senha, mesmo hash, 64 caracteres hex).

## A solução

[`seguro.py`](seguro.py) usa Argon2id (`argon2-cffi`) com os parâmetros mínimos do
[Password Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html):
**19 MiB de memória, 2 iterações, paralelismo 1**. O hash resultante carrega algoritmo,
parâmetros e sal (`$argon2id$v=19$m=19456,t=2,p=1$...`), então:

- a mesma senha gera hashes diferentes (sal aleatório);
- `precisa_rehash` detecta hashes antigos para atualizar no próximo login;
- hash corrompido vira "senha inválida", não exceção que vaza para o cliente.

Alternativas equivalentes listadas pelo OWASP (memória, iterações, paralelismo):
`m=47104 (46 MiB), t=1, p=1`; `m=19456 (19 MiB), t=2, p=1`; `m=12288 (12 MiB), t=3, p=1`;
`m=9216 (9 MiB), t=4, p=1`; `m=7168 (7 MiB), t=5, p=1`. A troca é CPU × RAM.

## O que mais o OWASP diz

- Sem Argon2id disponível: scrypt (`N=2^17, r=8, p=1`); bcrypt só como legado, com *work factor*
  de pelo menos 10 e limite de 72 bytes; PBKDF2-HMAC-SHA-256 com pelo menos 600.000 iterações
  apenas se FIPS-140 for exigido.
- *Pepper* é opcional e, se usado, fica em vault/HSM, **separado do banco**.
- Defina um tamanho máximo razoável de senha: o custo do hash cresce com a entrada.

## Além de senhas

- Tokens aleatórios (reset de senha, convites): `secrets.token_urlsafe`, nunca `random`.
- Comparação de segredos e assinaturas: `hmac.compare_digest` (ver [A08](../a08-integridade-de-software-e-dados/README.md)).
- Não invente criptografia: use bibliotecas mantidas e protocolos padrão (TLS em todo tráfego externo).
- Chaves e segredos fora do código: ver [`segredos/`](../../segredos/README.md).

## Quando não aplicar

Argon2id é para **senhas de usuário**. Para verificar integridade ou derivar identificadores,
um hash rápido é o correto; para assinar mensagens, HMAC. Escolher a primitiva errada é a falha
criptográfica que esta categoria descreve.

## Referências

- [OWASP Password Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)
- [argon2-cffi: parâmetros](https://argon2-cffi.readthedocs.io/en/stable/parameters.html)
- [NIST SP 800-63B-4](https://pages.nist.gov/800-63-4/sp800-63b.html), regras de senha em [`autenticacao-e-autorizacao/`](../../autenticacao-e-autorizacao/README.md)
