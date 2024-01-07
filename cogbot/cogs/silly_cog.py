import discord
from discord import app_commands
from discord.ext import commands
from typing import Optional

class Silly(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("> silly_cog loaded")
    
    @app_commands.command(name="member",description="( ͡° ͜ʖ ͡°)")
    @app_commands.describe(member="The user you want to check.",visible="Make output visible in channel?")
    async def phallus(self, interaction: discord.Interaction, member: Optional[discord.Member], visible: bool = False):
        if isinstance(interaction.user,discord.Member):
            member = member or interaction.user
        else:
            await interaction.response.send_message("> Error - member does not exist",ephemeral=not visible)
            return
        length = (int(member.id) % 11) + 1
        await interaction.response.send_message(f">>> {member.mention}:\n8"+"=".center(length,"=")+"D",ephemeral=not visible)

async def setup(bot):
        await bot.add_cog(Silly(bot))