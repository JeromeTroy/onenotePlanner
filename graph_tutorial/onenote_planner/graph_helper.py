from requests_oauthlib import OAuth2Session
import json
import io
import glob

from setup import PLANNER_NOTEBOOK_DISPLAYNAME, MONTHS, PAGES_PREFIX, TEMPLATES_PREFIX

graph_url = "https://graph.microsoft.com/v1.0"

def build_json(dict):
    dict_str = str(dict)
    dict_str = dict_str.replace("'", '"')

    dict_json = json.loads(dict_str)
    return dict_json

def collect_onenote_notebooks(token):

    graph_client = OAuth2Session(token=token)

    # send GET to /me/onenote/notebooks
    notebooks = graph_client.get('{0}/me/onenote/notebooks'.format(graph_url))

    #print(help(graph_client.get))
    return notebooks.json()

def collect_notebook_sections(token, notebook_id):
    graph_client = OAuth2Session(token=token)

    sections = graph_client.get('{0}/me/onenote/notebooks/{1}/sections'.format(graph_url, notebook_id))

    return sections.json()

def collect_notebook_pages(token, section_id):

    graph_client = OAuth2Session(token=token)

    pages = graph_client.get('{0}/me/onenote/sections/{1}/pages'.format(graph_url, section_id))

    return pages.json()

def get_page_content(token, page_id):

    graph_client = OAuth2Session(token=token)

    content = graph_client.get('{0}/me/onenote/pages/{1}/content'.format(graph_url, page_id))

    return content

def find_section_id(sections_json, section_name):
    section_id = None
    section_values = sections_json['value']

    for val in section_values:
        if val['displayName'] == section_name:
            section_id = val['id']
            break
    return section_id

def find_notebook_id(notebooks, name):

    notebook_id = None
    notebook_values = notebooks['value']
    for val in notebook_values:
        if val['displayName'] == name:
            notebook_id = val['id']

            break
    return notebook_id


def create_new_notebook(token):
    graph_client = OAuth2Session(token=token)

    notebook = {"displayName": "Test Planner"}

    notebook_json = build_json(notebook)
    output = graph_client.post('{0}/me/onenote/notebooks'.format(graph_url), json=notebook_json)

    return output

def create_new_notebook_section(token, notebook_id, section_name="Test Section"):

    graph_client = OAuth2Session(token=token)

    section = {"displayName": section_name}
    section_json = build_json(section)

    output = graph_client.post('{0}/me/onenote/notebooks/{1}/sections'.format(graph_url, notebook_id),
                json=section_json)


    return output

def create_new_page(token, section_id, fdict=None, headers=None):

    graph_client = OAuth2Session(token=token)

    # output = graph_client.post('{0}/me/onenote/sections/{1}/pages'.format(graph_url, section_id),
    #         files=fdict, headers={"Content-Type": "application/xhtml+xml",
    #                     "Content-Disposition": "form-data; name='Presentation'"})

    output = graph_client.post('{0}/me/onenote/sections/{1}/pages'.format(graph_url, section_id),
            files=fdict, headers=headers)
    return output

def find_month_files(month_number):

    printed_number = month_number + 1
    page_fname = PAGES_PREFIX + "months/month-{:02d}.html".format(printed_number)
    calendar_fname = PAGES_PREFIX + "months/tex/month-{:02d}.png".format(printed_number)
    budget_fname = TEMPLATES_PREFIX + "months/budget.png"

    return page_fname, calendar_fname, budget_fname

def post_month_page(token, section_id, page_fname, calendar_fname, budget_fname):

    files = {"Presentation": (None, open(page_fname, "rb"), "text/html"),
            "calendar": (None, open(calendar_fname, "rb"), "image/png"),
            "budget": (None, open(budget_fname, "rb"), "image/png")}

    output = create_new_page(token, section_id, fdict=files)

    return output

def post_week_page(token, section_id, week_fname, week_image):
    files = {"Presentation": (None, open(week_fname, "rb"), "text/html"),
            "week": (None, open(week_image, "rb"), "image/png")}

    output = create_new_page(token, section_id, fdict=files)

def find_week_files_for_month(month_number):
    printed_number = month_number + 1
    week_file_list = glob.glob(PAGES_PREFIX + "weeks/*date_{:02d}*".format(printed_number))
    return sorted(week_file_list)

def find_week_number_from_fname(week_filename):
    file_name_nodir = week_filename.split("/")[-1]
    week_no = file_name_nodir.split("_")[1]
    return week_no

def find_week_image_file(week_number):
    image_fname = PAGES_PREFIX + "weeks/tex/week-{0}.png".format(week_number)
    return image_fname

def find_day_files_for_week(week_number):
    day_files = glob.glob(PAGES_PREFIX + "days/week_{0}*".format(week_number))
    return sorted(day_files)

def post_day_page(token, section_id, day_fname):
    personal_file = TEMPLATES_PREFIX + "days/personal-day.png"
    work_file = TEMPLATES_PREFIX + "days/work-day.png"
    learn_file = TEMPLATES_PREFIX + "days/learn-day.png"

    files = {"Presentation": (None, open(day_fname, "rb"), "text/html"),
            "personal": (None, open(personal_file, "rb"), "image/png"),
            "work": (None, open(work_file, "rb"), "image/png"),
            "learn": (None, open(learn_file, "rb"), "image/png")}

    output = create_new_page(token, section_id, fdict=files)
    return output

def post_whole_week(token, section_id, week_number):
    day_files = find_day_files_for_week(week_number)
    outputs = []
    for day_fname in day_files:
        output = post_day_page(token, section_id, day_fname)
        outputs.append(output)

    return outputs

def post_all_month(token, notebook_id, month_number):

    month_name = MONTHS[month_number]

    sections = collect_notebook_sections(token, notebook_id)

    section_id = find_section_id(sections, month_name)

    if section_id is None:
        create_new_notebook_section(token, notebook_id, section_name=month_name)
        section_id = find_section_id(sections, month_name)

    all_outputs = []

    month_page, calendar_file, budget_file = find_month_files(month_number)

    month_output = post_month_page(token, section_id, month_page, calendar_file, budget_file)

    all_outputs.append(month_output)

    week_filelist = find_week_files_for_month(month_number)
    for k in range(len(week_filelist)):
        week_filename = week_filelist[k]
        week_number = find_week_number_from_fname(week_filename)
        week_image_fname = find_week_image_file(week_number)
        week_output = post_week_page(token, section_id, week_filename, week_image_fname)

        all_outputs.append(week_output)

        day_outputs = post_whole_week(token, section_id, week_number)

        all_outputs += day_outputs

    return all_outputs
