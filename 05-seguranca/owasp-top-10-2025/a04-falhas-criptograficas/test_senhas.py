from argon2 import PasswordHasher

from conftest import CarregarExemplo

SENHA = "correct horse battery staple"


def test_vulneravel_gera_sempre_o_mesmo_hash_e_permite_tabela_pre_computada(
    exemplo: CarregarExemplo,
) -> None:
    vulneravel = exemplo("vulneravel.py")

    assert vulneravel.hash_senha(SENHA) == vulneravel.hash_senha(SENHA)
    assert len(vulneravel.hash_senha(SENHA)) == 64  # SHA-256 em hex, sem sal nem custo


def test_seguro_usa_argon2id_com_os_parametros_minimos_do_owasp(
    exemplo: CarregarExemplo,
) -> None:
    seguro = exemplo("seguro.py")

    assert seguro.hash_senha(SENHA).startswith("$argon2id$v=19$m=19456,t=2,p=1$")


def test_seguro_gera_hash_diferente_a_cada_chamada_por_causa_do_sal(
    exemplo: CarregarExemplo,
) -> None:
    seguro = exemplo("seguro.py")

    assert seguro.hash_senha(SENHA) != seguro.hash_senha(SENHA)


def test_seguro_verifica_senha_certa_e_rejeita_a_errada(exemplo: CarregarExemplo) -> None:
    seguro = exemplo("seguro.py")
    guardado = seguro.hash_senha(SENHA)

    assert seguro.verificar_senha(guardado, SENHA) is True
    assert seguro.verificar_senha(guardado, "outra senha") is False


def test_seguro_trata_hash_corrompido_como_falha_de_verificacao(
    exemplo: CarregarExemplo,
) -> None:
    seguro = exemplo("seguro.py")

    assert seguro.verificar_senha("isto-nao-e-um-hash", SENHA) is False


def test_seguro_detecta_hash_antigo_que_precisa_de_rehash(exemplo: CarregarExemplo) -> None:
    seguro = exemplo("seguro.py")
    fraco = PasswordHasher(time_cost=1, memory_cost=8, parallelism=1).hash(SENHA)

    assert seguro.precisa_rehash(fraco) is True
    assert seguro.precisa_rehash(seguro.hash_senha(SENHA)) is False
