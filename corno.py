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
        self.MusicaAtual = ""

    def buscaYouTube(self, busca, solicitante):
        with YoutubeDL(CornoBot.OPCOES_YT) as ytdl:
            try:
                PrimeiroResultado = ytdl.extract_info(f'ytsearch:{busca}', download=False)['entries'][0]
                return {
                    'source' : PrimeiroResultado['formats'][0]['url'],
                    'title' : PrimeiroResultado['title'],
                    'solicitante' : solicitante
                    }
            except Exception as e:
                print(f'Erro ao tentar buscar no YouTube. Veja como foi a busca: {busca}\nERRO: {e}')
                return False

    def TocarProxima(self):
        if len(self.ListaDeMusicas) > 0:
            self.Tocando = True

            url = self.ListaDeMusicas[0][0]['source']
            self.MusicaAtual = self.ListaDeMusicas[0]
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
            
            self.MusicaAtual = self.ListaDeMusicas[0]
            self.ListaDeMusicas.pop(0)
            
            self.canal.play(discord.FFmpegPCMAudio(url, **CornoBot.OPCOES_FFMPEG), after=lambda e: self.TocarProxima())
        else:
            self.Tocando = False
    
    @commands.command(name='plau', help='Vou botar as música para rodar... Do YouTube')
    async def plau(self, ctx, *args):
        pedido = " ".join(args)
        try:
            canal = ctx.author.voice.channel
        except:
            await ctx.send("Ô arrombado (ou arrombada :heart_eyes:), você precisa estar conectado em um canal de áudio para ouvir áudio, né.")

        if self.Pausado:
            self.canal.resume()
        else:
            if pedido == "":
                await ctx.message.add_reaction("<:Dwight4:942070187920850975>")
                await ctx.send("Posso ser escravo, mas não sou adivinho, ô jumento. O que você quer ouvir?")
            else:
                musica = self.buscaYouTube(pedido, ctx.author.display_name)
                if type(musica) == type(True):
                    await ctx.send("Não achei nada dessa bosta que você escreveu. Você é burro e fez o pedido de uma forma burra... Melhore.")
                else:
                    await ctx.send(f'Procurei por "{pedido}"... Vai tocar agora... Ou em alguma hora.')
                    self.ListaDeMusicas.append([musica, canal])

                    if self.Tocando == False:
                        await self.TocarMusica(ctx)

    @commands.command(name='pleu', help='Vou pausar a música que estiver rodando.')
    async def pleu(self, ctx, *args):
        if self.Tocando:
            self.Tocando = False
            self.Pausado = True
            self.canal.pause()
            await ctx.send(f'Pausei "{self.MusicaAtual[0]["title"]}".')
        elif self.Pausado:
            self.canal.resume()

    @commands.command(name='pliu', help='Vou voltar a tocar a música que tava rodando.')
    async def pliu(self, ctx, *args):
        if self.Pausado:
            await ctx.send(f'Voltando a tocar "{self.MusicaAtual[0]["title"]}".')
            self.canal.resume()

    @commands.command(name='plue', help='Vou pular a tocar a música atual que estiver rodando.')
    async def plue(self, ctx):
        if self.canal != None and self.canal:
            await ctx.send(f'Ok, pulando a "{self.MusicaAtual[0]["title"]}". Não precisa gritar.')
            self.MusicaAtual = ""
            self.canal.stop()
            await self.TocarMusica(ctx)

    @commands.command(name='playlist', help='Vou mostrar a lista de músicas.')
    async def playlist(self, ctx):
        playlist = ""
        for x in range(0, len(self.ListaDeMusicas)):
            if x > 4: break
            playlist += str(x+1) + ' - ' + self.ListaDeMusicas[x][0]['title'] + ' (pedido por: ' + self.ListaDeMusicas[x][0]['solicitante'] + ')' + '\n'

        if self.MusicaAtual != "" and playlist == "":
            await ctx.send(f'Agora está tocando "{self.MusicaAtual[0]["title"]}" (pedido por: {self.ListaDeMusicas[x][0]["solicitante"]}) e não tenho mais nada para tocar')
        elif self.MusicaAtual != "" and playlist != "":
            await ctx.send(f'Agora está tocando "{self.MusicaAtual[0]["title"]}".\n\nAinda vai tocar isso aqui ó:\n{playlist}')
        else:
            await ctx.send("Tem nada aqui não, menó.")

    @commands.command(name='limpa', help='Vou parar a música atual e apagar toda a playlist atual que estiver rodando.')
    async def limpa(self, ctx):
        if self.canal != None and self.canal:
            self.canal.stop()
        self.ListaDeMusicas = []
        await ctx.send("Graças a Deus pararam de se torturar.")

    @commands.command(name='ajuda', aliases=["comando", "comandos"], help='Vou mandar a lista de comandos disponíveis..')
    async def ajuda(self, ctx):
        await ctx.send("""
        Ih alá... O caba precisa de ajudinha.

        `!ajuda` ou `!comandos` = Mostrar este menu
        `!plau nome ou link da música` = Tocar músicas
        `!pleu` = Pausar músicas
        `!pliu` = Voltar a tocar
        `!plue` = Pular músicas
        `!playlist` = Ver lista de músicas que serão reproduzidas
        `!limpa` Parar música e limpar playlis
        `!tchau` Desconectar bot

        ```Eu não executo playlists nem reproduzo Spotify. Adivinha de quem é a culpa?```
        """)
        
    @commands.command(name='tchau', help='Vou de base, F no chat.')
    async def tchau(self, ctx):
        self.Tocando = False
        self.Pausado = False
        self.ListaDeMusicas = []
        self.MusicaAtual = []
        await ctx.send("Beleza, pode crer, tô indo embora, tá suave, só não conta comigo pra mais nada...")
        await self.canal.disconnect()