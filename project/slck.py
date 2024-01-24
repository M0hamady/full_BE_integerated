import requests


def create_channel_and_get_invite_link(channel_name):
    slack_token = "xoxb-6324626309540-6426918789462-FWfhhaWhS9FTOuwQZNc9Pvdx"  # Replace with your Slack API token
    url = "https://slack.com/api/conversations.create"
    headers = {
        "Authorization": f"Bearer {slack_token}",
        "Content-Type": "application/json; charset=utf-8"
    }
    payload = {
        "name": channel_name
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error: {e}")
    except requests.exceptions.ConnectionError as e:
        print(f"Connection error: {e}")

    channel_id = response.json()["channel"]["id"]

    invite_link_url = "https://slack.com/api/conversations.getInviteLink"
    payload = {
        "channel": channel_id
    }

    try:
        response = requests.post(invite_link_url, headers=headers, json=payload)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error: {e}")
    except requests.exceptions.ConnectionError as e:
        print(f"Connection error: {e}")

    invite_link = response.json()["invite_link"]

    return invite_link

def send_slack_notification(channel, message, is_update=False):
    slack_token = ""  # Replace with your Slack API token
    url = "https://slack.com/api/chat.postMessage"
    headers = {
        "Authorization": f"Bearer {slack_token}",
        "Content-Type": "application/json; charset=utf-8"
    }
    payload = {
        "channel": channel,
        "text": message
    }
    if is_update:
        payload["text"] = f"[Update] {message}"

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()