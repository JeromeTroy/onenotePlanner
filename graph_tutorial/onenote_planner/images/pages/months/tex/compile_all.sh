#!/bin/bash

for n in $(seq 1 12)
do
	printf -v fno "%02d" $n 
	pdflatex month-$fno.tex
	echo "Converting to png..."
	magick -density 600 month-$fno.pdf -gravity north -extent 100x100% month-$fno.png
done

rm *.log
rm *.aux
rm *.pdf

