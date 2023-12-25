from pyrogram.types import Message
from pyrogram import filters
from pymongo import MongoClient
from AniPlay import app
import asyncio
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import UserNotParticipant, ChatWriteForbidden
from config import ADMINS, DB_URI, DB_NAME, MUST_JOIN

client = MongoClient(DB_URI)
db = client[DB_NAME]
user_collection = db["genvnano"]

async def validate_user(user_id, expected_id):
    return str(user_id) == expected_id

async def must_join_channel(message: Message):
    if MUST_JOIN:
        not_joined = []
        for channel in MUST_JOIN:
            try:
                await app.get_chat_member(channel, message.from_user.id)
            except UserNotParticipant:
                not_joined.append(channel)

        if not_joined:
            buttons = []
            for channel in not_joined:
                link = "https://t.me/" + channel if channel.isalpha() else (await app.get_chat(channel)).invite_link
                buttons.append([InlineKeyboardButton(f"Join {channel}", url=link)])

            try:
                await message.reply(
                    "You need to join the following channels to use the bot:",
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                await message.stop_propagation()
            except ChatWriteForbidden:
                pass

async def ok(user_id, username, first_name, last_name):
    user_data = {
        "user_id": user_id,
        "username": username,
        "first_name": first_name,
        "last_name": last_name,
    }
    user_collection.insert_one(user_data)

@app.on_message(filters.incoming & filters.private, group=-1)
async def must_join_channel_private(client, msg: Message):
    await must_join_channel(msg)

@app.on_message(filters.command('start'))
async def start(_, message: Message):
    await must_join_channel(message)

    await ok(
        message.from_user.id,
        message.from_user.username,
        message.from_user.first_name,
        message.from_user.last_name
    )

    try:
        await message.reply_text('hmmm ok ab aage kya karna he???')
    except:
        return

@app.on_message(filters.command('stats') & filters.user(ADMINS))
async def stats_command(_, message: Message):
    initial_message = await message.reply_text("Getting user count...")

    # Countdown
    for i in range(3, 0, -1):
        await asyncio.sleep(1)
        await initial_message.edit_text(f"Getting user count... {i}")

    await message.reply_sticker("CAACAgUAAx0CfMPc0gACBkRliZ6Xw5THI5Wx2lCEtTni-CYeFwACBAADwSQxMYnlHW4Ls8gQHgQ")

    await asyncio.sleep(2)

    await app.delete_messages(chat_id=message.chat.id, message_ids=[message.message_id])

    nano = user_collection.count_documents({})
    await message.reply_text(f"Total users 🫠: {nano}")
