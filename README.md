<h1 align="center">Banshee Bot</h1>
<p align="center">The Revenants' very own discord bot!</p>


### What is Banshee Bot?
Banshee Bot allows Discord server owners to define their own roster of players and compile reports directly in Discord.


**Planned Features**

- Query RaiderIO character data directly in discord
- Create custom rosters based on discord roles
- Weekly, monthly and season summary reports for individual characters and the guild


## Installing

**Python 3.8 or higher is required**

Clone the git repo or download files manually. 

    git clone git@github.com:koalth/BansheeBot.git

Open the project in your favorite code editor

Create a [new virtual environment and activate it](https://docs.python.org/3/library/venv.html)


Install all the project's dependencies, use this command:

    # Linux/macOS

    python3 -m pip install -r requirements.txt

    # Windows
    py -3 -m pip install -r requirements.txt

Create a new ``.env`` file in the project directory. Add your discord bot's token as so:

    DISCORD_TOKEN=###

Start the bot up using this command:

    # Linux/macOS

    python3 -m src

    # Windows
    py -3 -m src

## Example

Once you add the bot to the server you will get a dm. Here I want to have the initial setup workflow but for now that is handled in the discord server.

![bot_added_dm](/docs/imgs/bot_added_dm.png)


Next you will need to set the wow guild for the discord server so now all the guild commands will associated with the added guild.

![set_wow_guild_for_server](/docs/imgs/set_wow_guild_for_server.png)

Then you will need to add the wow characters that are in the guild. I hope to make this a role-specific command, where every user with said role sets up their character themselves.

![add_wow_characters](/docs/imgs/add_wow_characters_to_track.png)

Finally we have the guild summary command which will showcase all the guild details currently being tracked. This is an early iteration of the roster functionality which will allow admins to track specific characters and show a small summary of their stats

![view_guild_summary](/docs/imgs/view_guild_summary.png)


## Open Source
Feel free to contribute features, bug fixes, or tranlations to help improve Banshee Bot.
