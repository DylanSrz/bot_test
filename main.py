import os
import discord
from discord.ext import commands
import requests
from dotenv import load_dotenv # token del bot
import random  # Agregar este import arriba del todos

load_dotenv()
TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = discord.ext.commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree  # Árbol de slash commands

# ── Función para obtener datos de la API de acacias ───────────────

API_URL_ACACIAS = "https://api.muacacias.net/DiscordStats"

def obtener_datos():
    try:
        response = requests.get(API_URL_ACACIAS, timeout=5)
        response.raise_for_status()
        return response.json()
    except Exception:
        return None
    

# ── Comando: /estado ───────────────────────────────────
@tree.command(name="estado", description="Muestra el estado actual del servidor del juego")
async def estado(interaction: discord.Interaction):
    await interaction.response.defer()  # Evita timeout si la API tarda

    datos = obtener_datos()

    if datos is None:
        await interaction.followup.send("❌ No se pudo conectar con el servidor del juego.")
        return

    embed = discord.Embed(
        title="📊 Estado del servidor Mu Acacias",
        color=discord.Color.green()
    )
    embed.add_field(name="👑 Dueño del CS",      value=datos.get("CsOwner", "N/A"), inline=True)
    embed.add_field(name="🛡️ Master Guild",      value=datos.get("GuildO",  "N/A"), inline=True)
    embed.add_field(name="🟢 Jugadores Online",  value=datos.get("Online",  "N/A"), inline=True)

    await interaction.followup.send(embed=embed)

# ── Función para obtener datos de la API de pokemon ───────────────
# ── Comando: /poke ─────────────────────────────────────
@tree.command(name="poke", description="Muestra la imagen de un Pokémon")
async def poke(interaction: discord.Interaction, pokemon: str):
    await interaction.response.defer()
    try:
        nombre = pokemon.strip().lower()
        result = requests.get("https://pokeapi.co/api/v2/pokemon/" + nombre)

        if result.status_code == 404:
            await interaction.followup.send("❌ Pokémon no encontrado.")
            return

        image_url = result.json()['sprites']['front_default']

        embed = discord.Embed(
            title=f"🎮 {nombre.capitalize()}",
            color=discord.Color.red()
        )
        embed.set_image(url=image_url)
        await interaction.followup.send(embed=embed)

    except Exception as e:
        print("Error:", e)
        await interaction.followup.send("❌ Ocurrió un error al buscar el Pokémon.")

# ── Comando: /limpiar ──────────────────────────────────
@tree.command(name="limpiar", description="Elimina todos los mensajes del canal")
async def limpiar(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)  # Solo lo ve quien ejecuta el comando
    await interaction.channel.purge()
    await interaction.followup.send("✅ Mensajes eliminados", ephemeral=True)



# ════════════════════════════════════════════
#           UTILIDADES DEL SERVIDOR
# ════════════════════════════════════════════

# ── Comando: /userinfo ─────────────────────
@tree.command(name="userinfo", description="Muestra información de un usuario")
async def userinfo(interaction: discord.Interaction, usuario: discord.Member = None):
    usuario = usuario or interaction.user  # Si no pasan usuario, muestra el propio
    embed = discord.Embed(title=f"👤 Info de {usuario.display_name}", color=usuario.color)
    embed.set_thumbnail(url=usuario.display_avatar.url)
    embed.add_field(name="🏷️ Usuario",       value=str(usuario),                                          inline=True)
    embed.add_field(name="🆔 ID",             value=usuario.id,                                            inline=True)
    embed.add_field(name="📅 En Discord desde", value=usuario.created_at.strftime("%d/%m/%Y"),             inline=True)
    embed.add_field(name="📥 En el servidor desde", value=usuario.joined_at.strftime("%d/%m/%Y"),          inline=True)
    embed.add_field(name="🎭 Roles",          value=", ".join([r.name for r in usuario.roles[1:]]) or "Ninguno", inline=False)
    await interaction.response.send_message(embed=embed)

# ── Comando: /serverinfo ───────────────────
@tree.command(name="serverinfo", description="Muestra información del servidor")
async def serverinfo(interaction: discord.Interaction):
    server = interaction.guild
    embed = discord.Embed(title=f"🏰 {server.name}", color=discord.Color.blue())
    if server.icon:
        embed.set_thumbnail(url=server.icon.url)
    embed.add_field(name="👑 Dueño",          value=server.owner.display_name,                  inline=True)
    embed.add_field(name="👥 Miembros",        value=server.member_count,                        inline=True)
    embed.add_field(name="💬 Canales",         value=len(server.text_channels),                  inline=True)
    embed.add_field(name="🔊 Canales de voz",  value=len(server.voice_channels),                 inline=True)
    embed.add_field(name="📅 Creado el",       value=server.created_at.strftime("%d/%m/%Y"),     inline=True)
    embed.add_field(name="🎭 Roles",           value=len(server.roles),                          inline=True)
    await interaction.response.send_message(embed=embed)

# ── Comando: /avatar ───────────────────────
@tree.command(name="avatar", description="Muestra el avatar de un usuario en grande")
async def avatar(interaction: discord.Interaction, usuario: discord.Member = None):
    usuario = usuario or interaction.user
    embed = discord.Embed(title=f"🖼️ Avatar de {usuario.display_name}", color=discord.Color.blurple())
    embed.set_image(url=usuario.display_avatar.url)
    await interaction.response.send_message(embed=embed)

# ── Comando: /poll ─────────────────────────
@tree.command(name="poll", description="Crea una encuesta rápida")
async def poll(interaction: discord.Interaction, pregunta: str):
    embed = discord.Embed(title=f"📊 {pregunta}", color=discord.Color.gold())
    embed.set_footer(text=f"Encuesta creada por {interaction.user.display_name}")
    message = await interaction.response.send_message(embed=embed)
    msg = await interaction.original_response()
    await msg.add_reaction("✅")
    await msg.add_reaction("❌")


