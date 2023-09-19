import json
import subprocess
import sys

# Attempts to Install Requests if requirements.txt not properly executed
def install_and_import(package):
    import importlib
    try:
        importlib.import_module(package)
    except ImportError:
        import pip
        pip.main(['install', package])
    finally:
            globals()[package] = importlib.import_module(package)

install_and_import('requests')

import requests

# Define Function for Retrieving Messages from Discord
def retrieve_messages(channelid):
    headers = {
        'authorization': f'{authtoken}'
    }
    r = requests.get(f'https://discord.com/api/v9/channels/{channelid}/messages', headers=headers)
    jsonn = json.loads(r.text)
    for value in jsonn:
        print(value, '\n')
    f = open('output.json',"a+")
    f.write(r.text)
    f.close()

authtoken = input("Enter Authorization Token from your Discord Account:")
discordchannelid = input("Enter the Discord Channel ID:")

retrieve_messages(discordchannelid)