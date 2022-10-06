from ossapi import *
from os import getenv
from dotenv import load_dotenv
load_dotenv()
api = OssapiV2(int(getenv('OSUAPI_ID')), getenv('OSUAPI_TOKEN'))

def get_top_play(username):
    message_return = ""
    embed_description = ""
    embed_image = ""
    if api.search(query=username).users.data[0].username != username:
        message_return += "There's no user with the given username."
        return message_return, embed_description, embed_image
    best_score = api.user_scores(api.search(query=username).users.data[0].id, "best")[0]
    stats = best_score.statistics
    score_stats = f"[{stats.count_300}/{stats.count_100}/{stats.count_50}/{stats.count_miss}]"
    map_set = best_score.beatmapset
    length = str(best_score.beatmap.total_length // 60).zfill(2) + ":" + str(best_score.beatmap.total_length % 60).zfill(2)
    message_return += f"Top play of **{username}**:\n\n"

    embed_description += f"[{map_set.title} [{best_score.beatmap.version}] ]({best_score.beatmap.url}) "
    embed_description += f"*made by **{map_set.creator}** * [**{best_score.mods}**] [{best_score.beatmap.difficulty_rating}⭐] [{length}]\n"
    embed_description += f"**{best_score.pp} pp**\n"
    embed_description += f"Accuracy: **{round(best_score.accuracy * 100.0, 2)}%** | {score_stats}\n"
    embed_description += f"Played at {best_score.created_at}\n"
    embed_description += "\n *\* Star Ratings are not calculated with mods (NM).*"

    return message_return, embed_description


def get_top_5(username):
    message_return = ""
    embed_description = ""
    embed_image_url = ""
    if api.search(query=username).users.data[0].username != username:
        message_return += "There's no user with the given username."
        return message_return, embed_description
    top5 = api.user_scores(api.search(query=username).users.data[0].id, "best")[0:5]
    message_return += f"Top 5 plays of **{username}**:\n\n"
    embed_image_url = api.search(query=username).users.data[0].avatar_url
    for i in range(len(top5)):
        score = top5[i]
        stats = score.statistics
        score_stats = f"[{stats.count_300}/{stats.count_100}/{stats.count_50}/{stats.count_miss}]"
        map_set = score.beatmapset
        length = str(score.beatmap.total_length // 60).zfill(2) + ":" + str(score.beatmap.total_length % 60).zfill(2)
        embed_description += f"**{i+1}**. "
        embed_description += f"[{map_set.title} [{score.beatmap.version}] ]({score.beatmap.url}) "
        embed_description += f"*made by **{map_set.creator}** * [**{score.mods}**] [{score.beatmap.difficulty_rating}⭐] [{length}]\n"
        embed_description += f"**{score.pp} pp**\n"
        embed_description += f"Accuracy: **{round(score.accuracy * 100.0, 2)}%** | {score_stats}\n"
        embed_description += f"Played at {score.created_at}\n"
    embed_description += "\n *\* Star Ratings are not calculated with mods (NM).*"
    return message_return, embed_description, embed_image_url


def get_recent(username):
    message_return = ""
    embed_description = ""
    if api.search(query=username).users.data[0].username != username:
        message_return += "There's no user with the given username."
        return message_return, embed_description
    recent_score = api.user_scores(api.search(query=username).users.data[0].id, "recent")
    if recent_score:
        recent_score = recent_score[0]
        stats = recent_score.statistics
        score_stats = f"[{stats.count_300}/{stats.count_100}/{stats.count_50}/{stats.count_miss}]"
        map_set = recent_score.beatmapset
        length = str(recent_score.beatmap.total_length // 60).zfill(2) + ":" + str(recent_score.beatmap.total_length % 60).zfill(2)
        message_return += f"Recent play of **{username}**:\n\n"
        embed_description += f"[{map_set.title} [{recent_score.beatmap.version}] ]({recent_score.beatmap.url}) "
        embed_description += f"*made by **{map_set.creator}** * [**{recent_score.mods}**] [{recent_score.beatmap.difficulty_rating}⭐] [{length}]\n"
        embed_description += f"**{recent_score.pp} pp**\n"
        embed_description += f"Accuracy: **{round(recent_score.accuracy * 100.0, 2)}%** | {score_stats}\n"
        embed_description += f"Played at {recent_score.created_at}\n"
        embed_description += "\n *\* Star Ratings are not calculated with mods (NM).*"
    else:
        message_return += "This player has no recent plays."
    return message_return, embed_description


def get_profile(username): # UNDER DEVELOPMENT
    message_return = ""
    embed_description = ""
    if api.search(query=username).users.data[0].username != username:
        message_return += "There's no user with the given username."
        return message_return, embed_description