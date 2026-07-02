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


class Rolch(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def is_owner(self, interaction: discord.Interaction):
        return discord.utils.get(
            interaction.user.roles,
            name=self.bot.owner_role_name
        ) is not None

    def build_embed(self):
        embed = discord.Embed(
            title="🌱 Roles del servidor",
            description=(
                "Estos roles sirven para identificar tu perfil dentro del club.\n"
                "No son jerárquicos y **no limitan** en qué proyectos puedes participar."
            ),
            color=discord.Color.blurple()
        )

        embed.add_field(
            name="**⚙️ Backend**",
            value="Lógica del servidor, APIs, bases de datos y arquitectura.",
            inline=False
        )

        embed.add_field(
            name="**🎨 Frontend**",
            value="Interfaces, experiencia de usuario y aplicaciones cliente.",
            inline=False
        )

        embed.add_field(
            name="⛓️‍💥 Full-Stack",
            value="Backend + Frontend. Capaz de trabajar en ambos extremos.",
            inline=False
        )

        embed.add_field(
            name="🧬 Low-Level",
            value="Sistemas, C/C++, Rust, optimización, OS, hardware y rendimiento.",
            inline=False
        )

        embed.add_field(
            name="📦️ DevOps",
            value="Infraestructura, CI/CD, despliegue, automatización y servidores.",
            inline=False
        )

        embed.add_field(
            name="🖌️ Design",
            value="Diseño gráfico, UI/UX, branding y material audio-visual.",
            inline=False
        )

        embed.add_field(
            name="🧪 Tester",
            value="Pruebas, QA, detección de errores y mejora de estabilidad.",
            inline=False
        )

        embed.add_field(
            name="📣 Marketing",
            value="Difusión, redes sociales, comunicación y crecimiento del club.",
            inline=False
        )

        return embed

    async def update_roles_message(self, channel: discord.TextChannel):
        embed = self.build_embed()

        pinned = await channel.pins()
        if pinned:
            await pinned[0].edit(embed=embed)
        else:
            msg = await channel.send(embed=embed)
            await msg.pin()

    @app_commands.command(
        name="setup_rol",
        description="Publica o actualiza el mensaje de roles del servidor"
    )
    async def setup_rol(self, interaction: discord.Interaction):
        if not self.is_owner(interaction):
            await interaction.response.send_message(
                "❌ Solo el owner puede usar este comando.",
                ephemeral=True
            )
            return

        await interaction.response.defer(ephemeral=True)

        await self.update_roles_message(interaction.channel)

        await interaction.followup.send(
            "Mensaje de roles configurado correctamente ✅",
            ephemeral=True
        )


async def setup(bot):
    await bot.add_cog(Rolch(bot))
