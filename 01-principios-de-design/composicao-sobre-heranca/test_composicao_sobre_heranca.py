import pytest

from conftest import CarregarExemplo


def test_ruim_reenvia_apenas_no_canal_em_que_a_subclasse_foi_escrita(
    exemplo: CarregarExemplo,
) -> None:
    ruim = exemplo("ruim.py")
    smtp = ruim.NotificadorSmtpComReenvio(falhas_iniciais=2)

    smtp.enviar("oi")

    assert smtp.enviados == ["oi"]


def test_ruim_nao_tem_como_dar_reenvio_ao_sms_sem_copiar_o_laco(exemplo: CarregarExemplo) -> None:
    ruim = exemplo("ruim.py")
    sms = ruim.NotificadorSms(falhas_iniciais=2)

    with pytest.raises(ruim.FalhaTransitoriaError):
        sms.enviar("oi")

    assert not hasattr(ruim, "NotificadorSmsComReenvio")


def test_bom_da_reenvio_a_qualquer_canal_por_composicao(exemplo: CarregarExemplo) -> None:
    bom = exemplo("bom.py")
    sms = bom.NotificadorSms(falhas_iniciais=2)

    bom.ComReenvio(sms).enviar("oi")

    assert sms.enviados == ["oi"]


def test_bom_desiste_depois_do_limite_de_tentativas(exemplo: CarregarExemplo) -> None:
    bom = exemplo("bom.py")
    smtp = bom.NotificadorSmtp(falhas_iniciais=3)

    with pytest.raises(bom.FalhaTransitoriaError):
        bom.ComReenvio(smtp, tentativas=3).enviar("oi")

    assert smtp.enviados == []


def test_bom_combina_comportamentos_so_na_montagem(exemplo: CarregarExemplo) -> None:
    bom = exemplo("bom.py")
    registro: list[str] = []
    smtp = bom.NotificadorSmtp(falhas_iniciais=1)
    notificador = bom.ComRegistro(bom.ComReenvio(smtp), registro)

    notificador.enviar("oi")

    assert (registro, smtp.enviados) == (["enviando: oi"], ["oi"])
