# Import functions from libraries

from time import sleep
from os import chdir, path                              # To set Working Directory
from random import sample, randint, shuffle, choice            # For sampling lists
from math import ceil                                   #For rounding purposes

# Set Working directory to file directory

chdir(path.dirname(__file__))

# Import data from .txt into arrays - example layout:
# var_name = (open("txt_file_name.txt","r").readlines())[0].split(",")

adjective = (open("storage/adjectives.txt","r").readlines())[0].split(",")
wep_noun = (open("storage/weapon_nouns.txt", "r").readlines())[0].split(",")
arm_noun = (open("storage/armour_nouns.txt", "r").readlines())[0].split(",")
noun2 = (open("storage/nouns2.txt", "r").readlines())[0].split(",")

# Functions

def gen_weapon(): # Call to generate a weapon - returns a string
    sample_noun1 = sample(wep_noun,1)[0]
    sample_noun2 = sample(noun2,1)[0]
    return (f"{sample_noun1} of {sample_noun2}".title())

def gen_armour(): # Call to generate armour - returns a string
    sample_noun1 = sample(arm_noun,1)[0]
    sample_noun2 = sample(noun2,1)[0]
    return (f"{sample_noun1} of {sample_noun2}".title())

def add_buff(equip_in,num_of_buffs): # Call to add adjective to equipment - takes equipment name and number of buffs needed- returns a string
    sample_adj = sample(adjective,num_of_buffs)
    buff = ' '.join(sample_adj)
    return (f"{buff} {equip_in}".title())