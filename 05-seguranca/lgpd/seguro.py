"""LGPD: logar identificadores internos, nunca dados pessoais (minimização, art. 6º, III).

* ``registrar_login`` recebe só ``user_id`` e ``request_id``;
* ``FiltroSemPii`` é a rede de segurança: se um dado pessoal escapar para uma mensagem,
  ele é redigido antes de chegar ao handler.
"""

import logging
import re

PADRAO_CPF = re.compile(r"\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b")
PADRAO_EMAIL = re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+")
PADRAO_CAMPO_SENSIVEL = re.compile(r"(?i)\b(senha|password|token|authorization)\b(\s*[=:]\s*)\S+")


def redigir_texto(texto: str) -> str:
    texto = PADRAO_CPF.sub("[CPF]", texto)
    texto = PADRAO_EMAIL.sub("[EMAIL]", texto)
    return PADRAO_CAMPO_SENSIVEL.sub(r"\1\2[REDIGIDO]", texto)


class FiltroSemPii(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.msg = redigir_texto(record.getMessage())
        record.args = None
        return True


def registrar_login(log: logging.Logger, user_id: str, request_id: str) -> None:
    log.info("login_succeeded user_id=%s request_id=%s", user_id, request_id)
