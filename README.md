# TwitchCal

Turn a Twitch streamer's schedule into a calendar!

## Install
```bash
poetry install
# For the lazy...
python3 main.py 
# For the more upstanding
gunicorn 'twitchcal:create_app()'
```
