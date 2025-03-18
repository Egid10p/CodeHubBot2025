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
        
        if game_result:
            await member.add_roles(muted_role, reason="Muerte en la ruleta rusa")
            await ctx.send(f"El usuario {member.mention} ha jalado el gatillo y la bala ha sido disparada, causando su timeout.")
            
            
            await asyncio.sleep(300)

            await member.remove_roles(muted_role, reason="Timeout terminado")
            await ctx.send(f"El timeout de {member.mention} ha terminado, el rol 'Muted' ha sido removido.")
        else:
            await ctx.send(f"El usuario {member.mention} ha jalado el gatillo y la bala no ha sido disparada.")

async def setup(bot):
    await bot.add_cog(RussianRoulette(bot))
