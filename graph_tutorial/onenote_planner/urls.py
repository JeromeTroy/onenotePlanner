from django.urls import path

from . import views

urlpatterns = [
        # /
        # TODO: implement onenote view
        path('open_planner', views.open_planner, name='open_planner'),
        path('post_notebook', views.post_notebook, name='post_notebook'),
        path('post_section', views.post_notebook_section, name='post_section'),
        path('post_sections', views.post_month_sections, name='post_sections'),
        path('get_planner', views.get_notebooks, name='get_planner'),
        path('get_sections', views.get_notebook_sections, name='get_sections'),
        path('get_pages', views.get_notebook_pages, name='get_pages'),
        #path('post_sample_page', views.post_a_sample_page, name='post_sample_page'),
        path('post_month_pages', views.post_month_views, name='post_month_pages'),
        path('post_week_pages', views.post_week_views, name='post_week_pages'),
        path('post_day_pages', views.post_day_views, name='post_day_pages'),
        path('post_january', views.post_january, name='post_january'),
        path('post_february', views.post_february, name='post_february'),
        path('post_march', views.post_march, name='post_march'),
        path('post_april', views.post_april, name='post_april'),
        path('post_may', views.post_may, name='post_may'),
        path('post_june', views.post_june, name='post_june'),
        path('post_july', views.post_july, name='post_july'),
        path('post_august', views.post_august, name='post_august'),
        path('post_september', views.post_september, name='post_september'),
        path('post_october', views.post_october, name='post_october'),
        path('post_november', views.post_november, name='post_november'),
        path('post_december', views.post_december, name='post_december'),
]
