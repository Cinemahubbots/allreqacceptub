# Auto Approval Bot

A telegram userbot that automatically approves pending join requests in a chat. It can be used to approve join requests in bulk.

## Features
- Fast and efficient
- Can be used to approve join requests in bulk
- Written in Pyrogram
- Easy to use

## Usage
First of all, add the bot to your chat as an admin with can manage users permission. Then, send the following command in private chat with the userbot:
```.approve <chat_id>``` where ```<chat_id>``` is the ID of the chat you want to approve join requests in.

All commands:
- ```.approve <chat_id>``` - Approve join requests in the chat you added the bot to
- ```.ping``` - Check if the bot is online
- ```.adduser <user_id>``` - Authorize a user to use the bot
- ```.rmuser <user_id>``` - Deauthorize a user from using the bot


## Installation
To run this userbot, follow these steps:

1. Run ```pip3 install -r requirements.txt``` to install the required dependencies
2. Rename ```sample.config.py``` to ```config.py```
3. Add your configuration variables to ```config.py```
4. Run the bot by executing ```python3 bot.py```

For more information on how to configure the bot, please refer to the comments in config.py.

## License
This project is licensed under the AGPL-3.0 License. See the [LICENSE](LICENSE) file for details.