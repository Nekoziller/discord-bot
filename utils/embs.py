# Standard
import discord
from discord import Interaction, TextStyle, ui, ButtonStyle
from typing import List


def get_emb(name:str, url:str):
    embeds = discord.Embed(title=name, color=discord.Colour.green())
    embeds.set_thumbnail(url=url)
    return embeds


class share_button(ui.View):
    def __init__(self, interaction: Interaction, embeds: List[discord.Embed]):
        self.interaction: Interaction = interaction
        self.embeds = embeds
        super().__init__(timeout=300)

    async def on_timeout(self) -> None:
        """ Called when the view times out """
        await self.interaction.edit_original_message(view=None)

    @ui.button(label='Share to friends', style=ButtonStyle.primary)
    async def button_callback(self, interaction: Interaction, button: ui.Button):
        await interaction.channel.send(embeds=self.embeds)
        await self.interaction.edit_original_message(content='\u200b', embed=None, view=None)