# ════════════════════════════════════════════
#          DIVERSIÓN / ENTRETENIMIENTO
# ════════════════════════════════════════════

# ── Comando: /meme ─────────────────────────
@tree.command(name="meme", description="Trae un meme aleatorio")
async def meme(interaction: discord.Interaction):
    await interaction.response.defer()
    subs = ["memes", "dankmemes", "LatinoPeopleTwitter"]
    sub = random.choice(subs)
    result = requests.get(f"https://meme-api.com/gimme/{sub}")
    data = result.json()
    embed = discord.Embed(title=data["title"], color=discord.Color.orange())
    embed.set_image(url=data["url"])
    embed.set_footer(text=f"👍 {data['ups']} | r/{data['subreddit']}")
    await interaction.followup.send(embed=embed)

# ── Comando: /chiste ───────────────────────
@tree.command(name="chiste", description="Cuenta un chiste aleatorio")
async def chiste(interaction: discord.Interaction):
    chistes = [
        "¿Qué le dice un bit al otro? ... Nos vemos en el bus 🚌",
        "¿Por qué los programadores confunden Halloween con Navidad? Porque Oct 31 = Dec 25 🎃",
        "¿Cómo se despide un químico? Ácido un placer conocerte 🧪",
        "¿Qué hace una abeja en el gimnasio? ¡Zum-ba! 🐝",
        "¿Por qué el libro de matemáticas estaba triste? Tenía demasiados problemas 📚",
        "¿Qué le dijo el 0 al 8? Lindo cinturón 🤣",
    ]
    await interaction.response.send_message(f"😂 {random.choice(chistes)}")

# ── Comando: /dado ─────────────────────────
@tree.command(name="dado", description="Tira un dado de 6 caras")
async def dado(interaction: discord.Interaction):
    resultado = random.randint(1, 6)
    caras = {1: "1️⃣", 2: "2️⃣", 3: "3️⃣", 4: "4️⃣", 5: "5️⃣", 6: "6️⃣"}
    await interaction.response.send_message(f"🎲 ¡Tiraste el dado y salió: {caras[resultado]}!")

# ── Comando: /coinflip ─────────────────────
@tree.command(name="coinflip", description="Lanza una moneda: cara o cruz")
async def coinflip(interaction: discord.Interaction):
    resultado = random.choice(["🪙 ¡CARA!", "🪙 ¡CRUZ!"])
    await interaction.response.send_message(resultado)

# ── Comando: /8ball ────────────────────────
@tree.command(name="8ball", description="Hazle una pregunta a la bola mágica")
async def ball8(interaction: discord.Interaction, pregunta: str):
    respuestas = [
        "✅ Sí, definitivamente.",
        "✅ Todo apunta a que sí.",
        "✅ Sin duda alguna.",
        "🤔 Pregunta de nuevo más tarde.",
        "🤔 No puedo predecirlo ahora.",
        "🤔 Mejor no te digo...",
        "❌ No cuentes con ello.",
        "❌ La respuesta es no.",
        "❌ Mis fuentes dicen que no.",
    ]
    embed = discord.Embed(title="🎱 Bola Mágica", color=discord.Color.dark_purple())
    embed.add_field(name="❓ Pregunta", value=pregunta,                    inline=False)
    embed.add_field(name="🔮 Respuesta", value=random.choice(respuestas), inline=False)
    await interaction.response.send_message(embed=embed)


# ── Comando: /trivia ───────────────────────
@tree.command(name="trivia", description="Responde una pregunta de trivia")
async def trivia(interaction: discord.Interaction):
    await interaction.response.defer()

    result = requests.get("https://opentdb.com/api.php?amount=1&type=multiple&lang=es")
    data = result.json()["results"][0]

    pregunta = data["question"]
    correcta = data["correct_answer"]
    incorrectas = data["incorrect_answers"]

    # Mezclar opciones
    opciones = incorrectas + [correcta]
    random.shuffle(opciones)

    letras = ["🇦", "🇧", "🇨", "🇩"]
    opciones_texto = "\n".join([f"{letras[i]} {opciones[i]}" for i in range(len(opciones))])
    letra_correcta = letras[opciones.index(correcta)]

    embed = discord.Embed(title="🧠 Trivia", description=pregunta, color=discord.Color.teal())
    embed.add_field(name="Opciones", value=opciones_texto, inline=False)
    embed.set_footer(text="Tienes 15 segundos para responder...")

    await interaction.followup.send(embed=embed)

    # Esperar respuesta del usuario
    def check(m):
        return m.author == interaction.user and m.channel == interaction.channel

    try:
        msg = await bot.wait_for("message", timeout=15.0, check=check)
        if msg.content.upper() in letra_correcta:
            await interaction.channel.send(f"✅ ¡Correcto {interaction.user.mention}! La respuesta era {letra_correcta} **{correcta}**")
        else:
            await interaction.channel.send(f"❌ ¡Incorrecto {interaction.user.mention}! La respuesta era {letra_correcta} **{correcta}**")

    except TimeoutError:
        await interaction.channel.send(f"⏰ ¡Tiempo! {interaction.user.mention} La respuesta era {letra_correcta} **{correcta}**")


# ── Evento: bot conectado ──────────────────────────────
@bot.event
async def on_ready():
    await tree.sync()  # 🔑 Registra los slash commands en Discord
    print(f"✅ Bot conectado como {bot.user}")
    print("✅ Slash commands sincronizados")

bot.run(TOKEN)