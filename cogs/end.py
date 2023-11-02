import asyncio
import discord
import json
import traceback
from discord.ext import commands

class End(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    print(
      "Loaded command : chess.end"
    )

  @commands.command(
    name = "end",
    description = "End your current game of Chess"
  )
  async def end(self, ctx):
    with open('json/games.json', 'r') as f:
      games = json.load(f)
    user = ctx.author
    if str(user.id) not in games:
      err = discord.Embed(
        description = f"{user.mention}, You aren't playing a game of Chess with anyone !",
        color = 0xff3131
      ).set_author(
        name = self.bot.user.display_name,
        icon_url = self.bot.user.display_avatar
      )
      await ctx.send(
        embed = err,
        mention_author = False,
        delete_after = 10
      )
      return
    await asyncio.sleep(5)
    opponent = await self.bot.fetch_user(games[str(user.id)])
    boardMsg = None
    if isinstance(ctx.channel, discord.Thread):
      boardMsg = ctx.channel.starter_message
    else:
      async for message in ctx.channel.history(limit = None):
        if message.author == self.bot.user and len(message.embeds) != 0:
          if message.embeds[0].footer.text is not None and message.embeds[0].author.name is not None and message.embeds[0].title.endswith("turn !"):
            if (message.embeds[0].footer.text.startswith(user.display_name) and message.embeds[0].author.name.startswith(opponent.display_name)) or (message.embeds[0].footer.text.startswith(opponent.display_name) and message.embeds[0].author.name.startswith(user.display_name)):
              boardMsg = message
              break
    if boardMsg is None:
      err = discord.Embed(
        description = f"{user.mention}, You do not have an active game in this channel",
        color = 0xff3131
      ).set_author(
        name = self.bot.user.display_name,
        icon_url = self.bot.user.display_avatar
      )
      await ctx.send(
        embed = err,
        mention_author = False,
        delete_after = 10
      )
      return
    else:
      if boardMsg.embeds[0].title.endswith("ended the game"):
        return
      del games[str(user.id)]
      del games[str(opponent.id)]
      with open('json/games.json', 'w') as f:
        json.dump(games, f, indent = 2)
      embed = boardMsg.embeds[0].copy()
      embed.title = f"{user.display_name} ended the game"
      await boardMsg.edit(
        embed = embed
      )
      if isinstance(ctx.channel, discord.Thread):
        await ctx.channel.delete()
      else:
        try:
          boardThread = ctx.channel.get_thread(boardMsg.id)
          await boardThread.delete()
        except:
          pass
        await ctx.send(
          f"Ended **{user.display_name}** and **{opponent.display_name}**'s game",
          mention_author = False,
          delete_after = 10
        )

  @end.error
  async def error(self, ctx, error):
    traceback.print_exc()

async def setup(bot):
  await bot.add_cog(End(bot))