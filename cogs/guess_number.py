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
        await ctx.send("¡Adivina el número entre 1 y 100! Tienes 10 intentos y 5 segundos por intento.")

        attempts = 0
        max_attempts = 10

        while attempts < max_attempts:
            attempts += 1
            await ctx.send(f"Intento {attempts}/{max_attempts}. Tienes 5 segundos para adivinar.")

            def check(m):
                return m.author == ctx.author and m.channel == ctx.channel and m.content.isdigit()

            try:
                msg = await self.bot.wait_for("message", check=check, timeout=5.0) 
                guess = int(msg.content)

                if guess == number:
                    await ctx.send("¡Correcto! Adivinaste el número. 🎉")
                    return
                elif guess < number:
                    await ctx.send("El número es MAS MAYOR. ¡Intenta de nuevo!")
                else:
                    await ctx.send("El número es MENOR. ¡Intenta de nuevo!")

            except asyncio.TimeoutError:
                await ctx.send(f"⏳ ¡Se acabó el tiempo! El número era {number}.")
                return

        await ctx.send(f"¡Te quedaste sin intentos! El número era {number}.")

async def setup(bot):
    await bot.add_cog(GuessNumber(bot))