import discord
import traceback
from discord.ext import commands

class OnReady(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    print("Loaded event : on_ready")

  @commands.Cog.listener()
  async def on_ready(self):
    print(
      "Chess Bot is online"
    )

async def setup(bot):
  await bot.add_cog(OnReady(bot))