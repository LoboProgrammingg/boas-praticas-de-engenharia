"""Fator III aplicado: a configuração vem do ambiente, tipada e validada na inicialização.

``Config.do_ambiente`` recebe o mapeamento de variáveis (``os.environ`` em produção, um
``dict`` nos testes). Se algo obrigatório faltar ou tiver o tipo errado, o processo falha
ao subir, e não no meio de uma requisição. A chave de API é ``SecretStr``: não aparece em
``repr`` nem em log.
"""

from collections.abc import Mapping

from pydantic import BaseModel, ConfigDict, SecretStr


class Config(BaseModel):
    model_config = ConfigDict(frozen=True)

    database_url: str
    api_key: SecretStr
    port: int = 8000

    @classmethod
    def do_ambiente(cls, ambiente: Mapping[str, str]) -> "Config":
        valores = {
            nome.lower(): valor
            for nome, valor in ambiente.items()
            if nome.lower() in cls.model_fields
        }
        return cls.model_validate(valores)
