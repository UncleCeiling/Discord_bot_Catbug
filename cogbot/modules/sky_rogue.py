from random import sample, shuffle, choice


class Aircraft:
    def __init__(
        self,
        name: str = "EMPTY",
        type: str = "",
        role: str = "",
        payload: int = 0,
        avionics: int = 0,
    ):
        self.name = name
        self.type = type
        self.role = role
        self.payload = payload
        self.avionics = avionics


class Weapon:
    def __init__(
        self,
        code: str = "EMPTY",
        name: str = "",
        type: str = "",
        payload: int = 0,
        avionics: int = 0,
    ):
        self.code = code
        self.name = name
        self.type = type
        self.payload = payload
        self.avionics = avionics


class Secondary(Weapon):
    def __init__(
        self,
        code: str = "EMPTY",
        name: str = "",
        type: str = "",
        payload: int = 0,
        avionics: int = 0,
        air: bool = False,
        ground: bool = False,
    ):
        super().__init__(code, name, type, payload, avionics)
        self.air = True if air == 0 or air == "0" else False
        self.ground = True if ground == 0 or ground == "0" else False


class Loadout:
    def __init__(
        self,
        aircraft: Aircraft = Aircraft(),
        primary: Weapon = Weapon(),
        secondary1: Secondary = Secondary(),
        secondary2: Secondary = Secondary(),
        secondary3: Secondary = Secondary(),
        special: Weapon = Weapon(),
    ):
        self.aircraft = aircraft
        self.primary = primary
        self.secondary1 = secondary1
        self.secondary2 = secondary2
        self.secondary3 = secondary3
        self.special = special

    def budget(self):
        return (self.aircraft.payload, self.aircraft.avionics)

    def cost(self):
        return (
            sum(
                (
                    self.primary.payload,
                    self.secondary1.payload,
                    self.secondary2.payload,
                    self.secondary3.payload,
                    self.special.payload,
                )
            ),
            sum(
                (
                    self.primary.avionics,
                    self.secondary1.avionics,
                    self.secondary2.avionics,
                    self.secondary3.avionics,
                    self.special.avionics,
                )
            ),
        )

    def remaining_budget(self):
        return (self.budget()[0] - self.cost()[0], self.budget()[1] - self.cost()[1])
    
    def weapon_codes(self):
        return [self.primary.code,self.secondary1.code,self.secondary2.code,self.secondary3.code,self.special.code]
    def weapon_names(self):
        return [self.primary.name,self.secondary1.name,self.secondary2.name,self.secondary3.name,self.special.name]


def import_sky_rogue_lists(path_to_lists: str):
    """Returns a Dict containing 4 lists, containing Objects of the appropriate class, taken from the files in the specified path:

    {"aircraft" = [aircraft.csv],
    "primaries" = [primaries.csv],
    "secondaries" = [secondaries.csv],
    "specials" = [specials.csv]}"""
    aircraft, primaries, secondaries, specials = [], [], [], []
    for line in open(path_to_lists + "aircraft.csv", "r").readlines():
        details = line.strip().split(",")
        aircraft.append(
            Aircraft(
                details[0], details[1], details[2], int(details[3]), int(details[4])
            )
        )
    for line in open(path_to_lists + "primaries.csv", "r").readlines():
        details = line.strip().split(",")
        primaries.append(
            Weapon(details[0], details[1], details[2], int(details[3]), int(details[4]))
        )
    for line in open(path_to_lists + "secondaries.csv", "r").readlines():
        details = line.strip().split(",")
        secondaries.append(
            Secondary(
                details[0],
                details[1],
                details[2],
                int(details[3]),
                int(details[4]),
                True if details[5] == "1" else False,
                True if details[6] == "1" else False,
            )
        )
    for line in open(path_to_lists + "specials.csv", "r").readlines():
        details = line.strip().split(",")
        specials.append(
            Weapon(details[0], details[1], details[2], int(details[3]), int(details[4]))
        )
    lists = {
        "aircraft": aircraft,
        "primaries": primaries,
        "secondaries": secondaries,
        "specials": specials,
    }
    return lists


