
import datetime

# setup
template_fname = "../images/templates/days/day.html"
day_location = "../images/pages/days/"
year = 2020

# days in the year
no_days = 365
if year % 4 == 0:
    no_days = 366

# format day as "Sunday, May 5, 2020"
# %A, %b %d, %Y
form = "%A, %b %d, %Y"
fname_form = "week_%U_day_%d.html"

# initialize
first_day = datetime.date(year, 1, 1)
the_day = None
delta = datetime.timedelta(days=1)

fin = open(template_fname, "r")
lines = fin.readlines()
fin.close()


# iterate
for n in range(no_days):
    if n == 0:
        the_day = first_day
    else:
        the_day += delta
    
    out_fname = day_location + the_day.strftime(fname_form)
    fout = open(out_fname, "w")
    for line in lines:
        if "__" in line:
            output_line = "\t\t\t" + the_day.strftime(form) + "\n"
        else:
            output_line = line
        fout.write(output_line)
    fout.close()


