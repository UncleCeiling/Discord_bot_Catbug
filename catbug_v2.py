import discord,os,csv,asyncio
from random import choice
from modules import settings # For `.env` variables
from discord.ext import commands, tasks

#region Initialise
settings.check_env() # Make sure the `.env has stuff in it`
DISCORD_TOKEN, APPLICATION_ID = str(settings.DISCORD_TOKEN), str(settings.APPLICATION_ID) # Assign keys
intents = discord.Intents.all() # Declare intents
bot = commands.Bot(command_prefix="!",intents=intents) # Builds the bot

@bot.event
async def on_ready():
    """Handles startup sequence"""
    if bot.user:
        print(f"Signed in as {bot.user} (ID: {bot.user.id})") # Successful sign-in
    # Load cogs
    bot.tree.clear_commands(guild=None)
    print("Loading cogs:")
    try:
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                try:
                    await bot.load_extension(f"cogs.{filename[:-3]}")
                    print(f"> Loaded {filename[:-3]}.")
                except Exception as exception:
                    print(f"> Error loading {filename[:-3]} - {exception}")
    except Exception as exception:
        print(exception)
    # Sync Globally
    global_synced = await bot.tree.sync(guild=None)
    print(f"> Synced {len(global_synced)} commands Globally.")
    await bot.change_presence(status=discord.Status.online)
    # Sync Commands to Servers
    guilds = bot.guilds
    synced_servers = 0
    print("> Syncing")
    for guild in guilds:
        try:
            bot.tree.clear_commands(guild=guild)
            # bot.tree.copy_global_to(guild=guild)
            synced_list = await bot.tree.sync(guild=guild)
        except Exception as exception:
            print(f"> ERROR: \n\n```{exception}```")
        else:
            print(f"> > Synced {len(synced_list)} commands to `{guild.name}`")
            synced_servers += 1
    print(f"> Synced {synced_servers} servers.")
    await status_task.start()
#endregion Initialise

#region Tasks
@tasks.loop(hours=1)
async def status_task() -> None:
    with open("data/quotes.csv",encoding="utf8") as file:
        quotes = []
        for row in csv.DictReader(file,fieldnames=("quote","emoji")):
            quotes.append(row)
    quote = choice(quotes)
    status = f"{quote['emoji']} {quote['quote']}"
    await bot.change_presence(activity=discord.CustomActivity(name=status))
#endregion

# Main Loop
if __name__=="__main__":
    bot.run(DISCORD_TOKEN)