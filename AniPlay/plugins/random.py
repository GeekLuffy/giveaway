from AniPlay import app
from AniPlay.plugins.database.userdb import db, ok, user_collection, join_counts_collection, selected_users_collection
import random
from pyrogram import filters, Client
from pyrogram.types import Message
from config import ADMINS

user_data = {}

@app.on_message(filters.command('round3') & filters.user(ADMINS))
async def round3_command(_, message: Message):
    selection_value = db.selection_value.find_one({})["value"] if db.selection_value.find_one({}) else 0

    all_users = list(user_collection.find())

    selected_users = random.sample(all_users, min(selection_value, len(all_users)))

    for user_data in all_users:
        user_id = user_data["user_id"]
        if user_data in selected_users:
            await app.send_message(user_id, f"Congratulations! You are selected for Round 3!")
            selected_users_collection.insert_one(user_data)
        else:
            await app.send_message(user_id, "Better luck next time. Thank you for participating!")

    await message.reply_text("Round 3 notifications sent to users.")

@app.on_message(filters.command('select') & filters.user(ADMINS))
async def select_command(_, message: Message):
    try:
        value = int(message.command[1])
    except (IndexError, ValueError):
        await message.reply_text("Invalid command usage. Please use /select <value>")
        return

    db.selection_value.update_one({}, {"$set": {"value": value}}, upsert=True)

    await message.reply_text(f"Selection value set to {value}. Use /round3 to notify users.")

@app.on_message(filters.command('sclear') & filters.user(ADMINS))
async def clear_selected_wrapper(_, message: Message):
    selected_users_collection.delete_many({})

    await message.reply_text("Selected users list cleared.")

@app.on_message(filters.command('shows') & filters.user(ADMINS))
async def show_selected_wrapper(_, message):
    selected_users = list(selected_users_collection.find())

    if not selected_users:
        await message.reply_text("No users have been selected yet.")
        return

    selected_users_info = "\n".join(
        [f"{user['user_id']} - @{user.get('username', 'No username')}" for user in selected_users]
    )

    await message.reply_text(f"Selected Users:\n{selected_users_info}")

async def send_invite_link(user_id, channel_username):
    try:
        chat = await app.get_chat(channel_username)
        invite_link = await app.create_chat_invite_link(chat.id)

        user_id_str = str(user_id)
        user_info = f"@{user_id_str}" if user_id_str.startswith('@') else f"{user_id_str}"

        link_name = f"{user_data.get('username', 'User')} Link"

        message_text = f"Your Invite Link {link_name}: {invite_link.invite_link} as {user_info}"
        await app.send_message(user_id, message_text)
    except Exception as e:
        print(f"Error sending invite link to {user_id}: {str(e)}")

@app.on_message(filters.command('slink') & filters.user(ADMINS))
async def send_link_command(_, message: Message):
    selected_users = list(selected_users_collection.find())

    if not selected_users:
        await message.reply_text("No users have been selected yet.")
        return

    for user_data in selected_users:
        user_id = user_data["user_id"]
        username = user_data.get("username", "")
        if username:
            await send_invite_link(user_id, '@Encode_Status')  # Replace with your actual channel username
        else:
            await app.send_message(user_id, "Your selected user does not have a username. Please contact the admin.")

    await message.reply_text("Invite links sent to selected users.")
