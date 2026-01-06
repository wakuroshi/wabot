import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix= '!', intents = intents)

@bot.event
async def on_ready():
    print(f"Oh hell naw {bot.user.name}")

@bot.event
async def on_member_join(member):
    await member.send(f"Welcome {member.name}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if "amba" in message.content.lower():
        await message.delete()
        await message.channel.send(f"{message.author.mention} ambatunat")
                
    await bot.process_commands(message)

@bot.command()
async def hola(ctx):
    await ctx.send("stfu :rose:")

@bot.command()
async def assign(ctx):
    role = discord.utils.get(ctx.guild.roles, name="bih")
    if role:
        await ctx.author.add_roles(role)
        await ctx.send(f"{ctx.author.mention} is a bih :rose:")
    else:
        await ctx.send("No bih")

@bot.command()
async def remove(ctx):
    role = discord.utils.get(ctx.guild.roles, name="bih")
    if role:
        await ctx.author.remove_roles(role)
        await ctx.send(f"{ctx.author.mention} not a bih :car:")
    else:
        await ctx.send("No bih")

@bot.command()
@commands.has_role("bih")
async def phone(ctx):
    await ctx.send("You are a bih and went thru his phone :rose:")

@phone.error
async def phone_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("You aint no bih :sun:")

@bot.command()
async def dm(ctx, *, msg):
        await ctx.author.send(f"{dm}")

@bot.command()
async def reply(ctx):
        await ctx.reply("replllltyyyayasdfojansdo")

@bot.command()
async def poll(ctx, *, msg):
    embed = discord.Embed(title="Poll", description=msg)
    poll_message = await ctx.send(embed = embed)
    await poll_message.add_reaction(":thumbsup:")
    await poll_message.add_reaction(":rose:")

bot.run(token, log_handler=handler, log_level = logging.DEBUG)
