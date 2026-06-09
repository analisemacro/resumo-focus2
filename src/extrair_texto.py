"""Extrai o texto de um PDF do Focus e salva como .txt (UTF-8).

Uso típico:
    python src/extrair_texto.py                 # pega o PDF mais recente em data/
    python src/extrair_texto.py --pdf caminho.pdf
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pdfplumber

# Pasta data/ na raiz do projeto (um nível acima de src/).
DIR_DATA = Path(__file__).resolve().parent.parent / "data"


def extrair(pdf_path: str | Path) -> Path:
    """Extrai o texto de todas as páginas do PDF e salva como .txt.

    O .txt fica com o mesmo nome do PDF (só troca a extensão), em UTF-8.
    Retorna o caminho do arquivo de texto gerado.
    """
    pdf_path = Path(pdf_path)

    paginas: list[str] = []
    with pdfplumber.open(pdf_path) as pdf:
        for pagina in pdf.pages:
            # extract_text() pode devolver None em páginas sem texto.
            texto = pagina.extract_text() or ""
            paginas.append(texto)

    # Junta as páginas com quebra de linha entre elas.
    texto_completo = "\n".join(paginas)

    # Mesmo nome do PDF, trocando .pdf por .txt.
    txt_path = pdf_path.with_suffix(".txt")
    txt_path.write_text(texto_completo, encoding="utf-8")

    return txt_path


def _pdf_mais_recente() -> Path | None:
    """Retorna o focus_*.pdf mais recente em data/, ou None se não houver."""
    pdfs = sorted(DIR_DATA.glob("focus_*.pdf"))
    return pdfs[-1] if pdfs else None


def main() -> int:
    """CLI: extrai o texto do PDF indicado (ou do mais recente em data/)."""
    parser = argparse.ArgumentParser(
        description="Extrai o texto de um PDF do Focus e salva como .txt."
    )
    parser.add_argument(
        "--pdf",
        help="Caminho de um PDF específico. Se omitido, usa o mais recente em data/.",
    )
    args = parser.parse_args()

    # Escolhe o PDF: o informado em --pdf ou o mais recente da pasta data/.
    if args.pdf:
        pdf_path = Path(args.pdf)
    else:
        pdf_path = _pdf_mais_recente()
        if pdf_path is None:
            print(
                "Nenhum PDF encontrado em data/. "
                "Rode primeiro: python src/baixar_focus.py",
                file=sys.stderr,
            )
            return 1

    txt_path = extrair(pdf_path)
    print(f"Texto extraído: {txt_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
