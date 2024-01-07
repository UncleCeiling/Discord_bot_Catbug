import discord
from discord import app_commands
from discord.ext import commands

class Shell(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("> shell_cog loaded")
    
    @app_commands.command(name="shell",description="Summon a shell into Catbug's hardware.")
    @app_commands.describe(visible="Make output visible in channel?")
    async def shell(self, interaction: discord.Interaction, visible: bool = False):
        await interaction.response.send_message(f"> WIP - Sorry!",ephemeral=(not visible))

async def setup(bot):
        await bot.add_cog(Shell(bot))