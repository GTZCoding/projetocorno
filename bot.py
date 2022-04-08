import os

from discord.ext import commands

from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv('TOKEN')

bot = commands.Bot(command_prefix="!")

@bot.event
async def on_ready():
    print(f'{bot.user} tá pronto para botar para quebrar!')

# Reconhecer comandos
@bot.event
async def on_message(mensagem):
    if mensagem.content == "pleus":
        await mensagem.add_reaction('👍')

@bot.command()
async def plau(ctx, arg):
    await ctx.send(arg)

bot.run(TOKEN)