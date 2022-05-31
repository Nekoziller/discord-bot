import discord
from discord.ext import commands

class Valorant(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    # Cogが読み込まれた時に発動
    async def on_ready(self):
        await print('GreetingsCog on ready!')

    @commands.command()
    async def hello(self, ctx):
        await ctx.send(f'Hello {ctx.author.display_name}.')


async def setup(bot):
    await bot.add_cog(Valorant(bot))