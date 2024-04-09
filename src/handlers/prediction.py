"""Handler for prediction."""

import asyncio
from aiogram import F, Router, types
from aiogram.enums.parse_mode import ParseMode
from aiogram.filters import Command
from aiogram.filters.command import CommandObject
from aiogram.utils.formatting import Bold, Text, as_list, as_marked_list
from aiogram.utils.markdown import hlink

from src.utils import api_call, get_request, preprocess_string


router = Router()


@router.message(F.text, Command("predict"))
async def predict_handler(message: types.Message, command: CommandObject):
    """
    Handler for predict command.

    Args:
        message: Telegram message instance
    """
    try:
        dict_from_message = {
            "song_list": preprocess_string(command.args),
        }
        request_id = await api_call("api/generate", dict_from_message)
    except ValueError as err:
        await message.answer(str(err))
        return

    request = await get_request(f"requests/{request_id}")
    while request["status"] not in ("completed", "failed"):
        await asyncio.sleep(30)
        request = await get_request(f"requests/{request_id}")
        
    if request["status"] == "failed":
        await message.answer("Your request is failed.")
        return

    songs = request.get("songs", [])
    content = as_list(
        Bold("<b>Here is your playlist:</b>"),
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


@router.message(F.text, Command("search"))
async def search_handler(message: types.Message, command: CommandObject):
    """
    Handler for search command.

    Args:
        message: Telegram message instance
    """
    try:
        user_songs = preprocess_string(command.args)
        songs = await api_call("api/search", user_songs)
    except ValueError as err:
        await message.answer(str(err))
        return

    content = as_list(
        Text("<b>Here is songs you have requested:</b>"),
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


@router.message(F.text, Command("describe"))
async def describe_handler(message: types.Message, command: CommandObject):
    """
    Handler for search command.

    Args:
        message: Telegram message instance
    """

    def _format_song_info(song):
        seconds = song["duration_ms"] // 1000
        minutes = seconds // 60
        song_info = {
            "<b>Artists</b>": ", ".join(song["artist_name"]),
            "<b>Name</b>": song["track_name"],
            "<b>Album</b>": song["album_name"],
            "<b>Release date</b>": song["album_release_date"],
            "<b>Genres</b>": ", ".join(song["genres"]),
            "<b>Popularity</b>": song["popularity"],
            "<b>Duration</b>": f"{str(minutes).zfill(2)}:{seconds % 60}",
        }
        return "\n".join([f"{k}: {v}" for k, v in song_info.items()]) + "\n"

    try:
        user_songs = preprocess_string(command.args)
        songs = await api_call("api/search", user_songs)
    except ValueError as err:
        await message.answer(str(err))
        return

    songs_info = list(map(_format_song_info, songs))
    content = as_list(
        Text("<b>Here is description for songs you have requested:</b>"),
        as_marked_list(
            *[
                as_list(
                    hlink(
                        f"{song['artist_name'][0]} - {song['track_name']}", song["href"]
                    ),
                    Text(songs_info[i]),
                    sep="\n",
                )
                for i, song in enumerate(songs)
            ],
            marker="🎼 ",
        ),
        sep="\n\n",
    )

    await message.answer(**content.as_kwargs(parse_mode_key=ParseMode.HTML))
