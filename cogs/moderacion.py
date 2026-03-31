import discord
from discord.ext import commands
from datetime import timedelta

advertencias = {}  # Diccionario para guardar warns en memoria

class Moderacion(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ── Comando: /kick ─────────────────────────────────
    @discord.app_commands.command(name="kick", description="Expulsa a un usuario del servidor")
    @discord.app_commands.checks.has_permissions(kick_members=True)
    async def kick(self, interaction: discord.Interaction, usuario: discord.Member, razon: str = "Sin razón especificada"):
        await usuario.kick(reason=razon)
        embed = discord.Embed(title="👢 Usuario Expulsado", color=discord.Color.orange())
        embed.add_field(name="👤 Usuario", value=usuario.display_name,          inline=True)
        embed.add_field(name="📋 Razón",   value=razon,                         inline=True)
        embed.add_field(name="🛡️ Por",     value=interaction.user.display_name, inline=True)
        await interaction.response.send_message(embed=embed)

    @kick.error
    async def kick_error(self, interaction: discord.Interaction, error):
        await interaction.response.send_message("❌ No tienes permisos para expulsar usuarios.", ephemeral=True)

    # ── Comando: /ban ──────────────────────────────────
    @discord.app_commands.command(name="ban", description="Banea a un usuario del servidor")
    @discord.app_commands.checks.has_permissions(ban_members=True)
    async def ban(self, interaction: discord.Interaction, usuario: discord.Member, razon: str = "Sin razón especificada"):
        await usuario.ban(reason=razon)
        embed = discord.Embed(title="🔨 Usuario Baneado", color=discord.Color.red())
        embed.add_field(name="👤 Usuario", value=usuario.display_name,          inline=True)
        embed.add_field(name="📋 Razón",   value=razon,                         inline=True)
        embed.add_field(name="🛡️ Por",     value=interaction.user.display_name, inline=True)
        await interaction.response.send_message(embed=embed)

    @ban.error
    async def ban_error(self, interaction: discord.Interaction, error):
        await interaction.response.send_message("❌ No tienes permisos para banear usuarios.", ephemeral=True)

    # ── Comando: /mute ─────────────────────────────────
    @discord.app_commands.command(name="mute", description="Silencia a un usuario temporalmente (en minutos)")
    @discord.app_commands.checks.has_permissions(moderate_members=True)
    async def mute(self, interaction: discord.Interaction, usuario: discord.Member, minutos: int, razon: str = "Sin razón especificada"):
        duracion = timedelta(minutes=minutos)
        await usuario.timeout(duracion, reason=razon)
        embed = discord.Embed(title="🔇 Usuario Silenciado", color=discord.Color.yellow())
        embed.add_field(name="👤 Usuario",  value=usuario.display_name,          inline=True)
        embed.add_field(name="⏱️ Duración", value=f"{minutos} minutos",          inline=True)
        embed.add_field(name="📋 Razón",    value=razon,                         inline=True)
        embed.add_field(name="🛡️ Por",      value=interaction.user.display_name, inline=True)
        await interaction.response.send_message(embed=embed)

    @mute.error
    async def mute_error(self, interaction: discord.Interaction, error):
        await interaction.response.send_message("❌ No tienes permisos para silenciar usuarios.", ephemeral=True)

    # ── Comando: /warn ─────────────────────────────────
    @discord.app_commands.command(name="warn", description="Advierte a un usuario")
    @discord.app_commands.checks.has_permissions(kick_members=True)
    async def warn(self, interaction: discord.Interaction, usuario: discord.Member, razon: str):
        uid = str(usuario.id)
        if uid not in advertencias:
            advertencias[uid] = []
        advertencias[uid].append(razon)
        total = len(advertencias[uid])

        embed = discord.Embed(title="⚠️ Advertencia", color=discord.Color.yellow())
        embed.add_field(name="👤 Usuario",        value=usuario.display_name,          inline=True)
        embed.add_field(name="📋 Razón",          value=razon,                         inline=True)
        embed.add_field(name="🛡️ Por",            value=interaction.user.display_name, inline=True)
        embed.add_field(name="⚠️ Total de warns", value=f"{total}/3",                  inline=True)
        await interaction.response.send_message(embed=embed)

        if total >= 3:
            await usuario.kick(reason="3 advertencias acumuladas")
            await interaction.channel.send(f"👢 {usuario.mention} fue expulsado por acumular 3 advertencias.")
            advertencias[uid] = []

    @warn.error
    async def warn_error(self, interaction: discord.Interaction, error):
        await interaction.response.send_message("❌ No tienes permisos para advertir usuarios.", ephemeral=True)

# 🔑 Obligatorio en cada cog
async def setup(bot):
    await bot.add_cog(Moderacion(bot))