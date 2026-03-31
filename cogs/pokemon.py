import discord
from discord.ext import commands
import requests

class Pokemon(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ── Comando: /poke ─────────────────────────────────
    @discord.app_commands.command(name="poke", description="Muestra la imagen de un Pokémon")
    async def poke(self, interaction: discord.Interaction, pokemon: str):
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

# 🔑 Obligatorio en cada cog
async def setup(bot):
    await bot.add_cog(Pokemon(bot))