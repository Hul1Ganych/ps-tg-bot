"""Module with utils for bot usage."""


def preprocess_string(query_string: str):
    """
    Prepare user's message.
    """
    tracks = [track.strip().split("-") for track in query_string.split(",")]

    if any(map(lambda x: len(x) != 2, tracks)):
        raise ValueError("Incorrect input format: %s", query_string)
    return [{"artist": x[0], "name": x[1]} for x in tracks]
