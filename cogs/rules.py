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


class Rules(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def is_owner(self, interaction: discord.Interaction) -> bool:
        return discord.utils.get(
            interaction.user.roles,
            name=self.bot.owner_role_name
        ) is not None

    def build_general_rules_embed(self) -> discord.Embed:
        embed = discord.Embed(
            title="📘 Reglas Generales",
            description=(
                "Estas reglas estan basadas en el sentido común, por lo mismo son breves y precisas.\n"
                "Sigue las condiciones de servicio de Discord y deberias estar bien."
            ),
            color=discord.Color.blurple()
        )

        embed.add_field(
            name="🤝 Respeto",
            value="Respeta las preferencias, creencias y gustos de los demás miembros.",
            inline=False
        )

        embed.add_field(
            name="💬 Uso responsable del chat",
            value="No hagas menciones innecesarias ni llenes los canales con mensajes sin sentido (spam).",
            inline=False
        )

        embed.add_field(
            name="🔞 Contenido",
            value=(
                "Evita temas sensibles o polémicos.\n"
                "No se permite contenido NSFW, gore o inapropiado."
            ),
            inline=False
        )

        embed.add_field(
            name="🧭 Canales",
            value="Respeta la función de cada canal, puedes leerlo en la descripcion de cada uno.",
            inline=False
        )

        return embed

    def build_technical_rules_embed(self) -> discord.Embed:
        embed = discord.Embed(
            title="⚙️ Reglas Técnicas y GitHub",
            color=discord.Color.green()
        )

        embed.add_field(
            name="🐙 GitHub",
            value=(
                "Todos los proyectos se desarrollan usando GitHub.\n"
                "El código debe mantenerse organizado y documentado."
            ),
            inline=False
        )

        embed.add_field(
            name="🌱 Commits",
            value=(
                "Haz commits claros y descriptivos.\n"
                "Ejemplos:\n"
                "• `fix: corregir crash al iniciar`\n"
                "• `feat: añadir sistema de login`"
            ),
            inline=False
        )

        embed.add_field(
            name="🔀 Pull Requests",
            value=(
                "Las PR deben ser revisadas antes de hacer merge.\n"
                "Evita subir código roto a ramas principales."
            ),
            inline=False
        )

        embed.add_field(
            name="🧪 Testing",
            value=(
                "Si el proyecto lo requiere, prueba tu código antes de marcarlo "
                "como listo o completado."
            ),
            inline=False
        )

        embed.add_field(
            name="📂 Organización",
            value=(
                "Respeta la estructura del proyecto y las decisiones técnicas "
                "tomadas en grupo."
            ),
            inline=False
        )

        return embed

    async def update_rules_message(self, channel: discord.TextChannel):
        embed_general = self.build_general_rules_embed()
        embed_technical = self.build_technical_rules_embed()

        pins = await channel.pins()

        if pins:
            await pins[0].edit(embeds=[embed_general, embed_technical])
        else:
            msg = await channel.send(embeds=[embed_general, embed_technical])
            await msg.pin()

    @app_commands.command(
        name="rules",
        description="Publica o actualiza las reglas del servidor"
    )
    async def rules(self, interaction: discord.Interaction):
        if not self.is_owner(interaction):
            await interaction.response.send_message(
                "❌ Solo el owner puede usar este comando.",
                ephemeral=True
            )
            return

        await interaction.response.defer(ephemeral=True)

        await self.update_rules_message(interaction.channel)

        await interaction.followup.send(
            "📘 Reglas actualizadas correctamente ✅",
            ephemeral=True
        )

async def setup(bot):
    await bot.add_cog(Rules(bot))
