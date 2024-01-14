"""Module with utils for bot usage."""

import os
from typing import Dict, List

import aiohttp

from configs.bot_config import config


async def api_call(api_path: str, params: Dict[str, str]):
    """API call to service.

    Args:
        api_path: API endpoint to call
        params: params to pass into API request

    Returns:
        List of songs
    """
    async with aiohttp.ClientSession() as session:
        full_url = os.path.join(str(config.service_uri), api_path)
        async with session.post(url=full_url, json=params) as response:
            if not response.ok:
                raise ValueError("Sorry, we couldn't find your song.")
            songs = await response.json()

    if not songs:
        raise ValueError("Sorry, we couldn't find your song.")
    return songs


def preprocess_string(query_string: str) -> List[Dict[str, str]]:
    """
    Prepare user's message.

    Args:
        query_string: user input message

    Returns:
        List of tracks in format (artist, track name)
    """
    tracks = [track.strip().split("-") for track in query_string.split(",")]

    if any(map(lambda x: len(x) != 2, tracks)):
        raise ValueError("Incorrect input format: %s" % query_string)

    return [{"artist": x[0], "name": x[1]} for x in tracks]
