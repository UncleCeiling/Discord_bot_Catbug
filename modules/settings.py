# pip install python-dotenv
from discord.opus import APPLICATION_AUDIO
import os, dotenv
dotenv.load_dotenv(".env")
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
APPLICATION_ID = os.getenv("APPLICATION_ID")
def check_env() -> bool:
    """
    Loads the env file and attempts to ingest its contents
    Returns:
        int: `0` Success, `1` Failure getting Token ,`2` Failure getting ID
    """
    if DISCORD_TOKEN == None:
        print("Token is missing - please check.")
        raise
    if APPLICATION_ID == None:
        print("ID is missing - please check.")
        raise
    return True

if __name__ == "__main__":
    print(f"Discord Token = {DISCORD_TOKEN}")
    print(f"Application ID = {APPLICATION_ID}")
