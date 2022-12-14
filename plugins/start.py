import os
import time
from .database import db 
from config import Config
from translation import Translation
from .utils import __version__ as bot_version
from pyrogram import Client, filters, enums, __version__
from pyrogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

@Client.on_message(filters.command("start"))
async def start(bot, message):
   user = message.from_user
   if not await db.is_user_exist(user.id):
      await db.add_user(user.id)
   await message.reply_text(
        Translation.START_TXT.format(user.mention),
        reply_markup=InlineKeyboardMarkup(
             [[
               InlineKeyboardButton('đ Suppot', url='https://t.me/+eLB5a6LWmdRmOWQx'),
               InlineKeyboardButton('đ Updates', url='https://t.me/Tech_Projects2018')
             ],[
                InlineKeyboardButton("âšī¸ Help", callback_data = "help")
             ]]
         ))
                            
@Client.on_message(filters.command('settings'))
async def settings(bot, message):
    upload_mode = await db.get_uploadmode(message.from_user.id)
    upload_mode = "Default" if not upload_mode else upload_mode
    button = [[
      InlineKeyboardButton('đ Custom Caption', callback_data="custom_caption")
      ],[
      InlineKeyboardButton('đŧī¸ Custom Thumbnail', callback_data="custom_thumbnail")
      ],[
      InlineKeyboardButton(f'đ¤ Upload mode', callback_data="toggle_mode"),
      InlineKeyboardButton(upload_mode, callback_data="toggle_mode")
      ],[
      InlineKeyboardButton('đ Close', callback_data="close")
    ]]
    await message.reply_text(
         text=Translation.SETTINGS_TXT,
         reply_markup=InlineKeyboardMarkup(button))

@Client.on_message(filters.command('stats') & filters.user(Config.OWNER_ID))
async def stats(bot, message):
    user_id = message.from_user.id
    msg = await message.reply_text("Fetching...")
    total, banned = await db.total_users_count() 
    await msg.edit_text(
       f"<b>đ¤ Total Users:</b> `{total}`\n"
       f"<b>đĢ Banned Users:</b> `{banned}`"
    )
   
@Client.on_callback_query()
async def cb_handler(client: Client , query: CallbackQuery):
    data = query.data
    user_id = query.from_user.id
    
    if data == "start":
        await query.message.edit_text(
            text=Translation.START_TXT.format(query.from_user.mention),
            reply_markup=InlineKeyboardMarkup(
             [[
               InlineKeyboardButton('đ Suppot', url='https://t.me/+eLB5a6LWmdRmOWQx'),
               InlineKeyboardButton('đ Updates', url='https://t.me/Tech_Projects2018')
             ],[
                InlineKeyboardButton("âšī¸ Help", callback_data = "help")
             ]]
         )) 
        
    elif data == "help":
        await query.message.edit_text(
            text=Translation.HELP_TXT,
            disable_web_page_preview = True,
            reply_markup=InlineKeyboardMarkup(
                 [[
                 InlineKeyboardButton('đ¤´ Admin Commands', callback_data="owner_cmd"),
                 InlineKeyboardButton('đ¤  About', callback_data="about")
                 ],[
                 InlineKeyboardButton('đ Back', callback_data="start")
            ]]
        ))
        
    elif data == "owner_cmd":
        await query.message.edit_text(
            text=Translation.OWNER_COMMANDS_TXT,
            reply_markup=InlineKeyboardMarkup(
               [[InlineKeyboardButton('đ Back', callback_data="help")]]
        ))
     
    elif data == "about":
        await query.message.edit_text(
            text=Translation.ABOUT_TXT.format(client.me.first_name, client.me.username,
                                             __version__, bot_version),
            disable_web_page_preview = True,
            reply_markup=InlineKeyboardMarkup(
            [[
              InlineKeyboardButton('đ Back', callback_data = "help"),
            ]]
        ))
     
    elif data in ['settings', 'toggle_mode']:
       mode = await db.get_uploadmode(user_id)
       if data == "toggle_mode":
          if not mode:
             mode = "document"
          elif mode == "document":
             mode = "video"
          elif mode == "video":
             mode = "audio"
          else:
             mode = None 
          await db.change_uploadmode(user_id, mode)
       button = [[
         InlineKeyboardButton('đ Custom Caption', callback_data="custom_caption")
         ],[
         InlineKeyboardButton('đŧī¸ Custom Thumbnail', callback_data="custom_thumbnail")
         ],[
         InlineKeyboardButton(f'đ¤ Upload mode', callback_data="toggle_mode"),
         InlineKeyboardButton(mode if mode else "Default", callback_data="toggle_mode")
         ],[
         InlineKeyboardButton('đ Close', callback_data="close")
         ]] 
       await query.message.edit_text(
          text=Translation.SETTINGS_TXT,
          reply_markup=InlineKeyboardMarkup(button))
        
    elif data == "custom_caption":
        await query.message.edit_text(
            text=Translation.CUSTOM_CAPTION_TXT,
            disable_web_page_preview = True,
            reply_markup=InlineKeyboardMarkup(
              [[
                InlineKeyboardButton('đ Show Caption', callback_data="show_caption"),
                InlineKeyboardButton("đī¸ Delete Caption", callback_data="delete_caption")
              ],[
                InlineKeyboardButton('đ Back', callback_data="settings")
              ]]
        ))
             
    elif data =="show_caption":
        caption = await db.get_caption(user_id)
        if not caption:
           return await query.answer("You Don't Add Any Custom Caption âī¸", show_alert=True)
        await query.answer(f"Your Custom Caption:\n\n{caption}", show_alert=True)
        
    elif data == "delete_caption":
        caption = await db.get_caption(user_id)
        if not caption:
           return await query.answer("Nothing Will Found To Delete", show_alert=True)
        await db.set_caption(query.from_user.id, None)
        return await query.answer("Caption Deleted Successfully âī¸", show_alert=True)   
    
    elif data == "custom_thumbnail":
        await query.message.edit_text(
            text=Translation.THUMBNAIL_TXT,
            reply_markup=InlineKeyboardMarkup(
                [[
                InlineKeyboardButton('đ Show Thumbnail', callback_data="show_thumb"),
                InlineKeyboardButton("đī¸ Delete Thumbnail", callback_data="delete_thumb")
                ],[
                InlineKeyboardButton('đ Back', callback_data="settings")
               ]]
        ))
        
    elif data == "show_thumb":
        thumb = await db.get_thumbnail(user_id)
        if not thumb:
           return await query.answer(Translation.THUMB_NOT_FOUND_TXT, show_alert=True)
        await query.message.delete()
        await query.message.reply_photo(thumb)
            
    elif data == "delete_thumb":
        thumb = await db.get_thumbnail(user_id)
        if not thumb:
           return await query.answer(Translation.THUMB_NOT_FOUND_TXT, show_alert=True)
        await db.set_thumbnail(user_id, None)
        return await query.answer(Translation.REMOVE_CUSTOM_THUMB_TXT, show_alert=True)
        
    elif data == "close":
        await query.message.delete()
