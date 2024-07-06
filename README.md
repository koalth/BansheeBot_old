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



## Open Source
Feel free to contribute features, bug fixes, or tranlations to help improve Banshee Bot.
