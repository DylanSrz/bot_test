import discord
from discord.ext import commands
import json
import os

XP_POR_MENSAJE = 10
XP_POR_NIVEL   = 100
ARCHIVO_XP     = "xp_data.json"

class Niveles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ── Helpers JSON ───────────────────────────────────
    def cargar_xp(self):
        if os.path.exists(ARCHIVO_XP):
            with open(ARCHIVO_XP, "r") as f:
                return json.load(f)
        return {}

    def guardar_xp(self, data):
        with open(ARCHIVO_XP, "w") as f:
            json.dump(data, f, indent=4)

    # ── Evento: XP por mensaje ─────────────────────────
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        data = self.cargar_xp()
        uid  = str(message.author.id)

        if uid not in data:
            data[uid] = {"xp": 0, "nivel": 1}

        data[uid]["xp"] += XP_POR_MENSAJE
        xp_actual    = data[uid]["xp"]
        nivel_actual = data[uid]["nivel"]

        if xp_actual >= nivel_actual * XP_POR_NIVEL:
            data[uid]["nivel"] += 1
            data[uid]["xp"]     = 0
            await message.channel.send(
                f"🎉 ¡Felicidades {message.author.mention}! Subiste al **nivel {data[uid]['nivel']}** ⭐"
            )

        self.guardar_xp(data)

    # ── Comando: /nivel ────────────────────────────────
    @discord.app_commands.command(name="nivel", description="Muestra tu nivel y XP actual")
    async def nivel(self, interaction: discord.Interaction, usuario: discord.Member = None):
        usuario = usuario or interaction.user
        data    = self.cargar_xp()
        uid     = str(usuario.id)

        if uid not in data:
            await interaction.response.send_message(
                f"**{usuario.display_name}** aún no tiene XP. ¡Empieza a chatear! 💬",
                ephemeral=True
            )
            return

        xp      = data[uid]["xp"]
        nivel   = data[uid]["nivel"]
        xp_next = nivel * XP_POR_NIVEL
        barra   = "🟩" * int((xp / xp_next) * 10) + "⬛" * (10 - int((xp / xp_next) * 10))

        embed = discord.Embed(title=f"⭐ Nivel de {usuario.display_name}", color=discord.Color.gold())
        embed.set_thumbnail(url=usuario.display_avatar.url)
        embed.add_field(name="🏆 Nivel",    value=nivel,                inline=True)
        embed.add_field(name="✨ XP",       value=f"{xp} / {xp_next}", inline=True)
        embed.add_field(name="📊 Progreso", value=barra,                inline=False)
        await interaction.response.send_message(embed=embed)

    # ── Comando: /ranking ──────────────────────────────
    @discord.app_commands.command(name="ranking", description="Muestra el top 5 de usuarios con más nivel")
    async def ranking(self, interaction: discord.Interaction):
        data = self.cargar_xp()

        if not data:
            await interaction.response.send_message("❌ Aún no hay datos de XP.", ephemeral=True)
            return

        ordenado = sorted(data.items(), key=lambda x: (x[1]["nivel"], x[1]["xp"]), reverse=True)[:5]
        medallas = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"]

        embed = discord.Embed(title="🏆 Ranking de Niveles", color=discord.Color.gold())
        for i, (uid, stats) in enumerate(ordenado):
            usuario = interaction.guild.get_member(int(uid))
            nombre  = usuario.display_name if usuario else "Usuario desconocido"
            embed.add_field(
                name=f"{medallas[i]} {nombre}",
                value=f"Nivel **{stats['nivel']}** • {stats['xp']} XP",
                inline=False
            )
        await interaction.response.send_message(embed=embed)

# 🔑 Obligatorio en cada cog
async def setup(bot):
    await bot.add_cog(Niveles(bot))