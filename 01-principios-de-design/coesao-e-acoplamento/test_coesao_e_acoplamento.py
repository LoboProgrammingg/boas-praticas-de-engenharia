from decimal import Decimal

import pytest

from conftest import CarregarExemplo


class CanalEmMemoria:
    def __init__(self) -> None:
        self.enviados: list[tuple[str, str]] = []

    def enviar(self, telefone: str, mensagem: str) -> None:
        self.enviados.append((telefone, mensagem))


def test_ruim_mistura_assuntos_sem_relacao_na_mesma_classe(exemplo: CarregarExemplo) -> None:
    ruim = exemplo("ruim.py")

    metodos = {nome for nome in vars(ruim.Utils) if not nome.startswith("__")}

    assert metodos == {"formatar_cpf", "enviar_sms", "calcular_frete"}


def test_ruim_compartilha_estado_global_entre_quem_nao_tem_nada_a_ver(
    exemplo: CarregarExemplo,
) -> None:
    ruim = exemplo("ruim.py")

    ruim.Utils.enviar_sms("8199999-0000", "promoção do marketing")
    ruim.Utils.enviar_sms("8188888-0000", "aviso de entrega")

    assert len(ruim.SMS_ENVIADOS) == 2


def test_bom_formata_cpf_e_recusa_documento_malformado(exemplo: CarregarExemplo) -> None:
    bom = exemplo("bom.py")

    assert bom.Cpf("11144477735").formatado() == "111.444.777-35"
    with pytest.raises(ValueError, match="11 dígitos"):
        bom.Cpf("123")


def test_bom_calcula_frete_sem_depender_de_nada_alem_dos_proprios_dados(
    exemplo: CarregarExemplo,
) -> None:
    bom = exemplo("bom.py")

    assert bom.TabelaDeFrete().calcular(20) == Decimal("20.0")
    assert bom.TabelaDeFrete(base=Decimal("5"), por_km=Decimal("1")).calcular(20) == Decimal("25")


def test_bom_cada_servico_de_sms_tem_o_proprio_canal_sem_estado_compartilhado(
    exemplo: CarregarExemplo,
) -> None:
    bom = exemplo("bom.py")
    canal_a, canal_b = CanalEmMemoria(), CanalEmMemoria()

    bom.ServicoDeSms(canal_a).avisar_entrega("8199999-0000", "42")

    assert canal_a.enviados == [("8199999-0000", "Seu pedido 42 saiu para entrega.")]
    assert canal_b.enviados == []