def select_from_list(list_name: str, dict_of_lists: dict):
    return sample(dict_of_lists[list_name], 1)[0]


def is_experimental(item_to_check: Aircraft | Weapon):
    return True if "Experimental" in item_to_check.type else False


def generate_empty_loadout(sky_rogue_lists:dict,experimental: bool = False) -> Loadout:
    aircraft_list = sky_rogue_lists["aircraft"]
    shuffle(aircraft_list)
    for aircraft in aircraft_list:
        if not experimental and is_experimental(aircraft):
            pass
        else:
            return Loadout(
                aircraft, Weapon(), Secondary(), Secondary(), Secondary(), Weapon()
            )
    return Loadout()


def find_primary(sky_rogue_lists:dict,current_loadout: Loadout, experimental: bool) -> Weapon:
    weapon_list = sky_rogue_lists["primaries"]
    shuffle(weapon_list)
    for weapon in weapon_list:
        if experimental != is_experimental(weapon) or experimental == True:
            if (weapon.payload <= current_loadout.remaining_budget()[0]) and (weapon.avionics <= current_loadout.remaining_budget()[1]):
                return weapon
    return Weapon()


def find_secondary(sky_rogue_lists:dict,
    current_loadout: Loadout,
    experimental: bool,
    air: bool,
    ground: bool,
) -> Secondary:
    weapon_list = sky_rogue_lists["secondaries"]
    shuffle(weapon_list)
    for weapon in weapon_list:
        if experimental != is_experimental(weapon) or experimental == True:
            if (False if weapon.air == True and air == False else True) and (False if weapon.air == True and air == False else True):
                if (weapon.payload <= current_loadout.remaining_budget()[0]) and (weapon.avionics <= current_loadout.remaining_budget()[1]):
                    return weapon
    return Secondary()


def find_special(sky_rogue_lists:dict,current_loadout: Loadout) -> Weapon:
    weapon_list = sky_rogue_lists["specials"]
    shuffle(weapon_list)
    for weapon in weapon_list:
        if (weapon.payload <= current_loadout.remaining_budget()[0]) and (
            weapon.avionics <= current_loadout.remaining_budget()[1]
        ):
            return weapon
    return Weapon()


def fill_loadout(sky_rogue_lists:dict,
    current_loadout: Loadout,
    experimental: bool,
    air: bool,
    ground: bool,
) -> Loadout:
    choices = [1, 2, 2, 2, 3]
    while len(choices) > 0:
        match choice(choices):
            case 1:  # Primary
                current_loadout.primary = find_primary(sky_rogue_lists,current_loadout,experimental)
                choices.remove(1)
            case 2:  # Secondary
                if current_loadout.secondary1.name == "":
                    current_loadout.secondary1 = find_secondary(sky_rogue_lists,
                        current_loadout, experimental, air, ground
                    )
                elif current_loadout.secondary2.name == "":
                    current_loadout.secondary2 = find_secondary(sky_rogue_lists,
                        current_loadout, experimental, air, ground
                    )
                else:
                    current_loadout.secondary3 = find_secondary(sky_rogue_lists,
                        current_loadout, experimental, air, ground
                    )
                choices.remove(2)
            case 3:  # Special
                current_loadout.special = find_special(sky_rogue_lists,current_loadout)
                choices.remove(3)
    return current_loadout

# sr_lists = import_sky_rogue_lists("C:/Users/CodeNation CFarfan/Documents/GitHub/Catbug/cogbot/files/sky_rogue/")

# # region Testing

# loadout = generate_empty_loadout(sr_lists)
# loadout = fill_loadout(sr_lists,loadout,False,False,False)

# print(loadout.budget())
# print(loadout.cost())
# print(loadout.remaining_budget())

# print(
#     f"Aircraft: {loadout.aircraft.name}\nMicros  : {loadout.primary.code}\nSlot 1  : {loadout.secondary1.code}\nSlot 2  : {loadout.secondary2.code}\nSlot 3  : {loadout.secondary3.code}\nSpecial : {loadout.special.code}"
# )

# endregion
