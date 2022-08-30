import discord
import os

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.type.name == "reply":
        reply_thread = [f"{message.author}: {message.content}"]
        m = message.reference.resolved
        while m is not None:
            reply_thread.append(f"{m.author}: {m.content}")
            if m.reference:
                m = await message.channel.fetch_message(m.reference.message_id)
            else:
                m = None
        await message.reply(list(reversed(reply_thread)))


client.run(os.environ["DISCORD_SECRET"])
