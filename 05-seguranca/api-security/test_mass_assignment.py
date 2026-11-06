import pytest
from pydantic import ValidationError

from conftest import CarregarExemplo


def test_vulneravel_deixa_o_cliente_virar_admin_e_trocar_de_tenant(
    exemplo: CarregarExemplo,
) -> None:
    vulneravel = exemplo("vulneravel.py")
    usuario = vulneravel.Usuario(id=1, tenant_id=10, display_name="Ana")

    vulneravel.atualizar_perfil(usuario, {"display_name": "Ana", "is_admin": True, "tenant_id": 99})

    assert usuario.is_admin is True
    assert usuario.tenant_id == 99


def test_vulneravel_expoe_o_hash_da_senha_na_resposta(exemplo: CarregarExemplo) -> None:
    vulneravel = exemplo("vulneravel.py")
    usuario = vulneravel.Usuario(id=1, tenant_id=10, display_name="Ana")

    assert "senha_hash" in vulneravel.perfil_para_resposta(usuario)


def test_seguro_rejeita_campos_que_o_cliente_nao_deveria_enviar(
    exemplo: CarregarExemplo,
) -> None:
    seguro = exemplo("seguro.py")
    usuario = seguro.Usuario(id=1, tenant_id=10, display_name="Ana")

    with pytest.raises(ValidationError):
        seguro.atualizar_perfil(usuario, {"display_name": "Ana", "is_admin": True})

    assert usuario.is_admin is False


def test_seguro_atualiza_apenas_o_campo_permitido(exemplo: CarregarExemplo) -> None:
    seguro = exemplo("seguro.py")
    usuario = seguro.Usuario(id=1, tenant_id=10, display_name="Ana")

    seguro.atualizar_perfil(usuario, {"display_name": "  Ana Souza  "})

    assert usuario.display_name == "Ana Souza"
    assert usuario.tenant_id == 10


@pytest.mark.parametrize("nome", ["", "   ", "x" * 81])
def test_seguro_valida_tamanho_do_campo(exemplo: CarregarExemplo, nome: str) -> None:
    seguro = exemplo("seguro.py")
    usuario = seguro.Usuario(id=1, tenant_id=10, display_name="Ana")

    with pytest.raises(ValidationError):
        seguro.atualizar_perfil(usuario, {"display_name": nome})


def test_seguro_responde_so_com_os_campos_publicos(exemplo: CarregarExemplo) -> None:
    seguro = exemplo("seguro.py")
    usuario = seguro.Usuario(id=1, tenant_id=10, display_name="Ana")

    assert seguro.perfil_para_resposta(usuario) == {"id": 1, "display_name": "Ana"}
