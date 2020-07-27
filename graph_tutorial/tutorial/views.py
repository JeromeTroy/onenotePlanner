from django.shortcuts import render

from django.http import HttpResponse, HttpResponseRedirect

from django.urls import reverse
from tutorial.auth_helper import get_sign_in_url, get_token_from_code, store_token, store_user, remove_user_and_token, get_token
from tutorial.graph_helper import get_user, get_calendar_events

import dateutil.parser

# Create your views here.
def home(request):
    # Temporary
    # return HttpResponse("Welcome to the tutorial!")
    context = initialize_context(request)

    return render(request, 'tutorial/home.html', context)


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

def sign_in(request):
    # get sign in url
    sign_in_url, state = get_sign_in_url()

    # save expected state for later validation
    request.session['auth_state'] = state

    # redirect to Azure sign in page
    return HttpResponseRedirect(sign_in_url)


def callback(request):
    # get state saved in session
    expected_state = request.session.pop('auth_sate', '')

    # make token from request
    token = get_token_from_code(request.get_full_path(), expected_state)

    # get user profile
    user = get_user(token)

    # save token and user
    store_token(request, token)
    store_user(request, user)
    
    return HttpResponseRedirect(reverse('home'))

def sign_out(request):
    # clear user and token
    remove_user_and_token(request)

    return HttpResponseRedirect(reverse('home'))

def calendar(request):
    context = initialize_context(request)

    token = get_token(request)

    events = get_calendar_events(token)

    if events:
        # convert ISO 8601 date times to datetime object
        # allows Django template to format nicely
        for event in events['value']:
            event['start']['dateTime'] = dateutil.parser.parse(event['start']['dateTime'])
            event['end']['dateTime'] = dateutil.parser.parse(event['end']['dateTime'])

        context['events'] = events['value']
    return render(request, 'tutorial/calendar.html', context)
