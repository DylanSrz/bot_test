import discord
from discord.ext import commands
import requests
import random

class Diversion(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ── Comando: /meme ─────────────────────────────────
    @discord.app_commands.command(name="meme", description="Trae un meme aleatorio")
    async def meme(self, interaction: discord.Interaction):
        await interaction.response.defer()
        subs = ["memes", "dankmemes", "LatinoPeopleTwitter"]
        sub = random.choice(subs)
        result = requests.get(f"https://meme-api.com/gimme/{sub}")
        data = result.json()
        embed = discord.Embed(title=data["title"], color=discord.Color.orange())
        embed.set_image(url=data["url"])
        embed.set_footer(text=f"👍 {data['ups']} | r/{data['subreddit']}")
        await interaction.followup.send(embed=embed)

    # ── Comando: /chiste ───────────────────────────────
    @discord.app_commands.command(name="chiste", description="Cuenta un chiste aleatorio")
    async def chiste(self, interaction: discord.Interaction):
        chistes = [
            "¿Qué le dice un bit al otro? ... Nos vemos en el bus 🚌",
            "¿Por qué los programadores confunden Halloween con Navidad? Porque Oct 31 = Dec 25 🎃",
            "¿Cómo se despide un químico? Ácido un placer conocerte 🧪",
            "¿Qué hace una abeja en el gimnasio? ¡Zum-ba! 🐝",
            "¿Por qué el libro de matemáticas estaba triste? Tenía demasiados problemas 📚",
            "¿Qué le dijo el 0 al 8? Lindo cinturón 🤣",
        ]
        await interaction.response.send_message(f"😂 {random.choice(chistes)}")

    # ── Comando: /dado ─────────────────────────────────
    @discord.app_commands.command(name="dado", description="Tira un dado de 6 caras")
    async def dado(self, interaction: discord.Interaction):
        resultado = random.randint(1, 6)
        caras = {1: "1️⃣", 2: "2️⃣", 3: "3️⃣", 4: "4️⃣", 5: "5️⃣", 6: "6️⃣"}
        await interaction.response.send_message(f"🎲 ¡Tiraste el dado y salió: {caras[resultado]}!")

    # ── Comando: /coinflip ─────────────────────────────
    @discord.app_commands.command(name="coinflip", description="Lanza una moneda: cara o cruz")
    async def coinflip(self, interaction: discord.Interaction):
        resultado = random.choice(["🪙 ¡CARA!", "🪙 ¡CRUZ!"])
        await interaction.response.send_message(resultado)

    # ── Comando: /8ball ────────────────────────────────
    @discord.app_commands.command(name="ball8", description="Hazle una pregunta a la bola mágica")
    async def ball8(self, interaction: discord.Interaction, pregunta: str):
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
        embed.add_field(name="❓ Pregunta",  value=pregunta,                    inline=False)
        embed.add_field(name="🔮 Respuesta", value=random.choice(respuestas),   inline=False)
        await interaction.response.send_message(embed=embed)

    # ── Comando: /trivia ───────────────────────────────
    @discord.app_commands.command(name="trivia", description="Responde una pregunta de trivia")
    async def trivia(self, interaction: discord.Interaction):
        await interaction.response.defer()
        result = requests.get("https://opentdb.com/api.php?amount=1&type=multiple")
        data = result.json()["results"][0]

        pregunta    = data["question"]
        correcta    = data["correct_answer"]
        incorrectas = data["incorrect_answers"]

        opciones = incorrectas + [correcta]
        random.shuffle(opciones)

        letras        = ["🇦", "🇧", "🇨", "🇩"]
        opciones_texto = "\n".join([f"{letras[i]} {opciones[i]}" for i in range(len(opciones))])
        letra_correcta = letras[opciones.index(correcta)]

        embed = discord.Embed(title="🧠 Trivia", description=pregunta, color=discord.Color.teal())
        embed.add_field(name="Opciones", value=opciones_texto, inline=False)
        embed.set_footer(text="Tienes 15 segundos para responder...")
        await interaction.followup.send(embed=embed)

        def check(m):
            return m.author == interaction.user and m.channel == interaction.channel

        try:
            msg = await self.bot.wait_for("message", timeout=15.0, check=check)
            if msg.content.upper() in letra_correcta:
                await interaction.channel.send(f"✅ ¡Correcto {interaction.user.mention}! La respuesta era {letra_correcta} **{correcta}**")
            else:
                await interaction.channel.send(f"❌ ¡Incorrecto {interaction.user.mention}! La respuesta era {letra_correcta} **{correcta}**")
        except TimeoutError:
            await interaction.channel.send(f"⏰ ¡Tiempo! {interaction.user.mention} La respuesta era {letra_correcta} **{correcta}**")

# 🔑 Obligatorio en cada cog
async def setup(bot):
    await bot.add_cog(Diversion(bot))