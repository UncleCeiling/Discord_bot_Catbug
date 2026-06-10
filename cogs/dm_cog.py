import discord,csv
from discord import app_commands
from discord.ext import commands

class DM(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("> dm_cog loaded")
    
    @app_commands.command(name="sync",description="Syncs the bot commands")
    @app_commands.allowed_contexts(False,True,False)
    @app_commands.describe(command="command to run")
    @app_commands.choices(command=[
        app_commands.Choice(name="global", value="1"),
        app_commands.Choice(name="guilds", value="2"),
        app_commands.Choice(name="clear global", value="3"),
        app_commands.Choice(name="clear guilds", value="4"),
        app_commands.Choice(name="global to guilds", value="5"),
        ])
    async def example(self, interaction: discord.Interaction, command: app_commands.Choice[str]):
        with open("data/admins.csv",encoding="utf8") as file:
            admin_ids = []
            for row in csv.DictReader(file,fieldnames=("admin","id")):
                admin_ids.append(int(row["id"]))
        if interaction.user.id not in admin_ids:
            await interaction.response.send_message("> Command can only be run by Admins.")
        match int(command.value):
            case 1:
                global_synced = await self.bot.tree.sync(guild=None)
                message = f"> Synced {len(global_synced)} commands Globally."
                for synced in global_synced:
                    message += f"\n> > {synced.name}"
                await interaction.response.send_message(message,ephemeral=False)
            case 2:
                guilds = self.bot.guilds
                synced_servers = 0
                message = "> Syncing"
                await interaction.response.send_message(message,ephemeral=False)
                for guild in guilds:
                    try:
                        synced_list = await self.bot.tree.sync(guild=guild)
                    except Exception as exception:
                        message += f"\n> ERROR: \n```{exception}```"
                        await interaction.edit_original_response(content=message)
                    else:
                        message += f"\n> > Synced {len(synced_list)} commands to `{guild.name}`"
                        for synced_command in synced_list:
                            message += f"\n> > > {synced_command.name}"
                        synced_servers += 1
                        await interaction.edit_original_response(content=message)
                message += f"\n> Synced {synced_servers} servers."
                await interaction.edit_original_response(content=message)
            case 3:
                self.bot.tree.clear_commands(guild=None)
                await self.bot.tree.sync()
                await interaction.response.send_message("> Cleared Global Commands",ephemeral=False)
            case 4:
                guilds = self.bot.guilds
                cleared_servers = 0
                message = "> Clearing"
                await interaction.response.send_message(message,ephemeral=False)
                for guild in guilds:
                    try:
                        self.bot.tree.clear_commands(guild=guild)
                        self.bot.tree.copy_global_to(guild=guild)
                        synced_list = await self.bot.tree.sync(guild=guild)
                    except Exception as exception:
                        message += f"\n> ERROR: \n```{exception}```"
                        await interaction.edit_original_response(content=message)
                    else:
                        message += f"\n> > Syncing cleared {len(synced_list)} commands to `{guild.name}`"
                        for synced_command in synced_list:
                            message += f"\n> > > {synced_command.name}"
                        cleared_servers += 1
                        await interaction.edit_original_response(content=message)
                message += f"\n> Cleared {cleared_servers} servers."
                await interaction.edit_original_response(content=message)
            case 5:
                guilds = self.bot.guilds
                synced_servers = 0
                message = "> Copying global"
                await interaction.response.send_message(message,ephemeral=False)
                for guild in guilds:
                    try:
                        self.bot.tree.copy_global_to(guild=guild)
                        synced_list = await self.bot.tree.sync(guild=guild)
                    except Exception as exception:
                        message += f"\n> ERROR: \n```{exception}```"
                        await interaction.edit_original_response(content=message)
                    else:
                        message += f"\n> > Copied {len(synced_list)} commands to `{guild.name}`"
                        for synced_command in synced_list:
                            message += f"\n> > > {synced_command.name}"
                        synced_servers += 1
                        await interaction.edit_original_response(content=message)
                message += f"\n> Copied to {synced_servers} servers."
                await interaction.edit_original_response(content=message)

async def setup(bot):
        await bot.add_cog(DM(bot))