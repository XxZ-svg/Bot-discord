import discord
from discord.ext import commands
import asyncio

# Configuración del bot
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='/', intents=intents)

# 🔥 TUS IDs (YA ACTUALIZADOS)
GUILD_ID = 1505785843695222804
CANAL_ESTADOS_ID = 1505986571047010446  # Canal de estadísticas (embed 🔴🟢)
CANAL_AVISOS_ID = 1505986668522635264   # Canal de avisos (mensajes)
CANAL_COMANDOS_ID = 1505986533386358866 # Canal de comandos

# Estados iniciales
estados = {
    "Operativo": "🔴",
    "Entrenamiento": "🔴",
    "Patrullaje": "🔴",
    "Reuniones": "🔴"
}

# GIF de meteoritos
METEOR_GIF = "https://i.imgur.com/7X5V2gY.gif"

# ========== FUNCIÓN PARA ACTUALIZAR EMBED ==========
async def actualizar_embed():
    embed = discord.Embed(
        title="🚔 **POLICÍA ARGENTINA RP** 🚔",
        description="**PANEL DE CONTROL DE ESTADOS**\n",
        color=0xff0000 if any(v == "🔴" for v in estados.values()) else 0x00ff00
    )
    
    embed.set_image(url=METEOR_GIF)
    
    embed.add_field(name="🚨 **OPERATIVO**", value=f"┗━━ {estados['Operativo']}", inline=False)
    embed.add_field(name="🎯 **ENTRENAMIENTO**", value=f"┗━━ {estados['Entrenamiento']}", inline=False)
    embed.add_field(name="🚓 **PATRULLAJE**", value=f"┗━━ {estados['Patrullaje']}", inline=False)
    embed.add_field(name="📋 **REUNIONES**", value=f"┗━━ {estados['Reuniones']}", inline=False)
    
    embed.set_footer(text="⭐ Policía Argentina RP | Actualización automática")
    embed.timestamp = discord.utils.utcnow()
    
    canal = bot.get_channel(CANAL_ESTADOS_ID)
    if canal:
        async for mensaje in canal.history(limit=5):
            if mensaje.author == bot.user and mensaje.embeds:
                await mensaje.edit(embed=embed)
                return
        await canal.send(embed=embed)

# ========== FUNCIÓN PARA ENVIAR MENSAJES ==========
async def enviar_mensaje(titulo, mensaje, color, mencion_todo=False, mencion_aqui=False):
    embed = discord.Embed(
        title=titulo,
        description=mensaje,
        color=color
    )
    embed.set_footer(text="🚔 Policía Argentina RP")
    
    canal = bot.get_channel(CANAL_AVISOS_ID)
    if canal:
        content = ""
        if mencion_todo:
            content = "@everyone"
        elif mencion_aqui:
            content = "@here"
        
        msg = await canal.send(content=content, embed=embed)
        
        # Eliminar mensaje después de 10 minutos
        await asyncio.sleep(600)
        try:
            await msg.delete()
        except:
            pass

# ========== FUNCIÓN PARA VERIFICAR SI ES ADMIN ==========
def es_admin(ctx):
    # Verificar que el comando se use en el canal correcto
    if ctx.channel.id != CANAL_COMANDOS_ID:
        return False
    return ctx.author.guild_permissions.administrator

# ========== COMANDOS ==========

@bot.command(name='operativo')
async def operativo(ctx, estado: str = None):
    if not es_admin(ctx):
        if ctx.channel.id != CANAL_COMANDOS_ID:
            await ctx.send(f"❌ **Usá este comando en el canal <#{CANAL_COMANDOS_ID}>**", delete_after=5)
        else:
            await ctx.send("❌ **No tenés permiso para usar este comando.**", delete_after=5)
        return
    
    if estado == 'on':
        estados["Operativo"] = "🟢"
        await actualizar_embed()
        
        mensaje = (
            "⚠️ **Se informa que hay un operativo policial en curso.**\n"
            "👮 **Se solicita la presencia inmediata de todas las unidades disponibles.**\n\n"
            "📢 **¡Todos deben unirse y acudir al operativo AHORA!**\n\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "🚓 **Policía Argentina RP**\n"
            "━━━━━━━━━━━━━━━━━━"
        )
        await enviar_mensaje("╔══════════════════════╗\n🚨 **OPERATIVO ACTIVO** 🚨\n╚══════════════════════╝", mensaje, 0xff0000, mencion_todo=True)
        await ctx.send("✅ **Operativo activado**", delete_after=5)
        
    elif estado == 'off':
        estados["Operativo"] = "🔴"
        await actualizar_embed()
        
        mensaje = (
            "📢 **Se informa que el operativo ha finalizado con éxito.**\n"
            "👮 **Todas las unidades pueden volver a patrullaje normal.**\n\n"
            "⚠️ **Gracias por la colaboración y el apoyo brindado.**\n\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "🚓 **Policía Argentina RP**\n"
            "━━━━━━━━━━━━━━━━━━"
        )
        await enviar_mensaje("╔══════════════════════╗\n✅ **OPERATIVO FINALIZADO** ✅\n╚══════════════════════╝", mensaje, 0x00ff00, mencion_aqui=True)
        await ctx.send("✅ **Operativo desactivado**", delete_after=5)
        
    else:
        await ctx.send("❌ **Usá:** `/operativo on` o `/operativo off`", delete_after=5)

