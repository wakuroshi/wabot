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


class Info(commands.Cog):
    STATUS_ORDER = ["Activo", "Testing", "Completado"]
    STATUS_EMOJIS = {
        "Activo": "🟢",
        "Testing": "🟠",
        "Completado": "🔵"
    }

    def __init__(self, bot):
        self.bot = bot
        self.info_channel_id: int | None = None

    def is_owner(self, interaction: discord.Interaction):
        return discord.utils.get(
            interaction.user.roles,
            name=self.bot.owner_role_name
        ) is not None

    def build_projects_section(self):
        projects_cog = self.bot.get_cog("Projects")
        if not projects_cog:
            return "⚠️ No se pudo cargar la información de proyectos."

        data = projects_cog.project_data
        if not data:
            return "Aún no hay proyectos registrados."

        grouped = {status: [] for status in self.STATUS_ORDER}

        for channel_id_str, project in data.items():
            channel = self.bot.get_channel(int(channel_id_str))
            display_name = channel.mention if channel else "Sin canal"
            status = project.get("status", "Activo")
            if status in grouped:
                grouped[status].append(display_name)

        lines = []
        for status in self.STATUS_ORDER:
            emoji = self.STATUS_EMOJIS.get(status, "")
            lines.append(f"**{emoji} {status}**")
            if grouped[status]:
                for mention in grouped[status]:
                    lines.append(f"• {mention}")
            else:
                lines.append("_Sin proyectos_")
            lines.append("")

        return "\n".join(lines)

    def build_info_embed(self):
        embed = discord.Embed(
            title="📘 Información del Club",
            color=discord.Color.blurple(),
            description=(
                "El **Club de Desarrollo de Software** es una iniciativa estudiantil "
                "de la Universidad José Antonio Páez, mantenida por estudiantes y orientada "
                "a la creación de software real, libre y colaborativo."
            )
        )

        embed.add_field(
            name="📝 Filosofía",
            value=(
                "Aprender haciendo, compartir conocimiento y construir software en equipo, para así poder practicar en un entorno de trabajo y cada miembro pulir su desempeño en el area que desee.\n"
                "Estructura horizontal, libertad para proponer ideas y colaborar sin jerarquías rígidas."
            ),
            inline=False
        )

        embed.add_field(
            name="🐙 GitHub",
            value=(
                "GitHub es nuestra plataforma central de desarrollo y colaboración.\n"
                "Organización del club: **[placeholder]**"
            ),
            inline=False
        )

        embed.add_field(
            name="📂 Proyectos activos",
            value=self.build_projects_section(),
            inline=False
        )

        embed.add_field(
            name="📣 Redes sociales",
            value="(próximamente)",
            inline=False
        )

        return embed

    def build_workflow_embed(self):
        embed = discord.Embed(
            title="🛠️ Dinámica y Flujo de Trabajo",
            color=discord.Color.dark_teal(),
            description=(
                "Este club funciona de manera **abierta, colaborativa y transparente**.\n"
                "A continuación se explica cómo se organiza el trabajo y la participación."
            )
        )

        embed.add_field(
            name="🚀 Cómo nacen los proyectos",
            value=(
                "• Cualquier miembro puede proponer una idea.\n"
                "• Las ideas se discuten y refinan en comunidad, se pueden incluso mezclar ideas entre si para formar un solo proyecto solido.\n"
                "• El staff crea el proyecto y asigna un **lead** al proyecto.\n"
                "• El proyecto obtiene su propio canal, con su lead y total libertad en el mismo entre sus colaboradores, cualquiera puede contribuir a su manera."
            ),
            inline=False
        )

        embed.add_field(
            name="👥 Participación",
            value=(
                "**Staff**: organización general, creación y archivado de proyectos.\n"
                "**Lead**: coordina un proyecto, define estado, hilos y GitHub.\n"
                "**Colaboradores**: cualquier miembro que participe activamente."
            ),
            inline=False
        )

        embed.add_field(
            name="🔁 Flujo de trabajo",
            value=(
                "**Brainstorming** → **Discusión** → **Desarrollo** → "
                "**Testing** → **Completado** → **Archivado**\n\n"
                "Cada proyecto avanza a su propio ritmo."
            ),
            inline=False
        )


        return embed

    async def update_info_message(self, channel: discord.TextChannel):
        embeds = [
            self.build_info_embed(),
            self.build_workflow_embed()
        ]

        pinned = await channel.pins()
        if pinned:
            try:
                await pinned[0].edit(embeds=embeds)
            except discord.HTTPException:
                msg = await channel.send(embeds=embeds)
                await msg.pin()
        else:
            msg = await channel.send(embeds=embeds)
            await msg.pin()

    async def refresh_info(self):
        if not self.info_channel_id:
            return
        channel = self.bot.get_channel(self.info_channel_id)
        if isinstance(channel, discord.TextChannel):
            await self.update_info_message(channel)

    @app_commands.command(
        name="info",
        description="Publica o actualiza el mensaje de información del servidor"
    )
    async def info(self, interaction: discord.Interaction):
        if not self.is_owner(interaction):
            await interaction.response.send_message(
                "❌ Solo el owner puede usar este comando.",
                ephemeral=True
            )
            return

        await interaction.response.defer(ephemeral=True)
        self.info_channel_id = interaction.channel.id
        await self.update_info_message(interaction.channel)

        await interaction.followup.send(
            "📘 Mensaje de info actualizado y refresco activado ✅",
            ephemeral=True
        )


async def setup(bot):
    await bot.add_cog(Info(bot))

