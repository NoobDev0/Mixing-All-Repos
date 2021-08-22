#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) @AlbertEinsteinTG

from pyrogram import filters, Client
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from bot import Translation, LOGGER # pylint: disable=import-error
from bot.database import Database # pylint: disable=import-error
import asyncio
from pyrogram.errors import FloodWait
from bot.bot import Bot
from bot import ADMINS
 

db = Database()


@Client.on_message(filters.command(["start"]) & filters.private, group=1)
async def start(bot, update):
    
    try:
        file_uid = update.command[1]
    except IndexError:
        file_uid = False
    
    if file_uid:
        file_id, file_name, file_caption, file_type = await db.get_file(file_uid)
        
        if (file_id or file_type) == None:
            return
        
        caption = file_caption if file_caption != ("" or None) else ("<code>" + file_name + "</code>")
        try:
            await update.reply_cached_media(
                file_id,
                quote=True,
                caption = caption,
                parse_mode="html",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton
                                (
                                    'Share 😐', url="https://t.me/share/url?url=https://t.me/Cinema_Haunter"
                                )
                        ]
                    ]
                )
            )
        except Exception as e:
            await update.reply_text(f"<b>Error:</b>\n<code>{e}</code>", True, parse_mode="html")
            LOGGER(__name__).error(e)
        return



    await bot.send_photo(
        chat_id=update.chat.id,
        photo="https://telegra.ph/file/9d589c04d3db03a9ccb99.jpg",
        caption=Translation.START_TEXT.format(
                update.from_user.mention),
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("⚙️ℍ𝕖𝕝𝕡", callback_data = "help")
                ],
                [
                    InlineKeyboardButton('🏘️𝔾𝕣𝕠𝕦𝕡', url="https://t.me/Cinema_Haunter"),
                    InlineKeyboardButton('🎬ℂ𝕙𝕒𝕟𝕟𝕖𝕝', url="https://t.me/CinemaHaunter")
                ],
                [
                    InlineKeyboardButton('🔎𝕌𝕡𝕕𝕒𝕥𝕖𝕤', url="https://t.me/WhatTheCinema"),
                    InlineKeyboardButton('🗃️𝕊𝕠𝕦𝕣𝕔𝕖', callback_data = "source")
                ]
            ]
        ), 
        parse_mode="html",
        reply_to_message_id=update.message_id
    )


@Client.on_message(filters.command(["help"]) & filters.private, group=1)
async def help(bot, update):
    buttons = [[
        InlineKeyboardButton('𝔸𝕦𝕥𝕠 𝔽𝕚𝕝𝕥𝕖𝕣', callback_data = "autofilter"),
        InlineKeyboardButton('𝕍𝕔 ℙ𝕝𝕒𝕪𝕖𝕣', callback_data = "vcplayer")
    ],[
        InlineKeyboardButton('𝕌𝕟𝕝𝕚𝕞𝕚𝕥𝕖𝕕 𝔽𝕚𝕝𝕥𝕖𝕣', callback_data = "filter"),
        InlineKeyboardButton('𝔽𝕚𝕝𝕖 𝕊𝕥𝕠𝕣𝕖', callback_data = "filestore")
    ],[
        InlineKeyboardButton('𝔸𝕓𝕠𝕦𝕥', callback_data = "about")
    ]]
    
    reply_markup = InlineKeyboardMarkup(buttons)
    
    await bot.send_message(
        chat_id=update.chat.id,
        text=Translation.HELP_TEXT,
        reply_markup=reply_markup,
        parse_mode="html",
        reply_to_message_id=update.message_id
    )


@Client.on_message(filters.text & ~ filters.command(["start","help","batch","genlink","cccurrent","userbotjoinchannel","channelplay","play","dplay","splay","player","skip","pause","resume","end","current","playlist","cresume","cplayer","cplaylist","cdplay","unset","csplay","cplay","pmpermit","gcast","userbotleaveall","userbotjoin","admincache","remall","rem","viewfilters","filter","info","set","sets","id","status"]) & filters.private & ~ filters.me)
async def note(bot, update):
    buttons = [[
        InlineKeyboardButton('🏡 𝕄𝕒𝕚𝕟 𝕔𝕙𝕒𝕟𝕟𝕖𝕝', url="https://t.me/CinemaHaunter"),
        InlineKeyboardButton('📽️ 𝔾𝕣𝕠𝕦𝕡', url="https://t.me/Cinema_Haunter")
    ],[
        InlineKeyboardButton('🤔 ℍ𝕠𝕨 𝕥𝕠 ℝ𝕖𝕢?', url="https://t.me/aska2zmovies/4")
    ],[
        InlineKeyboardButton('𝕊𝕙𝕒𝕣𝕖 𝕋𝕠 𝕐𝕠𝕦𝕣 𝔽𝕣𝕚𝕖𝕟𝕕𝕤 😍', url="https://t.me/share/url?url=https://t.me/Cinema_Haunter")
  
    ]]
    
    reply_markup = InlineKeyboardMarkup(buttons)

    if update.from_user.id not in ADMINS:
        await bot.send_message(
            chat_id=update.chat.id,
            text=Translation.REQ_IN_PM,
            reply_markup=reply_markup,
            parse_mode="html",
            reply_to_message_id=update.message_id
        )
