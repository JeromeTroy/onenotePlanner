from django.shortcuts import render

from django.http import HttpResponse, HttpResponseRedirect

from django.urls import reverse

# TODO: import stuff from either graph helper or model
from tutorial.auth_helper import *
from tutorial.auth_helper import get_token
from tutorial.views import initialize_context
from onenote_planner.graph_helper import *

import glob

from setup import PLANNER_NOTEBOOK_DISPLAYNAME, MONTHS
# TODO: other utility imports


# Create your views here.


# TODO: implement view for onenote planner

def initialize_context(request):
    context = {}

    # check for session errors
    error = request.session.pop('flash_error', None)

    if error != None:
        context['errors'] = []
        context['errors'].append(error)

    # check for user in session
    context['user'] = request.session.get('user', {'is_authenticated': False})

    return context

def open_planner(request):

    context = initialize_context(request)

    token = get_token(request)

    return render(request, 'onenote_planner/makeplanner.html', context)

def get_notebooks(request):

    print("Requesting Notebooks...")

    context = initialize_context(request)

    token = get_token(request)

    notebooks = collect_onenote_notebooks(token)

    print(notebooks)

    return render(request, "onenote_planner/makeplanner.html", context)


def get_notebook_sections(request, name=PLANNER_NOTEBOOK_DISPLAYNAME):

    context = initialize_context(request)
    token = get_token(request)

    notebooks = collect_onenote_notebooks(token)
    notebook_id = find_notebook_id(notebooks, name)

    sections = collect_notebook_sections(token, notebook_id)

    print(sections)

    context['errors'] = sections
    return render(request, "onenote_planner/makeplanner.html", context)

def get_notebook_pages(request, name=PLANNER_NOTEBOOK_DISPLAYNAME):

    name = "Research Fracture"
    context = initialize_context(request)
    token = get_token(request)

    notebooks = collect_onenote_notebooks(token)
    notebook_id = find_notebook_id(notebooks, name)

    sections = collect_notebook_sections(token, notebook_id)['value']

    all_pages = []
    for section in sections:
        print(section)
        section_id = section['id']
        pages = collect_notebook_pages(token, section_id)
        all_pages.append(pages)

    print(all_pages)

    first_pages_set = all_pages[0]['value']
    first_page_id = first_pages_set[0]['id']
    content = get_page_content(token, first_page_id)

    context['errors'] = content

    print(str(content))
    return render(request, "tutorial/home.html", context)



def post_notebook(request):
    print("Posting Notebook...")

    context = initialize_context(request)
    token = get_token(request)

    output = create_new_notebook(token)

    return HttpResponse(output)

def post_notebook_section(request):

    print("Posting notebook section...")

    context = initialize_context(request)
    token = get_token(request)

    notebooks = collect_onenote_notebooks(token)

    notebook_id = find_notebook_id(notebooks, PLANNER_NOTEBOOK_DISPLAYNAME)

    output = create_new_notebook_section(token, notebook_id)

    print(output)
    context['errors'] = output

    #return render(request, "tutorial/home.html", context)
    return HttpResponse(output)

def post_month_sections(request):

    context = initialize_context(request)
    token = get_token(request)

    notebooks = collect_onenote_notebooks(token)

    notebook_id = find_notebook_id(notebooks, PLANNER_NOTEBOOK_DISPLAYNAME)

    output_lst = []
    for month in MONTHS:
        output_lst.append(create_new_notebook_section(token, notebook_id, section_name=month))

    context['errors'] = output_lst

    return HttpResponse(output_lst)

def post_month_views(request):

    context = initialize_context(request)
    token = get_token(request)

    notebooks = collect_onenote_notebooks(token)
    notebook_id = find_notebook_id(notebooks, PLANNER_NOTEBOOK_DISPLAYNAME)
    sections = collect_notebook_sections(token, notebook_id)
    for num in range(len(MONTHS)):
        month_name = MONTHS[num]
        section_id = find_section_id(sections, month_name)

        page_fname = "./onenote_planner/images/pages/months/month-{:02d}.html".format(num+1)
        calendar_image = "./onenote_planner/images/pages/months/tex/month-{:02d}.png".format(num+1)
        budget_image = "./onenote_planner/images/templates/months/budget.png"

        files = {"Presentation": (None, open(page_fname, "rb"), "text/html"),
                "calendar": (None, open(calendar_image, "rb"), "image/png"),
                "budget": (None, open(budget_image, "rb"), "image/png")}
        output = create_new_page(token, section_id, fdict=files)

    return HttpResponse(output)

