# Twitch bot
simple twitch chat bot

# how to use
setup env variables `TWITCH_NICK` to twitch bot username and `TWITCH_PASS` to bot oauth [irc token](https://twitchapps.com/tmi/)

then clone repository
```bash
git clone https://github.com/e6000000000/twitch-bot.git
cd twitch-bot
```

in `config.py` setup `COMMANDS` like
```python
{
    r'regular expression. will be searched in message.': 'response. write {user}. it will be replased with username of message author',
    r'^another one$': 'another one',
}
```

start bot
```bash
python3 bot.py
```

