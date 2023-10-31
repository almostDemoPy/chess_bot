import asyncio
import discord
import os
import traceback
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
  command_prefix = "chess.",
  help_command = None,
  intents = intents,
  activity = discord.Activity(
    type = discord.ActivityType.playing,
    name = "Chess in Discord"
  )
)

async def load():
  for file in os.listdir('cogs'):
    if file.endswith(".py"):
      await bot.load_extension(
        f'cogs.{file[:-3]}'
      )

async def main():
  await load()
  await bot.start(
    os.getenv("token")
  )

try:
  asyncio.run(main())
except:
  traceback.print_exc()