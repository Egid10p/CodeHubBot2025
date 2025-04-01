import discord
from discord.ext import commands

class Repository(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name="repository", aliases=["repositorio"], help="Muestra el repositorio del bot.")
    async def repository(self, ctx):
        embed = discord.Embed(
                    title="Repositorio del bot de CodeHub",
                    description="https://github.com/Egid10p/CodeHubBot2025",
                    color=discord.Color.red()
                )
        return await ctx.send(embed=embed)
    

async def setup(bot):
    await bot.add_cog(Repository(bot))
