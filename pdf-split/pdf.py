from pypdf import PdfReader, PdfWriter


def extrair_pagina(pdf_original, pdf_destino, numero_da_pagina):
    # Abre o arquivo PDF original
    leitor = PdfReader(pdf_original)

    # Cria um novo arquivo PDF na memória
    gravador = PdfWriter()

    # Adiciona a página escolhida (ajusta para contagem começando em 0)
    pagina = leitor.pages[numero_da_pagina - 1]
    gravador.add_page(pagina)

    # Salva o novo arquivo com a página extraída
    with open(pdf_destino, "wb") as arquivo_saida:
        gravador.write(arquivo_saida)


# Exemplo de uso:
# Extrai a página 3 do arquivo "documento.pdf" e salva como "pagina_3.pdf"
extrair_pagina("aula_26_08.pdf", "GABRIEL BRUM - aula_26_08.pdf", 3)
