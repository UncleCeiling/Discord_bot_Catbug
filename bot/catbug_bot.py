# region ===IMPORTS===

# pip install discord.py[voice]
# pip install python-dotenv
import asyncio,discord,settings,datetime,os,csv,subprocess,rpg_generator
from email import message
from random import choice
from typing import Optional
from discord.ext import commands, tasks
from discord import FFmpegPCMAudio, app_commands


os.chdir(os.path.dirname(__file__))
# endregion ===IMPORTS===
# region ===DECLARATIONS===

rpg_words = rpg_generator.import_rpg_words("files/rpg_words/")
intents = discord.Intents.all() # Declare intents
bot = commands.Bot(command_prefix="!",intents=intents) # Builds bot
# endregion ===DECLARATIONS===
# region ===ON_READY===

@bot.event
async def on_ready(): # When the client is ready
    if bot.user:
        print(f"Signed in as {bot.user} (ID: {bot.user.id})") # Successful sign-in
    try:
        synced = await bot.tree.sync() # Sync Command Tree
        print(f"Synced {len(synced)} command(s)") # Display results
    except Exception as exception:
        print(exception)
    await bot.change_presence(status=discord.Status.online)
    status_task.start()

# endregion ===ON_READY===
# region ===STATUS===


def new_status():
    with open("files/quotes.csv",encoding="utf8") as file:
        quotes = []
        for row in csv.DictReader(file,fieldnames=("quote","emoji")):
            quotes.append(row)
    quote = choice(quotes)
    return f"{quote['emoji']} {quote['quote']}"

@tasks.loop()
async def status_task() -> None:
    status = new_status()
    await bot.change_presence(activity=discord.CustomActivity(name=status))
    await asyncio.sleep(300)

@bot.tree.command(name="status",description="picks a new random status")
async def status(interaction: discord.Interaction):
    status = new_status()
    await bot.change_presence(activity=discord.CustomActivity(name=status))
    await interaction.response.send_message(f"""Changed Status to "{status}" """,ephemeral=True)

# endregion ===STATUS===
# region ===COMMANDS===
# region ==-EXAMPLE-==

# @bot.tree.command(name="example",description="description") # Adds command to tree
# @app_commands.describe(argument = "an argument",) # Adds argument description to command
# async def example(interaction: discord.Interaction, argument: str): # Defines the command
#     if isinstance(interaction.user,Member):
#         voicestatus = interaction.user.voice
#     else:
#         voicestatus = "Not Connected"
#     await interaction.response.send_message(f"This channel is:`{interaction.channel}`\nYou are:`{interaction.user}`\nThe message of this interaction is:`{interaction.message}`\nThe data of this interaction is:`{interaction.data}`\nYour VC status is:`{voicestatus}`\nThe argument you entered was:`{argument}`")

# endregion ==-EXAMPLE-==
# region ==-SILLY-==

@bot.tree.command(name="member",description="( ͡° ͜ʖ ͡°)")
@app_commands.describe(visible="Make output visible in channel?")
async def phallus(interaction: discord.Interaction, member: Optional[discord.Member], visible: bool = False):
    if isinstance(interaction.user,discord.Member):
        member = member or interaction.user
    else:
        await interaction.response.send_message("> Error - member does not exist",ephemeral=not visible)
        return
    length = (int(member.id) % 11) + 1
    await interaction.response.send_message(f">>> {member.mention}:\n8"+"=".center(length,"=")+"D",ephemeral=not visible)

# endregion ==-SILLY-==
# region ==-CLI-==

@bot.tree.command(name="pwd",description="Tells you WHERE you are.") # Also syncs commands
@app_commands.describe(visible="Make output visible in channel?")
async def pwd(interaction: discord.Interaction,visible: bool = False):
    await interaction.response.send_message(f"> `{interaction.guild}/{interaction.channel}`",ephemeral=(not visible))
    try:
        await bot.tree.sync()
    except Exception as exception:
        print(exception)

@bot.tree.command(name="whoami",description="Tells you WHO you are")
@app_commands.describe(visible="Make output visible in channel?")
async def whoami(interaction: discord.Interaction,visible: bool = False):
    await interaction.response.send_message(f"> `{interaction.user}`",ephemeral=(not visible))

@bot.tree.command(name="whois",description="Infodump about a user.")
@app_commands.describe(member = "The person you want to know more about (leave empty for yourself).",visible="Make output visible in channel?")
async def whois(interaction: discord.Interaction, member: Optional[discord.Member], visible: bool = False):
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

