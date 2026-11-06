from conftest import CarregarExemplo

INSTANCIA = "/pagamentos/abc123"


def test_ruim_erro_volta_com_200_e_vaza_detalhe_interno(exemplo: CarregarExemplo) -> None:
    ruim = exemplo("ruim.py")

    resposta = ruim.tratar(RuntimeError("psycopg: relation 'contas' does not exist"))

    assert resposta.status == 200
    assert "contas" in resposta.corpo["error"]


def test_bom_usa_media_type_problem_json_e_status_igual_ao_do_corpo(
    exemplo: CarregarExemplo,
) -> None:
    bom = exemplo("bom.py")

    resposta = bom.tratar(bom.SaldoInsuficienteError(30, 50), INSTANCIA)

    assert resposta.status == 403
    assert resposta.cabecalhos["Content-Type"] == "application/problem+json"
    assert resposta.corpo["status"] == resposta.status


def test_bom_membros_padrao_e_extensao_especifica_do_tipo(exemplo: CarregarExemplo) -> None:
    bom = exemplo("bom.py")

    corpo = bom.tratar(bom.SaldoInsuficienteError(30, 50), INSTANCIA).corpo

    assert corpo == {
        "type": "https://api.exemplo.com/problemas/saldo-insuficiente",
        "title": "Saldo insuficiente.",
        "status": 403,
        "detail": "Seu saldo é 30, mas a operação custa 50.",
        "instance": INSTANCIA,
        "balance": 30,
    }


def test_bom_erro_de_validacao_lista_cada_campo_com_ponteiro(exemplo: CarregarExemplo) -> None:
    bom = exemplo("bom.py")

    corpo = bom.tratar(
        bom.DadosInvalidosError("quantidade", "deve ser maior que zero"), INSTANCIA
    ).corpo

    assert corpo["errors"] == [{"detail": "deve ser maior que zero", "pointer": "#/quantidade"}]
    assert corpo["status"] == 422


def test_bom_type_padrao_e_about_blank_com_title_igual_a_frase_do_status(
    exemplo: CarregarExemplo,
) -> None:
    bom = exemplo("bom.py")

    resposta = bom.Problema(status=404).como_resposta()

    assert resposta.corpo == {"type": "about:blank", "title": "Not Found", "status": 404}


def test_bom_erro_inesperado_vira_500_generico_sem_vazar_detalhes(
    exemplo: CarregarExemplo,
) -> None:
    bom = exemplo("bom.py")

    resposta = bom.tratar(RuntimeError("psycopg: relation 'contas' does not exist"), INSTANCIA)

    assert resposta.status == 500
    assert "contas" not in str(resposta.corpo)
    assert resposta.corpo["title"] == "Internal Server Error"


def test_bom_extensoes_nao_sobrescrevem_membros_padrao(exemplo: CarregarExemplo) -> None:
    bom = exemplo("bom.py")

    corpo = bom.Problema(status=409, extensoes={"status": 200, "motivo": "x"}).como_resposta().corpo

    assert corpo["status"] == 409
    assert corpo["motivo"] == "x"
