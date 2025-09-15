# discord_bot.py
import discord
import asyncio
import uvicorn
import os
from fastapi import FastAPI, Body, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

# --- Load Environment Variables ---
load_dotenv(dotenv_path=".env.discord")
BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
CHANNEL_ID = int(os.getenv("NOTIFICATION_CHANNEL_ID"))

# --- Discord Bot Setup ---
intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)

# --- FastAPI Setup ---
app = FastAPI()

class SubmissionEvent(BaseModel):
    username: str
    problem_title: str
    problem_difficulty: str
    problem_url: str
    score: int

@app.post("/events/new-submission")
async def receive_submission_event(event: SubmissionEvent = Body(...)):
    try:
        channel = bot.get_channel(CHANNEL_ID)
        if not channel:
            print(f"Error: Channel with ID {CHANNEL_ID} not found.")
            return {"status": "error", "detail": "Channel not found"}

        # Create a rich embed message
        color = discord.Color.green()
        if event.problem_difficulty == "Medium":
            color = discord.Color.orange()
        elif event.problem_difficulty == "Hard":
            color = discord.Color.red()
        
        embed = discord.Embed(
            title=f"New Submission: {event.problem_title}",
            url=event.problem_url,
            color=color
        )
        embed.set_author(name=event.username)
        embed.add_field(name="Difficulty", value=event.problem_difficulty, inline=True)
        embed.add_field(name="Score Awarded", value=f"+{event.score} points", inline=True)
        embed.set_footer(text="Social LeetCode")

        # bot.send_message is deprecated, use channel.send
        await channel.send(embed=embed)
        return {"status": "success"}

    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal server error in bot")


# --- Combined Startup ---
async def run_bot():
    try:
        await bot.start(BOT_TOKEN)
    except Exception as e:
        print(f"Error starting bot: {e}")

async def run_api():
    config = uvicorn.Config(
        app,
        host="127.0.0.1",
        port=8001,
        log_level="info"
    )
    server = uvicorn.Server(config)
    await server.serve()

async def main():
    # Run both concurrently
    await asyncio.gather(
        run_bot(),
        run_api(),
    )

if __name__ == "__main__":
    if not BOT_TOKEN or not CHANNEL_ID:
        print("Error: DISCORD_BOT_TOKEN and NOTIFICATION_CHANNEL_ID must be set in .env.discord")
    else:
        try:
            asyncio.run(main())
        except KeyboardInterrupt:
            print("Shutting down.")