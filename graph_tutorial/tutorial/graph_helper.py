from requests_oauthlib import OAuth2Session

graph_url = "https://graph.microsoft.com/v1.0"

def get_user(token):
    graph_client = OAuth2Session(token=token)

    # send GET to /me
    user = graph_client.get('{0}/me'.format(graph_url))

    return user.json()

def get_calendar_events(token):
    graph_client = OAuth2Session(token=token)

    # configure query parameters
    # modify results
    query_params = {
            '$select': 'subject,organizer,start,end',
            '$orderby': 'createdDateTime DESC'
            }

    # send GET to /me/events
    events = graph_client.get('{0}/me/events'.format(graph_url), 
            params=query_params)
    # return json result
    return events.json()
