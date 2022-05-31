from utils import get_store
from utils import embs
import discord
from discord import Interaction, app_commands
from discord.ext import commands, tasks
from discord.utils import MISSING


class Valorant(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        super().__init__()  # this is now required in this context.

    @commands.Cog.listener()
    # Cogが読み込まれた時に発動
    async def on_ready(self):
        await print('GreetingsCog on ready!')


    @app_commands.command()
    async def hello(self, ctx):
        await ctx.send(f'Hello {ctx.author.display_name}.')


    @app_commands.command(description="Shows your daily store in your accounts")
    @app_commands.describe(username='Input username (without login)', password='password (without login)')
    # 関数の引数の説明文定義
    # @app_commands.guild_only() # サーバー内でコマンドを打った場合のみに適用
    async def store(self, interaction: Interaction, username: str = None, password: str = None) -> None:
        # language

        # check if user is logged in
        is_private_message = True if username is not None or password is not None else False

        await interaction.response.defer(ephemeral=is_private_message)

        # get endpoint
        getting = get_store.API()
        await getting.set_auth(username,password)
        data = await getting.store()

        embeds = discord.Embed(title=f"Store Offers of {username}", color=discord.Colour.green())
        embeds = [embeds]
        [embeds.append(embs.get_emb(name, url)) for name, url in data.items()]
        #print(embeds)

        await interaction.followup.send(embeds=embeds,
                                        view=embs.share_button(interaction, embeds) if is_private_message else MISSING)

async def setup(bot):
    await bot.add_cog(Valorant(bot))