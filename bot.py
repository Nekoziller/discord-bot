import aiohttp
import discord
import os
from discord.ext import commands
import asyncio
from dotenv import load_dotenv
import aiohttp

load_dotenv()

intents = discord.Intents.all()

INITIAL_EXTENSIONS = [
     'cogs.example'
 ]

class Discord_bot(commands.Bot):

    bot_app_info: discord.AppInfo

    def __init__(self, *args, **kwargs):
        super().__init__(command_prefix="-", case_insensitive=True, intents=intents)

    async def on_ready(self):
        for cog in INITIAL_EXTENSIONS:
            await bot.load_extension(cog)
        print(f'{bot.user} is Ready')

    async def setup_hook(self) -> None:
        self.session = aiohttp.ClientSession()
        await self.tree.sync(guild=discord.Object(id=(os.getenv('SERVER_ID'))))
        self.bot_app_info = await self.application_info()
        self.owner_id = self.bot_app_info.owner.id

    async def start(self):
        return await super().start(os.getenv('TOKEN'), reconnect=True)



if __name__ == "__main__":
    bot = Discord_bot()
    asyncio.run(bot.start())