import asyncio
import datetime
import random
from os import getenv
import logging

import discord
from discord import SlashCommandGroup
from discord.ext import pages
from dotenv import load_dotenv

from services import tenor_API_service, osuAPI_service, english_words_service
from resources.text_resources import HELP_TEXTS, UNSET_USERNAME_WARNING

# Logging
# Set the log file name to the current date
# log_MMDDYYYY.log
file_name = 'log_{0}.log'.format(datetime.datetime.now().strftime("%m%d%Y"))
f_handler = logging.FileHandler('.\\logs\\' + file_name)
f_handler.setLevel(logging.INFO)
f_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
f_handler.setFormatter(f_formatter)
c_handler = logging.StreamHandler()
c_handler.setLevel(logging.INFO)
c_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
c_handler.setFormatter(c_formatter)

logger = logging.getLogger(__name__)
logger.addHandler(f_handler)
logger.addHandler(c_handler)
logger.setLevel(logging.INFO)

bot = discord.Bot(intents=discord.Intents.all())


@bot.event
async def on_ready():
    activity = discord.Activity(name="/help", type=discord.ActivityType.playing)
    await bot.change_presence(status=discord.Status.online, activity=activity)
    logger.info('{0.user} is now online.'.format(bot))
    # print('{0.user} is now online.'.format(bot))


@bot.event
async def on_member_join(member):
    # Get the server the member joined
    server = member.guild
    # Get the server name
    server_name = server.name
    # Get the channel to send the message to
    channel = discord.utils.get(server.channels, name="general")
    # Send the message
    await channel.send("Welcome to the server, " + member.name + "!")
    logger.info("New user joined server \"" + server_name + "\": " + str(member.user))


# @bot.event
# async def on_message(message):
#    if message.author == bot.user:
#        return
#    if "727" in message.content:
#        await message.channel.send(tenor_API_service.get_random_gif("wysi"))


@bot.command(description="Send the bot's latency")
async def ping(ctx):
    await ctx.respond(f"Pinged! My latency is **{bot.latency * 1000:.0f}ms**.")
    logger.warning("Someone pinged the bot. Current latency: " + str(bot.latency * 1000) + "ms")


@bot.command(description="Shows the list of commands")
async def help(ctx):
    await ctx.respond(HELP_TEXTS.get('en'))


@bot.command(description="Xem các câu lệnh có sẵn")
async def cuu(ctx):
    await ctx.respond(HELP_TEXTS.get('vi'))


@bot.command(description="Get a random gif from tenor. Yes, I know /tenor exists.")
async def gif(ctx, search_term: discord.Option(str)):
    await ctx.respond(tenor_API_service.get_random_gif(search_term))


@bot.command(description="Roll a random number. Default range is 1-100")
async def roll(ctx, max_range: discord.Option(int, default=100, description="The max range of the random number")):
    roll_value = random.randint(1, max_range)
    response = ""
    if roll_value == 727:
        response += "When you see it!\n"
    response += f"{ctx.author.mention} rolled {roll_value}"
    await ctx.respond(response)


osu = SlashCommandGroup("osu", "osu! related commands")


@osu.command(description="Set the osu! username of the user")
async def set_username(ctx: discord.ApplicationContext, username: discord.Option(str, description="The osu! username")):
    if osuAPI_service.set_username(ctx.author.id, username):
        await ctx.respond("Your osu! username has been set to **" + username + "**.", ephemeral=True)
    else:
        await ctx.respond("Your osu! username cannot be found or is invalid.", ephemeral=True)


@osu.command(description="Get the osu! top plays of a user")
async def top(ctx: discord.ApplicationContext,
              username: discord.Option(str, description="An osu! username", required=False)):
    if username is None:
        username = osuAPI_service.get_osu_username(ctx.author.id)
        if username == "":
            await ctx.respond(UNSET_USERNAME_WARNING, ephemeral=True)
            return
    message, pages_to_send = osuAPI_service.get_top_50(username)
    if pages_to_send is None:
        await ctx.respond(message)
        return
    paginator = pages.Paginator(pages_to_send)
    await paginator.respond(ctx.interaction)


@osu.command(description="Get the osu! most recent play of a user")
async def recent(ctx: discord.ApplicationContext,
                 username: discord.Option(type=str, description="An osu! username.", required=False)):
    if username is None:
        username = osuAPI_service.get_osu_username(ctx.author.id)
        if username == "":
            await ctx.respond(UNSET_USERNAME_WARNING, ephemeral=True)
            return
    message, ed = osuAPI_service.get_recent(username)
    if ed == "":
        await ctx.respond(message)
        return
    embed = discord.Embed()
    embed.title = message
    embed.description = ed
    await ctx.respond(embed=embed)


@osu.command(description="Get the osu! user's top play")
async def best(ctx: discord.ApplicationContext,
               username: discord.Option(str, description="An osu! username", required=False)):
    if username is None:
        username = osuAPI_service.get_osu_username(ctx.author.id)
        if username == "":
            await ctx.respond(UNSET_USERNAME_WARNING, ephemeral=True)
            return
    message, ed, ei = osuAPI_service.get_top_play(username)
    if ed is None:
        await ctx.respond(message)
        return
    embed = discord.Embed()
    embed.title = message
    embed.description = ed
    embed.set_thumbnail(url=ei)
    await ctx.respond(embed=embed)


bot.add_application_command(osu)


@bot.command(description="Try to guess a scrambled word together!")
async def scramble(ctx):
    answer = english_words_service.get_random_lower_word()
    scrambled = english_words_service.scramble_word(answer)
    await ctx.respond("Unscramble this word: **" + scrambled + "**\nYou have 30 seconds.")
    try:
        msg = await bot.wait_for("message", check=lambda m: m.content.lower() == answer, timeout=30)
    except asyncio.TimeoutError:
        await ctx.respond(f"Time's up! The answer was **{answer}**.")
    else:
        await ctx.respond(f"{msg.author.mention} guessed the word! The answer was **{answer}**.")


@bot.command(description="Chatting")
async def chatting(ctx):
    await ctx.respond(tenor_API_service.get_chatting_gif())


@bot.command(description="bruh")
async def bruh(ctx):
    await ctx.respond(file=discord.File('resources/bruh.gif'))


def main():
    load_dotenv()
    bot.run(getenv('BOT_TOKEN'))


if __name__ == "__main__":
    main()
