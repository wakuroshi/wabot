import discord
from discord import app_commands
from discord.ext import commands
from datetime import timedelta

class Polls(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="poll",
        description="Crear una encuesta nativa de Discord (solo staff)"
    )
    @app_commands.describe(
        pregunta="Pregunta de la encuesta",
        opcion1="Primera opción",
        opcion2="Segunda opción",
        opcion3="(Opcional) Tercera opción",
        opcion4="(Opcional) Cuarta opción"
    )
    async def poll(
        self,
        interaction: discord.Interaction,
        pregunta: str,
        opcion1: str,
        opcion2: str,
        opcion3: str | None = None,
        opcion4: str | None = None
    ):
        # Check de rol 
        staff_role = discord.utils.get(
            interaction.guild.roles,
            name=self.bot.STAFF_ROLE_NAME
        )

        if staff_role not in interaction.user.roles:
            await interaction.response.send_message(
                "❌ Solo el **staff** puede crear encuestas.",
                ephemeral=True
            )
            return

        poll = discord.Poll(
            question=pregunta,
            duration=timedelta(hours=24)
        )

        poll.add_answer(text=opcion1)
        poll.add_answer(text=opcion2)

        if opcion3:
            poll.add_answer(text=opcion3)
        if opcion4:
            poll.add_answer(text=opcion4)

        await interaction.response.send_message(poll=poll)

async def setup(bot: commands.Bot):
    await bot.add_cog(Polls(bot))

