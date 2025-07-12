import discord, datetime, os, asyncio
from discord.ext import commands
from dotenv import load_dotenv
from chatbot import ask_openrouter

client = commands.Bot(command_prefix=".", help_command=None, intents=discord.Intents.all())
warnings_dict = {}

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
    await channel.send("[Message from " + str(message.author) + " deleted on "
                       + str(message.channel) + "]")

@client.command()
async def kick(ctx, member: discord.Member, *, reason=None):
    log_channel = client.get_channel(1249871058152980530)
    if reason is None:
        reason = "Sin razón especificada."

    try:
        await member.kick(reason=reason)
        await ctx.send(f"{member.mention} ha sido expulsado del servidor.")
        await log_channel.send(f"[{ctx.author} ha expulsado a "
                               f"{member} por {reason}]")
    except Exception as e:
        await ctx.send(f"[{member.name} no puede ser expulsado]")
        await log_channel.send(
            f"[No se pudo expulsar a {member.name}, {e}]")

@client.command()
async def ban(ctx, member: discord.Member, *, reason=None):
    log_channel = client.get_channel(1249871058152980530)
    if reason is None:
        reason = "Sin razón especificada."

    try:
        await member.ban(reason=reason)
        await ctx.send(f"{member.mention} ha sido baneado del servidor.")
        await log_channel.send(f"[{ctx.author} ha baneado a "
                               f"{member} por {reason}]")
    except Exception as e:
        await ctx.send(f"[{member.name} no puede ser baneado]")
        await log_channel.send(
            f"[No se pudo expulsar a {member.name}, {e}]")

@client.command()
async def mute(ctx, usuario: discord.Member, tiempo: int, *,
               razon: str = "Sin razón especificada."):
    log_channel = client.get_channel(1249871058152980530)
    servidor = ctx.guild
    rol_muteado = discord.utils.get(servidor.roles, name="Mute")

    if not rol_muteado:
        await ctx.send("No se encontró el rol 'Mute'.")
        return

    if tiempo <= 0:
        await ctx.send("El tiempo debe ser un número positivo en segundos.")
        return

    try:
        await usuario.add_roles(rol_muteado, reason=razon)
        await ctx.send(f"{usuario.mention} ha sido muteado por {tiempo} segundos.")
        await log_channel.send(f"[{ctx.author} ha muteado a {usuario} por "
                              f"{razon} durante {tiempo} segundos]")

        await asyncio.sleep(tiempo)

        await usuario.remove_roles(rol_muteado)
        await ctx.send(f"{usuario.mention} ha sido desmuteado automáticamente.")
        await log_channel.send(f"[{usuario} ha sido desmuteado tras {tiempo} "
                               f"segundos]")
    except Exception as error:
        await ctx.send("No se pudo aplicar el mute.")
        await log_channel.send(f"[Error al mutear a {usuario}: {error}]")

@client.command()
async def warn(ctx, miembro: discord.Member, *,
               razon: str = "Sin razón especificada."):
    log_channel = client.get_channel(1249871058152980530)
    user_id = str(miembro.id)

    if user_id not in warnings_dict:
        warnings_dict[user_id] = []
    warnings_dict[user_id].append(razon)

    total_warns = len(warnings_dict[user_id])
    await ctx.send(f"{miembro.mention} ha recibido una advertencia, lleva "
                   f"{total_warns}/3 acumuladas.")
    await log_channel.send(f"[{ctx.author} ha advertido a {miembro} "
                           f"por \"{razon}\". Total: {total_warns}/3]")

    if total_warns >= 3:
        try:
            await miembro.ban(reason="Acumulación de warnings")
            await ctx.send(f"{miembro.mention} ha sido baneado por acumulación "
                           f"de advertencias.")
            await log_channel.send(f"[{miembro} ha sido baneado "
                                   f"automáticamente por acumulación de warnings]")
            del warnings_dict[user_id]
        except Exception as e:
            await ctx.send(f"No se pudo banear a {miembro.mention}.")
            await log_channel.send(f"[Error al banear a {miembro}: {e}]")


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
async def connect(ctx):
    voice_channel = client.get_channel(1249858208793755723)
    if voice_channel is None:
        await ctx.send("No pude encontrar el canal de voz.")
        return

    if ctx.voice_client is not None:
        await ctx.voice_client.disconnect()

    try:
        await voice_channel.connect()
        await ctx.send(f"Conectado al canal de voz: {voice_channel.name}")
    except Exception as e:
        await ctx.send(f"No pude conectarme al canal de voz: {e}")

