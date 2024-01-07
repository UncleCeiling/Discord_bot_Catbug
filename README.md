# 🐞<u>**Catbug-bot**</u>🐞
## 🗒️<u>Contents</u>🗒️
- [A stupid bot amongst friends](#🃏-a-stupid-bot-amongst-friends-🃏)
- [Features](#🛠️-features-🛠️)
  - [Cogs](#⚙️-cogs-⚙️)
  - [Slash commands](#⌨️-slash-commands-⌨️)
  - [Ephemeral outputs](#🫥-ephemeral-outputs-🫥)
  - [Bot Status](#💭-bot-status-💭)
  - [Audio Streaming](#📻-audio-streaming-📻)
- [Commands](#📢-commands-📢)
  - [System](#🖥️-system-🖥️)
  - [Fun](#😆-fun-😆)
  - [Audio](#📻-audio-📻)
- [To-do](#🗓️-to-do-list-🗓️)
- [Other Ideas](#💡-other-ideas-💡)
- [Resources](#📚-resources-📚)
  - [Command Symbology Reference](#🔣-command-symbology-reference-🔣)
  - [Links](#🔗-links-🔗)

# 🃏 <u>A stupid bot amongst friends</u> 🃏
***Catbug*** started out as a project to make a bot that can stream Air-Traffic Control radio chatter into a Discord channel, but it has swiftly spiralled into a ressurection of the long-dead ***Catbug*** bot and playground for a bunch of different features.  

Right now the bot is somewhat closed-off, but that feel free to invite it to your server and have a play.
# 🛠️ <u>Features:</u> 🛠️

## ⚙️ Cogs ⚙️
- Allow the bot to be **modularised** to some degree.
- **Unstable** commands can be built and run **alongside** stable ones without too much interference.
- Improve the **stability** of the bot when dealing with **broken commands** or **unforseen errors**.

## ⌨️ Slash commands ⌨️
- Built in **validation** helps prevent user error or invalid inputs.
- Allows for simple **menus** and **options** navigation.
- Support for **argument descriptions** and other **QoL** features.

## 🫥 Ephemeral outputs 🫥
- Most Commands are **ephemeral** by **default**.
- Commands with the `visible` argument are **non-ephemeral** if `visible` is set to `True`

## 💭 Bot Status 💭
- A library of **custom statuses** are stored in a `.csv` file.
- The Statuses (and Emoji) **cycle periodically**.
- The [`/status`](#status) command can be used to **manually** cycle to a **random** new status.

## 📻 Audio Streaming 📻
- Libraries of **Radio** and **Air-Traffic-Control** streams are stored in a `.csv`, and are accessible via the [`/radio`](#radio-station-visiblefalse) and [`/atc`](#atc-option-visiblefalse) commands.
- Audio can also be streamed from a given **URL**.<br><br>

# 📢 <u>Commands</u> 📢

## 🖥️ <u>System</u> 🖥️

### `/pwd [visible{False}]`
Prints the **location** that it is executed in.

### `/whoami [visible{False}]`
Prints the **username** of whoever executes it.

### `/whois [member{User}] [visible{False}]`
Display a dynamic set of **information about a specified member**.

### `/reboot`
**Reboots** Catbug.  
Can only in DMs and if user is in admin list.  
Runs `git pull`right before shutting down, updating the bot with the latest info from this repo.

### `/status`
Refreshes the bot's status message.<br>

## 😆 <u>Fun</u> 😆

### `/member [member{User}] [visible{False}]`
Will generate a "**graphic**" for a given user.  
Based on **UserID** so the "**graphic**" should be consistent across servers.

### `/rpg <weapon/armour> [modifiers{None}] [visible{False}]`
Uses the `.csv` files in `files/rpg_words` to generate names of **weapons** and **armour**.

## 📻 <u>Audio</u> 📻

### `/vc <join/leave/pause/resume/stop>`
Used to control the bot's access to voice channels.
| Option | Function |
|---|---|
| `join` | The bot will join the vc you are in. |
| `leave` | The bot will leave the vc it is in. |
| `pause` | Playback will be pauses. |
| `resume` | Paused playback is resumed. |
| `stop` | Playback is stopped and cannot be resumed. |

### `/radio <station> [visible{False}]`
Presents options for the stations in the `.csv` in `files/streams`.  
Plays the selected stream in whatever VC you are in.

### `/atc <option> [visible{False}]`
Presents options for the ATC towers in the `.csv` in `files/streams`.  
Plays the selected stream in whatever VC you are in.

### `/stream <url>`
Streams any given url into whatever VC you are in.<br>

# 🗓️ <u>To-do List</u> 🗓️

|**Features**||
|---|---|
| `Channel Status` | Set and clear Channel Statuses as appropriate |
| `Reboot command` | Send message to admin if non-admin tries to reboot |
| `Birthday Announcements` | Makes announcements on people's Birthdays |

|**Commands**||
|---|---|
| `/dad-joke ` | Takes Jokes from lists, might have optional genres. |
| `/catbug <option> [specifics]` | A variety of Catbug references; like gifs, soundbytes and maybe videos? |
| `/CCFlamez` | Auto-mute/Auto-unmute based on rich-presence of Guitar Hero |
| `/monty` | Various Monty Python quotes |

# 💡 <u>Other Ideas</u> 💡

| Idea | Description |
|---|---|
| `Discord Shell` | Find a way to use a discord bot as a shell. |

# 📚 <u>Resources</u> 📚

## 🔣 <u>Command Symbology Reference</u> 🔣

| Symbol | Eg. | Meaning |
|---:|:---:|:---|
| Square Brackets | `[ ]` | **Optional** argument |
| Angled Brackets | `< >` | **Required** argument |
| Curly Braces | `{ }` | **Default** value |
| Parenthesis | `( )` | **Miscellaneous** info |

## 🔗 <u>Links</u> 🔗

- [Stack overflow thread about streaming radio with discord.py](https://stackoverflow.com/questions/61757011/how-to-create-a-discord-bot-that-streams-online-radio-in-python)
- [RadioParadise - An exellent online radio](https://radioparadise.com/listen/stream-links)
- [UKRadioLive - Links to radio stations](https://ukradiolive.com/)