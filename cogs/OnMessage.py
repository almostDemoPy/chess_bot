import discord
import traceback
from discord.ext import commands

class OnMessage(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    print(
      "Loaded event : on_message"
    )

  @commands.Cog.listener()
  async def on_message(self, message):
    commandList = ["chess.end", "chess.resign"]
    if message.content.lower() in commandList:
      pass

async def setup(bot):
  await bot.add_cog(OnMessage(bot))