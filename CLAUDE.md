# Focus BCB — Resumo Executivo

## Objetivo

Baixar o boletim Focus do Banco Central toda segunda-feira, extrair o texto
do PDF e preparar um resumo executivo a partir desse texto.

## Fonte

- Página oficial: https://www.bcb.gov.br/publicacoes/focus
- Padrão de URL do PDF: `https://www.bcb.gov.br/content/focus/focus/R{AAAAMMDD}.pdf`
  (onde `{AAAAMMDD}` é a data da publicação, ex.: `R20260608.pdf`)

## Estrutura de pastas

```
src/                 código-fonte (download, extração, resumo)
tests/               testes automatizados
data/                PDFs e textos baixados (insumos brutos)
output/focus/        resumos finais em markdown
.github/workflows/   automação (agendamento semanal)
```

## Convenções

- **Nomenclatura:** arquivos nomeados `focus_AAAA-MM-DD`, onde a data é a
  da publicação do boletim (não a data de execução).
  - PDF: `data/focus_AAAA-MM-DD.pdf`
  - Texto extraído: `data/focus_AAAA-MM-DD.txt`
  - Resumo: `output/focus/focus_AAAA-MM-DD.md`
- `data/` guarda os insumos baixados (PDFs e textos).
- `output/focus/` guarda os resumos executivos em markdown.

## Regras

- **Nunca inventar número.** Toda mediana (ou qualquer valor) citada no
  resumo deve estar literalmente presente no texto extraído do PDF. Se um
  número não está no texto, ele não entra no resumo.
- **Feriados:** quando a segunda-feira é feriado, o BCB publica o boletim na
  terça. O download deve retroceder dia a dia (segunda → domingo → sábado…
  ou avançar conforme o calendário real de publicação) até encontrar um PDF
  válido na URL. Na prática: testar a data esperada e, se a URL não
  retornar um PDF, retroceder um dia e tentar de novo até achar.
