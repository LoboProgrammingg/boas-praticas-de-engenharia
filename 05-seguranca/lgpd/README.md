# LGPD: incidentes, logs e minimização

> Material técnico para engenharia, **não parecer jurídico**. Confirme prazos e obrigações com
> o encarregado (DPO) e com a assessoria jurídica da sua organização.

| | |
|---|---|
| **Fontes** | [Lei 13.709/2018 (LGPD)](https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm), [ANPD: comunicado de incidente de segurança](https://www.gov.br/anpd/pt-br/canais_atendimento/agente-de-tratamento/comunicado-de-incidente-de-seguranca-cis) |
| **Resolve** | Dado pessoal vazando por logs, e incidente tratado sem prazo ou registro |
| **Em uma frase** | Colete e registre o mínimo; se algo vazar, o relógio de 3 dias úteis já está correndo |

## Incidente de segurança (art. 48 e Resolução CD/ANPD nº 15/2024)

O art. 48 manda o controlador comunicar à autoridade nacional **e ao titular** a ocorrência de incidente de
segurança que possa acarretar risco ou dano relevante aos titulares. O prazo foi regulamentado pela
**Resolução CD/ANPD nº 15/2024**, que a ANPD aprovou como
[Regulamento de Comunicação de Incidente de Segurança](https://www.gov.br/anpd/pt-br/assuntos/noticias/anpd-aprova-o-regulamento-de-comunicacao-de-incidente-de-seguranca).
Segundo a página da ANPD:

| Ponto | O que diz |
|---|---|
| Prazo | Comunicar a ANPD **e** os titulares em **3 dias úteis** (arts. 6º e 9º da Resolução), salvo legislação específica com outro prazo |
| Comunicação preliminar | Sem informação completa ou sem conseguir avisar todos os titulares a tempo, é possível enviar uma comunicação preliminar |
| Complementação | A comunicação preliminar pode ser complementada em até **20 dias úteis** a partir da data dela, no mesmo processo |
| Titulares | Avisar só a ANPD não basta |
| Risco | Dados de autenticação em sistema, financeiros, sensíveis, de menores ou tratados em larga escala caracterizam risco relevante |
| Registro | Manter registro dos incidentes por **pelo menos 5 anos** |

### O que isso pede da engenharia

- **Runbook de incidente** com responsáveis, canal e modelo da comunicação, ensaiado antes de precisar.
- **Quando começa a contar**: a ANPD fala em incidente *confirmado*; confirme com o jurídico o marco exato.
  Logs e alertas ([A09](../owasp-top-10-2025/a09-logging-e-alertas/README.md)) decidem quão cedo você sabe.
- **Responder rápido**: quais dados, de quantos titulares, por quanto tempo e quem acessou. Sem inventário de dados e
  sem logs de acesso, você não consegue responder.
- **Rotacionar credenciais primeiro** ([`segredos/`](../segredos/README.md)) e preservar evidências.
- **Registrar** todo incidente, inclusive os que não geraram comunicação.

## Logs sem dado pessoal

O art. 37 manda manter registro das operações de tratamento; e o log, por si só, **é tratamento de dado
pessoal** quando contém CPF, e-mail ou IP. Regra do repositório: logar identificadores internos
(`user_id`, `request_id`), nunca CPF, e-mail completo, senha, token ou cartão.

[`vulneravel.py`](vulneravel.py) interpola e-mail, CPF e senha na mensagem. [`seguro.py`](seguro.py):

- `registrar_login(log, user_id, request_id)` só aceita identificadores internos;
- `FiltroSemPii` (um `logging.Filter` no handler) redige CPF, e-mail e pares `senha=`/`token=`/`authorization:` que
  escaparem para uma mensagem. É **rede de segurança**, não substituto de não logar o dado: uma regex nunca cobre
  todos os formatos.

O teste [`test_logs.py`](test_logs.py) usa um CPF obviamente fictício (`000.000.000-00`) e um `StringIO`: a versão
vulnerável grava o dado, a segura não, e o filtro redige o que vazou por engano.

```bash
uv run pytest 05-seguranca/lgpd
```

## Minimização

O art. 6º, III, define a **necessidade** como "limitação do tratamento ao mínimo necessário para a realização de
suas finalidades". Na prática:

- Não colete o campo "por via das dúvidas"; cada campo precisa de uma finalidade.
- Respostas de API só com o que o cliente precisa ([API3](../api-security/README.md)).
- Defina **prazo de retenção** e apague/anonimize depois dele; backups e logs também têm retenção.
- Separe identificadores: use um `user_id` opaco em logs, métricas e analytics.
- Ambientes de teste e staging com dados sintéticos, não cópias de produção.
- O art. 46 exige medidas de segurança técnicas e administrativas aptas a proteger os dados contra acessos não
  autorizados; todo o restante desta seção são exemplos dessas medidas.

## Referências

- [Lei 13.709/2018 (LGPD)](https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm), arts. 6º, 37, 46 e 48
- [ANPD: comunicado de incidente de segurança](https://www.gov.br/anpd/pt-br/canais_atendimento/agente-de-tratamento/comunicado-de-incidente-de-seguranca-cis)
- [ANPD: aprovação do Regulamento de Comunicação de Incidente de Segurança](https://www.gov.br/anpd/pt-br/assuntos/noticias/anpd-aprova-o-regulamento-de-comunicacao-de-incidente-de-seguranca)
- [OWASP Logging Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html)
