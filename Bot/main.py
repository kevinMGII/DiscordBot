import discord, datetime
from discord.ext import commands

client = commands.Bot(command_prefix = ".", intents = discord.Intents.all())

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
    """channel: bienvenida"""
    channel = client.get_channel(1249870241140441182)
    await channel.send("[Hi " + str(member) + "]")

@client.event
async def on_member_remove(member):
    """channel: bienvenida"""
    channel = client.get_channel(1249870241140441182)
    await channel.send("[Bye " + str(member) + "]")

@client.event
async def on_member_ban(guild, user):
    """channel: logs"""
    channel = client.get_channel(1249871058152980530)
    current_time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    await channel.send("[User " + str(user) + " banned from " + str(guild) +
                       " at " + current_time + "]")

@client.event
async def on_member_unban(guild, user):
    """channel: logs"""
    channel = client.get_channel(1249871058152980530)
    current_time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    await channel.send("[User " + str(user) + " unbanned from " + str(guild) +
                       " at " + current_time + "]")

@client.event
async def on_member_update(before, after):
    """channel: logs"""
    channel = client.get_channel(1249871058152980530)
    await channel.send("[New update on " + str(before) + " now " + str(
        after) + "]")

@client.event
async def on_message_delete(message):
    """channel: logs"""
    channel = client.get_channel(1249871058152980530)
    await channel.send("[Message from " + str(message.author) + " deleted on " + str(message.channel) + "]")

client.run("MTI0OTg1MTcwNDA1NzUzMjQ5OA.Ge2BU4.g2JH2kvturV8667JnKXsBWKyZZzhjieEXmgrms")
