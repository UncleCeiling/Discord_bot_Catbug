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
        self.experimental = True if type == "Experimental" else False


class Weapon:
    def __init__(
        self,
        slot: int = 0,
        code: str = "EMPTY",
        name: str = "",
        type: str = "",
        target: str = "",
        payload: int = 0,
        avionics: int = 0,
    ):
        self.slot = slot
        self.code = code
        self.name = name
        self.type = type
        self.target = target
        self.payload = payload
        self.avionics = avionics
        self.experimental = True if type == "Experimental" else False


class Loadout:
    def __init__(
        self,
        aircraft: Aircraft = Aircraft(),
        primary: Weapon = Weapon(),
        secondary1: Weapon = Weapon(),
        secondary2: Weapon = Weapon(),
        secondary3: Weapon = Weapon(),
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
        return [
            self.primary.code,
            self.secondary1.code,
            self.secondary2.code,
            self.secondary3.code,
            self.special.code,
        ]

    def weapon_names(self):
        return [
            self.primary.name,
            self.secondary1.name,
            self.secondary2.name,
            self.secondary3.name,
            self.special.name,
        ]

    def weapon_types(self):
        return [
            self.primary.type,
            self.secondary1.type,
            self.secondary2.type,
            self.secondary3.type,
            self.special.type
        ]

def import_sky_rogue_lists(path_to_lists: str):
    """Returns a Dict containing 4 lists, containing Objects of the appropriate class, taken from the files in the specified path:

    {"aircraft" = [aircraft.csv],
    "weapons" = [weapons.csv]}"""
    aircraft, weapons = [], []
    for line in open(path_to_lists + "aircraft.csv", "r").readlines():
        details = line.strip().split(",")
        aircraft.append(
            Aircraft(
                details[0], details[1], details[2], int(details[3]), int(details[4])
            )
        )
    for line in open(path_to_lists + "weapons.csv", "r").readlines():
        details = line.strip().split(",")
        weapons.append(
            Weapon(
                int(details[0]),
                details[1],
                details[2],
                details[3],
                details[4],
                int(details[5]),
                int(details[6]),
            )
        )
    lists = {"aircraft": aircraft, "weapons": weapons}
    return lists


def select_from_list(list_name: str, dict_of_lists: dict):
    return sample(dict_of_lists[list_name], 1)[0]


def generate_empty_loadout(sky_rogue_lists: dict, experimental: bool) -> Loadout:
    aircraft_list = sky_rogue_lists["aircraft"]
    shuffle(aircraft_list)
    for aircraft in aircraft_list:
        if experimental == aircraft.experimental:
            return Loadout(aircraft, Weapon(), Weapon(), Weapon(), Weapon(), Weapon())
    return Loadout()

def find_weapon(
    sky_rogue_lists: dict,
    current_loadout: Loadout,
    slot: int,
    experimental: bool,
    target: str,
):
    weapon_list = sky_rogue_lists["weapons"]
    shuffle(weapon_list)
    for weapon in weapon_list:
        if slot == weapon.slot:
            if weapon.experimental == experimental or weapon.experimental == False:
                if weapon.target == "All" or weapon.target == target:
                    if (weapon.payload <= current_loadout.remaining_budget()[0]) and (
                        weapon.avionics <= current_loadout.remaining_budget()[1]
                    ):
                        return weapon
    return Weapon()


def fill_loadout(
    sky_rogue_lists: dict,
    current_loadout: Loadout,
    experimental: bool,
    target: str,
) -> Loadout:
    choices = [1, 2, 2, 2, 3]
    while len(choices) > 0:
        match choice(choices):
            case 1:  # Primary
                current_loadout.primary = find_weapon(
                    sky_rogue_lists, current_loadout, 1, experimental, target
                )
                choices.remove(1)
            case 2:  # Secondary
                if current_loadout.secondary1.name == "":
                    current_loadout.secondary1 = find_weapon(
                        sky_rogue_lists, current_loadout,2, experimental, target
                    )
                elif current_loadout.secondary2.name == "":
                    current_loadout.secondary2 = find_weapon(
                        sky_rogue_lists, current_loadout,2, experimental, target
                    )
                else:
                    current_loadout.secondary3 = find_weapon(
                        sky_rogue_lists, current_loadout,2, experimental, target
                    )
                choices.remove(2)
            case 3:  # Special
                current_loadout.special = find_weapon(sky_rogue_lists, current_loadout,3,experimental,target)
                choices.remove(3)
    return current_loadout


# # region Testing

# sr_lists = import_sky_rogue_lists(
#     "C:/Users/CodeNation CFarfan/Documents/GitHub/Catbug/cogbot/files/sky_rogue/"
# )
# for x in range(100):
#     loadout = generate_empty_loadout(sr_lists, False)
#     loadout = fill_loadout(sr_lists, loadout, False, "Air")
#     print(
#         f"Aircraft: {loadout.aircraft.name}\nMicros  : {loadout.primary.code}\nSlot 1  : {loadout.secondary1.code} {loadout.secondary1.target}\nSlot 2  : {loadout.secondary2.code} {loadout.secondary2.target}\nSlot 3  : {loadout.secondary3.code} {loadout.secondary3.target}\nSpecial : {loadout.special.code}\n"
#     )

# endregion