def post_week_views(request):

    context = initialize_context(request)
    token = get_token(request)

    notebooks = collect_onenote_notebooks(token)
    notebook_id = find_notebook_id(notebooks, PLANNER_NOTEBOOK_DISPLAYNAME)
    sections = collect_notebook_sections(token, notebook_id)

    for num in range(len(MONTHS)):
        month_name = MONTHS[num]
        section_id = find_section_id(sections, month_name)
        file_list = glob.glob("./onenote_planner/images/pages/weeks/*date_{:02d}*".format(num+1))

        for file_name in file_list:
            week_filename = file_name.split("/")[-1]
            week_no = week_filename.split("_")[1]
            week_file_name = "./onenote_planner/images/pages/weeks/tex/week-{0}.png".format(week_no)
            files = {"Presentation": (None, open(file_name, "rb"), "text/html"),
            "week": (None, open(week_file_name, "rb"), "image/png")}

            output = create_new_page(token, section_id, fdict=files)

    return HttpResponse(output)

def post_day_views(request):

    context = initialize_context(request)
    token = get_token(request)

    notebooks = collect_onenote_notebooks(token)
    notebook_id = find_notebook_id(notebooks, PLANNER_NOTEBOOK_DISPLAYNAME)
    sections = collect_notebook_sections(token, notebook_id)

    personal_file = "./onenote_planner/images/templates/days/personal-day.png"
    work_file = "./onenote_planner/images/templates/days/work-day.png"
    learn_file = "./onenote_planner/images/templates/days/learn-day.png"

    for num in range(len(MONTHS)):
        month_name = MONTHS[num]
        section_id = find_section_id(sections, month_name)
        week_list = file_list = glob.glob("./onenote_planner/images/pages/weeks/*date_{:02d}*".format(num+1))

        for week_file_name in week_list:
            week_file_name_file = week_file_name.split("/")[-1]
            week_no = week_file_name_file.split("_")[1]

            day_files = glob.glob("./onenote_planner/images/pages/days/week_{0}*".format(week_no))

            for day_file_name in day_files:
                files = {"Presentation": (None, open(day_file_name, "rb"), "text/html"),
                "personal": (None, open(personal_file, "rb"), "image/png"),
                "work": (None, open(work_file, "rb"), "image/png"),
                "learn": (None, open(learn_file, "rb"), "image/png")}

                output = create_new_page(token, section_id, fdict=files)
    return HttpResponse(output)


def post_given_month_all_pages(request, month_number):

    context = initialize_context(request)
    token = get_token(request)

    notebooks = collect_onenote_notebooks(token)
    notebook_id = find_notebook_id(notebooks, PLANNER_NOTEBOOK_DISPLAYNAME)

    all_outputs = post_all_month(token, notebook_id, month_number)

    return render(request, "onenote_planner/makeplanner.html", context)

def post_january(request):
    return post_given_month_all_pages(request, 0)
def post_february(request):
    return post_given_month_all_pages(request, 1)
def post_march(request):
    return post_given_month_all_pages(request, 2)
def post_april(request):
    return post_given_month_all_pages(request, 3)
def post_may(request):
    return post_given_month_all_pages(request, 4)
def post_june(request):
    return post_given_month_all_pages(request, 5)
def post_july(request):
    return post_given_month_all_pages(request, 6)
def post_august(request):
    return post_given_month_all_pages(request, 7)
def post_september(request):
    return post_given_month_all_pages(request, 8)
def post_october(request):
    return post_given_month_all_pages(request, 9)
def post_november(request):
    return post_given_month_all_pages(request, 10)
def post_december(request):
    return post_given_month_all_pages(request, 11)
