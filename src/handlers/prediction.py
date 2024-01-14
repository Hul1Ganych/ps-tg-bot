"""Handler for prediction."""

import pathlib

import aiohttp
from aiogram import F, Router, types
from aiogram.filters import Command

# from aiogram.utils.formatting import Text, Bold, as_list, as_marked_list
from aiogram.utils.markdown import hlink

from configs.bot_config import config
from utils import preprocess_string


# from aiogram.enums.parse_mode import ParseMode


router = Router()


@router.message(F.text, Command("predict"))
async def predict_handler(msg: types.Message):
    """
    Handler for predict command.

    Args:
        msg: Telegram message instance
    """
    dict_from_message = {
        "song_list": preprocess_string(msg, "predict"),
    }

    async with aiohttp.ClientSession() as session:
        generate_uri = pathlib.Path(config.service_uri) / "api" / "generate"
        async with session.post(url=generate_uri, json=dict_from_message) as response:
            songs = await response.json()

    song_list = [
        hlink(f"{song['artist_name'][0]} - {song['track_name']}", song["href"])
        for song in songs
    ]

    # хотелось бы прикрутить вот это ->
    # content = as_list(
    #     Bold("Here is your playlist:"),
    #     as_marked_list(
    #         *[
    #             hlink(f"{song['artist_name'][0]} - {song['track_name']}", song['href'])
    #             for song in songs
    #         ],
    #     marker="✅ ",
    #     ),
    #     sep="\n",
    # )
    # но тогда href некорректно отображаются

    await msg.answer("Here is your playlist:\n\n 🎼" + "\n\n 🎼".join(song_list))
    # await msg.answer(**content.as_kwargs())


@router.message(F.text, Command("search"))
async def search_handler(msg: types.Message):
    """
    Handler for search command.

    Args:
        msg: Telegram message instance
    """
    user_songs = preprocess_string(msg, cmd="search")

    async with aiohttp.ClientSession() as session:
        search_uri = pathlib.Path(config.service_uri) / "api" / "search"
        async with session.post(url=search_uri, json=user_songs) as response:
            songs = await response.json()

    song_info = [
        hlink(f"{song['artist_name'][0]} - {song['track_name']}", song["href"])
        for song in songs
    ]

    if song_info:
        await msg.answer(
            "Here is songs you have requested:\n\n 🎼" + "\n\n 🎼".join(song_info)
        )
    else:
        await msg.answer("Sorry, we couldn't find your song.")
