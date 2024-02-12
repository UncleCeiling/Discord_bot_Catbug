import discord
from modules import sky_rogue
from discord import app_commands
from discord.ext import commands
from typing import Optional


class SkyRogue(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("> sky_rogue_cog loaded")

    @app_commands.command(
        name="skyrogue", description="Generate a loadout for a Sky Rogue run."
    )
    @app_commands.describe(
        experimental="Choose whether to include 'Experimental' equipment in the loadout.",
        air="Disable weapons that are specifically for Air-combat.",
        ground="Disable weapons that are specifically for Ground-attack.",
        visible="Make output visible in channel.",
    )
    async def skyrogue(
        self,
        interaction: discord.Interaction,
        experimental: bool = False,
        air: bool = True,
        ground: bool = True,
        visible: bool = False,
    ):
        await interaction.response.send_message(
            f"> Generating...", ephemeral=(not visible)
        )
        loadout = sky_rogue.generate_empty_loadout(experimental)
        loadout = sky_rogue.fill_loadout(
            current_loadout=loadout, experimental=experimental, air=air, ground=ground
        )
        col2,col3 = len(max(loadout.weapon_codes(), key=len)),len(max(loadout.weapon_names(),key=len))
        message = f"""> ## {"__***" + loadout.aircraft.name.upper() + "***__"}
> ` {(loadout.aircraft.type + ' ` -=- ` ' + loadout.aircraft.role).center(col2+col3)} `
> ============{"LOADOUT".center(col2+col3,"=")}============
> `  Micro  ` | ` {loadout.primary.code.center(col2)} ` | ` {loadout.primary.name.center(col3)} ` | ` {loadout.primary.type} `
> ` Weapon1 ` | ` {loadout.secondary1.code.center(col2)} ` | ` {loadout.secondary1.name.center(col3)} ` | ` {loadout.secondary1.type} `
> ` Weapon2 ` | ` {loadout.secondary2.code.center(col2)} ` | ` {loadout.secondary2.name.center(col3)} ` | ` {loadout.secondary2.type} `
> ` Weapon3 ` | ` {loadout.secondary3.code.center(col2)} ` | ` {loadout.secondary3.name.center(col3)} ` | ` {loadout.secondary3.type} `
> ` Special ` | ` {loadout.special.code.center(col2)} ` | ` {loadout.special.name.center(col3)} ` | ` {loadout.special.type} `
> ============{"REMAINING".center(col2+col3,"=")}============
> Payload: {loadout.remaining_budget()[0]} | Avionics: {loadout.remaining_budget()[1]}
"""
        await interaction.edit_original_response(content=message)


async def setup(bot):
    await bot.add_cog(SkyRogue(bot))
