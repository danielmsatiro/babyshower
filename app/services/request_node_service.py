import os
from json import dumps, load

import requests


def request_token_node(id: int):
    """Get token from node api

    Args:
        id (int): parent_id to be added to the token

    Returns:
        _type_(string): access_token for node api
    """
    payload = {
        "email": os.getenv("EMAIL_MASTER_NODE"),
        "password": os.getenv("PASSWORD_MASTER_NODE"),
        "id": id,
    }
    url = f'{os.getenv("API_NODE")}/administrators/login'
    headers = {"Content-Type": "application/json"}
    try:
        r = requests.post(
            url,
            data=dumps(payload),
            headers=headers,
        )
    except:
        return "Servidor secundário node não disponível"

    return r.json().get("access_token")
