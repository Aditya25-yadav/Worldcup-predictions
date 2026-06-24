import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("FOOTBALL_API_KEY")

BASE_URL = "https://v3.football.api-sports.io"


def get_world_cup_fixtures():
    url = f"{BASE_URL}/fixtures"

    headers = {
        "x-apisports-key": API_KEY
    }

    params = {
        "league": 1,
        "season": 2022
    }

    response = requests.get(
        url,
        headers=headers,
        params=params,
        timeout=20
    )

    response.raise_for_status()

    return response.json()