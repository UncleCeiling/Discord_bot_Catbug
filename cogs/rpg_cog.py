import discord
from modules import rpg_generator
from discord import app_commands
from discord.ext import commands
from typing import Optional

rpg_words = rpg_generator.import_rpg_words("data/rpg_words/")

class Rpg(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("> rpg_cog loaded")
    
    @app_commands.command(name="rpg",description="Generate an RPG item.")
    @app_commands.describe(item_type="Type of Item to generate.",modifiers="How many modifiers should the item have?",visible="Make output visible in channel?")
    @app_commands.choices(item_type=[
        app_commands.Choice(name="weapon", value="1"),
        app_commands.Choice(name="armour", value="2")
        ])
    async def rpg(self, interaction:discord.Interaction,item_type:app_commands.Choice[str],modifiers:Optional[int]=0,visible:Optional[bool]=False):
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

async def setup(bot):
        await bot.add_cog(Rpg(bot))