@bot.tree.command(name="reboot",description="Reboots the bot.")
async def reboot(interaction: discord.Interaction):
    if interaction.guild:
        await interaction.response.send_message("> This command can only used in DMs.",ephemeral=True)
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
            output = str(subprocess.check_output(["git","pull"]))[2:-1].replace("Fast-forward","FastForward").replace("\\n", "\n> ").replace("\\t", "\t").replace("+","🟢").replace("-","🔴").replace("Already up to date.","Already up to date. ✅")
            message += f"\n\n> 🗒️ Output:\n> {output}"
            await interaction.edit_original_response(content=message)
            message += "\n\n> 🚪 Logging off..."
            await interaction.edit_original_response(content=message)
            await bot.change_presence(status=discord.Status.offline,activity=None)
            message += "\n\n> 🔄 Rebooting..."
            await interaction.edit_original_response(content=message)
            os.system("sudo reboot")

# endregion ==-CLI-==
# region ==-VC-==

@bot.tree.command(name="vc",description="join | leave | resume | pause | stop")
@app_commands.describe(command="What you want the bot to do.",visible="Make output visible in channel?")
@app_commands.choices(command=[
    app_commands.Choice(name="join", value="1"),
    app_commands.Choice(name="leave", value="2"),
    app_commands.Choice(name="resume", value="3"),
    app_commands.Choice(name="pause", value="4"),
    app_commands.Choice(name="stop", value="5")
    ])
async def vc(interaction:discord.Interaction,command:app_commands.Choice[str],visible:Optional[bool]=False):
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
                message += f"\n\n> Joined `{channel}`."
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
                message += f"\n\n> Left `{channel}`."
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
            message += "\n\n> Resumed."
            await interaction.edit_original_response(content=message)
        except Exception as exception:
            message += f"\n\n>>> Resume failed.\nError:\n```{exception}```"
            await interaction.edit_original_response(content=message)
    elif choice == 4:
        message = "> Pausing..."
        await interaction.response.send_message(message,ephemeral=(not visible))
        try:
            player.pause()
            message += "\n\n> Paused."
            await interaction.edit_original_response(content=message)
        except Exception as exception:
            message += f"\n\n>>> Pause failed.\nError:\n```{exception}```"
            await interaction.edit_original_response(content=message)
    elif choice == 5:
        message = "> Stopping..."
        await interaction.response.send_message(message,ephemeral=(not visible))
        try:
            player.stop()
            message += "\n\n> Stopped."
            await interaction.edit_original_response(content=message)
        except Exception as exception:
            message += f"\n\n>>> Stop failed.\nError:\n```{exception}```"
            await interaction.edit_original_response(content=message)

# endregion ==-VC-==
# region ==-Radio-==

def get_stations():
    with open("files/streams/stations.csv",encoding="utf8") as file:
        stations = []
        for station in csv.DictReader(file,fieldnames=("station","link")):
            stations.append(app_commands.Choice(name=station["station"], value=station["link"]))
    return stations

@bot.tree.command(name="radio",description="Radio channels")
@app_commands.describe(station="The Genre you'd like to listen to.",visible="Make output visible in channel?")
@app_commands.choices(station=get_stations())
async def radio(interaction:discord.Interaction,station: app_commands.Choice[str],visible: Optional[bool]=True):
    # Build URL with Args
    url = station.value
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
            message += f"\n\n> Disconnecting from {interaction.guild.voice_client.channel}..."
            await interaction.edit_original_response(content=message)
            try: # Try to disconnect from current Channel
                await interaction.guild.voice_client.disconnect(force=True)
            except Exception as exception: # Freak out if you can't
                message += f"\n\n>>> Couldn't disconnect.\nError:\n```{exception}```"
                await interaction.edit_original_response(content=message)
                return
        if not interaction.guild.voice_client: # If we aren't in a channel
            message += f"\n\n> Connecting to {channel}..."
            await interaction.edit_original_response(content=message)
            try: # Try to Connect
                player = await channel.connect()
            except Exception as exception: # Freak out if it doesn't work
                message += f"\n\n>>> Couldn't connect to {channel}.\nError:\n```{exception}```"
                await interaction.edit_original_response(content=message)
                return
        message += f"\n\n> Connected! Starting Stream..."
        await interaction.edit_original_response(content=message)
        try: # Try to Start the Stream
            player.stop()
            player.play(source=FFmpegPCMAudio(source=url))
        except Exception as exception: # Freak out if you can't
            message += f"\n\n>>> Couldn't start Stream.\nError:\n```{exception}```"
            await interaction.edit_original_response(content=message)
            return
        message += f"\n\n>>> {station.name} stream started!\nEnjoy! [Stream URL]({url})"
        await interaction.edit_original_response(content=message)

# endregion ==-Radio-==
# region ==-ATC-==

def get_towers():
    with open("files/streams/towers.csv",encoding="utf8") as file:
        towers = []
        for tower in csv.DictReader(file,fieldnames=("ICAO","IATA","City","Type","url")):
            towers.append(app_commands.Choice(name=f"{tower['IATA']} - {tower['City']} - {tower['Type']}", value=tower["url"]))
    return towers