@bot.command(name='patrullaje')
async def patrullaje(ctx, estado: str = None):
    if not es_admin(ctx):
        if ctx.channel.id != CANAL_COMANDOS_ID:
            await ctx.send(f"❌ **Usá este comando en el canal <#{CANAL_COMANDOS_ID}>**", delete_after=5)
        else:
            await ctx.send("❌ **No tenés permiso para usar este comando.**", delete_after=5)
        return
    
    if estado == 'on':
        estados["Patrullaje"] = "🟢"
        await actualizar_embed()
        
        mensaje = (
            "📢 **Se realizará un patrullaje grupal por toda la ciudad.**\n"
            "👮 **Todas las unidades disponibles deberán unirse y patrullar en conjunto.**\n\n"
            "⚠️ **Manténganse atentos y preparados ante cualquier situación.**\n\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "🚔 **Policía Argentina RP**\n"
            "━━━━━━━━━━━━━━━━━━"
        )
        await enviar_mensaje("╔══════════════════════╗\n🚓 **PATRULLAJE EN CURSO** 🚓\n╚══════════════════════╝", mensaje, 0x00aaff, mencion_todo=True)
        await ctx.send("✅ **Patrullaje activado**", delete_after=5)
        
    elif estado == 'off':
        estados["Patrullaje"] = "🔴"
        await actualizar_embed()
        
        mensaje = (
            "📢 **El patrullaje ha finalizado correctamente.**\n"
            "👮 **Todas las unidades pueden retirarse o volver a servicio normal.**\n\n"
            "⚠️ **Gracias por el compromiso y la participación de todos.**\n\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "🚔 **Policía Argentina RP**\n"
            "━━━━━━━━━━━━━━━━━━"
        )
        await enviar_mensaje("╔══════════════════════╗\n🏁 **PATRULLAJE FINALIZADO** 🏁\n╚══════════════════════╝", mensaje, 0x888888, mencion_aqui=True)
        await ctx.send("✅ **Patrullaje desactivado**", delete_after=5)
        
    else:
        await ctx.send("❌ **Usá:** `/patrullaje on` o `/patrullaje off`", delete_after=5)

@bot.command(name='entrenamiento')
async def entrenamiento(ctx, estado: str = None):
    if not es_admin(ctx):
        if ctx.channel.id != CANAL_COMANDOS_ID:
            await ctx.send(f"❌ **Usá este comando en el canal <#{CANAL_COMANDOS_ID}>**", delete_after=5)
        else:
            await ctx.send("❌ **No tenés permiso para usar este comando.**", delete_after=5)
        return
    
    if estado == 'on':
        estados["Entrenamiento"] = "🟢"
        await actualizar_embed()
        
        mensaje = (
            "📢 **Se realizará un entrenamiento oficial para todas las unidades disponibles.**\n"
            "👮 **Se solicita asistencia y participación obligatoria.**\n\n"
            "⚠️ **El código del servidor estará colocado abajo al momento de comenzar.**\n\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "🚔 **Policía Argentina RP**\n"
            "━━━━━━━━━━━━━━━━━━"
        )
        await enviar_mensaje("╔══════════════════════╗\n🎯 **ENTRENAMIENTO ACTIVO** 🎯\n╚══════════════════════╝", mensaje, 0xffaa00, mencion_todo=True)
        await ctx.send("✅ **Entrenamiento activado**", delete_after=5)
        
    elif estado == 'off':
        estados["Entrenamiento"] = "🔴"
        await actualizar_embed()
        
        mensaje = (
            "📢 **El entrenamiento ha finalizado correctamente.**\n"
            "👮 **Gracias a todas las unidades por participar y colaborar.**\n\n"
            "⚠️ **Continúen atentos y preparados para futuros operativos.**\n\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "🚔 **Policía Argentina RP**\n"
            "━━━━━━━━━━━━━━━━━━"
        )
        await enviar_mensaje("╔══════════════════════╗\n✅ **ENTRENAMIENTO FINALIZADO** ✅\n╚══════════════════════╝", mensaje, 0x00ff00, mencion_aqui=True)
        await ctx.send("✅ **Entrenamiento desactivado**", delete_after=5)
        
    else:
        await ctx.send("❌ **Usá:** `/entrenamiento on` o `/entrenamiento off`", delete_after=5)

