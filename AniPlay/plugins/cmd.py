from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, InputMediaVideo
from pyrogram import filters
from pyrogram.errors import UserNotParticipant, ChatWriteForbidden
from pymongo import MongoClient
import asyncio
from AniPlay import app
from config import ADMINS, MUST_JOIN
from AniPlay.plugins.database.userdb import ok, user_collection

async def validate_user(user_id, expected_id):
    return str(user_id) == expected_id

async def must_join_channel(message: Message):
    if MUST_JOIN:
        not_joined = []
        for i, channel in enumerate(MUST_JOIN, start=1):
            try:
                await app.get_chat_member(channel, message.from_user.id)
            except UserNotParticipant:
                not_joined.append((channel, i))

        if not_joined:
            buttons = []
            for channel, join_number in not_joined:
                link = "https://t.me/" + channel if channel.isalpha() else (await app.get_chat(channel)).invite_link
                buttons.append([InlineKeyboardButton(f"Join {join_number}", url=link)])

            try:
                await message.reply(
                    "You need to join the following channels to use the bot:",
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                await message.stop_propagation()
            except ChatWriteForbidden:
                pass

@app.on_message(filters.incoming & filters.private, group=-1)
async def must_join_channel_private(client, msg: Message):
    await must_join_channel(msg)

@app.on_message(filters.command('start'))
async def start(_, message: Message):
    await must_join_channel(message)

    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name

    existing_user = user_collection.find_one({"user_id": user_id})

    if existing_user:
        user_collection.update_one({"user_id": user_id}, {"$set": {"username": username}})
    else:
        await ok(user_id, username, first_name, last_name)

    # VIDEO_URL = 'https://graph.org/file/79ba8843dfcfc869c826a.mp4'
    CAPTION = ("""🤖 Mega Giveaway Bot Activation 🚀

Welcome, anime aficionado! 🌟 You're officially part of the Mega Giveaway extravaganza. 🎉

🌊 Next Steps: 
Between December 27th and 28th, our bots will randomly select 150 participants. If you're chosen, watch your DMs on December 28th for exciting details! 📬✨

Unleash your inner anime warrior! Stay tuned. 🚀🔥 #MegaGiveaway #AnimeAdventures""")

    try:
        await message.reply_text(CAPTION)
    except:
        return

@app.on_message(filters.command('stats') & filters.user(ADMINS))
async def stats_command(_, message: Message):
    initial_message = await message.reply_text("Getting user count...")

    # Countdown
    for i in range(3, 0, -1):
        await asyncio.sleep(1)
        await initial_message.edit_text(f"Getting user count... {i}")
        
    await asyncio.sleep(2)
    nano = user_collection.count_documents({})
    await message.reply_text(f"Total users 🫠: {nano}")
