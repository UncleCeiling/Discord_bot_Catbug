# region ===Imports===

import asyncio,discord,settings,datetime,os,csv
from random import choice
from typing import Optional
from discord.ext import commands, tasks
from discord import app_commands

os.chdir(os.path.dirname(__file__))
# endregion ===Imports===

intents = discord.Intents.all() # Declare intents
bot = commands.Bot(command_prefix="!",intents=intents) # Builds bot

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
    status_task.start()

# endregion ===ON_READY===
# region ===STATUS===

def new_status():
    with open("files/quotes.csv") as file:
        quotes = []
        for row in csv.DictReader(file,fieldnames=("quote","emoji")):
            quotes.append(row)
    quote = choice(quotes)
    return f"{quote["emoji"]} {quote["quote"]} {quote["emoji"]}"

@tasks.loop()
async def status_task() -> None:
    await bot.change_presence(activity=discord.CustomActivity(name=new_status()))
    await asyncio.sleep(300)

@bot.tree.command(name="status",description="picks a new random status")
async def status(interaction: discord.Interaction):
    status = new_status()
    await bot.change_presence(activity=discord.CustomActivity(name=status))
    await interaction.response.send_message(f"""Changed Status to "{status}" """,ephemeral=True)

# endregion ===STATUS===
# region ===EXAMPLE===

# @bot.tree.command(name="example",description="description") # Adds command to tree
# @app_commands.describe(argument = "an argument",) # Adds argument description to command
# async def example(interaction: discord.Interaction, argument: str): # Defines the command
#     if isinstance(interaction.user,Member):
#         voicestatus = interaction.user.voice
#     else:
#         voicestatus = "Not Connected"
#     await interaction.response.send_message(f"This channel is:`{interaction.channel}`\nYou are:`{interaction.user}`\nThe message of this interaction is:`{interaction.message}`\nThe data of this interaction is:`{interaction.data}`\nYour VC status is:`{voicestatus}`\nThe argument you entered was:`{argument}`")

# endregion ===EXAMPLE===
# region ===Silly===

@bot.tree.command(name="penis",description="( ͡° ͜ʖ ͡°)")
@app_commands.describe(visible="Make output visible in channel?")
async def example(interaction: discord.Interaction, member: Optional[discord.Member], visible: bool = False):
    if isinstance(interaction.user,discord.Member):
        member = member or interaction.user
    else:
        await interaction.response.send_message("Error - member does not exist",ephemeral=not visible)
        return
    length = (int(member.id) % 11) + 1
    await interaction.response.send_message(f"{member.mention}:\n8"+"=".center(length,"=")+"D",ephemeral=not visible)

# endregion ===Silly===
# region ===CLI===

@bot.tree.command(name="pwd",description="tells you *where* you are") # Also syncs commands
@app_commands.describe(visible="Make output visible in channel?")
async def pwd(interaction: discord.Interaction,visible: bool = False):
    try:
        await bot.tree.sync()
    except Exception as exception:
        print(exception)
    await interaction.response.send_message(f"`{interaction.guild}/{interaction.channel}`",ephemeral=not visible)

@bot.tree.command(name="whoami",description="tells you *who* you are")
@app_commands.describe(visible="Make output visible in channel?")
async def whoami(interaction: discord.Interaction,visible: bool = False):
    await interaction.response.send_message(f"`{interaction.user}`",ephemeral=not visible)

@bot.tree.command(name="whois",description="Prints out a bunch of information")
@app_commands.describe(member = "The person you want to know more about (leave empty for yourself)",visible="Make output visible in channel?")
async def whois(interaction: discord.Interaction, member: Optional[discord.Member], visible: bool = False):
    message = ""
    if isinstance(interaction.user,discord.Member):
        member = member or interaction.user
    else:
        await interaction.response.send_message("Error - member does not exist")
        return
    if member.bot == True or member.system == True:
        message += "## This account is "
        if member.bot == True and member.system == True:
            message += "an `official bot` :robot: :shield:\n"
        elif member.bot == True:
            message += "a `bot` :robot:\n"
        elif member.system == True:
            message += "an `official account`:shield:\n"
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
    await interaction.response.send_message(content=message,ephemeral=not visible)

# endregion ===CLI===
# region ===VC===

@bot.tree.command(name="join",description="asks the bot to join your VC")
async def join(interaction: discord.Interaction):
    if isinstance(interaction.user,discord.Member):
        if not interaction.user.voice:
            await interaction.response.send_message("You must be connected to a VC to use this command",ephemeral=True)
            return
        elif interaction.user.voice.channel:
            try:
                await interaction.user.voice.channel.connect()
                await interaction.response.send_message(f"Connected to {interaction.user.voice.channel}",ephemeral=True) 
            except:
                await interaction.response.send_message(f"Could not connect to {interaction.user.voice.channel}",ephemeral=True)
    else:
        await interaction.response.send_message(f"Error encountered: You are not recognised as a member. Either you are not in a guild or there is something else going on.\nFor reference, your user is {interaction.user}",ephemeral=True)

@bot.tree.command(name="atc",description="streams radio traffic")
@app_commands.describe(airport = "Enter an Airport code")
async def atc(interaction: discord.Interaction, airport: str):
    await interaction.response.send_message(f"This feature is still under construction, but for now:\nYou requested the {airport} airport.",ephemeral=True)
# endregion ===VC===

bot.run(settings.TOKEN)