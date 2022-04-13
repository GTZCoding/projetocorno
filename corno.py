import discord
from discord.ext import commands
from youtube_dl import YoutubeDL

class CornoBot(commands.Cog):
    # Constantes
    OPCOES_YT = {'format': 'bestaudio', 'noplaylist':'True'}
    OPCOES_FFMPEG = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}   

    # Classe
    def __init__(self, bot):
        self.bot = bot

        self.Tocando = False
        self.Pausado = False
        
        self.canal = None

        self.ListaDeMusicas = []

    def buscaYouTube(self, busca):
        with YoutubeDL(CornoBot.OPCOES_YT) as ytdl:
            try:
                PrimeiroResultado = ytdl.extract_info(f'ytsearch:{busca}', download=False)['entries'][0]
                return {
                    'source' : PrimeiroResultado['formats'][0]['url'],
                    'title' : PrimeiroResultado['title']
                    }
            except Exception as e:
                print(f'Erro ao tentar buscar no YouTube. Veja como foi a busca: {busca}\nERRO: {e}')
                return False

    def TocarProxima(self):
        if len(self.ListaDeMusicas) > 0:
            self.Tocando = True

            url = self.ListaDeMusicas[0][0]['source']
            self.ListaDeMusicas.pop(0)

            self.canal.play(discord.FFmpegPCMAudio(url, **CornoBot.OPCOES_FFMPEG))
        else:
            self.Tocando = False
    
    async def TocarMusica(self, ctx):
        if len(self.ListaDeMusicas) > 0:
            self.Tocando = True

            url = self.ListaDeMusicas[0][0]['source']
            
            if self.canal == None or not self.canal.is_connected():
                self.canal = await self.ListaDeMusicas[0][1].connect()

                if self.canal == None:
                    await ctx.send("Ô arrombado (ou arrombada :heart_eyes:), você precisa estar conectado em um canal de áudio para ouvir áudio, né.")
                    return
            else:
                await self.canal.move_to(self.ListaDeMusicas[0][1])

            self.ListaDeMusicas.pop(0)
            
            self.canal.play(discord.FFmpegPCMAudio(url, **CornoBot.OPCOES_FFMPEG), after=lambda e: self.TocarProxima())
        else:
            self.Tocando = False
    
    @commands.command(name='plau', help='Vou botar as música para rodar... Do YouTube')
    async def plau(self, ctx, *args):
        pedido = " ".join(args)

        canal = ctx.author.voice.channel

        if canal is None:
            await ctx.send("Ô arrombado (ou arrombada :heart_eyes:), você precisa estar conectado em um canal de áudio para ouvir áudio, né.")
        elif self.Pausado:
            self.canal.resume()
        else:
            musica = self.buscaYouTube(pedido)
            if type(musica) == type(True):
                await ctx.send("Não achei nada dessa bosta que você escreveu. Você é burro e fez o pedido de uma forma burra... Melhore.")
            else:
                await ctx.send("Achei esse lixo que você chama de música... Vai entrar na fila para tocar.")
                self.ListaDeMusicas.append([musica, canal])

                if self.Tocando == False:
                    await self.TocarMusica(ctx)

    @commands.command(name='pleu', help='Vou pausar a música que estiver rodando.')
    async def pleu(self, ctx, *args):
        if self.Tocando:
            self.Tocando = False
            self.Pausado = True
            self.canal.pause()
        elif self.Pausado:
            self.canal.resume()

    @commands.command(name='pliu', help='Vou voltar a tocar a música que tava rodando.')
    async def pliu(self, ctx, *args):
        if self.Pausado:
            self.canal.resume()

    @commands.command(name='pula', help='Vou pular a tocar a música atual que estiver rodando.')
    async def pula(self, ctx):
        if self.canal != None and self.canal:
            self.canal.stop()
            await self.TocarMusica(ctx)

    @commands.command(name='playlist', help='Vou mostrar a lista de músicas.')
    async def playlist(self, ctx):
        playlist = ""
        for x in range(0, len(self.ListaDeMusicas)):
            if x > 4: break
            playlist += self.ListaDeMusicas[x][0]['title'] + '\n'

        if playlist != "":
            await ctx.send(f'Ainda vai tocar isso aqui ó:\n\n{playlist}')
        else:
            await ctx.send("Tem nada aqui não, menó.")

    @commands.command(name='limpa', help='Vou parar a música atual e apagar toda a playlist atual que estiver rodando.')
    async def limpa(self, ctx):
        if self.canal != None and self.canal:
            self.canal.stop()
        self.ListaDeMusicas = []
        await ctx.send("Graças a Deus tiraram pensaram melhor e tiraram esse tanto de lixo.")
        
    @commands.command(name='tchau', help='Vou de base, F no chat.')
    async def tchau(self, ctx):
        self.Tocando = False
        self.Pausado = False
        await ctx.send("Beleza, pode crer, tô indo embora, tá suave, só não conta comigo pra mais nada...")
        await self.canal.disconnect()