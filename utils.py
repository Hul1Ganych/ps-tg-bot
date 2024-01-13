import pandas as pd 
from typing import List
from pandas.core.api import DataFrame as DataFrame

def string_preproseccing(msg: str, cmd: str):
    """
    Prepare user's message.
    """
    msg_lower = msg.text.lower().replace(f"/{cmd} ", "")
    msg_splitted = [x.split("-") for x in msg_lower.split(",")]
    
    return [{"artist": x[0], "name": x[1]} for x in msg_splitted]

