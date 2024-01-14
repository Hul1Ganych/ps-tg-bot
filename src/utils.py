"""Module with utils for bot usage."""

from typing import Dict, List


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
