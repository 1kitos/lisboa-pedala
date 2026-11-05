import sqlite3
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime



DuracaoMinutos = int

@dataclass
class DadosFatura:
    viagem_id: str
    utilizador_id: str
    duracao_minutos: DuracaoMinutos
    tipo_utilizador: str  # "assinante" | "ocasional"
    valor_euros: float
    timestamp_inicio: datetime
    timestamp_fim: datetime

DB_PATH = "lisboa_pedala.db"


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


@contextmanager
def transaction():
    """
    Context manager para transações atómicas.
    Fecho de viagem + emissão de fatura ocorrem aqui.
    Ver ARCHITECTURE.md secção 4, acoplamento temporal.
    """
    conn = get_connection()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()