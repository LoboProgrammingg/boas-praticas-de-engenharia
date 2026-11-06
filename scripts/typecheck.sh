#!/usr/bin/env bash
# mypy por pasta: tópicos diferentes repetem nomes de arquivo (ruim.py, bom.py),
# então cada pasta é verificada isoladamente, compartilhando o cache.
set -euo pipefail
cd "$(dirname "$0")/.."

uv run mypy conftest.py tests
mapfile -t pastas < <(find . -name '*.py' -not -path './.venv/*' -not -path './tests/*' \
  -not -path './conftest.py' -printf '%h\n' | grep -v '^\.$' | sort -u)
for pasta in "${pastas[@]}"; do
  uv run mypy "$pasta"
done
echo "mypy: ${#pastas[@]} pasta(s) de exemplo verificadas"
