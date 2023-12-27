from AniPlay import app
from AniPlay.plugins.database.userdb import user_collection
from pyrogram import filters, Client
from pyrogram.types import Message
from config import ADMINS

user_data = {}

# Admin-only
async def send_help_to_admin(admin_user_id):
    help_text = (
        "𝐇𝐞𝐫𝐞 𝐚𝐫𝐞 𝐭𝐡𝐞 𝐚𝐯𝐚𝐢𝐥𝐚𝐛𝐥𝐞 𝐜𝐨𝐦𝐦𝐚𝐧𝐝𝐬 𝐟𝐨𝐫 𝐚𝐝𝐦𝐢𝐧𝐬:\n"
        "/select <value> - Set the selection value for Round 3\n"
        "/round3 - Notify selected users for Round 3\n"
        "/sclear - Clear the list of selected users\n"
        "/shows - Show the list of selected users\n"
        "/slink - Send invite links to selected users\n"
        "/broadcast <message> - Broadcast a message to all users\n"
        "/sbroadcast <message> - Broadcast a message to selected users\n"
        "/help - Show this help message"
    )
    
    await app.send_message(admin_user_id, help_text)

@app.on_message(filters.command('help') & filters.user(ADMINS))
async def help_command(_, message: Message):
    if message.from_user.id in ADMINS:
        await send_help_to_admin(message.from_user.id)
    else:
        await message.reply_text("You don't have permission to use this command.")
