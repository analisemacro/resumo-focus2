"""Baixa o PDF mais recente do boletim Focus do Banco Central.

Estratégia: parte da última segunda-feira (data esperada de publicação) e,
caso o PDF não exista (feriado, atraso), recua dia a dia até encontrar um
arquivo válido na URL do BCB.
"""

from __future__ import annotations

from datetime import date, timedelta
from pathlib import Path

import requests

# URL do PDF: a data vai sem hífens, no formato AAAAMMDD.
URL_BASE = "https://www.bcb.gov.br/content/focus/focus/R{aaaammdd}.pdf"

# User-Agent de navegador: o site do BCB costuma recusar clientes "robô".
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )
}

# Número máximo de dias para recuar (cobre feriados prolongados).
MAX_TENTATIVAS = 7


def ultima_segunda(hoje: date) -> date:
    """Retorna a segunda-feira mais recente ESTRITAMENTE anterior a `hoje`.

    Se `hoje` já é segunda-feira, retrocede para a segunda da semana passada.
    """
    # weekday(): segunda=0, ..., domingo=6.
    # Quantos dias recuar para chegar na segunda anterior:
    #   - se hoje é segunda (0), recua 7 (segunda passada);
    #   - caso contrário, recua o próprio weekday() (volta à segunda da semana).
    dias_atras = hoje.weekday() or 7
    return hoje - timedelta(days=dias_atras)


def baixar(dest: str | Path) -> tuple[date, Path]:
    """Baixa o PDF do Focus mais recente para a pasta `dest`.

    Parte da última segunda-feira e recua um dia por tentativa (até
    MAX_TENTATIVAS) para cobrir feriados. Valida que o conteúdo começa com
    os bytes `%PDF` antes de aceitar.

    Retorna (data_da_publicacao, caminho_do_arquivo).
    Levanta RuntimeError se nenhuma tentativa funcionar.
    """
    dest = Path(dest)
    dest.mkdir(parents=True, exist_ok=True)

    # Começa na última segunda e vai recuando dia a dia.
    data = ultima_segunda(date.today())

    for _ in range(MAX_TENTATIVAS):
        url = URL_BASE.format(aaaammdd=data.strftime("%Y%m%d"))
        try:
            resp = requests.get(url, headers=HEADERS, timeout=30)
        except requests.RequestException:
            # Falha de rede nesta data: tenta a anterior.
            data -= timedelta(days=1)
            continue

        # Aceita só se a resposta veio OK e o conteúdo é mesmo um PDF.
        if resp.status_code == 200 and resp.content[:4] == b"%PDF":
            caminho = dest / f"focus_{data.isoformat()}.pdf"
            caminho.write_bytes(resp.content)
            return data, caminho

        # Não era um PDF válido: recua um dia.
        data -= timedelta(days=1)

    raise RuntimeError(
        f"Nenhum PDF do Focus encontrado em {MAX_TENTATIVAS} tentativas "
        f"a partir de {ultima_segunda(date.today()).isoformat()}."
    )


def main() -> None:
    """Baixa o Focus para a pasta data/ e imprime caminho e tamanho."""
    # Pasta data/ na raiz do projeto (um nível acima de src/).
    dest = Path(__file__).resolve().parent.parent / "data"

    data_pub, caminho = baixar(dest)
    tamanho_kb = caminho.stat().st_size / 1024
    print(f"Publicação: {data_pub.isoformat()}")
    print(f"Arquivo:    {caminho}")
    print(f"Tamanho:    {tamanho_kb:.1f} KB")


if __name__ == "__main__":
    main()
