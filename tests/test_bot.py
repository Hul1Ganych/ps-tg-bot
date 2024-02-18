"""Module with tests for bot search, describe and rate handlers."""

from unittest.mock import AsyncMock, patch

import pytest
from aiogram.enums.parse_mode import ParseMode
from aiogram.utils.formatting import Text, as_list, as_marked_list
from aiogram.utils.markdown import hlink

from src.handlers.prediction import describe_handler, search_handler
from src.handlers.rate import (
    callbacks_num_change_fab,
    get_rating_keyboard,
    rate_bot,
    update_rating,
)
from src.utils import preprocess_string


@pytest.fixture
def test_songs():
    return [
        {
            "artist_name": ["Kanye West"],
            "track_name": "Stronger",
            "duration_ms": 311_000,
            "album_name": "Graduation",
            "album_release_date": "2007-09-11",
            "genres": ["chicago rap", "hip hop", "rap"],
            "popularity": 85,
            "href": "https://open.spotify.com/track/0j2T0R9dR9qdJYsB7ciXhf",
        },
    ]


@pytest.fixture
def description_test_output(test_songs):
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

    songs_info = list(map(_format_song_info, test_songs))
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
                for i, song in enumerate(test_songs)
            ],
            marker="🎼 ",
        ),
        sep="\n\n",
    )

    return content.as_kwargs(parse_mode_key=ParseMode.HTML)


@pytest.fixture
def search_test_output(test_songs):
    content = as_list(
        Text("<b>Here is songs you have requested:</b>"),
        as_marked_list(
            *[
                hlink(f"{song['artist_name'][0]} - {song['track_name']}", song["href"])
                for song in test_songs
            ],
            marker="🎼 ",
        ),
        sep="\n\n",
    )

    return content.as_kwargs(parse_mode_key=ParseMode.HTML)


@pytest.fixture
def message_mock():
    user_mock = AsyncMock(id="123")
    return AsyncMock(from_user=user_mock)


@pytest.fixture
def callback_mock(message_mock):
    user_mock = AsyncMock(id="123")
    return AsyncMock(from_user=user_mock, message=message_mock)


@pytest.mark.asyncio
async def test_rate_bot(message_mock):
    target_response = "Rate our bot: "

    await rate_bot(message=message_mock)
    message_mock.answer.assert_called_with(
        target_response, reply_markup=get_rating_keyboard()
    )


@pytest.mark.asyncio
async def test_update_rating(message_mock):
    new_value = 5
    target_response = f"Rate our bot: {new_value}"

    await update_rating(message=message_mock, new_value=new_value)
    message_mock.edit_text.assert_called_with(
        target_response, reply_markup=get_rating_keyboard()
    )


@pytest.mark.asyncio
async def test_callbacks_update_rating(callback_mock):
    action, value = "update", 2
    callback_data_mock = AsyncMock(action=action, value=value)

    await callbacks_num_change_fab(
        callback=callback_mock, callback_data=callback_data_mock
    )

    target_response = f"Rate our bot: {value}"
    callback_mock.message.edit_text.assert_called_with(
        target_response, reply_markup=get_rating_keyboard()
    )
    callback_mock.answer.assert_called_with()


@pytest.mark.asyncio
async def test_callbacks_finish_rating(callback_mock):
    action, value = "finish", 2
    callback_data_mock = AsyncMock(action=action, value=value)

    await callbacks_num_change_fab(
        callback=callback_mock, callback_data=callback_data_mock
    )

    target_response = f"Your final rating: {value}"
    callback_mock.message.edit_text.assert_called_with(target_response)
    callback_mock.answer.assert_called_with(
        text="Thanks for using our bot!", show_alert=True
    )


@pytest.mark.asyncio
@patch("src.handlers.prediction.api_call")
async def test_describe_handler(mock_api_call, message_mock, description_test_output):
    query = "Kanye West - Stronger"
    command_mock = AsyncMock(args=query)
    user_songs = preprocess_string(command_mock.args)

    mock_api_call.return_value = [
        {
            "artist_name": ["Kanye West"],
            "track_name": "Stronger",
            "duration_ms": 311_000,
            "album_name": "Graduation",
            "album_release_date": "2007-09-11",
            "genres": ["chicago rap", "hip hop", "rap"],
            "popularity": 85,
            "href": "https://open.spotify.com/track/0j2T0R9dR9qdJYsB7ciXhf",
        },
    ]
    await describe_handler(message=message_mock, command=command_mock)

    mock_api_call.assert_called_with("api/search", user_songs)
    message_mock.answer.assert_called_with(**description_test_output)


@pytest.mark.asyncio
@patch("src.handlers.prediction.api_call")
async def test_search_handler(mock_api_call, message_mock, search_test_output):
    query = "Kanye West - Stronger"
    command_mock = AsyncMock(args=query)
    user_songs = preprocess_string(command_mock.args)

    mock_api_call.return_value = [
        {
            "artist_name": ["Kanye West"],
            "track_name": "Stronger",
            "duration_ms": 311_000,
            "album_name": "Graduation",
            "album_release_date": "2007-09-11",
            "genres": ["chicago rap", "hip hop", "rap"],
            "popularity": 85,
            "href": "https://open.spotify.com/track/0j2T0R9dR9qdJYsB7ciXhf",
        },
    ]
    await search_handler(message=message_mock, command=command_mock)

    mock_api_call.assert_called_with("api/search", user_songs)
    message_mock.answer.assert_called_with(**search_test_output)
