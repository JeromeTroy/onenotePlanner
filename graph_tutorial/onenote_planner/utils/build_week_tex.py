import datetime

year = 2020
latex_location = "../images/templates/weeks/week/week.tex"
output_location = "../images/pages/weeks/tex/"

fin = open(latex_location, "r")
lines = fin.readlines()


delta = datetime.timedelta(days=1)
week_delta = datetime.timedelta(days=7)

first_day = datetime.date(year, 1, 1)
the_day = first_day


def build_week_str(curr_day):
    first_half_day_numbers = []
    
    second_half_day_numbers = []

    no_prev_days = int(curr_day.strftime("%w"))
    for n in range(no_prev_days):
        curr_day -= delta
    
    start_day = curr_day.strftime("%b %d")
    
    for n in range(6):
        curr_day += delta
    
    end_day = curr_day.strftime("%b %d")

    week_str = start_day + " - " + end_day
    
    return week_str

def build_week_tex(curr_day):
    week_str = build_week_str(curr_day)

    week_no = curr_day.strftime("%U")

    out_fname = output_location + "week-" + week_no + ".tex"
    fout = open(out_fname, "w")

    for line in lines:
        if "<< date range >>" in line:
            fout.write("\t\t\t")
            fout.write(week_str)
            fout.write("\n")

        elif "<< the year >>" in line:
            fout.write("\t\t\t")
            fout.write(str(year))
            fout.write("\n")
 
        else:
            fout.write(line)
    
    fout.close()
    return the_day

num_weeks = 53
for n in range(num_weeks):
    build_week_tex(the_day)
    the_day += week_delta



