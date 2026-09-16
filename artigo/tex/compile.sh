pdflatex main.tex

bibtex main

pdflatex main.tex

pdflatex main.tex

rm *.out *.aux *.bbl *.blg *.fdb_latexmk *.fls *.gz main.log

mv main.pdf blockchain.pdf