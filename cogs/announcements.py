'''
Copyright (C) 2026 wirtnel

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''

import discord
from discord import app_commands
from discord.ext import commands

class Announcements(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def owner_check(self, interaction: discord.Interaction) -> bool:
        role = discord.utils.get(interaction.user.roles, name=self.bot.owner_role_name)
        return role is not None

    @app_commands.command(name="anuncio", description="Enviar un anuncio al canal actual")
    @app_commands.describe(
        contenido="Contenido del anuncio",
        reacciones="Emojis separados por espacio (ej: ❤️ 🚀 👀)"
    )
    async def anuncio(
        self,
        interaction: discord.Interaction,
        contenido: str,
        reacciones: str = ""
    ):
        if not self.owner_check(interaction):
            await interaction.response.send_message(
                "❌ Solo el owner puede enviar anuncios.",
                ephemeral=True
            )
            return

        await interaction.response.defer(ephemeral=True)

        channel = interaction.channel

        message = await channel.send(f"@everyone\n{contenido}")

        if reacciones:
            for emoji in reacciones.split():
                try:
                    await message.add_reaction(emoji)
                except discord.HTTPException:
                    pass

        await interaction.followup.send("📣 Anuncio enviado correctamente.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Announcements(bot))
