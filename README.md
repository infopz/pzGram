<img src="https://i.postimg.cc/j2J6RK9G/pz-Gram-New2.png" alt="pzGram Logo" width="600">

[![Downloads](http://pepy.tech/badge/pzgram)](http://pepy.tech/count/pzgram)

A pz-way to create your Telegram Bot

```python
import pzgram
bot = pzgram.Bot(BOTKEY)

def hello(chat, message):
    chat.send("Messaggio ricevuto")
    print(message.text)
    
bot.set_commands({"hello": hello})
bot.run()
```

pzgram is a python library that allows you to create your personal Telegram bot, in a very easy way.

English Documentaton [here](https://infopz.github.io/pzgram/)

Developers' Telegram Group [here](https://t.me/joinchat/ATdWXRIuqRInj6V5hhjjPA)

For more information contact me:
* telegram: @infopz
* email: casari.giovanni@gmail.com
* Project Website: [infopz.github.io/pzgram](https://infopz.github.io/pzgram/)
* My website: [infopz.hopto.org](http://infopz.hopto.org/)

**Supported Version**: Python 3.x

**License**: Apache License 2.0
