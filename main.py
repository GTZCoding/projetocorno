import os
from discord.ext import commands
from corno import CornoBot
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix="!")

bot.add_cog(CornoBot(bot))

@bot.event
async def on_ready():
    print(f'{bot.user} se conectou no Discord!')

bot.run(TOKEN)