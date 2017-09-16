# Couch bot
### Short description - A discord bot used for a discord server *obviously*.
### Current features:
* Level counting: you get a random xp value between 15 and 40, at an interval of 300 seconds, meaning if you spam in that interval it won't matter.
* Block/unblock command to remove verbose from specific channels.

# Setup
### Dependencies:
* [Discord py](https://github.com/Rapptz/discord.py)
* Python (*obviously*)
### Files needed:
First of all, you need to create a "**auth.py**" file in the main directory. The file needs to contain a variable called __BOT_TOKEN__.
Eg: ```BOT_TOKEN = "wzc02uaFw2SC9u1aMhaJ5RQP.DIqchQ.fir6VJJ4zO1cCNeLnvNMKwW9yCY"```

Next, you'll need to set yourself permission to use the bot's commands like __!block__ or __!unblock__, to do that you simply create a file called "**rights.json**". Syntax:

```json
[
    {
        "owner":["id1", "id2"]
        "admin":["id3", "id4"]
        "helper":["id5", "id6"]
    }
]
```
__Note__: Currently the ***admin*** and ***helper*** ranks are not *in use* meaning you should set yourself to be a owner so you'll have the higher permission.

Now, believe it or not, the setup is complete!
### Starting the bot
To start the bot, open a command terminal in the **directory of the main.py file** and simply write ```python main.py```