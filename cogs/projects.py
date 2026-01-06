import discord
from discord import app_commands
from discord.ext import commands
import json
import os

PROJECTS_FILE = "data/projects.json"

class Projects(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.project_data = self.load_projects()

    def load_projects(self):
        if os.path.exists(PROJECTS_FILE):
            with open(PROJECTS_FILE, "r") as f:
                return json.load(f)
        return {}

    def save_projects(self):
        os.makedirs(os.path.dirname(PROJECTS_FILE), exist_ok=True)
        with open(PROJECTS_FILE, "w") as f:
            json.dump(self.project_data, f, indent=4)

    def is_staff(self, interaction: discord.Interaction):
        role = discord.utils.get(interaction.user.roles, name=self.bot.staff_role_name)
        return role is not None

    def is_lead(self, user: discord.Member, channel_id: int):
        project = self.project_data.get(str(channel_id))
        return project and project.get("lead") == user.id

    async def update_info_channel(self, guild: discord.Guild):
        info_cog = self.bot.get_cog("Info")
        if info_cog and hasattr(info_cog, "info_channel_id") and info_cog.info_channel_id:
            try:
                await info_cog.refresh_info()
            except Exception:
                pass

    async def update_pin(self, channel: discord.TextChannel):
        project = self.project_data.get(str(channel.id))
        if not project:
            return

        lead_id = project.get("lead")
        lead_mention = f"<@{lead_id}>" if lead_id else "No asignado"

        threads = project.get("threads", [])
        threads_text = (
            "\n".join(f"- <#{t['id']}> {t['name']}" for t in threads)
            if threads else "Ninguno"
        )

        languages = project.get("languages", [])
        languages_text = ", ".join(languages) if languages else "Ninguno"

        status = project.get("status", "Activo")

        embed = discord.Embed(
            title=f"📌 {channel.mention}",
            description=project.get("description", ""),
            color=discord.Color.blue()
        )

        embed.add_field(name="👤 Lead", value=lead_mention, inline=True)
        embed.add_field(name="🌸 Estado", value=status, inline=True)
        embed.add_field(name="🧵 Hilos activos", value=threads_text, inline=False)
        embed.add_field(name="💻 Lenguajes", value=languages_text, inline=False)

        if project.get("github"):
            embed.add_field(name="📂 GitHub", value=project["github"], inline=False)

        pins = await channel.pins()
        if pins:
            await pins[0].edit(embed=embed)
        else:
            msg = await channel.send(embed=embed)
            await msg.pin()

    async def log(self, message: str):
        for guild in self.bot.guilds:
            channel = discord.utils.get(
                guild.text_channels,
                name=self.bot.bot_log_channel_name
            )
            if channel:
                await channel.send(message)

    @app_commands.command(name="init")
    async def init(
        self,
        interaction: discord.Interaction,
        title: str,
        description: str = "Crea un nuevo proyecto (staff-only)"
    ):
        if not self.is_staff(interaction):
            await interaction.response.send_message(
                "❌ Solo el staff puede crear proyectos.",
                ephemeral=True
            )
            return

        await interaction.response.defer(ephemeral=True)

        category = discord.utils.get(
            interaction.guild.categories,
            name=self.bot.project_category_name
        )
        if not category:
            return await interaction.followup.send(
                "No existe la categoría de proyectos.",
                ephemeral=True
            )

        channel = await interaction.guild.create_text_channel(
            title,
            category=category
        )

        self.project_data[str(channel.id)] = {
            "title": title,
            "description": description,
            "lead": interaction.user.id,
            "status": "Activo",
            "threads": [],
            "languages": [],
            "history": [f"{interaction.user} creó el proyecto"],
            "github": ""
        }

        self.save_projects()
        await self.update_pin(channel)
        await self.update_info_channel(interaction.guild)

        await interaction.followup.send(
            f"Proyecto **{title}** creado ✅",
            ephemeral=True
        )
        await self.log(f"📌 Proyecto **{title}** creado por {interaction.user}")

    @app_commands.command(name="status")
    @app_commands.choices(state=[
        app_commands.Choice(name="Activo", value="Activo"),
        app_commands.Choice(name="Testing", value="Testing"),
        app_commands.Choice(name="Completado", value="Completado")
    ])
    async def status(
        self,
        interaction: discord.Interaction,
        state: app_commands.Choice[str],
        description: str = "Cambia el estado de un proyecto"
    ):
        await interaction.response.defer(ephemeral=True)

        channel = interaction.channel
        if not self.is_lead(interaction.user, channel.id):
            return await interaction.followup.send(
                "❌ Solo el lead puede cambiar el estado de este proyecto.",
                ephemeral=True
            )

        project = self.project_data.get(str(channel.id))
        project["status"] = state.value
        project["history"].append(
            f"{interaction.user} cambió estado a {state.value}"
        )

        self.save_projects()
        await self.update_pin(channel)
        await self.update_info_channel(interaction.guild)

        await interaction.followup.send(
            "Estado actualizado ✅",
            ephemeral=True
        )
        await self.log(
            f"🔹 Estado de **{project['title']}** → {state.value}"
        )

    @app_commands.command(name="lead_add")
    async def lead_add(self, interaction: discord.Interaction, user: discord.Member):
        if not self.is_staff(interaction):
            return await interaction.response.send_message(
                "❌ Solo el staff puede cambiar el lead.",
                ephemeral=True
            )

        await interaction.response.defer(ephemeral=True)

        project = self.project_data.get(str(interaction.channel.id))
        if not project:
            return await interaction.followup.send(
                "No es un proyecto.",
                ephemeral=True
            )

        project["lead"] = user.id
        project["history"].append(
            f"{interaction.user} cambió lead a {user}"
        )

        self.save_projects()
        await self.update_pin(interaction.channel)
        await self.update_info_channel(interaction.guild)

        await interaction.followup.send(
            "Lead actualizado ✅",
            ephemeral=True
        )
        await self.log(
            f"👤 Lead de **{project['title']}** cambiado a {user}"
        )

    @app_commands.command(name="archivar")
    async def archivar(self, interaction: discord.Interaction):
        if not self.is_staff(interaction):
            return await interaction.response.send_message(
                "❌ Solo el staff puede archivar.",
                ephemeral=True
            )

        await interaction.response.defer(ephemeral=True)

        channel = interaction.channel
        project = self.project_data.get(str(channel.id))
        if not project:
            return await interaction.followup.send(
                "No es un proyecto.",
                ephemeral=True
            )

        archive = discord.utils.get(
            interaction.guild.categories,
            name=self.bot.archive_category_name
        )
        if not archive:
            return await interaction.followup.send(
                "No existe la categoría de archivados.",
                ephemeral=True
            )

        await channel.edit(category=archive)
        project["history"].append(
            f"{interaction.user} archivó el proyecto"
        )

        self.save_projects()
        await self.update_info_channel(interaction.guild)

        await interaction.followup.send(
            "Proyecto archivado 📦",
            ephemeral=True
        )
        await self.log(
            f"📦 Proyecto **{project['title']}** archivado"
        )

    @app_commands.command(name="languages")
    @app_commands.choices(action=[
        app_commands.Choice(name="add", value="add"),
        app_commands.Choice(name="remove", value="remove"),
        app_commands.Choice(name="clear", value="clear")
    ])
    async def languages(
        self,
        interaction: discord.Interaction,
        action: app_commands.Choice[str],
        language: str | None = None
    ):
        await interaction.response.defer(ephemeral=True)

        channel = interaction.channel
        if not self.is_lead(interaction.user, channel.id):
            return await interaction.followup.send(
                "❌ Solo el lead puede modificar los lenguajes del proyecto.",
                ephemeral=True
            )

        project = self.project_data.get(str(channel.id))
        if not project:
            return await interaction.followup.send(
                "No es un proyecto.",
                ephemeral=True
            )

        languages = project.setdefault("languages", [])

        if action.value == "add":
            if not language:
                return await interaction.followup.send(
                    "Debes indicar un lenguaje.",
                    ephemeral=True
                )
            if language in languages:
                return await interaction.followup.send(
                    "Ese lenguaje ya está añadido.",
                    ephemeral=True
                )

            languages.append(language)
            project["history"].append(
                f"{interaction.user} añadió el lenguaje {language}"
            )

        elif action.value == "remove":
            if not language:
                return await interaction.followup.send(
                    "Debes indicar un lenguaje.",
                    ephemeral=True
                )
            if language not in languages:
                return await interaction.followup.send(
                    "Ese lenguaje no está en la lista.",
                    ephemeral=True
                )

            languages.remove(language)
            project["history"].append(
                f"{interaction.user} eliminó el lenguaje {language}"
            )

        elif action.value == "clear":
            languages.clear()
            project["history"].append(
                f"{interaction.user} limpió los lenguajes del proyecto"
            )

        self.save_projects()
        await self.update_pin(channel)
        await self.update_info_channel(interaction.guild)

        await interaction.followup.send(
            "Lenguajes actualizados ✅",
            ephemeral=True
        )

    @app_commands.command(name="github")
    async def github(self, interaction: discord.Interaction, url: str):
        await interaction.response.defer(ephemeral=True)

        channel = interaction.channel
        if not self.is_lead(interaction.user, channel.id):
            return await interaction.followup.send(
                "❌ Solo el lead puede modificar el GitHub del proyecto.",
                ephemeral=True
            )

        project = self.project_data.get(str(channel.id))
        if not project:
            return await interaction.followup.send(
                "No es un proyecto.",
                ephemeral=True
            )

        project["github"] = url
        project["history"].append(
            f"{interaction.user} actualizó el repositorio GitHub"
        )

        self.save_projects()
        await self.update_pin(channel)
        await self.update_info_channel(interaction.guild)

        await interaction.followup.send(
            "Repositorio GitHub actualizado ✅",
            ephemeral=True
        )

    @app_commands.command(name="add_thread")
    async def add_thread(self, interaction: discord.Interaction, title: str):
        await interaction.response.defer(ephemeral=True)

        channel = interaction.channel
        if not self.is_lead(interaction.user, channel.id):
            return await interaction.followup.send(
                "❌ Solo el lead puede crear hilos en este proyecto.",
                ephemeral=True
            )

        thread = await channel.create_thread(
            name=title,
            type=discord.ChannelType.public_thread
        )

        project = self.project_data[str(channel.id)]
        project["threads"].append({"id": thread.id, "name": title})
        project["history"].append(
            f"{interaction.user} creó el hilo {title}"
        )

        self.save_projects()
        await self.update_pin(channel)
        await self.update_info_channel(interaction.guild)

        await interaction.followup.send(
            f"Hilo **{title}** creado ✅",
            ephemeral=True
        )

async def setup(bot):
    await bot.add_cog(Projects(bot))
