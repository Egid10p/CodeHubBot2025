from discord.ext import commands
import discord
import webserver
import dotenv
import asyncio
import os

dotenv.load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")


intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

async def load_cogs():
    cogs_folder = "./cogs"
    
    for filename in os.listdir(cogs_folder):
        if filename.endswith(".py") and not filename.startswith("__"):
            cog_name = f"cogs.{filename[:-3]}"
            try:
                await bot.load_extension(cog_name)
                print(f"o/ Cog: {cog_name} is Loaded.")
            except Exception as e:
                print(f"Ups... We cannot load this cog {cog_name}: {e}")

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

@commands.command()
async def ping(ctx):
    await ctx.send("pong")

bot.add_command(ping)
    
async def main():
    await load_cogs()
    await bot.start(TOKEN)

webserver.keep_alive()

asyncio.run(main())
