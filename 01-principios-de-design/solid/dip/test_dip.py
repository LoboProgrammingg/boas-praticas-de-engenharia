from datetime import UTC, datetime

from conftest import CarregarExemplo

EXPIRACAO = datetime(2026, 1, 31, 23, 59, tzinfo=UTC)


class RelogioFixo:
    def __init__(self, momento: datetime) -> None:
        self._momento = momento

    def agora(self) -> datetime:
        return self._momento


def test_ruim_resultado_depende_do_dia_em_que_o_teste_roda(exemplo: CarregarExemplo) -> None:
    ruim = exemplo("ruim.py")

    assert ruim.Cupom("BEMVINDO", EXPIRACAO).esta_expirado() is (datetime.now(UTC) > EXPIRACAO)


def test_bom_testa_as_duas_bordas_de_forma_deterministica(exemplo: CarregarExemplo) -> None:
    bom = exemplo("bom.py")
    cupom = bom.Cupom("BEMVINDO", EXPIRACAO)

    assert not cupom.esta_expirado(RelogioFixo(datetime(2026, 1, 31, 23, 59, tzinfo=UTC)))
    assert cupom.esta_expirado(RelogioFixo(datetime(2026, 2, 1, 0, 0, tzinfo=UTC)))


def test_bom_em_producao_usa_o_relogio_real(exemplo: CarregarExemplo) -> None:
    bom = exemplo("bom.py")

    assert bom.RelogioDoSistema().agora().tzinfo is UTC
