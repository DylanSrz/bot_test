import discord
from discord.ext import commands

class Utilidades(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ── Comando: /userinfo ─────────────────────────────
    @discord.app_commands.command(name="userinfo", description="Muestra información de un usuario")
    async def userinfo(self, interaction: discord.Interaction, usuario: discord.Member = None):
        usuario = usuario or interaction.user
        embed = discord.Embed(title=f"👤 Info de {usuario.display_name}", color=usuario.color)
        embed.set_thumbnail(url=usuario.display_avatar.url)
        embed.add_field(name="🏷️ Usuario",          value=str(usuario),                                           inline=True)
        embed.add_field(name="🆔 ID",                value=usuario.id,                                             inline=True)
        embed.add_field(name="📅 En Discord desde",  value=usuario.created_at.strftime("%d/%m/%Y"),                inline=True)
        embed.add_field(name="📥 En el servidor desde", value=usuario.joined_at.strftime("%d/%m/%Y"),             inline=True)
        embed.add_field(name="🎭 Roles",             value=", ".join([r.name for r in usuario.roles[1:]]) or "Ninguno", inline=False)
        await interaction.response.send_message(embed=embed)

    # ── Comando: /serverinfo ───────────────────────────
    @discord.app_commands.command(name="serverinfo", description="Muestra información del servidor")
    async def serverinfo(self, interaction: discord.Interaction):
        server = interaction.guild
        embed = discord.Embed(title=f"🏰 {server.name}", color=discord.Color.blue())
        if server.icon:
            embed.set_thumbnail(url=server.icon.url)
        embed.add_field(name="👑 Dueño",         value=server.owner.display_name,              inline=True)
        embed.add_field(name="👥 Miembros",       value=server.member_count,                    inline=True)
        embed.add_field(name="💬 Canales",        value=len(server.text_channels),              inline=True)
        embed.add_field(name="🔊 Canales de voz", value=len(server.voice_channels),             inline=True)
        embed.add_field(name="📅 Creado el",      value=server.created_at.strftime("%d/%m/%Y"), inline=True)
        embed.add_field(name="🎭 Roles",          value=len(server.roles),                      inline=True)
        await interaction.response.send_message(embed=embed)

    # ── Comando: /avatar ───────────────────────────────
    @discord.app_commands.command(name="avatar", description="Muestra el avatar de un usuario en grande")
    async def avatar(self, interaction: discord.Interaction, usuario: discord.Member = None):
        usuario = usuario or interaction.user
        embed = discord.Embed(title=f"🖼️ Avatar de {usuario.display_name}", color=discord.Color.blurple())
        embed.set_image(url=usuario.display_avatar.url)
        await interaction.response.send_message(embed=embed)

    # ── Comando: /poll ─────────────────────────────────
    @discord.app_commands.command(name="poll", description="Crea una encuesta rápida")
    async def poll(self, interaction: discord.Interaction, pregunta: str):
        embed = discord.Embed(title=f"📊 {pregunta}", color=discord.Color.gold())
        embed.set_footer(text=f"Encuesta creada por {interaction.user.display_name}")
        await interaction.response.send_message(embed=embed)
        msg = await interaction.original_response()
        await msg.add_reaction("✅")
        await msg.add_reaction("❌")

    # ── Comando: /limpiar ──────────────────────────────
    @discord.app_commands.command(name="limpiar", description="Elimina todos los mensajes del canal")
    async def limpiar(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        await interaction.channel.purge()
        await interaction.followup.send("✅ Mensajes eliminados", ephemeral=True)

# 🔑 Obligatorio en cada cog
async def setup(bot):
    await bot.add_cog(Utilidades(bot))