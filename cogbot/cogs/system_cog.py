import discord,csv,subprocess,datetime,os
from discord import app_commands
from discord.ext import commands
from typing import Optional

class System(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("> system_cog loaded")

    # region CLI-clone

    @app_commands.command(name="pwd",description="Tells you WHERE you are.") # Also syncs commands
    @app_commands.describe(visible="Make output visible in channel?")
    async def pwd(self, interaction: discord.Interaction,visible: bool = False):
        await interaction.response.send_message(f"> `{interaction.guild}/{interaction.channel}`",ephemeral=(not visible))
        try:
            await self.bot.tree.sync()
        except Exception as exception:
            print(exception)

    @app_commands.command(name="whoami",description="Tells you WHO you are")
    @app_commands.describe(visible="Make output visible in channel?")
    async def whoami(self, interaction: discord.Interaction,visible: bool = False):
        await interaction.response.send_message(f"> `{interaction.user}`",ephemeral=(not visible))

    @app_commands.command(name="whois",description="Infodump about a user.")
    @app_commands.describe(member = "The person you want to know more about (leave empty for yourself).",visible="Make output visible in channel?")
    async def whois(self, interaction: discord.Interaction, member: Optional[discord.Member], visible: bool = False):
        message = ""
        if isinstance(interaction.user,discord.Member):
            member = member or interaction.user
        else:
            await interaction.response.send_message(f"> Error - member does not exist or command is busted.\n> Member: {member}",ephemeral=(not visible))
            return
        if member.bot == True or member.system == True:
            message += ">>> ## This account is "
            if member.bot == True and member.system == True:
                message += "an `official bot` 🤖 🛡️\n"
            elif member.bot == True:
                message += "a `bot` 🤖\n"
            elif member.system == True:
                message += "an `official account` 🛡️\n"
        if member.global_name:
            message += f"### Global Nickname:\n`{member.global_name}`\n"
        message += f"### Username:\n`{member}`\n"
        if member.nick:
            message += f"### Server Nickname:\n`{member.nick}`\n"
        if member.discriminator and int(member.discriminator) > 0:
            message += f"### Discriminator:\n`{member.discriminator}`\n"
        message += f"### User ID:\n`{member.id}`\n"
        message += f"### Created:\n`{member.created_at.date().strftime('%a %d %B %Y')}`  {(datetime.date.today() - member.created_at.date()).days} days ago\n"
        if member and member.joined_at:
            message += f"### Joined Server:\n`{member.joined_at.date().strftime('%a %d %B %Y')}`  {(datetime.date.today() - member.joined_at.date()).days} days ago\n"
        message += f"### Verified:\n`{not member.pending}`\n"
        if member.mutual_guilds:
            message += "### Mutual Guilds (with bot):\n"
            for guild in member.mutual_guilds:
                message += f"> `{guild.name}`\n"
        if member.activities:
            message += "### Activities:\n"
            for activity in member.activities:
                message += f"> {activity.name}\n"
        if member.display_avatar or member.guild_avatar:
            message += "### Avatar\n"
            if member.display_avatar:
                message += f"[Main Avatar]({member.display_avatar.url})\n"
            if member.guild_avatar:
                message += f"[Guild Avatar]({member.guild_avatar.url})\n"
        await interaction.response.send_message(content=message,ephemeral=(not visible))

    @app_commands.command(name="reboot",description="Reboots the bot.")
    async def reboot(self, interaction: discord.Interaction):
        if interaction.guild:
            await interaction.response.send_message("> This command can only used in DMs.",ephemeral=False)
            return
        else:
            with open("files/admins.csv",encoding="utf8") as file:
                admins = {}
                for line in csv.DictReader(file,fieldnames=("Name","ID")):
                    admins.update({line["Name"]:int(line["ID"])})
            if interaction.user.id not in admins.values():
                await interaction.response.send_message("> You do not have permission to perform this command",ephemeral=True)
                return
            else:
                message = "> ⏳ Initiating shutdown..."
                await interaction.response.send_message(message,ephemeral=True)
                message += "\n\n> 🪝 Running `git pull`..."
                await interaction.edit_original_response(content=message)
                output = subprocess.run(["git","pull"],stdout=subprocess.PIPE).stdout.decode("utf-8").replace("Fast-forward","FastForward").replace("+","🟢").replace("-","🔴").replace("Already up to date.","Already up to date. ✅")
                message += f"\n\n> 🗒️ Output:\n> {output}"
                await interaction.edit_original_response(content=message)
                message += "\n\n> 🚪 Logging off..."
                await interaction.edit_original_response(content=message)
                await self.bot.change_presence(status=discord.Status.offline,activity=None)
                message += "\n\n> 🔄 Rebooting..."
                await interaction.edit_original_response(content=message)
                os.system("sudo reboot")

    # endregion ==-CLI-==

async def setup(bot):
        await bot.add_cog(System(bot))