
import datetime
import glob

# setup
week_template = "../images/templates/weeks/week.html"
week_location = "../images/pages/weeks/"
year = 2020

# weeks in the year
no_weeks = len(glob.glob(week_location + "/tex/*.png"))

print(no_weeks)
# format filename as week_00_date_01_01.html
fname_form = "week_%U_date_%m_%d.html"
day_form = "%b %d"

# initialize
first_day = datetime.date(year, 1, 1)

delta = datetime.timedelta(days=7)
day_delta = datetime.timedelta(days=1)

the_day = first_day
for j in range(int(first_day.strftime("%w"))):
        the_day -= day_delta

fin = open(week_template, "r")
lines = fin.readlines()

# iterate
for n in range(no_weeks):
    # determine day range for week
    start_day = the_day
    end_day = the_day + delta - day_delta

    # open appropriate file
    fname = week_location + start_day.strftime(fname_form)
    fout = open(fname, "w")
    
    title = start_day.strftime(day_form) + " - " + end_day.strftime(day_form)
    
    # write out to file
    for line in lines:
        if "__enter title__" in line:
            fout.write("\t\t\t")
            fout.write(title)
            fout.write("\n")
        else:
            fout.write(line)

    # close file
    fout.close()

    # increment day
    the_day += delta


