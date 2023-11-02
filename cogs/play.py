import chess
import discord
import json
import os
import traceback
from discord import app_commands, ui
from discord.ext import commands
from PIL import Image
from textBoard import TextSelectSide

class Play(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    print(
      "Loaded command : /play member : discord.Member visual : str"
    )

  @app_commands.command(
    name = "play",
    description = "[ALPHA] Play a game of Chess !"
  )
  @app_commands.describe(
    member = "Select your opponent",
    # visual = "Select your method of board display and mechanics"
  )
  # @app_commands.choices(
  #   visual = [
  #     app_commands.Choice(
  #       name = "Image",
  #       value = "image"
  #     ),
  #     app_commands.Choice(
  #       name = "Text",
  #       value = "text"
  #     )
  #   ]
  # )
  async def play(self, interaction : discord.Interaction, member : discord.Member):
    with open('json/games.json', 'r') as f:
      games = json.load(f)
    user = interaction.user
    response = interaction.response
    visual = "text"
    if isinstance(interaction.channel, discord.Thread):
      err = discord.Embed(
        description = "You cannot create a game of Chess in a thread !",
        color = 0xff3131
      ).set_author(
        name = self.bot.user.display_name,
        icon_url = self.bot.user.display_avatar
      )
      await response.send_message(
        embed = err,
        ephemeral = True
      )
      return
    if member == user:
      err = discord.Embed(
        description = "You cannot play Chess all by yourself ! Invite someone in to join you",
        color = 0xff3131
      ).set_author(
        name = self.bot.user.display_name,
        icon_url = self.bot.user.display_avatar
      )
      await interaction.response.send_message(
        embed = err,
        ephemeral = True
      )
      return
    if member.bot:
      err = discord.Embed(
        description = "You cannot play Chess with a bot ! Invite a human in to join you",
        color = 0xff3131
      ).set_author(
        name = self.bot.user.display_name,
        icon_url = self.bot.user.display_avatar
      )
      await interaction.response.send_message(
        embed = err,
        ephemeral = True
      )
      return
    if str(user.id) in games:
      opponent = await self.bot.fetch_user(games[str(user.id)])
      err = discord.Embed(
        description = f"You are currently playing a game with {opponent.mention} ! You cannot create another game in the mean time",
        color = 0xff3131
      ).set_author(
        name = self.bot.user.display_name,
        icon_url = self.bot.user.display_avatar
      )
      await response.send_message(
        embed = err,
        ephemeral = True
      )
      return
    board = discord.File('img/board.png', filename = "board.png")
    embed = discord.Embed(
      description = f"Select a side :",
      color = 0x2b2d31
    )
    if visual == "image":
      embed.set_image(
        url = "attachment://board.png"
      )
      await interaction.response.send_message(
        embed = embed,
        view = SelectSide(user, member, visual),
        file = board
      )
    else:
      Board = chess.Board().empty()
      strBoard = ""
      for ind, numberIndicator in enumerate([":eight:", ":seven:", ":six:", ":five:", ":four:", ":three:", ":two:", ":one:"]):
        strBoard += numberIndicator
        if ind % 2 == 0:
          strBoard += ":white_large_square::green_square::white_large_square::green_square::white_large_square::green_square::white_large_square::green_square:"
        else:
          strBoard += ":green_square::white_large_square::green_square::white_large_square::green_square::white_large_square::green_square::white_large_square:"
        strBoard += "\n"
      strBoard += ":black_large_square::regional_indicator_a::regional_indicator_b::regional_indicator_c::regional_indicator_d::regional_indicator_e::regional_indicator_f::regional_indicator_g::regional_indicator_h:"
      embed.description += f"\n{strBoard}"
      await interaction.response.send_message(
        embed = embed,
        view = TextSelectSide(user, member, visual, self.bot)
      )
    newData = {
      str(user.id): member.id,
      str(member.id): user.id
    }
    games.update(newData)
    with open('json/games.json', 'w') as f:
      json.dump(games, f, indent = 2)

  @play.error
  async def error(self, interaction : discord.Interaction, error):
    traceback.print_exc()
    err = discord.Embed(
      description = f"{interaction.user.mention}, Something went wrong",
      color = 0xff3131
    ).set_author(
      name = self.bot.user.display_name,
      icon_url = self.bot.user.display_avatar
    )
    try:
        await interaction.response.send_message(
            embed = err,
            ephemeral = True
        )
    except:
        await interaction.channel.send(
            embed = err,
            delete_after = 10
        )

async def setup(bot):
  await bot.add_cog(Play(bot))