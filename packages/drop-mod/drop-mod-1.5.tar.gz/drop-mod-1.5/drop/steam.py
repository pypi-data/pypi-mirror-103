import re
import requests

import drop.ext as ext
from drop.errors import GameNotFound

# steam_api_token = None

# def init_steam(token):
#     global steam_api_token
#     steam_api_token = token


def search_game(query: str):
    return re.findall('appid="(.*?)"', requests.get(
        f"https://store.steampowered.com/search/suggest?term={query}&f=games&cc=CA&l=english").text)


def get_protondb_summary(app_id: int):
    r = requests.get(f"https://www.protondb.com/api/v1/reports/summaries/{app_id}.json")
    if r.status_code == 404:
        raise GameNotFound(f"Could not find any reports for app ID {app_id}")

    received = r.json()

    tier = received.get("tier").title()
    confidence = received.get("confidence").title()
    score = received.get("score")
    total = received.get("total")
    trending_tier = received.get("trendingTier").title()
    best_reported_tier = received.get("bestReportedTier").title()

    string_result = f"{confidence} confidence, {total} reports, recently trending tier is {trending_tier}" \
                    f", best reported tier ever is {best_reported_tier}, score is {score}"

    if tier.lower() == "pending":
        string_result = string_result + f', provisional tier is {received.get("provisionalTier").title()}'

    color = 0xf00055
    supposed_color = ext.protondb_colors.get(tier)
    if supposed_color:
        color = supposed_color
    received["string_result"] = string_result
    received["tier_color"] = color
    return received


def get_steam_app_info(app_id: int):
    return requests.get(f"https://store.steampowered.com/api/appdetails?appids={app_id}").json()
