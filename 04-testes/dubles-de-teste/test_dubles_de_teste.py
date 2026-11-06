from unittest.mock import Mock, create_autospec

import pytest

from conftest import CarregarExemplo


def test_ruim_mock_sem_spec_fica_verde_mesmo_chamando_metodo_que_nao_existe(
    exemplo: CarregarExemplo,
) -> None:
    ruim = exemplo("ruim.py")
    repositorio, notificador = Mock(), Mock()

    ruim.Cadastrar(repositorio, notificador).executar("ana@exemplo.com")

    repositorio.adicionar.assert_called_once_with("ana@exemplo.com")


def test_ruim_o_mesmo_codigo_quebra_com_o_repositorio_de_verdade(
    exemplo: CarregarExemplo,
) -> None:
    ruim = exemplo("ruim.py")
    caso_de_uso = ruim.Cadastrar(ruim.RepositorioDeUsuarios(), Mock())

    with pytest.raises(AttributeError, match="adicionar"):
        caso_de_uso.executar("ana@exemplo.com")


def test_bom_fake_guarda_o_estado_e_o_teste_verifica_o_resultado(
    exemplo: CarregarExemplo,
) -> None:
    bom = exemplo("bom.py")
    repositorio = bom.RepositorioEmMemoria()
    caso_de_uso = bom.Cadastrar(repositorio, bom.NotificadorNulo(), bom.RelogioFixo(bom.INSTANTE))

    caso_de_uso.executar("ana@exemplo.com")

    assert repositorio.existe("ana@exemplo.com")


def test_bom_fake_com_comportamento_real_permite_testar_email_duplicado(
    exemplo: CarregarExemplo,
) -> None:
    bom = exemplo("bom.py")
    caso_de_uso = bom.Cadastrar(
        bom.RepositorioEmMemoria(), bom.NotificadorNulo(), bom.RelogioFixo(bom.INSTANTE)
    )
    caso_de_uso.executar("ana@exemplo.com")

    with pytest.raises(bom.EmailJaCadastradoError):
        caso_de_uso.executar("ana@exemplo.com")


def test_bom_stub_de_relogio_deixa_a_data_deterministica(exemplo: CarregarExemplo) -> None:
    bom = exemplo("bom.py")
    caso_de_uso = bom.Cadastrar(
        bom.RepositorioEmMemoria(), bom.NotificadorNulo(), bom.RelogioFixo(bom.INSTANTE)
    )

    usuario = caso_de_uso.executar("ana@exemplo.com")

    assert usuario.cadastrado_em == bom.INSTANTE


def test_bom_spy_registra_a_notificacao_para_o_teste_consultar(exemplo: CarregarExemplo) -> None:
    bom = exemplo("bom.py")
    espiao = bom.NotificadorEspiao()
    caso_de_uso = bom.Cadastrar(bom.RepositorioEmMemoria(), espiao, bom.RelogioFixo(bom.INSTANTE))

    caso_de_uso.executar("ana@exemplo.com")

    assert espiao.enviados == ["ana@exemplo.com"]


def test_bom_mock_com_autospec_recusa_metodo_que_a_porta_nao_tem(
    exemplo: CarregarExemplo,
) -> None:
    bom = exemplo("bom.py")
    repositorio = create_autospec(bom.RepositorioDeUsuarios, instance=True)

    with pytest.raises(AttributeError):
        repositorio.adicionar("ana@exemplo.com")
