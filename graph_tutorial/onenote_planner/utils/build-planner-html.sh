#!/bin/bash

planner_dir="../planner/"
pages_dir="../images/pages"

months=("January" 
	"February"
	"March"
	"April"
	"May"
	"June"
	"July"
	"August"
	"September"
	"October"
	"November"
	"December"
)

for month_no in $(seq 1 12)
do
	mkdir $planner_dir$months[$month_no-1]

	printf -v month_no_pad "%02d" month_no
	cp $pages_dir/$months[$month_no-1]/month-$month_no_pad.html $planner_dir

	printf -v week_vals date_$month_no_pad
	for fname in $(find $pages_dir/weeks/ -type f -iname "*$week_vals*"
	do
		short_fname=$($fname | sed 's:.*/::')
		cp fname $pages_dir/$months[$month_no-1]/$short_fname
	done


done
