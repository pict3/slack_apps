import functions_framework
import json

import os

import logging

logging.basicConfig(level=logging.DEBUG)

from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler
#from slack_bolt.adapter.google_cloud_functions import SlackRequestHandler
# Not Support
# https://github.com/slackapi/bolt-python/issues/46

from flask import Request



import ReactionedUsersViewer


# process_before_response must be True when running on FaaS
app = App(process_before_response = True,
          token = os.environ.get("SLACK_BOT_TOKEN"),
          signing_secret = os.environ['SLACK_SECRET'])

handler = SlackRequestHandler(app)


def respond_to_slack_within_3_seconds(body, ack):
    print("respond_to_slack_within_3_seconds: ", body)

    text = body.get("text")
    if text is None or len(text) == 0:
        ack(f":x: Usage: /start-process (description here)")
    else:
        ack(f"Accepted! (task: {body['text']})")

def run_long_process(respond, body):
    print("run_long_process: ", body)

    target_url = body['text']
    response = ReactionedUsersViewer.main(app, target_url)

    respond(f"Completed! (task: {body['text']})")


app.command("/reactioned_user_viewer")(
    # ack() is still called within 3 seconds
    ack=respond_to_slack_within_3_seconds,
    # Lazy function is responsible for processing the event
    lazy=[run_long_process]
)    

#---
# Not Support
# https://github.com/slackapi/bolt-python/issues/46
## Cloud Function
#def slack_reactioned_user_viewer(req: Request):
#    """HTTP Cloud Function.
#    Args:
#        req (flask.Request): The request object.
#        <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
#    Returns:
#        The response text, or any set of values that can be turned into a
#        Response object using `make_response`
#        <https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>.
#    """
#    return handler.handle(req)



@functions_framework.http
def slack_reactioned_user_viewer(request):
    return handler.handle(request)

