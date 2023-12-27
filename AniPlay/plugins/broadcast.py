from AniPlay import app
from AniPlay.plugins.database.userdb import db, user_collection, selected_users_collection, join_counts_collection
from pyrogram import filters, Client
from pyrogram.types import Message
from config import ADMINS

# Empty dictionary to avoid potential issues
user_data = {}

async def send_broadcast(user_id, message_text):
    try:
        await app.send_message(user_id, message_text)
        return True  # Successful
    except Exception as e:
        error_message = str(e)
        if "BLOCKED" in error_message:
            return False  # Blocked
        else:
            return None  # Errors

@app.on_message(filters.command('broadcast') & filters.user(ADMINS))
async def broadcast_command(_, message: Message):
    all_users = list(user_collection.find())
    message_text = message.text.split("/broadcast ", 1)[1]

    successful_users = 0
    failed_users = 0
    blocked_users = 0

    for user_data in all_users:
        user_id = user_data["user_id"]
        result = await send_broadcast(user_id, message_text)

        if result is True:
            successful_users += 1
        elif result is False:
            blocked_users += 1
        else:
            failed_users += 1

    total_users = len(all_users)

    reply_text = (
        f"Broadcast sent!\n"
        f"Successful Users: {successful_users}\n"
        f"Blocked Users: {blocked_users}\n"
        f"Failed Users: {failed_users}\n"
        f"Total Users: {total_users}"
    )

    await message.reply_text(reply_text)

@app.on_message(filters.command('sbroadcast') & filters.user(ADMINS))
async def selected_broadcast_command(_, message: Message):
    selected_users = list(selected_users_collection.find())
    message_text = message.text.split("/sbroadcast ", 1)[1]

    successful_users = 0
    failed_users = 0
    blocked_users = 0

    for user_data in selected_users:
        user_id = user_data["user_id"]
        result = await send_broadcast(user_id, message_text)

        if result is True:
            successful_users += 1
        elif result is False:
            blocked_users += 1
        else:
            failed_users += 1

    total_users = len(selected_users)

    reply_text = (
        f"Selected Broadcast sent!\n"
        f"Successful Users: {successful_users}\n"
        f"Blocked Users: {blocked_users}\n"
        f"Failed Users: {failed_users}\n"
        f"Total Selected Users: {total_users}"
    )

    await message.reply_text(reply_text)
