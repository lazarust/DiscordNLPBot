<h1 align="center">Discord Summarization Bot</h1>

<p align="center">
    <a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
</p>

## Setup
Currently, the discord bot is not "live" anywhere so to use it you'll have to run it locally, but since this uses Docker running the bot for your own server can be done in just a couple steps.
1. Go to the [Discord Developer](https://discord.com/developers/) site and create a new application and get the API token (under the Bot tab).
2. Go to the [HuggingFace Token](https://huggingface.co/settings/tokens) site and create a HuggingFace Interface API token.
3. Add the two tokens to your `.envrc`.
```
export DISCORD_SECRET=<SET EQUAL TO DISCORD API TOKEN>
export INFERENCE_API_KEY=<SET EQUAL TO HUGGINGFACE API TOKEN>
 ```
4. Finally, starting up the bot is as simple as running `docker-compose up bot`.

## Future Plans
There are some upgrades I want to do to this bot including, creating a Slack version, and creating a Twitter version. If there are any other things
that you'd want to see added please create an issue! 
