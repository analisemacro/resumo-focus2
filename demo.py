"""Roda o pipeline do Focus localmente: baixa o PDF e extrai o texto.

Uso:
    python demo.py            # baixa e extrai
    python demo.py --abrir    # baixa, extrai e abre o .txt no navegador
"""

from __future__ import annotations

import argparse
import sys
import webbrowser
from pathlib import Path

# Coloca src/ no path de import para acessar os módulos do projeto.
RAIZ = Path(__file__).resolve().parent
sys.path.insert(0, str(RAIZ / "src"))

from baixar_focus import baixar  # noqa: E402
from extrair_texto import extrair  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Baixa o Focus e extrai o texto, em sequência."
    )
    parser.add_argument(
        "--abrir",
        action="store_true",
        help="Abre o .txt gerado no navegador padrão ao final.",
    )
    args = parser.parse_args()

    dir_data = RAIZ / "data"

    # Passo 1: baixa o PDF mais recente para data/.
    _data_pub, pdf_path = baixar(dir_data)
    tamanho_kb = pdf_path.stat().st_size / 1024
    print(f"[1/2] PDF baixado: {pdf_path.name} ({tamanho_kb:.1f} KB)")

    # Passo 2: extrai o texto do PDF baixado.
    txt_path = extrair(pdf_path)
    print(f"[2/2] Texto extraído: {txt_path}")

    # Opcional: abre o texto no navegador padrão.
    if args.abrir:
        webbrowser.open(txt_path.as_uri())


if __name__ == "__main__":
    main()
