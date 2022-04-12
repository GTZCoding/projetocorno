import discord, os
from discord.utils import get
from discord.ext import commands
from dotenv import load_dotenv
from youtube_dl import YoutubeDL

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix="!")

filaDeMusicas = []
YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

def buscaYouTube(item):
    with YoutubeDL(YDL_OPTIONS) as ydl:
        print("Busca Youtube:", ydl)
        try:
            info = ydl.extract_info("ytsearch:%s" % item, download=False)['entries'][0]
        except Exception:
            return False
        return {
            'source' : info['formats'][0]['url'],
            'title' : info['title']
        }

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

@bot.command()
async def tchau(ctx):
    BotEstaConectado = get(ctx.bot.voice_clients, guild=ctx.guild)
    if BotEstaConectado:
        for x in bot.voice_clients:
            await ctx.send("Beleza, pode crer, tô indo embora, tá suave, só não conta comigo pra mais nada...")
            await x.disconnect()
    else:
        await ctx.send("Tá doidão, porra? Tá me dando tchau por quê? Tô quieto aqui, fazendo vários nada, só consumindo sua energia sem pagar nada...")

@bot.command()
async def bleu(ctx, *args):
    # Não estamos prontos pra quebrar.
    prontoParaMusica = False
    # Vamos se preparar. \/
    # O autor está conectado em um canal de áudio?
    if ctx.author.voice:
        # autor colocou a URL ou a palavra para buscar a música?
        if args == None:
            await ctx.message.add_reaction("<:Dwight4:942070187920850975>")
            await ctx.send("Beleza, você tá num canal de áudio, mas o que você quer ouvir? Posso ser escravo, mas não sou adivinho não, ô jumento.")
            prontoParaMusica = False
        else:
            # Se Sim, o BOT está no mesmo canal de áudio do autor ?
            BotEstaConectado = get(ctx.bot.voice_clients, guild=ctx.guild)
            if BotEstaConectado:
                await BotEstaConectado.move_to(ctx.author.voice.channel)
                await ctx.send("Achou mesmo que eu não ia te achar aqui?")
                prontoParaMusica = True
            else:
                canalDeVoz = await ctx.author.voice.channel.connect()
                prontoParaMusica = True
    # Se o solicitante NÃO estiver conectado, Corn o Bot responderá com uma mensagem educada de erro
    else:
        await ctx.message.add_reaction("<:Dwight4:942070187920850975>")
        await ctx.send("Ô arrombado (ou arrombada :heart_eyes:), você precisa estar conectado em um canal de áudio para ouvir áudio, né.")
    # Pronto para botar para quebrar!
    if prontoParaMusica:
        print("Agora ele tá pronto")
        query = " ".join(args)
        musica = buscaYouTube(query)
        print(musica)
        if type(musica) == type(True):
            await ctx.send("Não consegui reproduzir não. Você é burro e colocou o pedido de uma forma burra")
        else:
            await ctx.send("Achei esse lixo que você chama de música... Vai entrar na fila para tocar")
            filaDeMusicas.append(musica)
            m_url = musica['source']
            canalDeVoz.play(discord.FFmpegPCMAudio(m_url, **FFMPEG_OPTIONS))

bot.run(TOKEN)

