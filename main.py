import discord
from discord.ext import commands
import asyncio
import os
from dotenv import load_dotenv # token del bot

load_dotenv()
TOKEN = os.getenv("TOKEN")

# ── Setup del bot ──────────────────────────────────────
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ── Cargar todos los cogs automáticamente ─────────────
async def cargar_cogs():
    for archivo in os.listdir("./cogs"):
        if archivo.endswith(".py"):
            nombre = archivo[:-3]  # Quita el .py
            await bot.load_extension(f"cogs.{nombre}")
            print(f"✅ Cog cargado: {nombre}")

# ── Evento: bot conectado ──────────────────────────────
@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"✅ Bot conectado como {bot.user}")
    print("✅ Slash commands sincronizados")

# ── Arrancar todo ──────────────────────────────────────
async def main():
    async with bot:
        await cargar_cogs()
        await bot.start(TOKEN)

asyncio.run(main())