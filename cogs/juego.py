import discord
from discord.ext import commands
import requests

API_URL_ACACIAS = "https://api.muacacias.net/DiscordStats"  # 👈 Tu URL aquí

class Juego(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ── Función para obtener datos de la API ───────────
    def obtener_datos(self):
        try:
            response = requests.get(API_URL_ACACIAS, timeout=5)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None

    # ── Comando: /estado ───────────────────────────────
    @discord.app_commands.command(name="estado", description="Muestra el estado actual del servidor del juego")
    async def estado(self, interaction: discord.Interaction):
        await interaction.response.defer()

        datos = self.obtener_datos()

        if datos is None:
            await interaction.followup.send("❌ No se pudo conectar con el servidor del juego.")
            return

        embed = discord.Embed(
            title="📊 Estado del Servidor",
            color=discord.Color.green()
        )
        embed.add_field(name="👑 Dueño del CS",     value=datos.get("CsOwner", "N/A"), inline=True)
        embed.add_field(name="🛡️ Guild",            value=datos.get("GuildO",  "N/A"), inline=True)
        embed.add_field(name="🟢 Jugadores Online", value=datos.get("Online",  "N/A"), inline=True)

        await interaction.followup.send(embed=embed)

# 🔑 Obligatorio en cada cog
async def setup(bot):
    await bot.add_cog(Juego(bot))
