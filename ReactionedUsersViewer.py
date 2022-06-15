from curses.ascii import NUL
import os
import sys

from slack_bolt import App
#from slack_bolt.adapter.socket_mode import SocketModeHandler

# Initializes your app with your bot token and socket mode handler
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))


def get_users_list_1st():
    result = app.client.users_list(limit=300)
 
    return result
 
def get_users_list(cursor):
    result = app.client.users_list(limit=300, cursor=cursor)
 
    return result

def get_members():
    members = []

    first_call = True
    result     = True
    while True:
        if first_call:
            resources = get_users_list_1st()
            first_call = False
        else:
            resources = get_users_list(next_cursor)

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
    input_info = {}
    link_strs = link.split("/")
    timestamp = link_strs[5][1:11] + "." + link_strs[5][11:17]

    input_info = dict(channel = link_strs[4], timestamp = timestamp)

    return input_info

def main(args):
    if 2 > len(args):
        print('Arguments are too short')

        return

    input_info = get_input_info(args[1])

    try:
        members = get_members()

        result = app.client.reactions_get(channel = input_info["channel"], full = True, timestamp = input_info["timestamp"])
        reactions = result["message"]["reactions"]
        for reaction in reactions:
            print("-----", reaction["name"], "-----")

            users = reaction["users"]
            names = get_reacted_users_name(users, members)

            for name in names:
                print(name)

#    except SlackApiError as e:
#        logger.error("Error creating conversation: {}".format(e))
    except:
        print("Error:(")


if __name__ == "__main__":
    main(sys.argv)