import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix = ".", intents = intents)

@client.event
async def on_ready():
    print("[Bot is ready]")

@client.command()
async def hello(ctx):
    await ctx.send("[Hi]")

@client.command()
async def bye(ctx):
    await ctx.send("[Bye]")

@client.event
async def on_member_join(member):
    channel = client.get_channel(1249870241140441182)
    await channel.send("[Hi " + member + " ]")

@client.event
async def on_member_remove(member):
    channel = client.get_channel(1249870241140441182)
    await channel.send("[Bye " + member + " ]")

@client.event
async def on_member_ban(guild, user):
    channel = client.get_channel(1249871058152980530)
    await channel.send("[User " + user + " banned from " + guild + " ]")

@client.event
async def on_member_unban(guild, user):
    channel = client.get_channel(1249871058152980530)
    await channel.send("[User " + user + " banned from " + guild + " ]")

client.run("MTI0OTg1MTcwNDA1NzUzMjQ5OA.Ge2BU4.g2JH2kvturV8667JnKXsBWKyZZzhjieEXmgrms")
