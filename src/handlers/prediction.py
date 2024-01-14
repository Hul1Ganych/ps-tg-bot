"""Handler for prediction."""

import os

import aiohttp
from aiogram import F, Router, types
from aiogram.enums.parse_mode import ParseMode
from aiogram.filters import Command
from aiogram.filters.command import CommandObject
from aiogram.utils.formatting import Bold, as_list, as_marked_list
from aiogram.utils.markdown import hlink

from configs.bot_config import config
from src.utils import preprocess_string


router = Router()


@router.message(F.text, Command("predict"))
async def predict_handler(message: types.Message, command: CommandObject):
    """
    Handler for predict command.

    Args:
        msg: Telegram message instance
    """
    dict_from_message = {
        "song_list": preprocess_string(command.args),
    }

    async with aiohttp.ClientSession() as session:
        generate_uri = os.path.join(str(config.service_uri), "api/generate")
        async with session.post(url=generate_uri, json=dict_from_message) as response:
            if not response.ok:
                await message.answer("Sorry, we couldn't find your song.")
            songs = await response.json()

    if not songs:
        await message.answer("Sorry, we couldn't find your song.")
        return

    content = as_list(
        Bold("Here is your playlist:"),
        as_marked_list(
            *[
                hlink(f"{song['artist_name'][0]} - {song['track_name']}", song["href"])
                for song in songs
            ],
            marker="✅ ",
        ),
        sep="\n\n",
    )
    await message.answer(**content.as_kwargs(parse_mode_key=ParseMode.HTML))


@router.message(F.text, Command("search"))
async def search_handler(message: types.Message, command: CommandObject):
    """
    Handler for search command.

    Args:
        msg: Telegram message instance
    """
    user_songs = preprocess_string(command.args)

    async with aiohttp.ClientSession() as session:
        search_uri = os.path.join(str(config.service_uri), "api/search")
        async with session.post(url=search_uri, json=user_songs) as response:
            if not response.ok:
                await message.answer("Sorry, we couldn't find your song.")
            songs = await response.json()

    if not songs:
        await message.answer("Sorry, we couldn't find your song.")
        return

    content = as_list(
        Bold("Here is songs you have requested:"),
        as_marked_list(
            *[
                hlink(f"{song['artist_name'][0]} - {song['track_name']}", song["href"])
                for song in songs
            ],
            marker="🎼 ",
        ),
        sep="\n\n",
    )

    await message.answer(**content.as_kwargs(parse_mode_key=ParseMode.HTML))
