from curses.ascii import NUL
import os
import sys
from logging import getLogger
logger = getLogger(__name__)
logger.info('message')

import time



def get_users_list_1st(app):
    result = app.client.users_list(limit=300)
 
    return result
 
def get_users_list(app, cursor):
    try:
        result = app.client.users_list(limit=300, cursor=cursor)
    except:
        print("Error:(")
        time.sleep(3)
        result = app.client.users_list(limit=300, cursor=cursor)
 
    return result

def get_members(app):
    members = []

    first_call = True
    result     = True
    while True:
        if first_call:
            resources = get_users_list_1st(app)
            first_call = False
        else:
            resources = get_users_list(app, next_cursor)

        for member in resources['members']:
            members.append(member)

        if not resources['response_metadata']:
            break
        if not resources['response_metadata']['next_cursor']:
            break

        next_cursor = resources['response_metadata']['next_cursor']

    return members

def get_reacted_user_name(user, members):
    for member in members:
        if user != member["id"]:
            continue

        return member["real_name"]

def get_reacted_users_name(users, members):
    names = []

    for user in users:
        name = get_reacted_user_name(user, members)

        names.append(name)

    return names

def get_input_info(link):
    try:
        print("link",link)
        input_info = {}
        link_strs = link.split("/")
        print("link_strs", link_strs)
        timestamp = link_strs[5][1:11] + "." + link_strs[5][11:17]

        input_info = dict(channel = link_strs[4], timestamp = timestamp)
    except:
        raise ValueError('Invalid input')


    return input_info

def main(app, url):
    print("Exec: main(", url, ")")

    input_info = get_input_info(url)

    output_txt = ""

#    try:
    members = get_members(app)

    result = app.client.reactions_get(channel = input_info["channel"], full = True, timestamp = input_info["timestamp"])
    text = result["message"]["text"]
    
    print(text)

    reactions = result["message"]["reactions"]
    for reaction in reactions:
        output_txt += '----- :{}: {} -----\n'.format(reaction["name"], reaction["count"])
        print("----- ", reaction["name"], ": ", reaction["count"], " -----")

        users = reaction["users"]
        names = get_reacted_users_name(users, members)

        for name in names:
            output_txt += '{}\n'.format(name)
            print(name)

    result = app.client.chat_postMessage(
        channel = input_info["channel"],
        thread_ts = input_info["timestamp"],
        text = output_txt
        # You could also use a blocks[] array to send richer content
    )


#    except SlackApiError as e:
#        logger.error("Error creating conversation: {}".format(e))
#    except:
#        print("Error:(")

def call_main(args):
    if 2 > len(args):
        print('Arguments are too short')

        return

    main(args[1])


if __name__ == "__main__":
    call_main(sys.argv)