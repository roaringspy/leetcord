# Discord Bot Documentation

The Discord Bot is the "Notification Layer" of LeetCord. It's a standalone Python microservice responsible for posting real-time alerts about user submissions to a designated Discord channel.

## Architecture

The service is a hybrid application that runs two components concurrently using Python's `asyncio` library:
1.  **A `discord.py` Client**: Maintains a persistent WebSocket connection to Discord's servers to listen for commands (a future feature) and send messages.
2.  **A FastAPI Server**: Exposes a single, internal API endpoint (`/events/new-submission`) that listens for HTTP POST requests from the main backend API.

This design decouples the bot from the main application, improving scalability and resilience.

## Setup Guide

To run the bot, you must first create a Bot Application in the Discord Developer Portal.

1.  **Create an Application**: Go to the [Discord Developer Portal](https://discord.com/developers/applications) and click "New Application". Give it a name like "LeetCord Bot".
2.  **Create a Bot User**: Navigate to the "Bot" tab and click "Add Bot".
3.  **Get the Bot Token**: Under the bot's username, click "Reset Token" and copy the token. **Treat this like a password.**
4.  **Enable Privileged Intents**: On the "Bot" page, scroll down to "Privileged Gateway Intents" and enable both **SERVER MEMBERS INTENT** and **MESSAGE CONTENT INTENT**. Save changes. 
5.  **Generate an Invite Link**:
    - Go to "OAuth2" -> "URL Generator".
    - In "Scopes", check the box for `bot`.
    - In the "Bot Permissions" section that appears, check `Send Messages` and `Embed Links`.
    - Copy the generated URL at the bottom of the page.
6.  **Invite the Bot**: Paste the URL into your browser, select your Discord server from the dropdown, and click "Authorize".
7.  **Get the Channel ID**:
    - In your Discord client, go to User Settings > Advanced and enable **Developer Mode**.
    - Go to the text channel where you want notifications, right-click on its name, and select **"Copy Channel ID"**.

## Configuration

The bot is configured using the `backend/.env.discord` file.

-   **`DISCORD_BOT_TOKEN`**: The token you copied in Step 3.
-   **`NOTIFICATION_CHANNEL_ID`**: The channel ID you copied in Step 7.

## Event Handling

When the main backend API calls `POST /events/new-submission`, the bot's FastAPI server receives a JSON payload like this:
```json
{
  "username": "testuser",
  "problem_title": "Two Sum",
  "problem_difficulty": "Easy",
  "problem_url": "[https://leetcode.com/problems/two-sum/](https://leetcode.com/problems/two-sum/)",
  "score": 10
}
````

The bot then formats this data into a rich Discord embed message and sends it to the configured channel.
