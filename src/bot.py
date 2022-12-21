# bot.py
import os

import discord
from discord.ext.commands import Bot
from dotenv import load_dotenv


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = Bot("/", intents=intents)


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

    await bot.load_extension("cogs.generate")
    await bot.load_extension("cogs.regenerate")


bot.run(TOKEN)
