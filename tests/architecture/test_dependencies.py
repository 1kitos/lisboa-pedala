"""
Fitness functions — verificam as regras allowed-to-use
definidas em ARCHITECTURE.md e .importlinter.

Correr com: pytest tests/architecture/
Ou: lint-imports (directamente)
"""
import subprocess
import sys


def test_allowed_to_use_rules():
    """
    Verifica todas as regras allowed-to-use usando import-linter.
    Falha se qualquer componente importar de um módulo proibido
    ou se existir um ciclo de dependências.
    """
    result = subprocess.run(
        ["lint-imports"],
        capture_output=True,
        text=True,
    )
    print(result.stdout)
    if result.returncode != 0:
        print(result.stderr)
    assert result.returncode == 0, (
        "Violação de dependências detectada.\n"
        "Vê o output acima para identificar o componente e a importação proibida.\n"
        "Regras em ARCHITECTURE.md secção 2."
    )


def test_no_cycles():
    """
    Ciclos são verificados pelo contrato no-cycles no .importlinter.
    Este teste serve de documentação — a verificação real está em
    test_allowed_to_use_rules via lint-imports.
    """
    # Coberto pelo contrato no-cycles no .importlinter
    pass