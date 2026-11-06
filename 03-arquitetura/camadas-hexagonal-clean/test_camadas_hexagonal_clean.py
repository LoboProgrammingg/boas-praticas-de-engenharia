import ast
import sqlite3
from collections.abc import Iterator
from decimal import Decimal
from pathlib import Path

import pytest

from conftest import CarregarExemplo

PASTA = Path(__file__).parent


def _nomes_usados(arquivo: str, classe: str) -> set[str]:
    arvore = ast.parse((PASTA / arquivo).read_text(encoding="utf-8"))
    no = next(n for n in ast.walk(arvore) if isinstance(n, ast.ClassDef) and n.name == classe)
    return {n.id for n in ast.walk(no) if isinstance(n, ast.Name)}


@pytest.fixture
def conexao() -> Iterator[sqlite3.Connection]:
    conexao = sqlite3.connect(":memory:")
    yield conexao
    conexao.close()


class NotificadorEspiao:
    def __init__(self) -> None:
        self.avisados: list[str] = []

    def pedido_confirmado(self, pedido: object) -> None:
        self.avisados.append(getattr(pedido, "cliente", ""))


def test_ruim_regra_de_negocio_conhece_o_banco() -> None:
    assert "sqlite3" in _nomes_usados("ruim.py", "Pedido")


def test_ruim_confirmar_pedido_exige_infraestrutura_real(
    exemplo: CarregarExemplo, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    ruim = exemplo("ruim.py")
    monkeypatch.setattr(ruim, "CAMINHO_DO_BANCO", str(tmp_path / "pedidos.db"))

    ruim.Pedido("Ana", [Decimal("10")]).confirmar()

    assert (tmp_path / "pedidos.db").exists()


@pytest.mark.parametrize("classe", ["Pedido", "FazerPedido"])
def test_bom_camadas_internas_nao_mencionam_infraestrutura(classe: str) -> None:
    assert "sqlite3" not in _nomes_usados("bom.py", classe)


def test_bom_caso_de_uso_roda_com_adaptadores_em_memoria(exemplo: CarregarExemplo) -> None:
    bom = exemplo("bom.py")
    repositorio, notificador = bom.RepositorioEmMemoria(), NotificadorEspiao()

    pedido = bom.FazerPedido(repositorio, notificador)("Ana", (Decimal("10"), Decimal("5")))

    assert repositorio.salvos == [pedido]
    assert notificador.avisados == ["Ana"]
    assert pedido.total() == Decimal("15")


def test_bom_pedido_vazio_e_rejeitado_pelo_dominio_sem_tocar_na_infraestrutura(
    exemplo: CarregarExemplo,
) -> None:
    bom = exemplo("bom.py")
    repositorio, notificador = bom.RepositorioEmMemoria(), NotificadorEspiao()

    with pytest.raises(ValueError, match="vazio"):
        bom.FazerPedido(repositorio, notificador)("Ana", ())

    assert repositorio.salvos == []
    assert notificador.avisados == []


def test_bom_trocar_o_adaptador_nao_muda_o_caso_de_uso(
    exemplo: CarregarExemplo, conexao: sqlite3.Connection
) -> None:
    bom = exemplo("bom.py")

    bom.FazerPedido(bom.RepositorioSqlite(conexao), NotificadorEspiao())("Ana", (Decimal("10"),))

    assert conexao.execute("SELECT cliente, total FROM pedidos").fetchall() == [("Ana", "10")]
