import pytest

from conftest import CarregarExemplo


def test_vulneravel_deixa_admin_de_outra_empresa_excluir_a_fatura(
    exemplo: CarregarExemplo,
) -> None:
    vulneravel = exemplo("vulneravel.py")
    admin_da_empresa_a = vulneravel.Usuario("u1", "empresa-a", "admin")
    fatura_da_empresa_b = vulneravel.Fatura("f1", "empresa-b", "u9")

    assert vulneravel.pode_excluir_fatura(admin_da_empresa_a, fatura_da_empresa_b) is True


def test_vulneravel_quebra_com_variacao_do_nome_do_papel(exemplo: CarregarExemplo) -> None:
    vulneravel = exemplo("vulneravel.py")
    usuario = vulneravel.Usuario("u1", "empresa-a", "Admin")
    fatura = vulneravel.Fatura("f1", "empresa-a", "u1")

    assert vulneravel.pode_excluir_fatura(usuario, fatura) is False


def test_seguro_nega_admin_de_outro_tenant(exemplo: CarregarExemplo) -> None:
    seguro = exemplo("seguro.py")
    admin_da_empresa_a = seguro.Usuario("u1", "empresa-a", frozenset({"admin"}))
    fatura_da_empresa_b = seguro.Recurso("fatura", "empresa-b", "u9")

    assert not seguro.POLITICA_DE_FATURAS.pode(
        admin_da_empresa_a, "fatura:excluir", fatura_da_empresa_b
    )


def test_seguro_permite_admin_do_mesmo_tenant(exemplo: CarregarExemplo) -> None:
    seguro = exemplo("seguro.py")
    admin = seguro.Usuario("u1", "empresa-a", frozenset({"admin"}))
    fatura = seguro.Recurso("fatura", "empresa-a", "u9")

    assert seguro.POLITICA_DE_FATURAS.pode(admin, "fatura:excluir", fatura)


def test_seguro_combina_dono_ou_papel_para_leitura(exemplo: CarregarExemplo) -> None:
    seguro = exemplo("seguro.py")
    fatura = seguro.Recurso("fatura", "empresa-a", "u1")
    dono = seguro.Usuario("u1", "empresa-a", frozenset())
    financeiro = seguro.Usuario("u2", "empresa-a", frozenset({"financeiro"}))
    estranho = seguro.Usuario("u3", "empresa-a", frozenset())

    politica = seguro.POLITICA_DE_FATURAS

    assert politica.pode(dono, "fatura:ler", fatura)
    assert politica.pode(financeiro, "fatura:ler", fatura)
    assert not politica.pode(estranho, "fatura:ler", fatura)


def test_seguro_nega_por_padrao_acao_desconhecida(exemplo: CarregarExemplo) -> None:
    seguro = exemplo("seguro.py")
    admin = seguro.Usuario("u1", "empresa-a", frozenset({"admin"}))
    fatura = seguro.Recurso("fatura", "empresa-a", "u1")

    assert not seguro.POLITICA_DE_FATURAS.pode(admin, "fatura:exportar", fatura)


def test_seguro_nega_quando_uma_regra_lanca_excecao(exemplo: CarregarExemplo) -> None:
    seguro = exemplo("seguro.py")

    def regra_quebrada(_usuario: object, _recurso: object) -> bool:
        raise RuntimeError("serviço de atributos fora do ar")

    politica = seguro.PoliticaDeAcesso({"fatura:ler": [regra_quebrada]})
    usuario = seguro.Usuario("u1", "empresa-a", frozenset())
    fatura = seguro.Recurso("fatura", "empresa-a", "u1")

    assert not politica.pode(usuario, "fatura:ler", fatura)


def test_seguro_exigir_levanta_acesso_negado_com_404(exemplo: CarregarExemplo) -> None:
    seguro = exemplo("seguro.py")
    estranho = seguro.Usuario("u3", "empresa-a", frozenset())
    fatura = seguro.Recurso("fatura", "empresa-a", "u1")

    with pytest.raises(seguro.AcessoNegadoError) as erro:
        seguro.POLITICA_DE_FATURAS.exigir(estranho, "fatura:excluir", fatura)

    assert erro.value.status_http == 404
