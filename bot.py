# bot.py
import os

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} se conectou no Discord!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    MensagemDoBot1 = 'Olá, eu sou o C.O.R.N.O!'
       
    if message.content == 'Plau':
        await message.channel.send(MensagemDoBot1)
    if message.content == 'Pleu':
        await message.channel.send(f'Não me chame de corno. {MensagemDoBot1}.12*2. {40*15}')
    if message.content == 'Pliu':
        await message.channel.send(f'Eu não sei o que é {message.author} mas eu sei o que é {client.user}. Que loucura {message.content}.')
        print('Que loucura')
    
        
    
client.run(TOKEN)

