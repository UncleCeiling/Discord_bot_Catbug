from concurrent.futures import thread

import discord,csv,subprocess,datetime,os
from random import choice
from discord import app_commands
from discord import guild
from discord import channel
from discord.ext import commands
from typing import Optional

from catbug_v2 import status_task

class System(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("> system_cog loaded")

    @app_commands.command(name="status",description="Picks a new random status")
    async def status(self, interaction: discord.Interaction):
        new_status = await status_task(self.bot)
        await interaction.response.send_message(f"> Changed Status to:\n\n> {new_status[0]} {new_status[1]}",ephemeral=True)

    @app_commands.command(name="pwd",description="Tells you WHERE you are.") # Also syncs commands
    @app_commands.describe(visible="Make output visible in channel?")
    async def pwd(self, interaction: discord.Interaction,visible: bool = False):
        guild = interaction.guild # Get guild of message.
        if interaction.guild == None or interaction.channel == None: # Check for if we're in DMs
            await interaction.response.send_message("> We are in DMs")
            return
        elif isinstance(interaction.channel,discord.Thread):
            channel = self.bot.get_channel(interaction.channel.parent_id)
            thread = self.bot.get_channel(interaction.channel.id)
        else:
            channel = interaction.channel
            thread = None
        message = f"> `{guild} / {channel}"
        message += "`" if thread == None else f" / {thread}`"
        await interaction.response.send_message(message,ephemeral=(not visible))

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
                message += f"[Profile Avatar]({member.display_avatar.url})\n"
            if member.guild_avatar:
                message += f"[Server Avatar]({member.guild_avatar.url})\n"
        await interaction.response.send_message(content=message,ephemeral=(not visible))

async def setup(bot):
        await bot.add_cog(System(bot))
