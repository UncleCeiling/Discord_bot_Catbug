# <u>**Catbug-bot**</u>

A stupid bot amongst friends.

Starting out as a project to make a bot that can stream Air-Traffic Control radio chatter into a Discord channel, it has spiralled into a ressurection of the long-dead ***Catbug*** bot.
___
## ***Feature List:***
- Visibility toggle for most commands
- Bot Custom statuses - Cycling Quotes & Emoji from a .csv
- [Radio Streaming](https://stackoverflow.com/questions/61757011/how-to-create-a-discord-bot-that-streams-online-radio-in-python) from [RadioParadise](https://radioparadise.com/listen/stream-links)
___
## ***Commands***
| **CLI** ||
|---|---|
| `/pwd [Visible{False}]` | Prints the location that it is executed in. |
| `/whoami [Visible{False}]` | Prints the username of whoever executes it. |
| `/whois [member{User}] [Visible{False}]` | Display a Dynamic set of information about a specified member. |

| **Fun** ||
|---|---|
| `/penis [member{User}]` | Will generate a graphic for any user, to show-off or hide accordingly. Based on UserID. |

| **Catbug References** ||
|---|---|
| `/status` | Refreshes the bot's status message. |

| **Radio Streaming** ||
|---|---|
| `/radio <Station/Genre> [Quality{64kbps}] [Visible{False}]` |  |

___
## ***To-do List***
|**Features**||
|---|---|
| `Channel Status` | Set and clear Channel Statuses as appropriate |

|**Commands**||
|---|---|
| `Equipment Generator` | A command that generates random equipment based on txt files. Based on the bones of an old project. |
| `/atc <option> [search]` | Ability to stream Air Traffic Control feeds into a channel. |
| `/dad-joke ` | Takes Jokes from lists, might have optional genres. |
| `/catbug <option> [specifics]` | A variety of Catbug references; like gifs, soundbytes and maybe videos? |
| `/CCFlamez` | Auto-mute/Auto-unmute based on rich-presence of Guitar Hero |
| `/monty` | Various Monty Python quotes |


<!--
square brackets [optional option]
angle brackets <required argument>
curly braces {default values}
parenthesis (miscellaneous info)
-->