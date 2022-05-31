import discord
import os
from discord.ext import commands
import asyncio
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.all()

INITIAL_EXTENSIONS = [
     'cogs.example'
 ]

class Discord_bot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(command_prefix="/", case_insensitive=True, intents=intents)

    async def on_ready(self):
        for cog in INITIAL_EXTENSIONS:
            await bot.load_extension(cog)
        print(f'{bot.user} is Ready')

    async def start(self):
        return await super().start(os.getenv('TOKEN'), reconnect=True)



if __name__ == "__main__":
    bot = Discord_bot()
    asyncio.run(bot.start())