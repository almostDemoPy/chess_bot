import discord
import traceback
from discord import app_commands, ui
from discord.ext import commands

class HowToPlaySelect(ui.Select):
  def __init__(self, bot):
    super().__init__(
      min_values = 1,
      max_values = 1,
      placeholder = "Select an option...",
      options = [
        discord.SelectOption(
          label = "How to play Chess ?",
          value = "chess-tutorial"
        ),
        discord.SelectOption(
          label = "How to move my pieces ?",
          value = "move-tutorial"
        ),
        discord.SelectOption(
          label = "How do I end the game or resign ?",
          value = "end-resign"
        )
      ]
    )
    self.bot = bot

  async def callback(self, interaction : discord.Interaction):
    user = interaction.user
    response = interaction.response
    value = self.values[0]
    if value == "chess-tutorial":
      embed = discord.Embed(
        title = "How to play Chess ?",
        description = """
Still new to Chess and wanting to learn how to play it ? You can refer to [this resource](<https://www.chess.com/learn-how-to-play-chess>) offered by chess.com !

` 1 ` Execute </play:1168521804546060309> and specify ` member ` as to who you opponent will be.
` --- ` You cannot create another if you have an existing / ongoing game

` 2 ` Upon executing, the bot will prompt buttons for one of the players ( you or the selected ` member ` ) to choose their preferred side to play.

` 3 ` Once one of the players have selected a side, the bot will create a thread where the players can send their moves in.
` --- ` Moves sent outside the thread will not be counted
` --- ` Moves must be in lowercases

` 4 ` The thread will be deleted once the game has been ended, a king has been checkmate or stalemate.
        """,
        color = 0x2b2d31
      ).set_author(
        name = self.bot.user.display_name,
        icon_url = self.bot.user.display_avatar
      )
      await response.edit_message(
        embed = embed
      )
    elif value == "move-tutorial":
      embed = discord.Embed(
        title = "How to move my pieces ?",
        description = f"""
Select a position / tile ( letter-number ) of a piece that you want to move. Then, select a tile that you want to move the piece to.

### Example :
If you want to move the piece in E-file ( ` e2 ` ) to tile ` e4 ` ( 2 tiles forward ), the move will be ` e2e4 `.
        """,
        color = 0x2b2d31
      ).set_author(
        name = self.bot.user.display_name,
        icon_url = self.bot.user.display_avatar
      )
      await response.edit_message(
        embed = embed
      )
    elif value == "end-resign":
      embed = discord.Embed(
        title = "How do I end the game or resign ?",
        description = """
To end a game, do : ` chess.end `
To resign from your game, do : ` chess.resign `
        """,
        color = 0x2b2d31
      ).set_author(
        name = self.bot.user.display_name,
        icon_url = self.bot.user.display_avatar
      )
      await response.edit_message(
        embed = embed
      )

  async def on_error(self, interaction : discord.Interaction, error):
    traceback.print_exc()

class HowToPlay(commands.GroupCog, name = "how"):
  def __init__(self, bot):
    self.bot = bot
    print(
      "Loaded command : /how to play"
    )

  howto = app_commands.Group(
    name = "to",
    description = "..."
  )

  @howto.command(
    name = "play",
    description = "Learn how to play Chess or move your pieces around !"
  )
  async def howtoplay(self, interaction : discord.Interaction):
    user = interaction.user
    response = interaction.response
    embed = discord.Embed(
      title = "Hello ! How may I help you today ?",
      description = "Select an option below :",
      color = 0x2b2d31
    ).set_author(
      name = self.bot.user.display_name,
      icon_url = self.bot.user.display_avatar
    )
    view = ui.View().add_item(
      HowToPlaySelect(self.bot)
    )
    await response.send_message(
      embed = embed,
      ephemeral = True,
      view = view
    )
  
  @howtoplay.error
  async def error(self, interaction : discord.Interaction, error):
    traceback.print_exc()

async def setup(bot):
  await bot.add_cog(HowToPlay(bot))