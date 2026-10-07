from pypdf import PdfReader, PdfWriter
from datetime import date


def extrair_pagina(pdf_original):
    # Define o nome do arquivo como "GABRIEL BRUM - Aula {dia do mes} do {mes}"
    hoje = date.today()
    pdf_destino = f"aula_de_hoje.pdf"

    # Abre o arquivo PDF original
    leitor = PdfReader(pdf_original)

    # Cria um novo arquivo PDF na memória
    gravador = PdfWriter()

    # Pega a última página do PDF original)
    pagina = leitor.pages[len(leitor.pages) - 1]
    gravador.add_page(pagina)

    # Salva o novo arquivo com a página extraída
    with open(pdf_destino, "wb") as arquivo_saida:
        gravador.write(arquivo_saida)


# Exemplo de uso:
# Extrai a página 3 do arquivo "documento.pdf" e salva como "pagina_3.pdf"
# extrair_pagina("aulas.pdf")
extrair_pagina("aulas.pdf")
