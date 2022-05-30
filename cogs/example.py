import discord
from discord.ext import commands

class Valorant(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    # Cogが読み込まれた時に発動
    async def on_ready(self):
        await print('GreetingsCog on ready!')

    async def get_endpoint(self, user_id: int, username: str = None,
                           password: str = None) -> API_ENDPOINT:
        if username is not None and password is not None:
            auth = self.db.auth
            data = await auth.temp_auth(username, password)
        elif username or password:
            raise RuntimeError(f"Please provide both username and password!")

        endpoint = self.endpoint
        await endpoint.activate(data)
        return endpoint

    @commands.command()
    async def hello(self, ctx):
        await ctx.send(f'Hello {ctx.author.display_name}.')

    @commands.command(description="Shows your daily store in your accounts")
    @commands.describe(username='Input username (without login)', password='password (without login)')
    # 関数の引数の説明文定義
    # @app_commands.guild_only() # サーバー内でコマンドを打った場合のみに適用
    async def store(self, interaction: Interaction, username: str = None, password: str = None) -> None:
        # language

        response = ResponseLanguage(interaction.command.name, interaction.locale)

        # check if user is logged in
        is_private_message = True if username is not None or password is not None else False

        await interaction.response.defer(ephemeral=is_private_message)

        # get endpoint
        endpoint = await self.get_endpoint(interaction.user.id, interaction.locale, username, password)

        # fetch skin price
        skin_price = await endpoint.store_fetch_offers()
        self.db.insert_skin_price(skin_price)

        # data
        data = await endpoint.store_fetch_storefront()
        embeds = Generate_Embed.store(endpoint.player, data, language, response, self.bot)

        await interaction.followup.send(embeds=embeds,
                                        view=share_button(interaction, embeds) if is_private_message else MISSING)


async def setup(bot):
    await bot.add_cog(Valorant(bot))