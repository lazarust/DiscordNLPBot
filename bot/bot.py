import discord
import os
import requests
import json

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


def summarize(thread: list[str]) -> str:
    headers = {"Authorization": f'Bearer {os.environ["INFERENCE_API_KEY"]}'}
    API_URL = (
        f"https://api-inference.huggingface.co/models/philschmid/bart-large-cnn-samsum"
    )
    response = requests.post(
        API_URL,
        headers=headers,
        json={"inputs": str(thread), "options": {"wait_for_model": True}},
    )
    summary_text = json.loads(response.content.decode("utf-8"))[0]["summary_text"]
    return summary_text[: summary_text.find("    .")]


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
            reply_thread.append(f"{m.author.display_name}: {m.content}")
            if m.reference:
                m = await message.channel.fetch_message(m.reference.message_id)
            else:
                m = None
        await message.reply(summarize(list(reversed(reply_thread))))


client.run(os.environ["DISCORD_SECRET"])
