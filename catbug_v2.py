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
        print(f"Signed in as {bot.user} (ID: {bot.user.id})")
    # Load cogs
    await asyncio.sleep(1)
    print("Loading cogs:")
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            try:
                await bot.load_extension(f"cogs.{filename[:-3]}")
                print(f"> Loaded {filename[:-3]}.")
            except Exception as exception:
                print(f"> Error loading {filename[:-3]} - ```{exception}```")
    await bot.change_presence(status=discord.Status.online)
    status_task.start(bot)
    sync_global.start(bot)
    print("Finished startup")
#endregion Initialise

#region Tasks
@tasks.loop(hours=1)
async def status_task(bot) -> list[str]:
    """Changes status to one of their quotes

    Returns:
        list[str]: [quote_text,quote_emoji]
    """
    with open("data/quotes.csv",encoding="utf8") as file:
        quotes = []
        for row in csv.DictReader(file,fieldnames=("quote","emoji")):
            quotes.append(row)
    quote = choice(quotes)
    status_text = f"{quote["quote"]} {quote["emoji"]}"
    await bot.change_presence(activity=discord.CustomActivity(name=status_text))
    print(f"Changed Status to `{status_text}`")
    return [quote["quote"],quote["emoji"]]

@tasks.loop(hours=24)
async def sync_global(bot) -> None:
    print("Syncing Global Commands ")
    synced_list = await bot.tree.sync()
    print(f"> Synced {len(synced_list)} commands:")
    for synced in synced_list:
        print(f"> > {synced}")


#endregion

# Main Loop
if __name__=="__main__":
    bot.run(DISCORD_TOKEN)