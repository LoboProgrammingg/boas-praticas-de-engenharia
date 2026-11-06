import secrets
from datetime import UTC, datetime, timedelta
from types import ModuleType

import jwt
import pytest

from conftest import CarregarExemplo


@pytest.fixture
def chave() -> bytes:
    return secrets.token_bytes(64)


def _forjar(seguro: ModuleType, chave: bytes, **alteracoes: object) -> str:
    agora = datetime.now(UTC)
    claims: dict[str, object] = {
        "sub": "usuario-1",
        "aud": seguro.AUDIENCIA,
        "iss": seguro.EMISSOR,
        "iat": agora,
        "exp": agora + timedelta(minutes=5),
    }
    claims.update(alteracoes)
    return jwt.encode(claims, chave, algorithm="HS256")


def test_vulneravel_aceita_token_sem_assinatura(exemplo: CarregarExemplo, chave: bytes) -> None:
    vulneravel = exemplo("vulneravel.py")
    forjado = jwt.encode({"sub": "admin"}, None, algorithm="none")

    assert vulneravel.validar_token(forjado, chave)["sub"] == "admin"


def test_vulneravel_aceita_token_assinado_com_outra_chave(
    exemplo: CarregarExemplo, chave: bytes
) -> None:
    vulneravel = exemplo("vulneravel.py")
    forjado = jwt.encode({"sub": "admin"}, secrets.token_bytes(64), algorithm="HS256")

    assert vulneravel.validar_token(forjado, chave)["sub"] == "admin"


def test_seguro_aceita_token_legitimo(exemplo: CarregarExemplo, chave: bytes) -> None:
    seguro = exemplo("seguro.py")

    claims = seguro.validar_token(seguro.emitir_token(chave, "usuario-1"), chave)

    assert claims["sub"] == "usuario-1"


def test_seguro_rejeita_token_sem_assinatura(exemplo: CarregarExemplo, chave: bytes) -> None:
    seguro = exemplo("seguro.py")
    forjado = jwt.encode({"sub": "admin"}, None, algorithm="none")

    with pytest.raises(seguro.TokenInvalidoError):
        seguro.validar_token(forjado, chave)


def test_seguro_rejeita_token_assinado_com_outra_chave(
    exemplo: CarregarExemplo, chave: bytes
) -> None:
    seguro = exemplo("seguro.py")

    with pytest.raises(seguro.TokenInvalidoError):
        seguro.validar_token(_forjar(seguro, secrets.token_bytes(64)), chave)


def test_seguro_rejeita_algoritmo_fora_da_lista_fixa(
    exemplo: CarregarExemplo, chave: bytes
) -> None:
    seguro = exemplo("seguro.py")
    outro_algoritmo = jwt.encode({"sub": "admin"}, chave, algorithm="HS384")

    with pytest.raises(seguro.TokenInvalidoError):
        seguro.validar_token(outro_algoritmo, chave)


def test_seguro_rejeita_token_expirado(exemplo: CarregarExemplo, chave: bytes) -> None:
    seguro = exemplo("seguro.py")
    antigo = seguro.emitir_token(chave, "usuario-1", datetime.now(UTC) - timedelta(hours=2))

    with pytest.raises(seguro.TokenInvalidoError):
        seguro.validar_token(antigo, chave)


@pytest.mark.parametrize("claim", ["aud", "iss"])
def test_seguro_rejeita_audiencia_ou_emissor_errados(
    exemplo: CarregarExemplo, chave: bytes, claim: str
) -> None:
    seguro = exemplo("seguro.py")

    with pytest.raises(seguro.TokenInvalidoError):
        seguro.validar_token(_forjar(seguro, chave, **{claim: "outro"}), chave)


@pytest.mark.parametrize("claim", ["exp", "aud", "iss", "sub", "iat"])
def test_seguro_exige_as_claims_obrigatorias(
    exemplo: CarregarExemplo, chave: bytes, claim: str
) -> None:
    seguro = exemplo("seguro.py")
    agora = datetime.now(UTC)
    claims: dict[str, object] = {
        "sub": "usuario-1",
        "aud": seguro.AUDIENCIA,
        "iss": seguro.EMISSOR,
        "iat": agora,
        "exp": agora + timedelta(minutes=5),
    }
    del claims[claim]

    with pytest.raises(seguro.TokenInvalidoError):
        seguro.validar_token(jwt.encode(claims, chave, algorithm="HS256"), chave)
