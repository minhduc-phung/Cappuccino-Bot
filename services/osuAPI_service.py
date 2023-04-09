import discord
from discord.ext.pages import Page
from ossapi import *
from os import getenv
from dotenv import load_dotenv
from os import path
import json

load_dotenv()
api = OssapiV2(int(getenv('OSUAPI_ID')), getenv('OSUAPI_TOKEN'))
_directory_path = path.abspath(".")
DATA_PATH = _directory_path + "\\data\\osu_usernames.json"


def _get_data_from_file() -> dict:
    with open(DATA_PATH, "r") as file:
        osu_username_dict = json.load(file)
    return osu_username_dict


def get_osu_username(user_id: int) -> str:
    osu_username_dict = _get_data_from_file()
    if str(user_id) not in osu_username_dict:
        return ""
    return osu_username_dict[str(user_id)]


def set_username(user_id: int, username: str) -> bool:

    # Check if the username can be found in the Bancho database with the search
    if len(api.search(query=username).users.data) == 0:
        return False

    # Check if the username is the same as the one found in the Bancho database
    username_searched = api.search(query=username).users.data[0].username
    if username_searched != username:
        return False

    if not path.isfile(DATA_PATH):
        # Create the file
        with open(DATA_PATH, "w") as file:
            json.dump({str(user_id): username}, file, indent=4)
    else:
        with open(DATA_PATH, "r") as file:
            old_username_dict = json.load(file)
        print(old_username_dict)
        old_username_dict.update({str(user_id): username})
        print(old_username_dict)
        with open(DATA_PATH, "w") as file:
            json.dump(old_username_dict, file, indent=4)
    return True


def get_top_play(username):
    message_return = ""
    embed_description = ""
    if len(api.search(query=username).users.data) == 0:
        message_return += "There's no user with the given username."
        return message_return, None, None
    user_data = api.search(query=username).users.data[0]
    best_score = api.user_scores(user_data.id, "best")[0]
    message_return += f"Top play of **{username}**:\n\n"
    embed_image_url = user_data.avatar_url
    embed_description += _get_score_embed(best_score)
    embed_description += "\n *\* Star Ratings are not calculated with mods (NM).*"
    return message_return, embed_description, embed_image_url


def get_top_50(username):
    message_return = ""
    embed_description = ""
    if len(api.search(query=username).users.data) == 0:
        message_return += "There's no user with the given username."
        return message_return, None
    user_data = api.search(query=username).users.data[0]
    user_found = user_data.username
    top50 = api.user_scores(user_id=user_data.id, type_="best", limit=50)
    message_return += f"Top 50 plays of **{user_found}**:\n\n"
    embed_image_url = user_data.avatar_url
    pages_to_send = []
    for i in range(len(top50)):
        score = top50[i]
        embed_description += f"**{i + 1}**. "
        embed_description += _get_score_embed(score)
        if i % 5 == 4:
            embed_description += "\n *\* Star Ratings are not calculated with mods (NM).*"
            embed = discord.Embed(description=embed_description)
            embed.set_thumbnail(url=embed_image_url)
            page = Page(content=f"Top 50 plays of **{user_found}**:\n\n",
                        embeds=[embed])
            pages_to_send.append(page)
            embed_description = ""
    return message_return, pages_to_send


def get_recent(username):
    message_return = ""
    embed_description = ""
    if len(api.search(query=username).users.data) == 0:
        message_return += "There's no user with the given username."
        return message_return, None
    user_data = api.search(query=username).users.data[0]
    user_found = user_data.username
    recent_score = api.user_scores(user_data.id, "recent")
    if recent_score:
        recent_score = recent_score[0]
        message_return += f"Recent play of **{user_found}**:\n\n"
        embed_description += _get_score_embed(recent_score)
        embed_description += "\n *\* Star Ratings are not calculated with mods (NM).*"
    else:
        message_return += "This player has no recent plays."
    return message_return, embed_description


def get_profile(username):  # UNDER DEVELOPMENT
    message_return = ""
    embed_description = ""
    if api.search(query=username).users.data[0].username != username:
        message_return += "There's no user with the given username."
        return message_return, embed_description


def _get_score_embed(score):
    embed_description = ""
    stats = score.statistics
    score_stats = f"[{stats.count_300}/{stats.count_100}/{stats.count_50}/{stats.count_miss}]"
    map_set = score.beatmapset
    length = str(score.beatmap.total_length // 60).zfill(2) + ":" + str(score.beatmap.total_length % 60).zfill(2)
    embed_description += f"[{map_set.title} [{score.beatmap.version}] ]({score.beatmap.url}) "
    embed_description += f"*made by **{map_set.creator}** * [**{score.mods}**] [{score.beatmap.difficulty_rating}⭐] [{length}]\n"
    embed_description += f"**{score.pp} pp**\n"
    embed_description += f"Accuracy: **{round(score.accuracy * 100.0, 2)}%** | {score_stats}\n"
    ts = "<t:" + str(int(score.created_at.timestamp())) + ":f>"
    embed_description += f"Played at {ts}\n"
    return embed_description

