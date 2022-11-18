from .database import db
from config import Config
from .utils import filter
from pyrogram import Client, filters
from pyrogram.errors import ChatAdminRequired
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

@Client.on_message(filters.private & filter.is_not_subscribed)
async def force_sub(bot, message):
    try:
       invite_link = await bot.create_chat_invite_link(int(AUTH_CHANNEL))
    except ChatAdminRequired:
       bot.log.exception("Make Sure Bot Is Admin In Forcesub Channel")
       Config.AUTH_CHANNEL = None 
       return
    button = [[
       InlineKeyboardButton(
                    "🤖 Join Updates Channel", url=invite_link.invite_link)
       ]]
    await message.reply_text(
       text="<b>Please Join My Updates Channel To Use Me !!</b>",
       reply_markup=InlineKeyboardMarkup(button))
    
@Client.on_message(filters.private & filter.is_banned_user)
async def ban_message(bot, message):
    await message.reply_text(f"Sorry Dude 😔, You Were Banned From Using Me 🚫\nContact My Support Group")
    
@Client.on_message(filters.command('ban') & filters.user(Config.OWNER_ID))
async def ban(bot, message):
    if len(message.command) < 2:
       return await message.reply("Give Me A User Id")
    split = message.text.split()
    reason = "No reason provided"
    user_id = split[1]
    if len(split) > 2:
       reason = split[3]
    if user_id.isnumeric():
       user_id = int(user_id)
    try:
       user = await bot.get_users(user_id)
    except Exception as e:
       return await message.reply(f"Error: `{e}`")
    if user.id in Config.BANNED_USERS:
       return await message.reply_text(f"{user.mention} Is Already Banned")
    await db.ban_user(user.id, reason)
    Config.BANNED_USERS.append(user.id)
    await message.reply_text(f"{user.mention} Is Successfully Banned")
    
@Client.on_message(filters.command('unban') & filters.user(Config.OWNER_ID))
async def unban(bot, message):
    if len(message.command) < 2:
       return await message.reply("Give me a user id") 
    user_id = message.text.split()[1]
    if user_id.isnumeric():
      user_id = int(user_id)
    try:
      user = await bot.get_users(user_id)
    except Exception as e:
      return await message.reply(f"Error: `{e}`")
    if user.id not in Config.BANNED_USERS:
       return await message.reply(f"{user.mention} Is Not Banned Yet")
    await db.unban_user(user.id)
    Config.BANNED_USERS.remove(user.id)
    await message.reply_text(f"{user.mention} Is Successfully Unbanned")