@bot.command(name='reuniones')
async def reuniones(ctx, estado: str = None):
    if not es_admin(ctx):
        if ctx.channel.id != CANAL_COMANDOS_ID:
            await ctx.send(f"❌ **Usá este comando en el canal <#{CANAL_COMANDOS_ID}>**", delete_after=5)
        else:
            await ctx.send("❌ **No tenés permiso para usar este comando.**", delete_after=5)
        return
    
    if estado == 'on':
        estados["Reuniones"] = "🟢"
        await actualizar_embed()
        
        mensaje = (
            "📢 **Se solicita la presencia de todas las unidades en la sala de reuniones.**\n"
            "👮 **La asistencia es importante para recibir información e indicaciones.**\n\n"
            "⚠️ **Acudir de inmediato y mantenerse atentos.**\n\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "🚔 **Policía Argentina RP**\n"
            "━━━━━━━━━━━━━━━━━━"
        )
        await enviar_mensaje("╔══════════════════════╗\n📋 **REUNIÓN OFICIAL** 📋\n╚══════════════════════╝", mensaje, 0xaa00ff, mencion_todo=True)
        await ctx.send("✅ **Reunión activada**", delete_after=5)
        
    elif estado == 'off':
        estados["Reuniones"] = "🔴"
        await actualizar_embed()
        
        mensaje = (
            "📢 **La reunión ha concluido correctamente.**\n"
            "👮 **Gracias a todas las unidades por asistir y mantenerse informadas.**\n\n"
            "⚠️ **Pueden regresar a sus actividades y patrullajes habituales.**\n\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "🚔 **Policía Argentina RP**\n"
            "━━━━━━━━━━━━━━━━━━"
        )
        await enviar_mensaje("╔══════════════════════╗\n✅ **REUNIÓN FINALIZADA** ✅\n╚══════════════════════╝", mensaje, 0x00ff00, mencion_aqui=True)
        await ctx.send("✅ **Reunión desactivada**", delete_after=5)
        
    else:
        await ctx.send("❌ **Usá:** `/reuniones on` o `/reuniones off`", delete_after=5)

@bot.command(name='reset')
async def reset(ctx):
    if not es_admin(ctx):
        if ctx.channel.id != CANAL_COMANDOS_ID:
            await ctx.send(f"❌ **Usá este comando en el canal <#{CANAL_COMANDOS_ID}>**", delete_after=5)
        else:
            await ctx.send("❌ **No tenés permiso para usar este comando.**", delete_after=5)
        return
    
    for key in estados:
        estados[key] = "🔴"
    await actualizar_embed()
    await ctx.send("✅ **Todos los estados han sido reiniciados a 🔴**", delete_after=5)

@bot.command(name='ayuda')
async def ayuda(ctx):
    if ctx.channel.id != CANAL_COMANDOS_ID:
        await ctx.send(f"❌ **Usá este comando en el canal <#{CANAL_COMANDOS_ID}>**", delete_after=5)
        return
    
    embed = discord.Embed(
        title="📋 **COMANDOS DISPONIBLES**",
        description="**Solo administradores pueden ejecutar estos comandos:**",
        color=0x00ff00
    )
    embed.add_field(name="🚨 `/operativo on/off`", value="Activa o finaliza el operativo", inline=False)
    embed.add_field(name="🚓 `/patrullaje on/off`", value="Activa o finaliza el patrullaje grupal", inline=False)
    embed.add_field(name="🎯 `/entrenamiento on/off`", value="Activa o finaliza el entrenamiento", inline=False)
    embed.add_field(name="📋 `/reuniones on/off`", value="Activa o finaliza la reunión", inline=False)
    embed.add_field(name="🔄 `/reset`", value="Reinicia todos los estados a 🔴", inline=False)
    embed.set_footer(text="🚔 Policía Argentina RP")
    await ctx.send(embed=embed, delete_after=30)

@bot.event
async def on_ready():
    print(f"✅ {bot.user} está online!")
    await actualizar_embed()

# ⚠️ PONÉ ACÁ TU TOKEN ⚠️
bot.run('MTUwNTc4Nzc1Mjg0OTk5NzkzNQ.GKN18I.xe7yVKDBg18DVkp8c0LvPpRZyXH6jVU0Wm2BPs')
