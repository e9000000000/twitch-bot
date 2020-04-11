# Twitch bot
simple twitch chat bot

# how to use
open py file and write your twitch nickname to "NICK" and "[irc token](https://twitchapps.com/tmi/)" to PASS.

in main fuction u can see
```python
stream.chat.add_in_answers("алло", lambda username: f"@{username}, че аллокаешь")
```
in this example if someone wrote in his message "алло" bot will write "@someone, че аллокаешь"

for
```python
stream.chat.add_only_answers("украине\r\n", lambda username: "СЛАВА")
```
if someones message consist only of "украине" word, bot will write "СЛАВА"


after this start the programm.
write chanel and u can see messages from chat.

* type "/run" to start bot
* type "/stop" to stop bot
* type "/clear" to clear terminal
* type message with not "/" first symbol to write it to chat

