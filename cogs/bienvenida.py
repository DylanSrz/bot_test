import discord
from discord.ext import commands

CANAL_BIENVENIDA_ID = 1458690214053810310  # 👈 Reemplaza con el ID de tu canal de bienvenida

class Bienvenida(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ── Evento: nuevo miembro ──────────────────────────
    @commands.Cog.listener()
    async def on_member_join(self, member):

        # ── Mensaje en canal ───────────────────────────
        canal = self.bot.get_channel(CANAL_BIENVENIDA_ID)
        if canal:
            embed = discord.Embed(
                title=f"👋 ¡Bienvenido/a, {member.display_name}!",
                description=f"Eres el miembro número **{member.guild.member_count}** de **{member.guild.name}**.\n¡Esperamos que disfrutes tu estadía!",
                color=discord.Color.green()
            )
            embed.set_thumbnail(url=member.display_avatar.url)
            embed.set_footer(text=f"Únete: {member.joined_at.strftime('%d/%m/%Y')}")
            await canal.send(embed=embed)

        # ── Mensaje privado al nuevo miembro ───────────
        try:
            embed_dm = discord.Embed(
                title=f"👋 ¡Hola, {member.display_name}!",
                description=f"Bienvenido/a a **{member.guild.name}**.\n¡Esperamos que la pases genial! 🎉",
                color=discord.Color.blurple()
            )
            await member.send(embed=embed_dm)
        except discord.Forbidden:
            pass  # El usuario tiene los DMs desactivados

# 🔑 Obligatorio en cada cog
async def setup(bot):
    await bot.add_cog(Bienvenida(bot))
