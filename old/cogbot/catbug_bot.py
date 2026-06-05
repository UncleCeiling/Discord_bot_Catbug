# pip install discord.py[voice]
# pip install python-dotenv
import asyncio,discord,settings,os,csv
from random import choice
from discord.ext import commands, tasks
os.chdir(os.path.dirname(__file__))

intents = discord.Intents.all() # Declare intents
bot = commands.Bot(command_prefix="!",intents=intents) # Builds bot

@bot.event
async def on_ready(): # When the client is ready
    if bot.user:
        print(f"Signed in as {bot.user} (ID: {bot.user.id})") # Successful sign-in
    try:
        print("Loading cogs:")
        await load()
    except Exception as exception:
        print(exception)
    try:
        synced = await bot.tree.sync() # Sync Command Tree
        print(f"Synced {len(synced)} command(s)") # Display results
    except Exception as exception:
        print(exception)
    await bot.change_presence(status=discord.Status.online)
    status_task.start()

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

@bot.tree.command(name="status",description="Picks a new random status")
async def status(interaction: discord.Interaction):
    status = new_status()
    await bot.change_presence(activity=discord.CustomActivity(name=status))
    await interaction.response.send_message(f"""> Changed Status to:\n\n> {status} """,ephemeral=True)

async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            try:
                await bot.load_extension(f"cogs.{filename[:-3]}")
                print(f"> Loaded {filename[:-3]}")
            except Exception as exception:
                print(f"> Error loading {filename[:-3]} - {exception}")

bot.run(settings.TOKEN)