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
        target="Choose which types of weapons to include.",
        experimental="Choose whether to include 'Experimental' equipment in the loadout.",
        visible="Make output visible in channel.",
    )
    @app_commands.choices(target=[
        app_commands.Choice(name="All",value="All"),
        app_commands.Choice(name="Air",value="Air"),
        app_commands.Choice(name="Ground",value="Ground")
    ])
    async def skyrogue(
        self,
        interaction: discord.Interaction,
        target: app_commands.Choice[str],
        experimental: bool = False,
        visible: bool = False,
    ):
        await interaction.response.send_message(
            f"> Generating loadout...", ephemeral=(not visible)
        )
        sr_lists = sky_rogue.import_sky_rogue_lists("./files/sky_rogue/")
        loadout = sky_rogue.generate_empty_loadout(sr_lists,experimental)
        loadout = sky_rogue.fill_loadout(sky_rogue_lists=sr_lists,
            current_loadout=loadout, experimental=experimental, target=target.value
        )
        col2,col3,col4 = len(max(loadout.weapon_codes(), key=len)),len(max(loadout.weapon_names(),key=len)),len(max(loadout.weapon_types(),key=len))
        message = f"""> ## {"__***" + loadout.aircraft.name.upper() + "***__"}
> ` {(loadout.aircraft.type + ' ` -=- ` ' + loadout.aircraft.role).center(col2+col3)} `
> ============{"LOADOUT".center(col2+col3,"=")}============
> `  Micro  ` | ` {loadout.primary.code.center(col2)} ` | ` {loadout.primary.name.center(col3)} ` | ` {loadout.primary.type.center(col4)} ` | ` {loadout.primary.target} `
> ` Weapon1 ` | ` {loadout.secondary1.code.center(col2)} ` | ` {loadout.secondary1.name.center(col3)} ` | ` {loadout.secondary1.type.center(col4)} ` | ` {loadout.secondary1.target} `
> ` Weapon2 ` | ` {loadout.secondary2.code.center(col2)} ` | ` {loadout.secondary2.name.center(col3)} ` | ` {loadout.secondary2.type.center(col4)} ` | ` {loadout.secondary2.target} `
> ` Weapon3 ` | ` {loadout.secondary3.code.center(col2)} ` | ` {loadout.secondary3.name.center(col3)} ` | ` {loadout.secondary3.type.center(col4)} ` | ` {loadout.secondary3.target} `
> ` Special ` | ` {loadout.special.code.center(col2)} ` | ` {loadout.special.name.center(col3)} ` | ` {loadout.special.type.center(col4)} ` | ` {loadout.special.target} `
> ============{"REMAINING".center(col2+col3,"=")}============
> Payload: {loadout.remaining_budget()[0]} | Avionics: {loadout.remaining_budget()[1]}
"""
        await interaction.edit_original_response(content=message)


async def setup(bot):
    await bot.add_cog(SkyRogue(bot))
