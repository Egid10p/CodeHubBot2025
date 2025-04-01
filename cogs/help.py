import discord
from discord.ext import commands

class HelpCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help", help="Muestra la lista de comandos disponibles.")
    async def help_command(self, ctx, command_name: str = None):
        if command_name:
            # Buscar información específica de un comando
            command = self.bot.get_command(command_name)
            if command:
                embed = discord.Embed(
                    title=f"Comando: {command.name}",
                    description=command.help or "No hay descripción disponible.",
                    color=discord.Color.blue()
                )
                await ctx.send(embed=embed)
            else:
                await ctx.send(f"❌ No se encontró el comando `{command_name}`.")
        else:
            # Mostrar lista de comandos organizados por cogs
            embed = discord.Embed(
                title="Lista de Comandos",
                description="Aquí tienes todos los comandos disponibles en el bot.",
                color=discord.Color.blue()
            )

            for cog in self.bot.cogs:
                commands_list = [f"`{cmd.name}` - {cmd.help}" for cmd in self.bot.get_cog(cog).walk_commands()]
                if commands_list:
                    embed.add_field(name=f"📌 {cog}", value="\n".join(commands_list), inline=False)

            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(HelpCommand(bot))
