#!/usr/bin/env python3
import logging
import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# When using Bolt, you can use either `app.client` or the `client` passed to listeners.
client = WebClient(token=os.environ.get("SLACK_BOT_TOKEN"))
# Channel ID can contain IM etc. See https://api.slack.com/methods/chat.postMessage#channels
# right click on channel, copy the link and extract the last part
# channel_id = "C020D8AMHFT"  # channel #exp-notifier
# chnan # channel_id = "C020D8AMHFT"
user_id = "D01NZQPN2RY"

logger = logging.getLogger(__name__)

try:
    # Call the chat.postMessage method using the WebClient
    result = client.conversations_open(users=[user_id])
    result['channel']['id']
    # result = client.chat_postMessage(
    #     # channel='#exp-notifier', 
    #     # channel='@Ondra',  # does not work
    #     channel=channel_id,
    #     text="Hello world from Bolt Slack simple wrapper - channel name"
    # )
    logger.info(result)

except SlackApiError as e:
    logger.error(f"Error posting message: {e}")
