import discord,csv,stun
from discord import app_commands
from discord.ext import commands
from modules.tools import is_admin

class DM(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("> dm_cog loaded")
    
    @app_commands.command(name="ip",description="Fetches the bot's public ip.")
    @app_commands.dm_only()
    async def ip(self, interaction: discord.Interaction):
        if not is_admin(interaction.user.id):
            print(f"> {interaction.user.name} tried to run `ip`.")
            await interaction.response.send_message("> You do not have permission to perform this command.",ephemeral=False)
            return
        if interaction.guild:
            print(f"> {interaction.user.name} ran `ip`.")
            await interaction.response.send_message("> This command can only used in DMs.",ephemeral=True)
            return
        nat_type, external_ip, external_port = stun.get_ip_info()
        await interaction.response.send_message(f"NAT Type:`{nat_type}`\nExternal IP: {external_ip}\nExternal Port: {external_port}",ephemeral=True)

    @app_commands.command(name="reboot",description="Reboots the bot.")
    @app_commands.dm_only()
    async def reboot(self, interaction: discord.Interaction):
        print(f"> {interaction.user.name} tried to run `reboot`.")
        if not is_admin(interaction.user.id):
            await interaction.response.send_message("> You do not have permission to perform this command.",ephemeral=False)
            return
        print(f"> {interaction.user.name} ran `reboot`.")
        if interaction.guild:
            await interaction.response.send_message("> This command can only used in DMs.",ephemeral=True)
            return
        message = "> ⏳ Initiating shutdown..."
        await interaction.response.send_message(message,ephemeral=True)
        # message += "\n\n> 🪝 Running `git pull`..."
        # await interaction.edit_original_response(content=message)
        # output = subprocess.run(["git","pull"],stdout=subprocess.PIPE).stdout.decode("utf-8").replace("Fast-forward","FastForward").replace("+","🟢").replace("-","🔴").replace("Already up to date.","Already up to date. ✅").replace("\n","\n> ")
        # message += f"\n\n> 🗒️ Output:\n> {output}"
        # await interaction.edit_original_response(content=message)
        message += "\n\n> 🚪 Logging off..."
        await interaction.edit_original_response(content=message)
        await self.bot.change_presence(status=discord.Status.offline,activity=None)
        message += "\n\n> 🔄 Rebooting..."
        await interaction.edit_original_response(content=message)
        exit(0)

async def setup(bot):
        await bot.add_cog(DM(bot))