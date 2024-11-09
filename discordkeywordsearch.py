import requests
import pandas
import csv
import tkinter
from tkinter import simpledialog

# Replace this with your Discord user token
DISCORD_AUTH_TOKEN = simpledialog.askstring(title="Discord Authorization Token", prompt="Enter your Discord Authorization Token: ")

# Replace this with the channel ID of the Discord channel to scrape
CHANNEL_ID = simpledialog.askstring(title="Channel ID", prompt="Enter the Discord Channel ID that you would like to search: ")

# List of keywords to search for
KEYWORDS = ["keyword"]

# Discord API base URL
BASE_URL = "https://discord.com/api/v9"

# Name CSV File
csvname = simpledialog.askstring(title="CSV Name", prompt="If keywords are found, what filename do you want for your csv? (Format: filename.csv)")

def get_channel_messages(channel_id, auth_token, limit=50, before=None):
    """Fetches messages from a Discord channel."""
    headers = {
        "Authorization": auth_token,
        "User-Agent": "Mozilla/5.0",
    }

    params = {
        "limit": limit,  # Number of messages to fetch (max 100 per request)
    }
    if before:
        params["before"] = before  # Fetch messages before a specific message ID

    url = f"{BASE_URL}/channels/{channel_id}/messages"

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        messages = response.json()
        return messages
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return []

def filter_messages_by_keywords(messages, keywords):
    """Filters messages that contain any of the specified keywords."""
    filtered = []
    for msg in messages:
        content = msg.get('content', '').lower()
        if any(keyword.lower() in content for keyword in keywords):
            filtered.append(msg)
    return filtered

def main():
    fetched_messages = []
    last_message_id = None  # For pagination

    # Fetch messages in batches
    while True:
        messages = get_channel_messages(CHANNEL_ID, DISCORD_AUTH_TOKEN, before=last_message_id)
        if not messages:
            break

        # Add messages to the fetched list
        fetched_messages.extend(messages)

        # Get the ID of the last message to fetch the next batch
        last_message_id = messages[-1]['id']

        # Break if no more messages are available
        if len(messages) < 50:  # Adjust according to the batch size
            break

    print(f"Total messages fetched: {len(fetched_messages)}")

    # Filter messages by keywords
    filtered_messages = filter_messages_by_keywords(fetched_messages, KEYWORDS)
    keywordlst=[]
    if filtered_messages:
        print(f"Found {len(filtered_messages)} messages containing the keywords.")
        for msg in filtered_messages:
            author = msg['author']['username']
            content = msg['content']
            timestamp = msg['timestamp']
            # print(f"[{timestamp}] {author}: {content}")
            keywordlst.append(msg)
        df = pandas.DataFrame(keywordlst, columns=['timestamp', 'author', 'content'])
        df.to_csv(f"{csvname}", sep=',', index=False)
        print("CSV Export Complete!")
        
    else:
        print("No messages found containing the keywords.")

if __name__ == "__main__":
    main()
