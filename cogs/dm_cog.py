from aiostun import constants
import discord,aiostun
from discord import app_commands
from discord.ext import commands
from modules.tools import is_admin

class DM(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("> dm_cog loaded")
    
    @app_commands.command(name="ip",description="Fetches the bot's ip.")
    async def ip(self, interaction: discord.Interaction):
        if not is_admin(interaction.user.id):
            print(f"> {interaction.user.name} tried to run `ip`.")
            await interaction.response.send_message("> You do not have permission to perform this command.",ephemeral=False)
            return False
        if interaction.guild != None:
            print(f"> {interaction.user.name} ran `ip`.")
            await interaction.response.send_message("> This command can only used in DMs.",ephemeral=True)
            return False
        message = "> Fetching IP..."
        await interaction.response.send_message(content=message,ephemeral=True)
        STUN_HOST = "stun.stunprotocol.org"
        STUN_PORT = 3478
        async with aiostun.Client(host=STUN_HOST,port=STUN_PORT) as stun_client:
            mapped_address = await stun_client.get_mapped_address()
        if mapped_address == None:
            await interaction.edit_original_response(content="> Something went wrong...")
            return False
        ip = mapped_address["ip"]
        await interaction.edit_original_response(content=f"> IP: ||`{ip}`||")
        return True

    @app_commands.command(name="reboot",description="Reboots the bot.")
    @app_commands.dm_only()
    async def reboot(self, interaction: discord.Interaction):
        print(f"> {interaction.user.name} tried to run `reboot`.")
        if not is_admin(interaction.user.id):
            await interaction.response.send_message("> You do not have permission to perform this command.",ephemeral=False)
            return
        print(f"> {interaction.user.name} ran `reboot`.")
        if interaction.guild != None:
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