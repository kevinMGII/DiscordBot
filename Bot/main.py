import discord
from discord.ext import commands

client = commands.Bot(command_prefix = ".", intents = discord.Intents.all())

@client.event
async def on_ready():
    print("[Bot is ready]")

@client.command()
async def hello(ctx):
    await ctx.send("[Hi]")

client.run("MTI0OTg1MTcwNDA1NzUzMjQ5OA.Ge2BU4.g2JH2kvturV8667JnKXsBWKyZZzhjieEXmgrms")

