# Resumo Focus BCB

Pipeline que baixa o boletim **Focus** do Banco Central, extrai o texto do
PDF e, numa automação agendada, gera um **resumo executivo** que é enviado
por e-mail.

## Como funciona

- Os **scripts Python só baixam e extraem**: `baixar_focus.py` busca o PDF
  mais recente no site do BCB e `extrair_texto.py` converte esse PDF em texto.
- O **resumo é escrito por um agente** que lê o texto extraído. Nenhum script
  Python "resume" ou interpreta números — essa etapa é do agente, que se
  apoia diretamente no texto do boletim.
- Regra central: **nunca inventar número.** Toda mediana ou valor citado no
  resumo deve estar literalmente presente no texto extraído do PDF.

## Estrutura de pastas

```
resumo-focus2/
├── CLAUDE.md               briefing do projeto (para o agente)
├── README.md
├── demo.py                 roda o pipeline local: baixa + extrai
├── requirements.txt
├── pytest.ini
├── src/
│   ├── baixar_focus.py     baixa o PDF mais recente do Focus
│   └── extrair_texto.py    extrai o texto do PDF -> .txt
├── tests/
│   └── test_baixar_focus.py
├── data/                   PDFs e textos baixados (insumos)
├── output/focus/           resumos executivos em markdown (versionados)
└── .github/workflows/
    └── focus-download.yml  baixa e extrai toda segunda (agendado)
```

## Rodar localmente

```bash
python -m pip install -r requirements.txt
python demo.py            # baixa o Focus e extrai o texto
python demo.py --abrir    # idem, e abre o .txt no navegador
```

A saída fica em `data/focus_AAAA-MM-DD.pdf` e `data/focus_AAAA-MM-DD.txt`
(data da publicação do boletim).

## Rodar os testes

```bash
python -m pytest -m "not network"    # só testes offline (rápido)
python -m pytest -m network          # inclui o download real do BCB
python -m pytest                     # tudo
```

O marker `network` separa os testes que fazem chamada de rede; o
desenvolvimento normal usa `-m "not network"`.
