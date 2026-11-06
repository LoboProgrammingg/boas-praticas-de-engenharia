import secrets

import pytest

from conftest import CarregarExemplo

CORPO = b'{"evento": "pagamento.confirmado", "id": "evt_1"}'
AGORA = 1_800_000_000.0


@pytest.fixture
def segredo() -> bytes:
    return secrets.token_bytes(32)


def test_vulneravel_aceita_mensagem_capturada_muito_tempo_depois(
    exemplo: CarregarExemplo, segredo: bytes
) -> None:
    vulneravel = exemplo("vulneravel.py")
    assinatura = vulneravel.assinar(segredo, CORPO)

    for _ in range(2):  # a mesma mensagem, reenviada, continua valendo
        assert vulneravel.processar_webhook(CORPO, assinatura, segredo)["id"] == "evt_1"


def test_seguro_aceita_mensagem_recente_e_assinada(
    exemplo: CarregarExemplo, segredo: bytes
) -> None:
    seguro = exemplo("seguro.py")
    timestamp = str(int(AGORA))
    assinatura = seguro.assinar(segredo, timestamp, CORPO)

    evento = seguro.processar_webhook(CORPO, timestamp, assinatura, segredo, AGORA)

    assert evento["evento"] == "pagamento.confirmado"


def test_seguro_recusa_replay_fora_da_janela(exemplo: CarregarExemplo, segredo: bytes) -> None:
    seguro = exemplo("seguro.py")
    timestamp = str(int(AGORA))
    assinatura = seguro.assinar(segredo, timestamp, CORPO)

    with pytest.raises(seguro.AssinaturaInvalidaError):
        seguro.processar_webhook(CORPO, timestamp, assinatura, segredo, AGORA + 3600)


def test_seguro_recusa_corpo_adulterado(exemplo: CarregarExemplo, segredo: bytes) -> None:
    seguro = exemplo("seguro.py")
    timestamp = str(int(AGORA))
    assinatura = seguro.assinar(segredo, timestamp, CORPO)

    with pytest.raises(seguro.AssinaturaInvalidaError):
        seguro.processar_webhook(
            CORPO.replace(b"evt_1", b"evt_2"), timestamp, assinatura, segredo, AGORA
        )


def test_seguro_recusa_timestamp_trocado_com_a_mesma_assinatura(
    exemplo: CarregarExemplo, segredo: bytes
) -> None:
    seguro = exemplo("seguro.py")
    assinatura = seguro.assinar(segredo, str(int(AGORA) - 3600), CORPO)

    with pytest.raises(seguro.AssinaturaInvalidaError):
        seguro.processar_webhook(CORPO, str(int(AGORA)), assinatura, segredo, AGORA)


@pytest.mark.parametrize("timestamp", ["", "abc", "-5", "12.5", "١٢٣"])
def test_seguro_recusa_timestamp_malformado(
    exemplo: CarregarExemplo, segredo: bytes, timestamp: str
) -> None:
    seguro = exemplo("seguro.py")

    with pytest.raises(seguro.AssinaturaInvalidaError):
        seguro.processar_webhook(CORPO, timestamp, "00", segredo, AGORA)


def test_seguro_recusa_assinatura_nao_ascii_sem_estourar_typeerror(
    exemplo: CarregarExemplo, segredo: bytes
) -> None:
    seguro = exemplo("seguro.py")

    with pytest.raises(seguro.AssinaturaInvalidaError):
        seguro.processar_webhook(CORPO, str(int(AGORA)), "assinatura-é", segredo, AGORA)
