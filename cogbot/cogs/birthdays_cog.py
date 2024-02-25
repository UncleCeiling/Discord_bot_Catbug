import discord,datetime
from discord import app_commands
from discord.ext import commands
from typing import Optional

class System(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("> birthdays_cog loaded")

    # Birthday command
    # Options: Add|Edit|Remove|List

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

async def setup(bot):
        await bot.add_cog(System(bot))
