import discord
import random
import asyncio
from discord.ext import commands

class GuessNumber(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="guess_number", aliases=["adivinar"])
    async def guess(self, ctx):
        number = random.randint(1, 100)
        max_attempts = 10
        attempts = 0

        embed = discord.Embed(
            title="🎯 Adivina el número",
            description="¡Intenta adivinar el número entre **1 y 100**!\nTienes **10 intentos** y **5 segundos** por intento.",
            color=discord.Color.blue()
        )
        embed.set_footer(text="Escribe un número en el chat para jugar.")
        await ctx.send(embed=embed)

        while attempts < max_attempts:
            attempts += 1

            embed = discord.Embed(
                title=f"Intento {attempts}/{max_attempts} ⏳",
                description="Tienes **5 segundos** para responder.",
                color=discord.Color.orange()
            )
            await ctx.send(embed=embed)

            def check(m):
                return m.author == ctx.author and m.channel == ctx.channel and m.content.isdigit()

            try:
                msg = await self.bot.wait_for("message", check=check, timeout=5.0)
                guess = int(msg.content)

                if guess == number:
                    embed = discord.Embed(
                        title="🎉 ¡Correcto!",
                        description=f"¡Felicidades {ctx.author.mention}, adivinaste el número! 🎯",
                        color=discord.Color.green()
                    )
                    return await ctx.send(embed=embed)
                elif guess < number:
                    hint = "El número es **MAYOR** 🔼"
                else:
                    hint = "El número es **MENOR** 🔽"

                embed = discord.Embed(
                    title="❌ Incorrecto",
                    description=f"{hint} | Intentos restantes: **{max_attempts - attempts}**",
                    color=discord.Color.red()
                )
                await ctx.send(embed=embed)

            except asyncio.TimeoutError:
                embed = discord.Embed(
                    title="⏳ ¡Se acabó el tiempo!",
                    description=f"No respondiste a tiempo. El número era **{number}**.",
                    color=discord.Color.red()
                )
                return await ctx.send(embed=embed)

        embed = discord.Embed(
            title="❌ ¡Te quedaste sin intentos!",
            description=f"El número era **{number}**. ¡Mejor suerte la próxima vez! 🎲",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(GuessNumber(bot))
