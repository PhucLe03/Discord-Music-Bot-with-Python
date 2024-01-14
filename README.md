# Discord Music Bot with Python

## Available Commands

/help - displays all the available commands\
/join - joins your current channel\
/play \<keyword/youtube link> - finds the song on youtube and plays it in your current channel. Will resume playing the current song if it was paused\
/queue - displays the current music queue\
/skip - skips the current song being played\
/disconnect - Disconnected the bot from the voice channel

## Installation
- To run the discord bot first you need python 3.4 or above.
- Run `pip install -r requirements.txt` to install all of the python dependencies.
- FFMPEG:
    - Windows: Install `ffmpeg` from https://ffmpeg.org/download.html and make sure that the path to the bin folder is in your environment variables. 
    - Linux: run `sudo apt install ffmpeg -y`

## Set Discord Bot's Token
Create a file named `.env` with your Discord bot's token (Instructions to get token [here](https://docs.discordbotstudio.org/setting-up-dbs/finding-your-bot-token)):
```
TOKEN=<your bot's token>
```

## Run and test Bot
Once you complete installing python and bot's dependencies, run `python main.py`.

## References
[pawel02/music_bot](https://github.com/pawel02/music_bot) (Tutorial Video: https://www.youtube.com/watch?v=PJDuI9n7rWE&t=325s&ab_channel=Computeshorts)

