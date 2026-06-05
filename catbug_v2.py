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
    try:
        synced = await bot.tree.sync()
        for command in synced:
            print(f"> > Synced {command}")
    except Exception as exception:
        print(exception)
    await bot.change_presence(status=discord.Status.online)
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