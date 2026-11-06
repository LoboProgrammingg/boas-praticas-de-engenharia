from decimal import Decimal
from pathlib import Path

import pytest

from conftest import CarregarExemplo

CSV = "produto,quantidade,preco\ncafe,2,10.00\npao,3,1.50\ncafe,1,10.00\n"


def test_ruim_so_calcula_com_arquivo_em_disco_e_saida_capturada(
    exemplo: CarregarExemplo, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    ruim = exemplo("ruim.py")
    arquivo = tmp_path / "vendas.csv"
    arquivo.write_text(CSV, encoding="utf-8")

    ruim.relatorio(str(arquivo))

    assert capsys.readouterr().out.splitlines() == [
        "cafe     R$   30.00",
        "pao      R$    4.50",
    ]


def test_ruim_nem_chega_ao_calculo_sem_o_arquivo(exemplo: CarregarExemplo) -> None:
    ruim = exemplo("ruim.py")

    with pytest.raises(FileNotFoundError):
        ruim.relatorio("nao-existe.csv")


def test_bom_calcula_totais_sem_disco_e_sem_saida(exemplo: CarregarExemplo) -> None:
    bom = exemplo("bom.py")

    totais = bom.totais_por_produto(bom.ler_vendas(CSV))

    assert totais == {"cafe": Decimal("30.00"), "pao": Decimal("4.50")}


def test_bom_troca_o_formato_sem_tocar_na_leitura_nem_no_calculo(
    exemplo: CarregarExemplo,
) -> None:
    bom = exemplo("bom.py")
    totais = {"cafe": Decimal("30.00")}

    assert bom.formatar_relatorio(totais) == "cafe     R$   30.00"


def test_bom_gera_o_mesmo_relatorio_que_o_ruim_imprime(exemplo: CarregarExemplo) -> None:
    bom = exemplo("bom.py")

    assert bom.gerar_relatorio(CSV).splitlines() == [
        "cafe     R$   30.00",
        "pao      R$    4.50",
    ]
