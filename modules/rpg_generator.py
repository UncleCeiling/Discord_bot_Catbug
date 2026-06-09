from random import sample

def import_rpg_words(path_to_lists: str):
    """Returns a Dict containing 4 lists, taken from the files in the specified path:

    {"adjectives" = [adjectives.csv],
    "weapons" = [weapons.csv],
    "armour" = [armour.csv],
    "nouns" = [nouns.csv]}"""
    adjectives = (open(path_to_lists + "adjectives.csv","r").readlines())[0].split(",")
    weapons = (open(path_to_lists + "weapons.csv", "r").readlines())[0].split(",")
    armour = (open(path_to_lists + "armour.csv", "r").readlines())[0].split(",")
    nouns = (open(path_to_lists + "nouns.csv", "r").readlines())[0].split(",")
    rpg_words = {"adjectives":adjectives,"weapons":weapons,"armour":armour,"nouns":nouns}
    return rpg_words

def gen_equipment(equipment_list:list[str],noun_list:list[str]):
    """Returns a random combination of equipment and noun from the given lists."""
    sample1 = sample(equipment_list,1)[0]
    sample2 = sample(noun_list,1)[0]
    return (f"{sample1} of {sample2}".title())

def add_modifier(equipment_in:str,num_of_buffs:int,adjectives_list:list[str]):
    """Returns a buffed version of a given bit of equipment.
    
    Takes the equipment to be buffed, number of buffs and list of adjectives."""
    sampled_adjectives = sample(adjectives_list,num_of_buffs)
    buff = ", ".join(sampled_adjectives)
    return (f"{buff}, {equipment_in}".title())