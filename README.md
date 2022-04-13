# Projeto C.O.R.N.O
## Projeto Computador Original Regular Neutro para Ouvintes

Este repositório consiste em fazer um Bot para o servidor de Discsord do GTZ, que execute o processamento de arquivos que armazenam em seu interior, ondas sonoras para degustações auriculares dos participantes do servidor. 

A língua de programação esscolhida é *Python*, porque os membros deste servidor gostam de cobra. É importante salientar que, se houvesse necessidade, usaríamos o " *MongoDB* ", devido ao nome peculiar do serviço de banco de dados

### Comandos Diretrizes:

- **!plau** - Tocar músicas
- **!pleu** - Pausar músicas
- **!pliu** - Voltar a tocar
- **!plue** - Pular músicas
- **!playlist** - Ver lista de músicas que serão reproduzidas
- **!limpa** - Parar música e limpar playlis
- **!tchau** - Desconectar bot

## Como instalar

### Baixe o repositório em seu PC

    git clone https://github.com/GTZCoding/projetocorno.git

### Instale o FFmpeg

No windows, acompanhe [este tutorial](https://www.geeksforgeeks.org/how-to-install-ffmpeg-on-windows/)

No Ubuntu, basta executar o comando abaixo após realizar um *apt update*:

`sudo apt install ffmpeg`

Para testar, após instalação, digite no console

`ffmpeg -version`

### Crie um ambiente virtual no Python e instale os requerimentos

Crie ambiente virtual com  `python3 -m venv venv` e ative-o com `source venv/bin/activate`

Instale os requerimentos
`pip install -r requerimentos.txt`

### Obtenha as credenciais e execute

Obtenha o CLIENT_SECRET do Bot no [site de desenvolvedor do Discord](https://discord.com/developers/applications "site de desenvolvedor do Discord") e crie um arquivo chamado ".env" desta forma:

    DISCORD_TOKEN = CLIENT_SECRET_AQUI

Para executar, basta executar `python3 main.py`. Você verá a mensagem `CornoBot#6897 se conectou no Discord!` em seu Console.
Para parar o Bot, basta apertar `CTRL + C`

### Update 1.2.1 - 13/04/2022

- Guia para instalação e documentação corrigida. 

### Update 1.2 - 13/04/2022

- Implementação de playlists.
- O Bot agora diz qual é a música atual que está tocando e retorna quais músicas estão na lista.
- Correção na documentação, o comando correto para pular músicas é "plue".

### Update 1.1 - 12/04/2022

- Bot totalmente funcional neste momento. Aceita os comandos acima. Vai passar por um período de beta-testing para ver quais os problemas que aparecerão.

### Update 1.0 - 09/04/2022

- O bot está se conectando ao Discord, consegue identificar os comandos.

Para fins didáticos, a documentação oficial do discord.py encara o "autor" como o usuário que fez o pedido ao Bot.

Para o CornoBot ficar pronto para tocar uma música, ele precisa responder estas perguntas;

- O autor está em canal de audio? SIM ou NÃO?
- CornoBot está no mesmo canal de audio do autor? SIM ou NÃO?
- O autor passou o link ou nome da música que ele quer tocar? SIM ou NÃO?