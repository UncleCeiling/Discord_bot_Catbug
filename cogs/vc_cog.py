from encodings import utf_8

import discord,csv
from discord import app_commands,FFmpegPCMAudio
from discord.ext import commands
from typing import Optional

def get_station_values():
    with open("data/streams/stations.csv",encoding="utf8") as file:
        stations = []
        value = 0
        for row in csv.DictReader(file,fieldnames=("station","link")):
            stations.append(app_commands.Choice(name=row["station"], value=str(value)))
            value += 1
    return stations

def get_station_url_from_value(value: int):
    with open("data/streams/stations.csv",encoding="utf8") as file:
        urls = []
        for row in csv.DictReader(file,fieldnames=("station","link")):
            urls.append(row["link"])
    return urls[value]

def get_towers():
    with open("data/streams/towers.csv",encoding="utf8") as file:
        towers = []
        for tower in csv.DictReader(file,fieldnames=("ICAO","IATA","City","Type","url")):
            towers.append(app_commands.Choice(name=f"{tower['IATA']} - {tower['City']} - {tower['Type']}", value=tower["url"]))
    return towers

class Vc(commands.Cog):
    def __init__(self, bot: commands.Bot,):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("> vc_cog loaded")
    
    # region VC

    @app_commands.command(name="vc",description="join | leave | resume | pause | stop")
    @app_commands.describe(command="What you want the bot to do.",visible="Make output visible in channel?")
    @app_commands.choices(command=[
        app_commands.Choice(name="join", value="1"),
        app_commands.Choice(name="leave", value="2"),
        app_commands.Choice(name="resume", value="3"),
        app_commands.Choice(name="pause", value="4"),
        app_commands.Choice(name="stop", value="5")
        ])
    async def vc(self, interaction:discord.Interaction,command:app_commands.Choice[str],visible:Optional[bool]=False):
        choice = int(command.value)
        global player
        if choice == 1:
            if not interaction.guild:
                await interaction.response.send_message("> This command can only be used in a Server.",ephemeral=(not visible))
                return
            elif interaction.guild.voice_client:
                await interaction.guild.voice_client.disconnect(force=True)
            if isinstance(interaction.user,discord.Member) and interaction.user.voice and interaction.user.voice.channel:
                channel = interaction.user.voice.channel
                message = f"> Joining `{channel}`..."
                await interaction.response.send_message(message,ephemeral=(not visible))
                try:
                    player = await channel.connect()
                    message = f"> Joined `{channel}`."
                    await interaction.edit_original_response(content=message)
                except Exception as exception:
                    message += f"\n\n>>> Joining `{channel}` failed.\nError:\n```{exception}```"
                    await interaction.edit_original_response(content=message)
            else:
                await interaction.response.send_message(f">>> This command can only be used when connected to a Voice Channel in the current Server.\nCurrent Server:{interaction.guild}",ephemeral=(not visible))
                return
        elif choice == 2:
            if interaction.guild and interaction.guild.voice_client: # If in voice-chat
                channel = interaction.guild.voice_client.channel # Store channel
                message = f"> Leaving `{channel}`..."
                await interaction.response.send_message(message,ephemeral=(not visible))
                try: # Try to stop and leave.
                    player.stop()
                    await interaction.guild.voice_client.disconnect(force=True)
                    message = f"> Left `{channel}`."
                    await interaction.edit_original_response(content=message)
                except Exception as exception: # You tried
                    message += f"\n\n>>> Leaving `{channel}` failed.\nError:\n```{exception}```"
                    await interaction.edit_original_response(content=message)
            else:
                if interaction.guild: # If we're even in a server
                    await interaction.response.send_message("> This command can only be used if I'm in a voice channel already.",ephemeral=(not visible))
                else:
                    await interaction.response.send_message("> This command can only be used in a Server.",ephemeral=(not visible))
        elif choice == 3:
            message = "> Resuming..."
            await interaction.response.send_message(message,ephemeral=(not visible))
            try:
                player.resume()
                message = "> Resumed."
                await interaction.edit_original_response(content=message)
            except Exception as exception:
                message += f"\n\n>>> Resume failed.\nError:\n```{exception}```"
                await interaction.edit_original_response(content=message)
        elif choice == 4:
            message = "> Pausing..."
            await interaction.response.send_message(message,ephemeral=(not visible))
            try:
                player.pause()
                message = "> Paused."
                await interaction.edit_original_response(content=message)
            except Exception as exception:
                message += f"\n\n>>> Pause failed.\nError:\n```{exception}```"
                await interaction.edit_original_response(content=message)
        elif choice == 5:
            message = "> Stopping..."
            await interaction.response.send_message(message,ephemeral=(not visible))
            try:
                player.stop()
                message = "> Stopped."
                await interaction.edit_original_response(content=message)
            except Exception as exception:
                message += f"\n\n>>> Stop failed.\nError:\n```{exception}```"
                await interaction.edit_original_response(content=message)

