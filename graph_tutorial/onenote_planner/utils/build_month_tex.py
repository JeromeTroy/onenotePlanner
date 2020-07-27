import datetime

year = 2020
latex_location = "../images/templates/months/month/month.tex"
output_location = "../images/pages/months/tex/"

fin = open(latex_location, "r")
lines = fin.readlines()


delta = datetime.timedelta(days=1)
week_delta = datetime.timedelta(days=7)

first_day = datetime.date(year, 1, 1)
the_day = first_day

week_template = """\\hline 
\\cellcolor{{weekendcolor}}\\mkday{{
    {0}
}} & 
\\mkday{{
    {1}
}} &
\\mkday{{
    {2}
}} &
\\mkday{{
    {3}
}} &
\\mkday{{
    {4}
}} &
\\mkday{{
    {5}
}} &
\\cellcolor{{weekendcolor}}\\mkday{{
    {6}
}} 
\\\\
"""


def build_week_str(curr_day):
    day_numbers = []

    for n in range(7):
        day_numbers.append(curr_day.strftime("%d"))
        curr_day += delta

    week_str = week_template.format(*day_numbers)
    return week_str

def build_month_str(curr_day):
    the_month = curr_day.strftime("%m")
    curr_month = the_month
    
    month_str = ""
 
    starting_day = int(curr_day.strftime("%w"))

    for j in range(starting_day):
        curr_day -= delta
    
    if int(the_month) > 1 and int(curr_day.strftime("%d")) > 1:
        curr_day -= week_delta

    while curr_month == the_month:
        temp_day = curr_day
        
        month_str += build_week_str(temp_day)
        
        curr_day += week_delta
        curr_month = curr_day.strftime("%m")
        no_blank_days = None

    return month_str, curr_day

def build_month_tex(curr_day):
    month_str, the_day = build_month_str(curr_day)

    month_no = curr_day.strftime("%m")
    month_name = curr_day.strftime("%B")

    out_fname = output_location + "month-" + month_no + ".tex"
    fout = open(out_fname, "w")

    for line in lines:
        if "<< the month >>" in line:
            fout.write("\t\t\t")
            fout.write(month_name)
            fout.write("\n")

        elif "<< the year >>" in line:
            fout.write("\t\t\t")
            fout.write(str(year))
            fout.write("\n")

        elif "<< table >>" in line:
            fout.write(month_str)
            
        else:
            fout.write(line)
    fout.close()
    return the_day


for n in range(12):
    the_day = build_month_tex(the_day) 



