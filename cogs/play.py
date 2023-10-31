import discord
import json
import os
import traceback
from discord import app_commands, ui
from discord.ext import commands
from PIL import Image

class SelectSide(ui.View):
  def __init__(self, user, member):
    super().__init__(
      timeout = None
    )
    self.user = user
    self.member = member

  @ui.button(
    label = "White",
    custom_id = "selectWhiteSide",
    style = discord.ButtonStyle.primary
  )
  async def selectWhiteSide(self, interaction : discord.Interaction, button : ui.Button):
    response = interaction.response
    user = interaction.user
    if interaction.user not in [self.user, self.member]:
      err = discord.Embed(
        description = "You do not own this menu !",
        color = 0xff3131
      ).set_author(
        name = user.display_name,
        icon_url = user.display_avatar
      )
      await interaction.response.send_message(
        embed = err,
        ephemeral = True
      )
      return
    with Image.open('img/board.png').convert("RGBA") as board:
      with Image.open('img/pawn.png').resize(((board.width // 8) - 5, (board.height // 8) - 5)).convert("RGBA") as pawn:
        board.paste(pawn, (3, 3), mask = pawn)
        board.save(f"boards/{interaction.message.id}.png")
    Board = discord.File(f"boards/{interaction.message.id}.png", filename = "newBoard.png")
    embed = discord.Embed(
      color = 0x2b2d31
    ).set_image(
      url = "attachment://newBoard.png"
    ).set_author(
      name = self.member.display_name,
      icon_url = self.member.display_avatar
    ).set_footer(
      text = self.user.display_name,
      icon_url = self.user.display_avatar
    )
    await response.edit_message(
      embed = embed,
      view = None
    )

  @ui.button(
    label = "Black",
    custom_id = "selectBlackSide",
    style = discord.ButtonStyle.primary
  )
  async def selectBlackSide(self, interaction : discord.Interaction, button : ui.Button):
    response = interaction.response
    user = interaction.user
    if interaction.user not in [self.user, self.member]:
      err = discord.Embed(
        description = "You do not own this menu !",
        color = 0xff3131
      ).set_author(
        name = user.display_name,
        icon_url = user.display_avatar
      )
      await interaction.response.send_message(
        embed = err,
        ephemeral = True
      )
      return
    board = discord.File('img/board.png', filename = "board.png")
    embed = discord.Embed(
      color = 0x2b2d31
    ).set_image(
      url = "attachment://board.png"
    ).set_author(
      name = self.user.display_name,
      icon_url = self.user.display_avatar
    ).set_footer(
      text = self.member.display_name,
      icon_url = self.member.display_avatar
    )
    await response.edit_message(
      embed = embed,
      view = None
    )

  async def on_error(self, interaction : discord.Interaction, error):
    traceback.print_exc()

class Play(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    print(
      "Loaded command : /play member : discord.Member"
    )

  @app_commands.command(
    name = "play",
    description = "[ALPHA] Play a game of Chess !"
  )
  @app_commands.describe(
    member = "Select your opponent"
  )
  async def play(self, interaction : discord.Interaction, member : discord.Member):
    user = interaction.user
    response = interaction.response
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
    board = discord.File('img/board.png', filename = "board.png")
    embed = discord.Embed(
      description = f"Select a side :",
      color = 0x2b2d31
    ).set_image(
      url = "attachment://board.png"
    )
    await interaction.response.send_message(
      embed = embed,
      view = SelectSide(user, member),
      file = board
    )

  @play.error
  async def error(self, interaction : discord.Interaction, error):
    traceback.print_exc()
    err = discord.Embed(
      description = "Something went wrong",
      color = 0xff3131
    ).set_author(
      name = self.bot.user.display_name,
      icon_url = self.bot.user.display_avatar
    )
    await interaction.response.send_message(
      embed = err,
      ephemeral = True
    )

async def setup(bot):
  await bot.add_cog(Play(bot))