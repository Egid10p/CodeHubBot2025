import discord
from discord.ext import commands


class Mute(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name="mute", aliases=["silenciar"])
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member: discord.Member, *, reason="No se especificó razón"):
        muted_role = discord.utils.get(ctx.guild.roles, name="Muted")

        if not muted_role:
            muted_role = await ctx.guild.create_role(name="Muted")
            for channel in ctx.guild.text_channels:
                await channel.set_permissions(muted_role, send_messages=False)

        await member.add_roles(muted_role, reason=reason)
        await ctx.send(f"🔇 {member.mention} ha sido silenciado. Razón: {reason}")

    @commands.command(name="unmute", aliases=["desilenciar"])
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, member: discord.Member):
        muted_role = discord.utils.get(ctx.guild.roles, name="Muted")

        if muted_role in member.roles:
            await member.remove_roles(muted_role)
            await ctx.send(f"🔊 {member.mention} ha sido desmuteado.")
        else:
            await ctx.send(f"⚠️ {member.mention} no está muteado.")

    @mute.error
    @unmute.error
    async def mute_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ No tienes permisos para ejecutar este comando.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("⚠️ Menciona a un usuario. Ejemplo: `!mute @usuario`")
        else:
            await ctx.send("⚠️ Ocurrió un error inesperado.")

async def setup(bot):
    await bot.add_cog(Mute(bot))
