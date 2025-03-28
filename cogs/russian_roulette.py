import discord
import asyncio
from discord.ext import commands
from utils.roulette_logic import russian_roulette

class RussianRoulette(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name="russian_roulette", aliases=["ruleta"])
    async def roulette(self, ctx):
        game_result = russian_roulette()
        member = ctx.author
        
        muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
        
        if not muted_role:
            muted_role = await ctx.guild.create_role(name="Muted", reason="Rol para ruleta rusa")
            for channel in ctx.guild.channels:
                await channel.set_permissions(muted_role, send_messages=False)
        
        embed = discord.Embed(title="🎰 Ruleta Rusa 🎰", color=discord.Color.red())

        if game_result:
            await member.add_roles(muted_role, reason="Muerte en la ruleta rusa")
            embed.description = f"{member.mention} jaló el gatillo y **¡la bala fue disparada!** 💀"
            embed.color = discord.Color.dark_red()
            await ctx.send(embed=embed)

            await asyncio.sleep(300)

            await member.remove_roles(muted_role, reason="Timeout terminado")
            embed.description = f"{member.mention} ha revivido. El rol 'Muted' ha sido removido. ✅"
            embed.color = discord.Color.green()
            await ctx.send(embed=embed)
        else:
            embed.description = f"{member.mention} jaló el gatillo y **no pasó nada...** 😌"
            embed.color = discord.Color.green()
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(RussianRoulette(bot))
