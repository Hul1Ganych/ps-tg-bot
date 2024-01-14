"""Module with utils for bot usage."""


def preprocess_string(msg: str, cmd: str):
    """
    Prepare user's message.
    """
    msg_lower = msg.text.lower().replace(f"/{cmd} ", "")
    msg_splitted = [x.split("-") for x in msg_lower.split(",")]

    return [{"artist": x[0], "name": x[1]} for x in msg_splitted]
