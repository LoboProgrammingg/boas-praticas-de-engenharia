from collections.abc import Mapping

import pytest

from conftest import CarregarExemplo


@pytest.mark.parametrize("valor", ["80a", ""])
def test_ruim_engole_valor_nao_numerico_e_sobe_na_porta_padrao(
    exemplo: CarregarExemplo, monkeypatch: pytest.MonkeyPatch, valor: str
) -> None:
    ruim = exemplo("ruim.py")
    monkeypatch.setenv("PORT", valor)

    assert ruim.porta() == 8080


@pytest.mark.parametrize("valor", ["0", "70000", "-1"])
def test_ruim_aceita_porta_fora_do_intervalo_valido(
    exemplo: CarregarExemplo, monkeypatch: pytest.MonkeyPatch, valor: str
) -> None:
    ruim = exemplo("ruim.py")
    monkeypatch.setenv("PORT", valor)

    assert ruim.porta() == int(valor)


def test_ruim_nao_distingue_variavel_ausente_de_variavel_digitada_errado(
    exemplo: CarregarExemplo, monkeypatch: pytest.MonkeyPatch
) -> None:
    ruim = exemplo("ruim.py")

    monkeypatch.delenv("PORT", raising=False)
    ausente = ruim.porta()
    monkeypatch.setenv("PORT", "80a")
    errada = ruim.porta()

    assert ausente == errada == 8080


@pytest.mark.parametrize("valor", ["80a", "", "70000", "-1", "0"])
def test_bom_recusa_valor_invalido_com_mensagem_que_aponta_a_causa(
    exemplo: CarregarExemplo, valor: str
) -> None:
    bom = exemplo("bom.py")

    with pytest.raises(bom.ConfiguracaoInvalidaError, match="PORT"):
        bom.ler_porta({"PORT": valor})


def test_bom_preserva_a_causa_original_do_erro(exemplo: CarregarExemplo) -> None:
    bom = exemplo("bom.py")

    with pytest.raises(bom.ConfiguracaoInvalidaError) as informacao:
        bom.ler_porta({"PORT": "80a"})

    assert isinstance(informacao.value.__cause__, ValueError)


@pytest.mark.parametrize(
    ("ambiente", "esperada"),
    [({}, 8080), ({"PORT": "3000"}, 3000), ({"PORT": "65535"}, 65535)],
)
def test_bom_aceita_ausente_com_padrao_explicito_e_valores_validos(
    exemplo: CarregarExemplo, ambiente: Mapping[str, str], esperada: int
) -> None:
    bom = exemplo("bom.py")

    assert bom.ler_porta(ambiente) == esperada
