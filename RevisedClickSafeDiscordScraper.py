import requests
import pandas as pd  # Updated for enhanced CSV handling
import time  # Added for rate-limiting between API calls
import logging  # Added for logging errors and operations
import tkinter
from tkinter import simpledialog

# Set up logging for better error tracking and debugging
logging.basicConfig(filename='keyword_search.log', level=logging.INFO)

# Prompt for Discord Authorization Token (User Input via tkinter dialog)
DISCORD_AUTH_TOKEN = simpledialog.askstring(title="Discord Authorization Token", prompt="Enter your Discord Authorization Token: ")

# Prompt for the Discord Channel ID (User Input via tkinter dialog)
CHANNEL_ID = simpledialog.askstring(title="Channel ID", prompt="Enter the Discord Channel ID that you would like to search: ")

# Prompt for CSV file name to store results
csvname = simpledialog.askstring(title="CSV Name", prompt="If keywords are found, what filename do you want for your csv? (Format: filename.csv)")

# Define the list of keywords to search for
# NOTE: Supports multi-word phrases and case-insensitive search
KEYWORDS = ["loli","shota","child","young","teen","atf","all the fallen", "kid"]

# Updated API version for compatibility and performance
BASE_URL = "https://discord.com/api/v10"  # Changed from v9 to v10 for latest API support

def get_channel_messages(channel_id, auth_token, limit=50, before=None):
    """
    Fetches messages from a Discord channel.
    Handles pagination using the 'before' parameter for historical data collection.
    """
    headers = {
        "Authorization": auth_token,
        "User-Agent": "Mozilla/5.0",
    }

    params = {
        "limit": limit,  # Max number of messages to fetch in one API request
    }
    if before:
        params["before"] = before  # Fetch messages before a specific message ID

    url = f"{BASE_URL}/channels/{channel_id}/messages"

    try:
        # Make the API request
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching messages: {e}")  # Log error details
        print(f"Error: {e}")
        return []

def filter_messages_by_keywords(messages, keywords):
    """
    Filters messages to match any of the keywords provided.
    Uses case-insensitive search and supports multi-word phrases.
    """
    filtered = []
    for msg in messages:
        content = msg.get('content', '').lower()
        if any(keyword.lower() in content for keyword in keywords):  # Case-insensitive matching
            filtered.append(msg)
    return filtered

def main():
    fetched_messages = []  # List to store all fetched messages
    last_message_id = None  # Used for pagination (fetching older messages)

    # Fetch messages in batches
    while True:
        messages = get_channel_messages(CHANNEL_ID, DISCORD_AUTH_TOKEN, before=last_message_id)
        if not messages:  # Break loop if no more messages are returned
            break

        fetched_messages.extend(messages)  # Append fetched messages to the list
        last_message_id = messages[-1]['id']  # Update to the last message ID for pagination

        # Break if fewer than the batch limit (no more data to fetch)
        if len(messages) < 50:
            break
        
        time.sleep(1)  # Added delay to avoid hitting API rate limits

    logging.info(f"Total messages fetched: {len(fetched_messages)}")

    # Filter messages by the keywords provided
    filtered_messages = filter_messages_by_keywords(fetched_messages, KEYWORDS)

    # Prepare for CSV export if messages match the keywords
    if filtered_messages:
        logging.info(f"Found {len(filtered_messages)} messages containing the keywords.")
        
        # Create a DataFrame with structured data
        # Includes additional metadata for better traceability
        df = pd.DataFrame(
            [{'timestamp': msg['timestamp'], 
              'author': msg['author']['username'], 
              'author_id': msg['author']['id'], 
              'message_id': msg['id'], 
              'content': msg['content']} 
             for msg in filtered_messages]
        )
        
        # Export DataFrame to a CSV file
        df.to_csv(f"{csvname}", sep=',', index=False)
        print("CSV Export Complete!")
    else:
        print("No messages found containing the keywords.")
        logging.info("No messages found containing the keywords.")

if __name__ == "__main__":
    main()