@client.command()
async def disconnect(ctx):
    voice_client = ctx.voice_client
    if voice_client is None:
        await ctx.send("No estoy conectado a ningún canal de voz.")
        return

    await voice_client.disconnect()
    await ctx.send("Me he desconectado del canal de voz.")

@client.command()
async def remindme(ctx, *, args):
    try:
        parts = args.split()
        seconds = int(parts[-1])
        reminder = " ".join(parts[:-1])

        if seconds <= 0:
            await ctx.send("Por favor ingresa un tiempo válido mayor que 0.")
            return
        if reminder == "":
            await ctx.send("Por favor ingresa un mensaje para el recordatorio.")
            return

        await ctx.send(f"Recordatorio programado en {seconds} segundos.")

        await asyncio.sleep(seconds)

        await ctx.send(f"[Recordatorio {ctx.author.mention}: {reminder}]")

    except ValueError:
        await ctx.send("Usa el comando así: `.remindme <mensaje> "
                       "<segundos>`\nEjemplo: `.remindme Despierta 180`")


@client.command()
async def show(ctx, member: discord.Member = None):
    member = member or ctx.author

    activity = None
    for act in member.activities:
        if isinstance(act, discord.Spotify):
            activity = act
            break
        elif act.type == discord.ActivityType.listening:
            activity = act
            break

    if activity:
        if isinstance(activity, discord.Spotify):
            artistas = ", ".join(activity.artists)
            await ctx.send(f"Estás escuchando {activity.title} de {artistas}")
        else:
            desc = activity.details if hasattr(activity, 'details') else str(
                activity)
            await ctx.send(desc)
    else:
        await ctx.send(
            f"{member.display_name}, no estás escuchando nada ahora mismo.")

@client.command()
async def mystats(ctx):
    member = ctx.author
    joined_at = member.joined_at

    if joined_at is None:
        await ctx.send("No pude obtener la fecha de unión.")
        return

    now = datetime.datetime.now(datetime.timezone.utc)
    dias_en_servidor = (now - joined_at).days

    embed = discord.Embed(
        title="📊 Estadísticas del Usuario",
        color=int("58ff37", 16)
    )
    embed.add_field(name="Usuario", value=member.name, inline=False)
    embed.add_field(name="Apodo", value=member.display_name, inline=False)
    embed.add_field(name="Miembro desde", value=joined_at.strftime(
        "%d/%m/%Y %H:%M:%S"), inline=False)
    embed.add_field(name="Tiempo transcurrido",
                    value=f"{dias_en_servidor} días", inline=False)

    await ctx.send(embed=embed)


@client.command()
async def help(ctx):
    embed = discord.Embed(
        title="📁 Lista de comandos disponibles",
        description="Aquí tienes un resumen rápido de lo que puedes usar:",
        color=int("33ffff", 16)
    )

    embed.add_field(name=".hello", value="Saludo breve del bot", inline=False)
    embed.add_field(name=".bye", value="Despedida breve del bot", inline=False)
    embed.add_field(name=".connect", value="Unir bot al canal de voz",
                    inline=False)
    embed.add_field(name=".disconnect",
                    value="Desconectar bot del canal de voz",
                    inline=False)
    embed.add_field(name=".purge <n>",
                    value="Borra los últimos n mensajes del canal",
                    inline=False)
    embed.add_field(name=".create_text_channel <nombre>",
                    value="Crea un canal de texto con el nombre dado",
                    inline=False)
    embed.add_field(name=".delete_text_channel <#canal> <razón>",
                    value="Elimina un canal específico con una razón",
                    inline=False)
    embed.add_field(name=".remindme <mensaje> <segundos>",
                    value="Establece un recordatorio",
                    inline=False)
    embed.add_field(name=".mystats",
                    value="Muestra las estadísticas del usuario",
                    inline=False)
    embed.add_field(name=".help", value="Muestra esta lista de comandos",
                    inline=False)

    embed.set_footer(
        text="Los eventos como joins, bans o mensajes eliminados se registran automáticamente.")

    await ctx.send(embed=embed)


load_dotenv()
client.run(os.getenv("DISCORD_TOKEN"))