import discord
import os
import requests

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


def summarize(thread: list[str]) -> str:
    headers = {"Authorization": f'Bearer {os.environ["INFERENCE_API_KEY"]}'}
    # Implement Summarizing the thread
    API_URL = f"https://api-inference.huggingface.co/models/google/pegasus-xsum"
    response = requests.post(API_URL, headers=headers, json=str(thread))
    return response.json()


@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.type.name == "reply" and message.content.startswith("/summarize"):
        reply_thread = []
        m = message.reference.resolved
        while m is not None:
            reply_thread.append(f"{m.author}: {m.content}")
            if m.reference:
                m = await message.channel.fetch_message(m.reference.message_id)
            else:
                m = None
        await message.reply(summarize(list(reversed(reply_thread))))


client.run(os.environ["DISCORD_SECRET"])
