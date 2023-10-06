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

CREATE_TABLE_QUERY = """
CREATE TABLE IF NOT EXISTS users (
    id  INTEGER PRIMARY KEY
);
"""

INSERT_USER_QUERY = "INSERT OR IGNORE INTO users (id) VALUES (?);"

DELETE_USER_QUERY = "DELETE FROM users WHERE id = ?;"

GET_ALL_USERS_QUERY = "SELECT * FROM users;"
