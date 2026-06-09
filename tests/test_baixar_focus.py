"""Testes para src/baixar_focus.py.

Os testes de ultima_segunda são puros (sem rede). O teste de download real
está marcado com @pytest.mark.network e pode ser pulado com -m "not network".
"""

from __future__ import annotations

import sys
from datetime import date, timedelta
from pathlib import Path

import pytest

# Insere src/ no path de import, como no demo.py.
RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "src"))

from baixar_focus import baixar, ultima_segunda  # noqa: E402


# --- Testes puros de ultima_segunda (sem rede) -----------------------------


def test_quinta():
    # Quinta 2026-06-04 -> segunda da mesma semana: 2026-06-01.
    assert ultima_segunda(date(2026, 6, 4)) == date(2026, 6, 1)


def test_terca():
    # Terça 2026-06-09 -> segunda da mesma semana: 2026-06-08.
    assert ultima_segunda(date(2026, 6, 9)) == date(2026, 6, 8)


def test_segunda_recua_uma_semana():
    # Segunda 2026-06-08 -> deve recuar para a segunda anterior: 2026-06-01.
    assert ultima_segunda(date(2026, 6, 8)) == date(2026, 6, 1)


def test_domingo():
    # Domingo 2026-06-07 -> segunda da mesma semana: 2026-06-01.
    assert ultima_segunda(date(2026, 6, 7)) == date(2026, 6, 1)


def test_varredura_60_dias():
    # Para 60 dias consecutivos, o retorno deve ser sempre uma segunda
    # (weekday 0) e estritamente anterior à data dada.
    base = date(2026, 1, 1)
    for i in range(60):
        hoje = base + timedelta(days=i)
        resultado = ultima_segunda(hoje)
        assert resultado.weekday() == 0, f"{resultado} não é segunda"
        assert resultado < hoje, f"{resultado} não é anterior a {hoje}"


# --- Teste de download real (rede) -----------------------------------------


@pytest.mark.network
def test_baixar_download_real(tmp_path):
    data_pub, caminho = baixar(tmp_path)

    # Arquivo criado de fato.
    assert caminho.exists()

    conteudo = caminho.read_bytes()
    # Começa com a assinatura de PDF.
    assert conteudo[:4] == b"%PDF"
    # PDF do Focus tem dezenas de páginas; > 50 KB é piso seguro.
    assert len(conteudo) > 50 * 1024

    # Nome do arquivo bate com a data de publicação retornada.
    assert caminho.name == f"focus_{data_pub.isoformat()}.pdf"

    # Janela esperada: não no futuro e dentro dos últimos ~14 dias
    # (cobre uma semana normal mais folga para feriados).
    hoje = date.today()
    assert data_pub <= hoje, "data de publicação no futuro"
    assert hoje - data_pub <= timedelta(days=14), "data de publicação muito antiga"
