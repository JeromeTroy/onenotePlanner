# onenotePlanner
Automated building of Yearly Digital planner in OneNote

This app integrates with Microsoft Graph / Azure to build a digital planner
with various views for months, weeks, and individual days.  Planners can be
edited remotely to add pages and entire sections at a time.
It is based off a tutorial on Microsoft's site:
https://docs.microsoft.com/en-us/graph/tutorials/python.

My hope in this project is to provide a grounding point for others to build
projects using Microsoft Graph and Azure to do other interesting and neat
things with Microsoft's cloud services and office products.  I have no
affiliation with Microsoft other than having a Microsoft 365 account.

## Dependacies

- ImageMagick
- Latex
- Python & Django Framework
- Microsoft 365 Account
- A web browser

## Usage

Download the app, and find the graph_tutorial/oauth_settings_pub.yml file.
Copy this to graph_tutorial/oauth_settings.yml, and enter the
app ID and app secret generated from the third page of the Microsoft tutorial.

The server can be run using

$python manage.py runserver

And opening a webpage at the printed localhost from the command.

The variable PLANNER_NOTEBOOK_DISPLAYNAME in setup.py controls which
onenote notebook is the planner.  From there the buttons on the planner page allow you to find specific notebooks, add pages, sections, or
entire months at a time to your planner.

## Backend

The planner is comprised of onenote sections (one for each month) with
pages in each section for a month overview, a page for each week overview,
and a page for each specific day.  These are made by uploading a png image
as a background over which you can write, much like a traditional planner.
The png images are made using latex to build pdfs in an automated fashion
then imagemagick is used to convert the pdfs to pngs as Onenote cannot handle
pdf imports as an image to display.
The directory graph_tutorial/onenote_planner/utils contains python files
used for generating individual views and creating the corresponding html
files that onenote can import.