@bot.tree.command(name="atc",description="Air Traffic Control radio feed.")
@app_commands.describe(tower="ATC Tower you'd like to listen to.",visible="Make output visible in channel?")
@app_commands.choices(tower=get_towers())
async def atc(interaction:discord.Interaction,tower: app_commands.Choice[str],visible: Optional[bool]=True):
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
            message += f"\n\n> Disconnecting from {interaction.guild.voice_client.channel}..."
            await interaction.edit_original_response(content=message)
            try: # Try to disconnect from current Channel
                await interaction.guild.voice_client.disconnect(force=True)
            except Exception as exception: # Freak out if you can't
                message += f"\n\n>>> Couldn't disconnect.\nError:\n```{exception}```"
                await interaction.edit_original_response(content=message)
                return
        if not interaction.guild.voice_client: # If we aren't in a channel
            message += f"\n\n> Connecting to {channel}..."
            await interaction.edit_original_response(content=message)
            try: # Try to Connect
                player = await channel.connect()
            except Exception as exception: # Freak out if it doesn't work
                message += f"\n\n>>> Couldn't connect to {channel}.\nError:\n```{exception}```"
                await interaction.edit_original_response(content=message)
                return
        message += f"\n\n> Connected! Starting Stream..."
        await interaction.edit_original_response(content=message)
        try: # Try to Start the Stream
            player.stop()
            player.play(source=FFmpegPCMAudio(source=url))
        except Exception as exception: # Freak out if you can't
            message += f"\n\n>>> Couldn't start Stream.\nError:\n```{exception}```"
            await interaction.edit_original_response(content=message)
            return
        message += f"\n\n>>> {tower.name} stream started!\nEnjoy! [Stream URL]({url})"
        await interaction.edit_original_response(content=message)

# endregion ==-ATC-==
# region ==-URL-==

@bot.tree.command(name="stream",description="Stream a url")
@app_commands.describe(url="The link you want to stream",visible="Make output visible in channel?")
async def stream(interaction: discord.Interaction,url: str,visible: Optional[bool]=True):
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
            message += f"\n\n> Disconnecting from {interaction.guild.voice_client.channel}..."
            await interaction.edit_original_response(content=message)
            try: # Try to disconnect from current Channel
                await interaction.guild.voice_client.disconnect(force=True)
            except Exception as exception: # Freak out if you can't
                message += f"\n\n>>> Couldn't disconnect.\nError:\n```{exception}```"
                await interaction.edit_original_response(content=message)
                return
        if not interaction.guild.voice_client: # If we aren't in a channel
            message += f"\n\n> Connecting to {channel}..."
            await interaction.edit_original_response(content=message)
            try: # Try to Connect
                player = await channel.connect()
            except Exception as exception: # Freak out if it doesn't work
                message += f"\n\n>>> Couldn't connect to {channel}.\nError:\n```{exception}```"
                await interaction.edit_original_response(content=message)
                return
        message += f"\n\n> Connected! Starting Stream..."
        await interaction.edit_original_response(content=message)
        try: # Try to Start the Stream
            player.stop()
            player.play(source=FFmpegPCMAudio(source=url))
        except Exception as exception: # Freak out if you can't
            message += f"\n\n>>> Couldn't start Stream.\nError:\n```{exception}```"
            await interaction.edit_original_response(content=message)
            return
        message += f"\n\n>>> Stream started!\nEnjoy! [Stream URL]({url})"
        await interaction.edit_original_response(content=message)

# endregion ==-URL-==
# region ==-RPG-==

@bot.tree.command(name="rpg",description="Generate an RPG item.")
@app_commands.describe(item_type="What type of Item you want to generate.",visible="Make output visible in channel?")
@app_commands.choices(item_type=[
    app_commands.Choice(name="weapon", value="1"),
    app_commands.Choice(name="armour", value="2")
    ])
async def rpg(interaction:discord.Interaction,item_type:app_commands.Choice[str],modifiers:Optional[int]=0,visible:Optional[bool]=False):
    choice = int(item_type.value)
    if choice == 1: # Weapon
        message = "> Your Weapon is the..."
        await interaction.response.send_message(message,ephemeral=(not visible))
        if modifiers == 0 or modifiers == None:
            weapon = rpg_generator.gen_equipment(rpg_words["weapons"],rpg_words["nouns"])
        else:
            weapon = rpg_generator.gen_equipment(rpg_words["weapons"],rpg_words["nouns"])
            weapon = rpg_generator.add_modifier(weapon,modifiers,rpg_words["adjectives"])
        message += f"\n\n>>> {weapon}."
        await interaction.edit_original_response(content=message)
    elif choice == 2: # Armour
        message = "> Your Armour is the..."
        await interaction.response.send_message(message,ephemeral=(not visible))
        armour = rpg_generator.gen_equipment(rpg_words["armour"],rpg_words["nouns"])
        if modifiers != 0 and modifiers != None:
            armour = rpg_generator.add_modifier(armour,modifiers,rpg_words["adjectives"])
        message += f"\n\n>>> {armour}."
        await interaction.edit_original_response(content=message)

# endregion ==-RPG-==
# endregion ===COMMANDS===

bot.run(settings.TOKEN)