import asyncio
import random
from os import getenv

import discord
from discord import SlashCommandGroup
from discord.ext import pages
from dotenv import load_dotenv

import english_words_service
import osuAPI_service
import tenor_API_service
from text_resources import HELP_TEXTS

bot = discord.Bot(intents=discord.Intents.all())


@bot.event
async def on_ready():
    activity = discord.Activity(name="/help", type=discord.ActivityType.playing)
    await bot.change_presence(status=discord.Status.online, activity=activity)
    print('{0.user} is now online.'.format(bot))


@bot.event
async def on_member_join(member):
    await member.send("Good morning, " + member.name + "!" + "\nWelcome to the server.")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if "727" in message.content:
        await message.channel.send(tenor_API_service.get_random_gif("wysi"))


@bot.command(description="Send the bot's latency")
async def ping(ctx):
    await ctx.respond(f"Pinged! My latency is **{bot.latency * 1000:.0f}ms**.")


@bot.command(description="Shows the list of commands")
async def help(ctx):
    await ctx.respond(HELP_TEXTS.get('en'))


@bot.command(description="Xem các câu lệnh có sẵn")
async def cuu(ctx):
    await ctx.respond(HELP_TEXTS.get('vi'))


@bot.command(description="Get a random gif from tenor")
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


@osu.command(description="Get the osu! top plays of a user")
async def top(ctx: discord.ApplicationContext, username: discord.Option(str, description="The osu! username")):
    message, pages_to_send = osuAPI_service.get_top_50(username)
    if pages_to_send is None:
        await ctx.respond(message)
        return
    paginator = pages.Paginator(pages_to_send)
    await paginator.respond(ctx.interaction)


@osu.command(description="Get the osu! most recent play of a user")
async def recent(ctx: discord.ApplicationContext, username: discord.Option(str, description="The osu! username")):
    message, ed = osuAPI_service.get_recent(username)
    if ed == "":
        await ctx.respond(message)
        return
    embed = discord.Embed()
    embed.description = ed
    await ctx.respond(message, embed=embed)


@osu.command(description="Get the osu! user's top play")
async def best(ctx: discord.ApplicationContext, username: discord.Option(str, description="The osu! username")):
    message, ed, ei = osuAPI_service.get_top_play(username)
    if ed is None:
        await ctx.respond(message)
        return
    embed = discord.Embed()
    embed.description = ed
    embed.set_thumbnail(url=ei)
    await ctx.respond(message, embed=embed)


bot.add_application_command(osu)


@bot.command(description="Try to guess a scrambled word together!")
async def scramble(ctx):
    answer = english_words_service.get_random_lower_word()
    scrambled = english_words_service.scramble_word(answer)
    await ctx.respond("Unscramble this word: **" + scrambled + "**\n You have 30 seconds.")
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
    await ctx.respond(file=discord.File('bruh.gif'))


def main():
    load_dotenv()
    bot.run(getenv('BOT_TOKEN'))


if __name__ == "__main__":
    main()
