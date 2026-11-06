"""O repositório segue o próprio padrão: todo tópico com exemplo tem README e teste."""

from pathlib import Path

RAIZ = Path(__file__).parent.parent
PARES = (("ruim.py", "bom.py"), ("vulneravel.py", "seguro.py"))
IGNORADAS = {".git", ".venv", "node_modules", ".mypy_cache", ".ruff_cache", ".pytest_cache"}


def _pastas_de_topico() -> list[Path]:
    return [
        pasta
        for pasta in RAIZ.rglob("*")
        if pasta.is_dir()
        and not IGNORADAS.intersection(pasta.parts)
        and any((pasta / ruim).exists() or (pasta / bom).exists() for ruim, bom in PARES)
    ]


def test_todo_exemplo_tem_par_readme_e_teste() -> None:
    problemas: list[str] = []
    for pasta in _pastas_de_topico():
        nome = pasta.relative_to(RAIZ)
        if not (pasta / "README.md").exists():
            problemas.append(f"{nome}: falta README.md")
        if not any(pasta.glob("test_*.py")) and not any(pasta.glob("*.test.ts")):
            problemas.append(f"{nome}: falta teste")
        for ruim, bom in PARES:
            if (pasta / ruim).exists() != (pasta / bom).exists():
                problemas.append(f"{nome}: {ruim} e {bom} devem existir juntos")
    assert problemas == []


def test_secoes_numeradas_tem_readme() -> None:
    secoes = [pasta for pasta in RAIZ.iterdir() if pasta.is_dir() and pasta.name[:2].isdigit()]
    assert all((secao / "README.md").exists() for secao in secoes)
