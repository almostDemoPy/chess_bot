import discord
import traceback
from discord.ext import commands

class Sync(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    print("Loaded command : chess.sync")

  @commands.command(
    name = "sync",
    description = "Sync all application commands"
  )
  @commands.is_owner()
  async def sync(self, ctx):
    await self.bot.tree.sync()
    embed = discord.Embed(
      description = "Successfully synced all application commands",
      color = 0x39ff14
    ).set_author(
      name = ctx.author.display_name,
      icon_url = ctx.author.display_avatar
    )
    await ctx.send(
      embed = embed,
      mention_author = False,
      delete_after = 10
    )

  @sync.error
  async def error(self, ctx, error):
    traceback.print_exc()
    err = discord.Embed(
      description = "Something went wrong while syncing application commands",
      color = 0xff3131
    ).set_author(
      name = ctx.author.display_name,
      icon_url = ctx.author.display_avatar
    )
    await ctx.send(
      embed = err,
      mention_author = False,
      delete_after = 10
    )

async def setup(bot):
  await bot.add_cog(Sync(bot))