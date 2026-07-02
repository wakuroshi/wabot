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

CATEGORY_ROLES = {
    "💻 Backend": "Backend",
    "🎨 Frontend": "Frontend",
    "⚙️ DevOps": "DevOps",
    "🧪 Tester": "Tester",
    "📱 Mobile": "Mobile"
}

COLOR_ROLES = {
    "🍎 Rojo": "Rojo",
    "🍵 Verde": "Verde",
    "❄️ Azul": "Azul",
    "🍌 Amarillo": "Amarillo",
    "🍇 Morado": "Morado",
    "🥕 Naranja": "Naranja",
    "🍫 Marrón": "Marrón",
    "🌸 Rosado": "Rosado",
    "🌑 Negro": "Negro"
}

class Roles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="rol_categoria", description="Elige tu categoría")
    @app_commands.describe(rol="Categoría a asignar")
    @app_commands.choices(rol=[app_commands.Choice(name=name, value=name) for name in CATEGORY_ROLES.values()])
    async def rol_categoria(self, interaction: discord.Interaction, rol: app_commands.Choice[str]):
        await interaction.response.defer(ephemeral=True)
        guild = interaction.guild
        member = interaction.user

        for role_name in CATEGORY_ROLES.values():
            if role_name == rol.value:
                continue
            role_obj = discord.utils.get(guild.roles, name=role_name)
            if role_obj and role_obj in member.roles:
                await member.remove_roles(role_obj)

        role_obj = discord.utils.get(guild.roles, name=rol.value)
        if role_obj:
            await member.add_roles(role_obj)
            await interaction.followup.send(f"Tu categoría ha sido actualizada a **{rol.value}** ✅", ephemeral=True)
        else:
            await interaction.followup.send(f"No se encontró el rol **{rol.value}** en el servidor.", ephemeral=True)

    @app_commands.command(name="rol_color", description="Elige tu color")
    @app_commands.describe(color="Color a asignar")
    @app_commands.choices(color=[app_commands.Choice(name=name, value=name) for name in COLOR_ROLES.values()])
    async def rol_color(self, interaction: discord.Interaction, color: app_commands.Choice[str]):
        await interaction.response.defer(ephemeral=True)
        guild = interaction.guild
        member = interaction.user

        for role_name in COLOR_ROLES.values():
            if role_name == color.value:
                continue
            role_obj = discord.utils.get(guild.roles, name=role_name)
            if role_obj and role_obj in member.roles:
                await member.remove_roles(role_obj)

        role_obj = discord.utils.get(guild.roles, name=color.value)
        if role_obj:
            await member.add_roles(role_obj)
            await interaction.followup.send(f"Tu color ha sido actualizado a **{color.value}** ✅", ephemeral=True)
        else:
            await interaction.followup.send(f"No se encontró el rol **{color.value}** en el servidor.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Roles(bot))

