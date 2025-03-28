import discord
from discord.ext import commands


class ServerStatistics(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="server_stats", aliases=["estadisticas_servidor"])
    async def server_stats(self, ctx):
        guild = ctx.guild
        total_members = guild.member_count
        online_members = sum(1 for member in guild.members if member.status != discord.Status.offline)
        total_channels = len(guild.channels)
        total_roles = len(guild.roles)

        embed = discord.Embed(title=f"Estadísticas del servidor: {guild.name}", color=discord.Color.red())
        embed.add_field(name="Total de miembros", value=total_members, inline=True)
        embed.add_field(name="Miembros en línea", value=online_members, inline=True)
        embed.add_field(name="Total de canales", value=total_channels, inline=True)
        embed.add_field(name="Total de roles", value=total_roles, inline=True)

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(ServerStatistics(bot))