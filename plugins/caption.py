from .database import db 
from pyrogram import Client, filters 

@Client.on_message(filters.command('addcaption'))
async def add_caption(bot, message):
    text = message.text.split(" ", 1)
    user_id = message.from_user.id
    if len(text) == 1:
       return await message.reply_text("Please Provide Your Custom Caption\nEx: `/addcaption <caption>`")
    await db.set_caption(user_id, text[1])
    await message.reply_text("<b>Caption Added Successfully ✔️</b>")
    
@Client.on_message(filters.command('showcaption'))
async def show_caption(bot, message):
    user_id = message.from_user.id
    caption = await db.get_caption(user_id)
    if not caption:
       return await message.reply_text("You Don't Add Any Custom Caption ✖️")
    await message.reply_text(f"<b>Your Custom Caption:</b>\n\n`{caption}`")
