import chess
import discord
import json
import traceback
from discord import app_commands, ui
from discord.ext import commands

class TextSelectSide(ui.View):
  def __init__(self, user, member, visual : str, bot):
    super().__init__(
      timeout = None
    )
    self.user = user
    self.member = member
    self.visual = visual
    self.bot = bot
    self.board = None
    self.boardMsg = None

  async def startGame(self, interaction : discord.Interaction, side : str):
    try:
      with open('json/emojis.json', 'r') as f:
        emojis = json.load(f)
      with open('json/games.json', 'r') as f:
        games = json.load(f)
      players = {
        str(self.user.id): None,
        str(self.member.id): None
      }
      if interaction.user == self.user:
        if side == "white":
          players[str(self.user.id)] = "white"
          players[str(self.member.id)] = "black"
        else:
          players[str(self.member.id)] = "white"
          players[str(self.user.id)] = "black"
      else:
        if side == "white":
          players[str(self.member.id)] = "white"
          players[str(self.user.id)] = "black"
        else:
          players[str(self.user.id)] = "white"
          players[str(self.member.id)] = "black"
      while True:
        if self.board.is_checkmate() or self.board.is_stalemate():
          embed = self.boardMsg.embeds[0].copy()
          if self.board.outcome() is None:
            winner = "It's a draw !"
          elif self.board.outcome() == chess.WHITE:
            winner = "White wins !"
          elif self.board.outcome() == chess.BLACK:
            winner = "Black wins !"
          embed.description = winner
          await self.boardMsg.edit(
            embed = embed
          )
          del games[str(self.user.id)]
          del games[str(self.member.id)]
          with open('json/games.json', 'w') as f:
            json.dump(games, f, indent = 2)
          break
        currentTurn = "white" if self.board.turn == chess.WHITE else "black"
        def messageCheck(message):
          if message.author.id in [self.user.id, self.member.id]:
            if message.content.lower() in ["chess.end", "chess.resign"]:
              return True
          return message.author.id in [self.user.id, self.member.id] and players[str(message.author.id)] == currentTurn and message.channel.id == interaction.channel.id
        msg = await self.bot.wait_for("message", check = messageCheck)
        if msg.content.lower() in ["chess.end", "chess.resign"]:
          await msg.delete()
          await self.bot.process_commands(msg)
          break
        msgMove = msg.content
        try:
          move = chess.Move.from_uci(msgMove)
          if move not in self.board.legal_moves:
            print("not in legal moves")
            continue
          self.board.push(move)
          strBoard = ""
          numberIndicatorList = [":eight:", ":seven:", ":six:", ":five:", ":four:", ":three:", ":two:", ":one:"]
          for ind, numberIndicator in enumerate(numberIndicatorList):
            strBoard += numberIndicator + str(self.board).split("\n")[ind]
            strBoard += "\n"
          strBoard += ":black_large_square::regional_indicator_a::regional_indicator_b::regional_indicator_c::regional_indicator_d::regional_indicator_e::regional_indicator_f::regional_indicator_g::regional_indicator_h:"
          strBoard = strBoard.replace(
            " ",
            ""
          )
          strBoard2 = ""
          for ind, number in enumerate(numberIndicatorList):
            strBoard2 += number
            line = strBoard.split("\n")[ind][len(number):]
            print(line)
            for ind2, char in enumerate(line):
              if char == ".":
                if ind % 2 == 0:
                  color = ":white_large_square:" if ind2 % 2 != 0 else ":green_square:"
                else:
                  color = ":white_large_square:" if ind2 % 2 == 0 else ":green_square:"
                strBoard2 += color
                continue
              if ind % 2 == 0:
                if ind2 % 2 == 0:
                  color = "green"
                else:
                  color = "white"
                strBoard2 += str(self.bot.get_emoji(emojis[color][char]))
                continue
              else:
                if ind2 % 2 == 0:
                  color = "white"
                else:
                  color = "green"
                strBoard2 += str(self.bot.get_emoji(emojis[color][char]))
                continue
            strBoard2 += "\n"
          strBoard2 += ":black_large_square::regional_indicator_a::regional_indicator_b::regional_indicator_c::regional_indicator_d::regional_indicator_e::regional_indicator_f::regional_indicator_g::regional_indicator_h:"
          currentTurn = "White" if self.board.turn == chess.WHITE else "Black"
          embed = discord.Embed(
            title = f"**{currentTurn}**'s turn !",
            description = strBoard2,
            color = 0x2b2d31
          )
          if players[str(self.member.id)] == "white":
            embed.set_author(
              name = self.user.display_name + (f" | {msgMove}" if msg.author == self.user else "") + (" | Check" if msg.author == self.member and self.board.is_check() else "") + (" | Checkmate" if msg.author == self.member and self.board.is_checkmate() else "") + (" | Stalemate" if msg.author == self.member and self.board.is_stalemate() else ""),
              icon_url = self.user.display_avatar
            ).set_footer(
              text = self.member.display_name + (f" | {msgMove}" if msg.author == self.member else "") + (" | Check" if msg.author == self.user and self.board.is_check() else "") + (" | Checkmate" if msg.author == self.user and self.board.is_checkmate() else "") + (" | Stalemate" if msg.author == self.user and self.board.is_stalemate() else ""),
              icon_url = self.member.display_avatar
            )
          else:
            embed.set_author(
              name = self.member.display_name + (f" | {msgMove}" if msg.author == self.member else "") + (" | Check" if msg.author == self.user and self.board.is_check() else "") + (" | Checkmate" if msg.author == self.user and self.board.is_checkmate() else "") + (" | Stalemate" if msg.author == self.user and self.board.is_stalemate() else ""),
              icon_url = self.member.display_avatar
            ).set_footer(
              text = self.user.display_name + (f" | {msgMove}" if msg.author == self.user else "") + (" | Check" if msg.author == self.member and self.board.is_check() else "") + (" | Checkmate" if msg.author == self.member and self.board.is_checkmate() else "") + (" | Stalemate" if msg.author == self.member and self.board.is_stalemate() else ""),
              icon_url = self.user.display_avatar
            )
          await self.boardMsg.delete()
          self.boardMsg = await interaction.channel.send(
            embed = embed
          )
          await msg.delete()
          continue
        except Exception as error:
          if isinstance(error, chess.InvalidMoveError):
            traceback.print_exc()
          continue
    except:
      traceback.print_exc()

  @ui.button(
    label = "White",
    custom_id = "selectWhiteSide",
    style = discord.ButtonStyle.primary
  )
  async def selectWhiteSide(self, interaction : discord.Interaction, button : ui.Button):
    with open('json/emojis.json', 'r') as f:
      emojis = json.load(f)
    response = interaction.response
    await response.defer()
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
    self.board = chess.Board()
    strBoard = ""
    numberIndicatorList = [":eight:", ":seven:", ":six:", ":five:", ":four:", ":three:", ":two:", ":one:"]
    for ind, numberIndicator in enumerate(numberIndicatorList):
      strBoard += numberIndicator + str(self.board).split("\n")[ind].replace(
        ". . . . . . . .",
        ":white_large_square::green_square::white_large_square::green_square::white_large_square::green_square::white_large_square::green_square:" if ind % 2 == 0 else ":green_square::white_large_square::green_square::white_large_square::green_square::white_large_square::green_square::white_large_square:"
      )
      strBoard += "\n"
    strBoard += ":black_large_square::regional_indicator_a::regional_indicator_b::regional_indicator_c::regional_indicator_d::regional_indicator_e::regional_indicator_f::regional_indicator_g::regional_indicator_h:"
    whitePawnWhite = self.bot.get_emoji(1169093436528398417)
    whitePawnGreen = self.bot.get_emoji(1169093434854875187)
    blackPawnWhite = self.bot.get_emoji(1169104510019444796)
    blackPawnGreen = self.bot.get_emoji(1169104506441699410)
    strBoard = strBoard.replace(
      " ",
      ""
    )
    for ind, number in enumerate(numberIndicatorList):
      line = strBoard.split("\n")[ind].replace(
        number,
        ""
      ).replace(
        ":white_large_square:",
        "."
      ).replace(
        ":green_square:",
        "."
      )
      for ind, char in enumerate(line):
        if char == ".":
          continue
        if ind % 2 == 0:
          color = "white" if char.islower() else "green"
          if char in ["p", "P"]:
            color = "green" if char.islower() else "white" 
          strBoard = strBoard.replace(
            char,
            str(self.bot.get_emoji(emojis[color][char])),
            1
          )
        else:
          color = "green" if char.islower() else "white"
          if char in ["p", "P"]:
            color = "white" if char.islower() else "green" 
          strBoard = strBoard.replace(
            char,
            str(self.bot.get_emoji(emojis[color][char])),
            1
          )
    embed = discord.Embed(
      title = "**White**'s turn !",
      description = strBoard,
      color = 0x2b2d31
    ).set_author(
      name = self.member.display_name,
      icon_url = self.member.display_avatar
    ).set_footer(
      text = self.user.display_name,
      icon_url = self.user.display_avatar
    )
    origRes = await interaction.original_response()
    await origRes.delete()
    self.boardMsg = await interaction.channel.send(
      embed = embed
    )
    await self.startGame(interaction, "white")

  @ui.button(
    label = "Black",
    custom_id = "selectBlackSide",
    style = discord.ButtonStyle.primary
  )
  async def selectBlackSide(self, interaction : discord.Interaction, button : ui.Button):
    with open('json/emojis.json', 'r') as f:
      emojis = json.load(f)
    response = interaction.response
    user = interaction.user
    await response.defer()
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
    self.board = chess.Board()
    strBoard = ""
    numberIndicatorList = [":eight:", ":seven:", ":six:", ":five:", ":four:", ":three:", ":two:", ":one:"]
    for ind, numberIndicator in enumerate(numberIndicatorList):
      strBoard += numberIndicator + str(self.board).split("\n")[ind].replace(
        ". . . . . . . .",
        ":white_large_square::green_square::white_large_square::green_square::white_large_square::green_square::white_large_square::green_square:" if ind % 2 == 0 else ":green_square::white_large_square::green_square::white_large_square::green_square::white_large_square::green_square::white_large_square:"
      )
      strBoard += "\n"
    strBoard += ":black_large_square::regional_indicator_a::regional_indicator_b::regional_indicator_c::regional_indicator_d::regional_indicator_e::regional_indicator_f::regional_indicator_g::regional_indicator_h:"
    whitePawnWhite = self.bot.get_emoji(1169093436528398417)
    whitePawnGreen = self.bot.get_emoji(1169093434854875187)
    blackPawnWhite = self.bot.get_emoji(1169104510019444796)
    blackPawnGreen = self.bot.get_emoji(1169104506441699410)
    strBoard = strBoard.replace(
      " ",
      ""
    )
    for ind, number in enumerate(numberIndicatorList):
      line = strBoard.split("\n")[ind].replace(
        number,
        ""
      ).replace(
        ":white_large_square:",
        "."
      ).replace(
        ":green_square:",
        "."
      )
      for ind, char in enumerate(line):
        if char == ".":
          continue
        if ind % 2 == 0:
          color = "white" if char.islower() else "green"
          if char in ["p", "P"]:
            color = "green" if char.islower() else "white" 
          strBoard = strBoard.replace(
            char,
            str(self.bot.get_emoji(emojis[color][char])),
            1
          )
        else:
          color = "green" if char.islower() else "white"
          if char in ["p", "P"]:
            color = "white" if char.islower() else "green" 
          strBoard = strBoard.replace(
            char,
            str(self.bot.get_emoji(emojis[color][char])),
            1
          )
    embed = discord.Embed(
      title = "**White**'s turn !",
      description = strBoard,
      color = 0x2b2d31
    ).set_author(
      name = self.user.display_name,
      icon_url = self.user.display_avatar
    ).set_footer(
      text = self.member.display_name,
      icon_url = self.member.display_avatar
    )
    origRes = await interaction.original_response()
    await origRes.delete()
    self.boardMsg = await interaction.channel.send(
      embed = embed
    )
    await self.startGame(interaction, "black")
  
  async def on_error(self, interaction : discord.Interaction, error):
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