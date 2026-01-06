import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
import os

# env load (en tu .env debes tener tu token y la ID de la guild/server. Si haces un fork NO SUBAS TU .env a GitHub NI LA COMPARTAS DE NINGUNA MANERA)
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = os.getenv("GUILD_ID")

# Cambia el nombre del role "staff" (o encargado de designar lead y gestionar a nivel general), y del canal de logs, el owner recomendablemente SOLO AL VERDADERO DUEÑO, ajustar los canales a gusto

STAFF_ROLE_NAME = "Staff"
BOT_LOG_CHANNEL = "💾・logs"
PROJECT_CATEGORY = "📌 | Proyectos"
ARCHIVE_CATEGORY = "📦 | Archivados"
OWNER_ROLE = "Owner" 

intents = discord.Intents.default()

# bot init
class WaBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="!",  
            intents=intents
        )

    async def setup_hook(self):
        # Cargar cogs
        await self.load_extension("cogs.polls")
        await self.load_extension("cogs.projects")
        await self.load_extension("cogs.info")
        await self.load_extension("cogs.announcements")
        await self.load_extension("cogs.roles")
        await self.load_extension("cogs.rolch")
        await self.load_extension("cogs.rules")
        await self.load_extension("cogs.wabot")
        
        # Sincronizar slash commands
        await self.tree.sync()

bot = WaBot()
bot.staff_role_name = STAFF_ROLE_NAME
bot.project_category_name = PROJECT_CATEGORY
bot.archive_category_name = ARCHIVE_CATEGORY
bot.bot_log_channel_name = BOT_LOG_CHANNEL
bot.guild_id = GUILD_ID
bot.owner_role_name = OWNER_ROLE 

@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")
    await bot.tree.sync(guild=discord.Object(id=GUILD_ID))
    print("Comandos sincronizados con el servidor")

bot.run(TOKEN)

