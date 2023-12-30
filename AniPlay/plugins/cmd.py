from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram import filters
from pyrogram.errors import UserNotParticipant, ChatWriteForbidden
from pymongo import MongoClient
import asyncio
from AniPlay import app
from config import ADMINS, MUST_JOIN
from AniPlay.plugins.database.userdb import ok, user_collection, get_user_points, join_counts_collection, referral_cache


async def validate_user(user_id, expected_id):
    return str(user_id) == expected_id


# New command to generate referral link
@app.on_message(filters.command('refer'))
async def generate_referral_link(_, message: Message):
    user_id = message.from_user.id
    referral_link = f"https://t.me/Super_GiveawayBot?start={user_id}"

    await message.reply_text(f"Your Referral Link:\n{referral_link}\n\nShare this link with your friends and get 1 point for each referral!")

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

            # Add a "Try Again" button that restarts the bot
                        # Add a "Try Again" button that restarts the bot
            if len(message.command) > 1:
                buttons.append(
                    [InlineKeyboardButton("Try Again", url=f"https://t.me/Super_GiveawayBot?start={message.command[1]}")])
            else:
                buttons.append([InlineKeyboardButton("Try Again", url="https://t.me/Super_GiveawayBot?start")])

            try:
                await message.reply(
                    "You need to join the following channels to use the bot so Please join them to proceed.\n\nIf you have already joined, press the try again button below to continue:",
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
    # Check for channel joins
    await must_join_channel(message)

    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name

    existing_user = user_collection.find_one({"user_id": user_id})

    if existing_user:
        user_collection.update_one({"user_id": user_id}, {"$set": {"username": username}})
        CAPTION = """🤖 Mega Giveaway Bot 🚀

Welcome, anime aficionado! 🌟 You're officially part of the Mega Giveaway extravaganza. 🎉

🌊 Round 1: 
🔗 Referral Game Plan:
1. Start the Mentioned Bot.
2. Type /refer to get your refferal link.
3. Share the link with friends, fellow anime fans, and others.
4. When someone clicks on your referral link and follows the specified action (like joining a group or channel), you may receive referral point.

📊 Leaderboard Check:
- Use /leaderboard to view your position in the table; gather more people if your name is not there, secure your position in top 50 spot and make your way to Round 2.
Unleash your inner anime warrior! Stay tuned. 🚀🔥 #MegaGiveaway #AnimeOcean #AnimeEdge #AnimeSupernova #logoplanet"""
        try:
            await message.reply_text(CAPTION)
        except:
            return

    else:
        # Updated to include the referral logic
        referrer_id = None

        # Check if the /start command has arguments
        if len(message.command) > 1:
            referrer_id = message.command[1]

        print(f"User ID: {user_id}, Referrer ID: {referrer_id}")

        if referrer_id:
            await ok(user_id, username, first_name, last_name, referrer_id)
        else:
            await ok(user_id, username, first_name, last_name)

        # Print points for debugging
        user_points = get_user_points(user_id)
        print(f"User ID: {user_id}, Points: {user_points}")

        if referrer_id:
            await message.reply_text(
                "🌟 Hoorayyy! 🌟\n\nGreat news! Your referral point has been added to the participant. 🎉 Let's cross our fingers for strong support that propels them into Round 2 and closer to our mega prizes!\n\n🚀 Want to join the fun and win mega prizes (https://t.me/MegaaGiveaway/13)? Follow these steps:\n1. Type /refer\n2. Invite other users to start the bot through your referral link.\n\nBe part of this amazing competition and amplify the excitement! 🌈✨")
        else:
            # Your existing response message...
            CAPTION = """🤖 Mega Giveaway Bot 🚀

Welcome, anime aficionado! 🌟 You're officially part of the Mega Giveaway extravaganza. 🎉

🌊 Round 1: 
🔗 Referral Game Plan:
1. Start the Mentioned Bot.
2. Type /refer to get your refferal link.
3. Share the link with friends, fellow anime fans, and others.
4. When someone clicks on your referral link and follows the specified action (like joining a group or channel), you may receive referral point.

📊 Leaderboard Check:
- Use /leaderboard to view your position in the table; gather more people if your name is not there, secure your position in top 50 spot and make your way to Round 2.
Unleash your inner anime warrior! Stay tuned. 🚀🔥 #MegaGiveaway #AnimeOcean #AnimeEdge #AnimeSupernova #logoplanet"""
            try:
                await message.reply_text(CAPTION)
            except:
                return

@app.on_message(filters.command('points'))
async def check_points(_, message: Message):
    user_id = message.from_user.id
    points = get_user_points(user_id)  # Remove 'await' here

    await message.reply_text(f"Your Referral Points: {points}")

# New command to show the top 50 referrers
@app.on_message(filters.command('leaderboard'))
async def show_leaderboard(_, message: Message):
    leaderboard_text = "Top 50 Referrers:\n\n"

    # Retrieve the top 50 referrers based on points
    top_referrers = join_counts_collection.find().sort("count", -1).limit(50)

    # Format the leaderboard text
    for i, referrer in enumerate(top_referrers, start=1):
        user_id = referrer["user_id"]
        points = referrer["count"]

        try:
            # Use get_users to get user information
            user = await _.get_users(user_id)

            # Extract the first name from the user
            first_name = user.first_name
            last_name = user.last_name
            # Create a profile link
            profile_link = f"tg://user?id={user_id}"
            full_name = f"{first_name} {last_name}" if last_name else first_name
            leaderboard_text += f"{i}. User: [{full_name}]({profile_link}), Points: {points}\n"
        except Exception as e:
            profile_link = f"tg://user?id={user_id}"
            leaderboard_text += f"{i}. User ID: [{user_id}]({profile_link}), Points: {points}\n"

    # Send the leaderboard to the user
    await message.reply_text(leaderboard_text)

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
