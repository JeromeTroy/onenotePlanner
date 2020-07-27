
import datetime
import glob

# setup
month_template = "../images/templates/months/month.html"
latex_loc = "tex/"
month_location = "../images/pages/months/"
year = 2020

# months in the year
month_view_files = glob.glob(month_location + latex_loc + "*.pdf")
budget_view_file = "../images/templates/months/budget.pdf"
no_months = 12

# format filename as month_01.html
fname_form = "month-%m.html"
month_title_form = "%B"

# initialize

fin = open(month_template, "r")
lines = fin.readlines()

# iterate
for n in range(no_months):
    # open appropriate file
    start_day = datetime.date(year, n + 1, 1)
    fname = month_location + start_day.strftime(fname_form)
    fout = open(fname, "w")
    
    title = start_day.strftime(month_title_form)
    curr_month_pdf = latex_loc + "month-" + start_day.strftime("%m") + ".pdf"

    # write out to file
    for line in lines:
        if "__enter title__" in line:
            fout.write("\t\t\t")
            fout.write(title)
            fout.write("\n")
        elif 'src="month.pdf"' in line:
            fout.write("\t\t\tsrc='")
            fout.write(curr_month_pdf)
            fout.write("'\n")
        elif 'src="budget.pdf"' in line:
            fout.write("\t\t\tsrc='")
            fout.write("../../templates/months/budget.pdf")
            fout.write("'\n")
        else:
            fout.write(line)

    # close file
    fout.close() 
