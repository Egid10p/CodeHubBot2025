import discord
from discord.ext import commands

class Mute(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="mute", aliases=["silenciar"], help="Silencia a un usuario en el servidor. Uso unico de administradores.")
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member: discord.Member, *, reason="No se especificó razón"):
        muted_role = discord.utils.get(ctx.guild.roles, name="Muted")

        if not muted_role:
            try:
                muted_role = await ctx.guild.create_role(name="Muted", reason="Rol de mute")
                for channel in ctx.guild.text_channels:
                    await channel.set_permissions(muted_role, send_messages=False)
            except discord.Forbidden:
                embed = discord.Embed(
                    title="❌ Error",
                    description="No tengo permisos para crear el rol de mute.",
                    color=discord.Color.red()
                )
                return await ctx.send(embed=embed)

        await member.add_roles(muted_role, reason=reason)

        embed = discord.Embed(
            title="🔇 Usuario silenciado",
            description=f"**{member.mention} ha sido silenciado.**",
            color=discord.Color.dark_red()
        )
        embed.add_field(name="Razón", value=reason, inline=False)
        embed.set_thumbnail(url=member.avatar.url if member.avatar else ctx.guild.icon.url)
        
        await ctx.send(embed=embed)

    @commands.command(name="unmute", aliases=["desilenciar"])
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, member: discord.Member):
        muted_role = discord.utils.get(ctx.guild.roles, name="Muted")

        if muted_role in member.roles:
            await member.remove_roles(muted_role)

            embed = discord.Embed(
                title="🔊 Usuario desmuteado",
                description=f"**{member.mention} ha sido desmuteado.**",
                color=discord.Color.green()
            )
            embed.set_thumbnail(url=member.avatar.url if member.avatar else ctx.guild.icon.url)

            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="⚠️ Error",
                description=f"{member.mention} **no está muteado.**",
                color=discord.Color.orange()
            )
            await ctx.send(embed=embed)

    @mute.error
    @unmute.error
    async def mute_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title="❌ Permiso denegado",
                description="No tienes permisos para ejecutar este comando.",
                color=discord.Color.red()
            )
        elif isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                title="⚠️ Uso incorrecto",
                description="Debes mencionar a un usuario.\nEjemplo: `!mute @usuario`",
                color=discord.Color.orange()
            )
        else:
            embed = discord.Embed(
                title="⚠️ Error inesperado",
                description="Ha ocurrido un error. Inténtalo de nuevo.",
                color=discord.Color.red()
            )
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Mute(bot))