# endregion VC
    # region Radio

    @app_commands.command(name="radio",description="Radio channels")
    @app_commands.describe(station="The Genre you'd like to listen to.",visible="Make output visible in channel?")
    @app_commands.choices(station=get_station_values())
    async def radio(self, interaction:discord.Interaction,station: app_commands.Choice[str],visible: Optional[bool]=False):
        # Build URL with Args
        url = get_station_url_from_value(int(station.value))
        # Filter cases where no action is taken
        if not interaction.guild: # Not in Server
            await interaction.response.send_message("> This command can only be used in a Server.",ephemeral=True)
            return
        elif not interaction.guild.voice_channels: # No Voice Channels
            await interaction.response.send_message("> This command can only be used in Servers with Voice Channels.",ephemeral=True)
            return
        elif not (isinstance(interaction.user,discord.Member) and interaction.user.voice and interaction.user.voice.channel): # If User is not in Voice Channel
            await interaction.response.send_message(f">>> This command can only be used when connected to a Voice Channel in the current Server.\nCurrent Server:{interaction.guild}",ephemeral=True)
        else: # Enter the channel
            channel = interaction.user.voice.channel # Find which channel to go to
            message = f"> Starting Connection..."
            await interaction.response.send_message(message,ephemeral=(not visible),suppress_embeds=True)
            global player
            if interaction.guild.voice_client and (interaction.guild.voice_client.channel != channel): # If we are already in a channel, but not the right one
                message = f"> Disconnecting from {interaction.guild.voice_client.channel}..."
                await interaction.edit_original_response(content=message)
                try: # Try to disconnect from current Channel
                    await interaction.guild.voice_client.disconnect(force=True)
                except Exception as exception: # Freak out if you can't
                    message += f"\n\n>>> Couldn't disconnect.\nError:\n```{exception}```"
                    await interaction.edit_original_response(content=message)
                    return
            if not interaction.guild.voice_client: # If we aren't in a channel
                message = f"> Connecting to {channel}..."
                await interaction.edit_original_response(content=message)
                try: # Try to Connect
                    player = await channel.connect()
                except Exception as exception: # Freak out if it doesn't work
                    message += f"\n\n>>> Couldn't connect to {channel}.\nError:\n```{exception}```"
                    await interaction.edit_original_response(content=message)
                    return
            message = f"> Connected! Starting Stream..."
            await interaction.edit_original_response(content=message)
            try: # Try to Start the Stream
                player.stop()
                player.play(source=discord.PCMVolumeTransformer(FFmpegPCMAudio(source=url),volume=0.1))
            except Exception as exception: # Freak out if you can't
                message += f"\n\n>>> Couldn't start Stream.\nError:\n```{exception}```"
                await interaction.edit_original_response(content=message)
                return
            message = f">>> {station.name} stream started!\nEnjoy! [Stream URL]({url})"
            await interaction.edit_original_response(content=message)

    # endregion Radio
    # region ATC

    @app_commands.command(name="atc",description="Air Traffic Control radio feed.")
    @app_commands.describe(tower="ATC Tower you'd like to listen to.",visible="Make output visible in channel?")
    @app_commands.choices(tower=get_towers())
    async def atc(self, interaction:discord.Interaction,tower: app_commands.Choice[str],visible: Optional[bool]=False):
        # Build URL with Args
        url = tower.value
        # Filter cases where no action is taken
        if not interaction.guild: # Not in Server
            await interaction.response.send_message("> This command can only be used in a Server.",ephemeral=True)
            return
        elif not interaction.guild.voice_channels: # No Voice Channels
            await interaction.response.send_message("> This command can only be used in Servers with Voice Channels.",ephemeral=True)
            return
        elif not (isinstance(interaction.user,discord.Member) and interaction.user.voice and interaction.user.voice.channel): # If User is not in Voice Channel
            await interaction.response.send_message(f"> This command can only be used when connected to a Voice Channel in the current Server.\n> Current Server:{interaction.guild}",ephemeral=True)
            return
        else: # Enter the channel
            channel = interaction.user.voice.channel # Find which channel to go to
            message = f"> Starting Connection..."
            await interaction.response.send_message(message,ephemeral=(not visible),suppress_embeds=True)
            global player
            if interaction.guild.voice_client and (interaction.guild.voice_client.channel != channel): # If we are already in a channel, but not the right one
                message = f"> Disconnecting from {interaction.guild.voice_client.channel}..."
                await interaction.edit_original_response(content=message)
                try: # Try to disconnect from current Channel
                    await interaction.guild.voice_client.disconnect(force=True)
                except Exception as exception: # Freak out if you can't
                    message += f"\n\n>>> Couldn't disconnect.\nError:\n```{exception}```"
                    await interaction.edit_original_response(content=message)
                    return
            if not interaction.guild.voice_client: # If we aren't in a channel
                message = f"> Connecting to {channel}..."
                await interaction.edit_original_response(content=message)
                try: # Try to Connect
                    player = await channel.connect()
                except Exception as exception: # Freak out if it doesn't work
                    message += f"\n\n>>> Couldn't connect to {channel}.\nError:\n```{exception}```"
                    await interaction.edit_original_response(content=message)
                    return
            message = f"> Connected! Starting Stream..."
            await interaction.edit_original_response(content=message)
            try: # Try to Start the Stream
                player.stop()
                player.play(source=discord.PCMVolumeTransformer(FFmpegPCMAudio(source=url),volume=0.1))
            except Exception as exception: # Freak out if you can't
                message += f"\n\n>>> Couldn't start Stream.\nError:\n```{exception}```"
                await interaction.edit_original_response(content=message)
                return
            message = f">>> {tower.name} stream started!\nEnjoy! [Stream URL]({url})"
            await interaction.edit_original_response(content=message)

    # endregion ATC
    # region URL

    @app_commands.command(name="stream",description="Stream a url")
    @app_commands.describe(url="The link you want to stream",visible="Make output visible in channel?")
    async def stream(self, interaction: discord.Interaction,url: str,visible: Optional[bool]=False):
        # Filter cases where no action is taken
        if not interaction.guild: # Not in Server
            await interaction.response.send_message("> This command can only be used in a Server.",ephemeral=True)
            return
        elif not interaction.guild.voice_channels: # No Voice Channels
            await interaction.response.send_message("> This command can only be used in Servers with Voice Channels.",ephemeral=True)
            return
        elif not (isinstance(interaction.user,discord.Member) and interaction.user.voice and interaction.user.voice.channel): # If User is not in Voice Channel
            await interaction.response.send_message(f">>> This command can only be used when connected to a Voice Channel in the current Server.\nCurrent Server:{interaction.guild}",ephemeral=True)
        else: # Enter the channel
            channel = interaction.user.voice.channel # Find which channel to go to
            message = f"> Starting Connection..."
            await interaction.response.send_message(message,ephemeral=(not visible),suppress_embeds=True)
            global player
            if interaction.guild.voice_client and (interaction.guild.voice_client.channel != channel): # If we are already in a channel, but not the right one
                message = f"> Disconnecting from {interaction.guild.voice_client.channel}..."
                await interaction.edit_original_response(content=message)
                try: # Try to disconnect from current Channel
                    await interaction.guild.voice_client.disconnect(force=True)
                except Exception as exception: # Freak out if you can't
                    message += f"\n\n>>> Couldn't disconnect.\nError:\n```{exception}```"
                    await interaction.edit_original_response(content=message)
                    return
            if not interaction.guild.voice_client: # If we aren't in a channel
                message = f"> Connecting to {channel}..."
                await interaction.edit_original_response(content=message)
                try: # Try to Connect
                    player = await channel.connect()
                except Exception as exception: # Freak out if it doesn't work
                    message += f"\n\n>>> Couldn't connect to {channel}.\nError:\n```{exception}```"
                    await interaction.edit_original_response(content=message)
                    return
            message = f"> Connected! Starting Stream..."
            await interaction.edit_original_response(content=message)
            try: # Try to Start the Stream
                player.stop()
                player.play(source=discord.PCMVolumeTransformer(FFmpegPCMAudio(source=url),volume=0.1))
            except Exception as exception: # Freak out if you can't
                message += f"\n\n>>> Couldn't start Stream.\nError:\n```{exception}```"
                await interaction.edit_original_response(content=message)
                return
            message = f">>> Stream started!\nEnjoy! [Stream URL]({url})"
            await interaction.edit_original_response(content=message)

    # endregion URL


async def setup(bot):
        await bot.add_cog(Vc(bot))