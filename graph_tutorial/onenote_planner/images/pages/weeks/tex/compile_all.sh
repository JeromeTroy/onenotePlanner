#!/bin/bash

for n in $(seq 0 52)
do
	printf -v fno "%02d" $n 
	pdflatex week-$fno.tex
	echo "Converting to png..."
	magick -density 300 week-$fno.pdf -gravity north -extent 100x100% week-$fno.png

done


rm *.log
rm *.aux
rm *.pdf
