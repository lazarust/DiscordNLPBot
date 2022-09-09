import discord
import os
import requests
import json

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
headers = {"Authorization": f'Bearer {os.environ["INFERENCE_API_KEY"]}'}


def summarize(thread: list[str]) -> str:
    API_URL = (
        "https://api-inference.huggingface.co/models/lidiya/bart-large-xsum-samsum"
    )
    response = requests.post(
        API_URL,
        headers=headers,
        json={"inputs": str(thread), "options": {"wait_for_model": True}},
    )
    # Now to just get the text from the json response and clean out some random quotation marks
    summary_text = json.loads(response.content.decode("utf-8"))[0][
        "summary_text"
    ].replace('"', "")
    return summary_text


def sentiment(message: str) -> str:
    API_URL = "https://api-inference.huggingface.co/models/cardiffnlp/twitter-roberta-base-sentiment"
    response = requests.post(
        API_URL,
        headers=headers,
        json={"inputs": message, "options": {"wait_for_model": True}},
    )
    sentiment_dicts = {}
    for dict in json.loads(response.content.decode("utf-8"))[0]:
        if dict["label"] == "LABEL_0":
            sentiment_dicts["Negative"] = round(dict["score"] * 100, 2)
        elif dict["label"] == "LABEL_1":
            sentiment_dicts["Neutral"] = round(dict["score"] * 100, 2)
        elif dict["label"] == "LABEL_2":
            sentiment_dicts["Positive"] = round(dict["score"] * 100, 2)
    return str(sentiment_dicts)


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

    if message.type.name == "reply" and message.content.startswith("/sentiment"):
        m = message.reference.resolved
        await message.reply(sentiment(m.content))

    if message.content.startswith("/help"):
        if message.content.contains("sentiment"):
            await message.reply(
                "Using the command `/sentiment` will return a dictionary of scores for if the message is Negative, Neutral, or Positive. The model used can be found at: https://huggingface.co/cardiffnlp/twitter-roberta-base-sentiment"
            )
        elif message.content.contains("summarize"):
            await message.reply(
                "Using the command `/summarize` will return of a summary of all messages in a thread of replies. The model used can be found at https://huggingface.co/lidiya/bart-large-xsum-samsum"
            )


client.run(os.environ["DISCORD_SECRET"])
