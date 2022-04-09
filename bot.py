import os
from discord.utils import get
from discord.ext import commands
from discord import FFmpegPCMAudio
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix="!")

@bot.event
async def on_ready():
    print(f'{bot.user} se conectou no Discord!')

# Comando "!plau"
# Função do Bot que recebe o link/busca da música, se não enviar parâmetro, ele vai reclamar.
@bot.command()
async def plau(ctx, arg = None):
    if arg == None:
        await ctx.message.add_reaction("<:Dwight4:942070187920850975>")
        await ctx.send("Cadê o link, porra?")
    else:
        if ctx.author.voice:
            await ctx.send("Hum... Agora tá tudo certo... Mas... Eu ainda não sei falar música... *Ainda*. ")
            await ctx.message.add_reaction("<:guedes:702528303772467280>")
            channel = ctx.author.voice.channel
            voice = await channel.connect()
            source = FFmpegPCMAudio("teste.wav")
            player = voice.play(source)
        else:
            await ctx.message.add_reaction("<:Dwight4:942070187920850975>")
            await ctx.send("Porra, você precisa estar conectado em áudio para ouvir áudio, né filho da puta.")

bot.run(TOKEN)

