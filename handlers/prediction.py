"""Handler for prediction."""

import json
import numpy as np
from aiogram import types, F, Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram import html
from aiogram.utils.formatting import Text, Bold, as_list, as_marked_list
from aiogram.utils.markdown import hlink
import aiohttp
from aiogram.enums.parse_mode import ParseMode
from utils import string_preproseccing

router = Router()


@router.message(Command("predict"))
async def predict_handler(msg: Message):


    # text_from_message = msg.text.lower().replace("/predict ", "")

    # text_from_message = [x.split("-") for x in text_from_message.split(",")]
    dict_from_message = {}
    # dict_from_message["song_list"] = [{"artist": x[0], "name": x[1]} for x in text_from_message]
    dict_from_message["song_list"] = string_preproseccing(msg, "predict")

    async with aiohttp.ClientSession() as session:
        async with session.post(url="http://0.0.0.0:5000/api/generate", json=dict_from_message) as response:
            songs = await response.json()

    song_list = [
        hlink(f"{song['artist_name'][0]} - {song['track_name']}", song['href'])
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

    await msg.answer(
        "Here is your playlist:\n\n 🎼" + "\n\n 🎼".join(song_list)
    )
    # await msg.answer(**content.as_kwargs())


@router.message(Command("search"))
async def predict_handler(msg: Message):
    # text_from_message = msg.text.lower().replace("/search ", "")

    # text_from_message = [x.split("-") for x in text_from_message.split(",")]
    # user_songs = [{"artist": x[0], "name": x[1]} for x in text_from_message]
    user_songs = string_preproseccing(msg, cmd="search")

    async with aiohttp.ClientSession() as session:
        async with session.post(url="http://0.0.0.0:5000/api/search", json=user_songs) as response:
            songs = await response.json()

    song_info = [
        hlink(f"{song['artist_name'][0]} - {song['track_name']}", song['href'])
        for song in songs
    ]
    
    if len(song_info) == 0:
        await msg.answer("Sorry, we couldn't find your song.")
    else:
        await msg.answer(
            "Here is songs you have requested:\n\n 🎼" + "\n\n 🎼".join(song_info)
        )