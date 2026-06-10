import discord,csv,stun
from discord import app_commands
from discord.ext import commands

class DM(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("> dm_cog loaded")
    
    @app_commands.command(name="ip",description="fetches the bot's public ip")
    @app_commands.dm_only()
    @app_commands.describe(command="command to run")
    @app_commands.choices(command=[
        app_commands.Choice(name="global", value="1"),
        app_commands.Choice(name="guilds", value="2"),
        app_commands.Choice(name="clear global", value="3"),
        app_commands.Choice(name="clear guild", value="4"),
        app_commands.Choice(name="copy global to guilds", value="5"),
        ])
    async def ip(self, interaction: discord.Interaction, command: app_commands.Choice[str]):
        admin_ids = []
        with open("data/admins.csv",encoding="utf8") as file:
            for row in csv.DictReader(file,fieldnames=("Name","ID")):
                admin_ids.append(int(row["ID"]))
        if interaction.user.id not in admin_ids:
                await interaction.response.send_message("> You do not have permission to perform this command",ephemeral=True)
                return
        nat_type, external_ip, external_port = stun.get_ip_info()
        await interaction.response.send_message(f"NAT Type:`{nat_type}`\nExternal IP: {external_ip}\nExternal Port: {external_port}")

async def setup(bot):
        await bot.add_cog(DM(bot))