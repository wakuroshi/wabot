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


class Wabot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def is_owner(self, interaction: discord.Interaction) -> bool:
        return discord.utils.get(
            interaction.user.roles,
            name=self.bot.owner_role_name
        ) is not None

    def build_wabot_embed(self) -> discord.Embed:
        embed = discord.Embed(
            title="🤖 Wabot — Bot del servidor",
            description=(
                "Wabot es un bot sencillo, hecho desde cero para ayudar con la gestión "
                "de proyectos dentro del servidor, además de algunas utilidades generales.\n\n"
                "El código del bot es **Open Source**. "
                "¡Sugiere nuevas funcionalidades o impleméntalas tú mismo!"
            ),
            color=discord.Color.blurple()
        )

        embed.add_field(
            name="**📚 Comandos generales**",
            value=(
                "Comandos de utilidad general:\n"
                "• **/poll** — Crear encuestas (máx. 4 opciones)\n"
                "• **/rol_categoria** — Elegir tu área de desempeño\n"
                "• **/rol_color** — Elegir tu color en el servidor"
            ),
            inline=False
        )

        embed.add_field(
            name="**🦑 Comandos de proyecto**",
            value=(
                "Comandos para la gestión de proyectos:\n"
                "• **/status** — Cambia el estado del proyecto (**solo el lead**)\n"
                "• **/set_github** — Coloca link al repositorio de github a la descripcion del proyecto (**solo el lead**)\n"
                "• **/add_thread** — Crear un hilo dentro del proyecto (**solo el lead**)\n"
                "• **/del_thread** — Eliminar un hilo del proyecto (**solo el lead**)\n"
                "• **/language** — Añadir, modificar o eliminar los lenguajes de programación asociados al proyecto (**solo el lead**)"
            ),
            inline=False
        )

        embed.set_footer(text="Wabot • Gestión simple y transparente")

        return embed

    async def update_wabot_message(self, channel: discord.TextChannel):
        embed = self.build_wabot_embed()

        pinned = await channel.pins()
        if pinned:
            try:
                await pinned[0].edit(embed=embed)
            except discord.HTTPException:
                msg = await channel.send(embed=embed)
                await msg.pin()
        else:
            msg = await channel.send(embed=embed)
            await msg.pin()

    @app_commands.command(
        name="setup_wabot",
        description="Publica o actualiza el mensaje de información del bot"
    )
    async def setup_wabot(self, interaction: discord.Interaction):
        if not self.is_owner(interaction):
            await interaction.response.send_message(
                "❌ Solo el owner puede usar este comando.",
                ephemeral=True
            )
            return

        await interaction.response.defer(ephemeral=True)

        await self.update_wabot_message(interaction.channel)

        await interaction.followup.send(
            "🤖 Mensaje de Wabot configurado correctamente ✅",
            ephemeral=True
        )

async def setup(bot):
    await bot.add_cog(Wabot(bot))

