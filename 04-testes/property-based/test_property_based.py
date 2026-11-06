from itertools import pairwise

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from conftest import CarregarExemplo

DETERMINISTICO = settings(database=None, derandomize=True, max_examples=200)

TEXTOS_COM_REPETICOES = st.lists(st.tuples(st.sampled_from("abc"), st.integers(1, 15))).map(
    lambda trechos: "".join(caractere * vezes for caractere, vezes in trechos)
)


def test_ruim_passa_nos_exemplos_classicos(exemplo: CarregarExemplo) -> None:
    ruim = exemplo("ruim.py")

    assert ruim.codificar("aaabcc") == "3a1b2c"
    assert ruim.decodificar("3a1b2c") == "aaabcc"
    assert ruim.decodificar(ruim.codificar("")) == ""


def test_ruim_a_propriedade_de_ida_e_volta_acha_o_defeito(exemplo: CarregarExemplo) -> None:
    ruim = exemplo("ruim.py")

    @DETERMINISTICO
    @given(TEXTOS_COM_REPETICOES)
    def ida_e_volta(texto: str) -> None:
        assert ruim.decodificar(ruim.codificar(texto)) == texto

    with pytest.raises((AssertionError, ValueError)):
        ida_e_volta()


def test_bom_ida_e_volta_vale_para_qualquer_texto(exemplo: CarregarExemplo) -> None:
    bom = exemplo("bom.py")

    @DETERMINISTICO
    @given(st.one_of(st.text(max_size=60), TEXTOS_COM_REPETICOES))
    def ida_e_volta(texto: str) -> None:
        assert bom.decodificar(bom.codificar(texto)) == texto

    ida_e_volta()


def test_bom_pares_vizinhos_sempre_tem_caracteres_diferentes(exemplo: CarregarExemplo) -> None:
    bom = exemplo("bom.py")

    @DETERMINISTICO
    @given(TEXTOS_COM_REPETICOES)
    def sem_pares_repetidos(texto: str) -> None:
        codigo = bom.codificar(texto)
        assert all(a[0] != b[0] for a, b in pairwise(codigo))
        assert all(contagem >= 1 for _, contagem in codigo)

    sem_pares_repetidos()


def test_bom_codificar_nunca_aumenta_o_numero_de_pares_alem_do_tamanho(
    exemplo: CarregarExemplo,
) -> None:
    bom = exemplo("bom.py")

    @DETERMINISTICO
    @given(TEXTOS_COM_REPETICOES)
    def tamanho(texto: str) -> None:
        assert len(bom.codificar(texto)) <= len(texto)

    tamanho()
