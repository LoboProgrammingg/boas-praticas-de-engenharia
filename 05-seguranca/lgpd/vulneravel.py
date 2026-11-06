"""LGPD: o log vira um segundo banco de dados pessoais, sem controle de acesso.

E-mail, CPF e senha em texto puro, interpolados na mensagem.
"""

import logging


def registrar_login(log: logging.Logger, email: str, cpf: str, senha: str) -> None:
    log.info(f"login email={email} cpf={cpf} senha={senha}")
