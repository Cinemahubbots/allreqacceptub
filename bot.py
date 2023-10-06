# Auto Approve Bot for Telegram
# Copyright (C) 2023
# Author: Anony (i@anodite.co) <github.com/celestix>
# Programming Language: Python
# Description: A simple telegram bot to auto approve join requests in a group.
# Usage:
# 1. Add the bot to your group as an admin.
# 2. Send /approve <chat_id> to approve all join requests in that group. (OWNER_ONLY)
# 3. Send /adduser <user_id> to add a user to the authorized users list. (OWNER_ONLY)
# 4. Send /rmuser <user_id> to remove a user from the authorized users list.
# 5. Send /ping to check if the bot is alive.
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Afferno General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Afferno General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from re import match
from asyncio import get_event_loop
from functools import wraps
from contextlib import suppress

from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import ChatAdminRequired
from pyrogram.methods.utilities.idle import idle

from config import APP_ID, API_HASH, MOBILE_NUMBER, OWNER_ID
from db import CREATE_TABLE_QUERY, INSERT_USER_QUERY, GET_ALL_USERS_QUERY, DELETE_USER_QUERY

print('Auto Approve Bot by github.com/celestix')

print("[INFO] Initializing bot...")
# create a pyrogram client
app = Client("autobot", api_id=APP_ID, api_hash=API_HASH, phone_number=MOBILE_NUMBER)

print('[INFO] Starting bot...')
# start the pyrogram client
app.start()

print("[INFO] Preparing database...")
# create users table if not exists
app.storage.conn.execute(CREATE_TABLE_QUERY)

print("[INFO] Fetching authorized users...")
# get all authorized users from database
# since fetchall returns the list of tuples, we need to unpack them and get the first element of each tuple
AUTHORIZED_USERS = [i[0] for i in app.storage.conn.execute(GET_ALL_USERS_QUERY).fetchall()]
print("[INFO] AUTHORIZED USERS:", AUTHORIZED_USERS)

# pyrogram error regexp
PYROGRAM_ERROR_SYNTAX_REGEXP = r'.*:\s\[.*\]\s-\s(.*)\s\(caused by ".*"\)'

# decorator to sanitize the commands and block unauthorized access
def sanitize(func):
    @wraps(func)
    async def __run_sanitizer(client: Client, message: Message, *args, **kwargs):
        user_id = message.from_user.id
        # Ignore unauthorized users
        if user_id != OWNER_ID and user_id not in AUTHORIZED_USERS:
            return
        # Ignore bots
        if message.from_user.is_bot:
            return
        return await func(client, message, *args, **kwargs)
    return __run_sanitizer

@app.on_message(filters.command("adduser",prefixes="."))
async def add_user(client: Client, message: Message):
    if message.from_user.id != OWNER_ID:
        return
    args = message.text.split()
    if len(args) < 2:
        await message.reply("You need to provide me a user id as an argument to use this command.")
        return
    try:
        user_id = int(args[1])
    except ValueError:
        await message.reply("You need to provide me a valid integer as a user id.")
        return
    
    client.storage.conn.execute(INSERT_USER_QUERY, (user_id,))
    AUTHORIZED_USERS.append(user_id)
    client.storage.conn.commit()
    
    await message.reply("Success!")

@app.on_message(filters.command("rmuser",prefixes="."))
async def rm_user(client: Client, message: Message):
    if message.from_user.id != OWNER_ID:
        return
    args = message.text.split()
    if len(args) < 2:
        await message.reply("You need to provide me a user id as an argument to use this command.")
        return
    try:
        user_id = int(args[1])
    except ValueError:
        await message.reply("You need to provide me a valid integer as a user id.")
        return
    if not user_id in AUTHORIZED_USERS:
        await message.reply("This user is not even authorized.")
        return
    
    client.storage.conn.execute(DELETE_USER_QUERY, (user_id,))
    AUTHORIZED_USERS.remove(user_id)
    client.storage.conn.commit()

    await message.reply("Success!")

@app.on_message(filters.command("approve", prefixes="."))
@sanitize
async def approve(client: Client, message: Message):
    args = message.text.split()
    if len(args) < 2:
        await message.reply("You need to provide me a chat id as an argument to use this command.")
        return
    try:
        chat_id = int(args[1])
    except ValueError:
        await message.reply("You need to provide me a valid integer as an argument.")
        return

    success = 0
    fails = 0
    
    try:
        async for i in client.get_chat_join_requests(chat_id):
            try:
                success += 1
                await client.approve_chat_join_request(chat_id, i.user.id)
            except Exception as e:
                fails += 1
                print(f"Failed due to: {e}")
    except ChatAdminRequired:
        await message.reply("You need to make me an admin in that chat!")
        return
    except Exception as err:
        re_match = match(PYROGRAM_ERROR_SYNTAX_REGEXP, str(err))
        if re_match:
            err = re_match.group(1)
        await message.reply(f"Failed to process because: {err}")
        return
    
    text = f"Requests have been approved!\nSuccess: {success}\nFails: {fails}"
    await message.reply(text)

@app.on_message(filters.command("ping", "."))
@sanitize
async def ping(_: Client, message: Message):
    await message.reply("Pong")
    return 

print("[INFO] Bot is running...")

loop = get_event_loop()
with suppress(TypeError):
    loop.run_until_complete(idle())

print("[INFO] Bot is stopping...")
app.stop()