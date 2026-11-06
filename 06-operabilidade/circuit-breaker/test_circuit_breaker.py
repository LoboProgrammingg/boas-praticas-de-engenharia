import pytest

from conftest import CarregarExemplo


class RelogioFalso:
    def __init__(self) -> None:
        self.agora = 0.0

    def __call__(self) -> float:
        return self.agora


class Fornecedor:
    def __init__(self) -> None:
        self.chamadas = 0
        self.fora_do_ar = True

    def __call__(self, usuario: str = "") -> list[str]:
        self.chamadas += 1
        if self.fora_do_ar:
            raise TimeoutError("fornecedor não respondeu")
        return ["a", "b"]


def test_ruim_cada_requisicao_insiste_no_fornecedor_que_esta_fora(
    exemplo: CarregarExemplo,
) -> None:
    ruim = exemplo("ruim.py")
    fornecedor = Fornecedor()

    for _ in range(20):
        with pytest.raises(TimeoutError):
            ruim.buscar_recomendacoes(fornecedor, "ana")

    assert fornecedor.chamadas == 20


def test_bom_abre_apos_n_falhas_e_poupa_o_fornecedor(exemplo: CarregarExemplo) -> None:
    bom = exemplo("bom.py")
    fornecedor = Fornecedor()
    breaker = bom.CircuitBreaker(limite_de_falhas=3, relogio=RelogioFalso())

    rejeitadas = 0
    for _ in range(20):
        try:
            breaker.chamar(fornecedor)
        except bom.CircuitoAbertoError:
            rejeitadas += 1
        except TimeoutError:
            pass

    assert fornecedor.chamadas == 3
    assert rejeitadas == 17
    assert breaker.estado == "aberto"


def test_bom_continua_fechado_abaixo_do_limite(exemplo: CarregarExemplo) -> None:
    bom = exemplo("bom.py")
    fornecedor = Fornecedor()
    breaker = bom.CircuitBreaker(limite_de_falhas=3, relogio=RelogioFalso())

    for _ in range(2):
        with pytest.raises(TimeoutError):
            breaker.chamar(fornecedor)

    assert breaker.estado == "fechado"


def test_bom_um_sucesso_zera_a_contagem_de_falhas(exemplo: CarregarExemplo) -> None:
    bom = exemplo("bom.py")
    fornecedor = Fornecedor()
    breaker = bom.CircuitBreaker(limite_de_falhas=3, relogio=RelogioFalso())
    for _ in range(2):
        with pytest.raises(TimeoutError):
            breaker.chamar(fornecedor)
    fornecedor.fora_do_ar = False
    breaker.chamar(fornecedor)
    fornecedor.fora_do_ar = True

    for _ in range(2):
        with pytest.raises(TimeoutError):
            breaker.chamar(fornecedor)

    assert breaker.estado == "fechado"


def test_bom_meio_aberto_apos_o_tempo_e_fecha_quando_a_tentativa_funciona(
    exemplo: CarregarExemplo,
) -> None:
    bom = exemplo("bom.py")
    relogio, fornecedor = RelogioFalso(), Fornecedor()
    breaker = bom.CircuitBreaker(limite_de_falhas=2, reabrir_apos=30.0, relogio=relogio)
    for _ in range(2):
        with pytest.raises(TimeoutError):
            breaker.chamar(fornecedor)
    relogio.agora = 29.9
    assert breaker.estado == "aberto"

    relogio.agora = 30.0
    fornecedor.fora_do_ar = False

    assert breaker.estado == "meio-aberto"
    assert breaker.chamar(fornecedor) == ["a", "b"]
    assert breaker.estado == "fechado"


def test_bom_tentativa_meio_aberta_que_falha_reabre_o_circuito(exemplo: CarregarExemplo) -> None:
    bom = exemplo("bom.py")
    relogio, fornecedor = RelogioFalso(), Fornecedor()
    breaker = bom.CircuitBreaker(limite_de_falhas=2, reabrir_apos=30.0, relogio=relogio)
    for _ in range(2):
        with pytest.raises(TimeoutError):
            breaker.chamar(fornecedor)
    relogio.agora = 30.0

    with pytest.raises(TimeoutError):
        breaker.chamar(fornecedor)

    assert breaker.estado == "aberto"
    with pytest.raises(bom.CircuitoAbertoError):
        breaker.chamar(fornecedor)
    relogio.agora = 59.9
    assert breaker.estado == "aberto"
    relogio.agora = 60.0
    assert breaker.estado == "meio-aberto"


def test_bom_erros_que_nao_contam_como_falha_nao_abrem_o_circuito(
    exemplo: CarregarExemplo,
) -> None:
    bom = exemplo("bom.py")
    breaker = bom.CircuitBreaker(
        limite_de_falhas=1, relogio=RelogioFalso(), conta_como_falha=(TimeoutError,)
    )

    def operacao_com_bug() -> None:
        raise KeyError("bug nosso, não do fornecedor")

    with pytest.raises(KeyError):
        breaker.chamar(operacao_com_bug)

    assert breaker.estado == "fechado"
