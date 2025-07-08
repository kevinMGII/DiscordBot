import discord, datetime, os
from discord.ext import commands
from dotenv import load_dotenv
from chatbot import ask_openrouter

client = commands.Bot(command_prefix=".", help_command=None, intents=discord.Intents.all())

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

@client.command()
async def create_text_channel(ctx, nombre: str):
    """channel: logs"""
    channel = client.get_channel(1249871058152980530)
    canal = await ctx.guild.create_text_channel(name=nombre)
    await channel.send("[Canal " + canal.mention + " creado]")

@client.command()
async def delete_text_channel(ctx, canal: discord.TextChannel, *, razon=None):
    channel = client.get_channel(1249871058152980530)
    await canal.delete(reason=razon)
    await channel.send("[Canal " + canal.name + " eliminado debido a " +
                       razon + "]")

@client.command()
@commands.has_permissions(manage_messages=True)
async def purge(ctx, amount: int):
    """Borra una cantidad de mensajes en el canal actual"""
    deleted = await ctx.channel.purge(limit=amount)
    confirm = await ctx.send(f"[{len(deleted)} mensajes eliminados]", delete_after=3)

    log_channel = client.get_channel(1249871058152980530)
    await log_channel.send(f"[{ctx.author} purgó {len(deleted)} mensajes en {ctx.channel.mention}]")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    ctx = await client.get_context(message)
    if ctx.valid:
        await client.process_commands(message)
        return

    if message.channel.id == 1250909488756555930:
        async with message.channel.typing():
            response = await ask_openrouter(message.content)
            await message.channel.send(response)

@client.command()
async def help(ctx):
    embed = discord.Embed(
        title="📁 Lista de comandos disponibles",
        description="Aquí tienes un resumen rápido de lo que puedes usar:",
        color=int("33ffff", 16)
    )

    embed.add_field(name=".hello", value="Saludo breve del bot", inline=False)
    embed.add_field(name=".bye", value="Despedida breve del bot", inline=False)
    embed.add_field(name=".purge <n>",
                    value="Borra los últimos n mensajes del canal",
                    inline=False)
    embed.add_field(name=".create_text_channel <nombre>",
                    value="Crea un canal de texto con el nombre dado",
                    inline=False)
    embed.add_field(name=".delete_text_channel <#canal> <razón>",
                    value="Elimina un canal específico con una razón",
                    inline=False)
    embed.add_field(name=".help", value="Muestra esta lista de comandos",
                    inline=False)

    embed.set_footer(
        text="Los eventos como joins, bans o mensajes eliminados se registran automáticamente.")

    await ctx.send(embed=embed)


load_dotenv()
client.run(os.getenv("DISCORD_TOKEN"))
