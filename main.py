import discord
import random
from os import getenv
from dotenv import load_dotenv
import osuAPIService
import tenorAPIService

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

PREFIX = "c."

EMOJI_GOOD_COMMAND = '✅'
EMOJI_BAD_COMMAND = '❌'

HELP_TEXT = f'''I am Cappuccino, a bot made by Lulu x Pix.
I am currently under huge development (unless my creator is lazy).
My prefix is **{PREFIX}**!
Here are all of the commands currently available:
*\*Note [required] {{optional}} *
- **help**: Show this entire message
- **cuu**: Hiện danh sách câu lệnh của bot
- **hello**
- **roll** {{range}}: Get a random number from 1 to 100, unless range specified
- **osutopplay** [username]: Get the osu! top play of the user specified
- **osutop** [username]: Get the osu! top 5 plays of the user specified
- **osurecent** [username]: Get the osu! recent play of the user specified
'''

CUU_TEXT = f'''Đây là Cappuccino, một bot tạo bởi Lulu x Pix.
Bot đang được phát triển nên sẽ chưa có nhiều tính năng.
Các câu lệnh bắt đầu bằng **{PREFIX}**!
Các câu lệnh hiện đang có (toàn bộ output của các câu lệnh đều là tiếng Anh):
*Lưu ý: \* [bắt buộc] {{không bắt buộc}} *
- **help**: Show command list
- **cuu**: Hiện tin nhắn này
- **hello**
- **roll** {{range}}: Trả về một số từ 1-100, hoặc từ 1 tới số được ghi trong lệnh
- **osutopplay** [username]: (osu!) Trả về top play của người chơi có username được ghi trong lệnh
- **osutop** [username]: (osu!) Trả về 5 top plays của người chơi được ghi trong lệnh
- **osurecent** [username]: (osu!) Trả về lượt chơi gần đây nhất của người chơi được ghi trong lệnh
'''


@client.event
async def on_ready():
    activity = discord.Game(name="c.help | c.cuu!")
    await client.change_presence(status=discord.Status.online, activity=activity)
    print('{0.user} is now online.'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith(PREFIX):

        command = message.content[2:]

        if command == 'help':
            await message.add_reaction(EMOJI_GOOD_COMMAND)
            await message.channel.send(HELP_TEXT)

        if command == 'cuu':
            await message.add_reaction(EMOJI_GOOD_COMMAND)
            await message.channel.send(CUU_TEXT)

        if command == 'hello':
            await message.add_reaction(EMOJI_GOOD_COMMAND)
            await message.channel.send('Please to meet you. :purple_heart:')

        if command.startswith('roll ') or command == 'roll':
            await message.add_reaction(EMOJI_GOOD_COMMAND)
            roll_range = str(message.content)[7:len(str(message.content))]
            if roll_range.isdigit():
                roll_range = int(roll_range)
                roll_value = random.randrange(1, roll_range + 1)
                message_sent = str(message.author)[0:-5] + " rolled " + str(
                    roll_value) + " point(s)"
                if roll_value == 727: message_sent += '\nWYSI'
                if '69' in str(roll_value): message_sent += '\nNice.'
                await message.channel.send(message_sent)
            else:
                message_sent = str(message.author)[0:-5] + " rolled " + str(random.randrange(1, 101)) + " point(s)"
                await message.channel.send(message_sent)

        if command.startswith('pull '):
            message_received = str(message.content)
            message_sent = message_received[8:(len(message_received))]
            await message.channel.send(message_sent)

        if command.startswith('osutopplay'):
            message_sent = "Error :/"  # If no conditions met
            if len(command) == len('osutopplay'):
                await message.add_reaction(EMOJI_BAD_COMMAND)
                message_sent = "**Usage**: osutopplay {**username**}"
                ed = ''
            elif command[len('osutopplay')] == ' ':
                username = command[(len('osutopplay') + 1):]
                if username == '':
                    await message.add_reaction(EMOJI_BAD_COMMAND)
                    ed = ''
                    message_sent = "**Missing argument**: Player username.\n **Usage**: osutopplay {**username**}"
                else:
                    await message.add_reaction(EMOJI_GOOD_COMMAND)
                    message_sent, ed = osuAPIService.get_top_play(username)
            await message.channel.send(message_sent)
            if ed != '':
                embed = discord.Embed()
                embed.description = ed
                await message.channel.send(embed=embed)

        if command.startswith('osutop') and not (command.startswith('osutopplay')):
            message_sent = "Error :/"  # If no conditions met
            ei = ''
            if len(command) == 6:
                await message.add_reaction(EMOJI_BAD_COMMAND)
                message_sent = "**Usage**: osutop {**username**}"
                ed = ei = ''
            elif command[6] == ' ':
                username = command[7:]
                if username == '':
                    await message.add_reaction(EMOJI_BAD_COMMAND)
                    ed = ei = ''
                    message_sent = "**Missing argument**: Player username.\n **Usage**: osutop {**username**}"
                else:
                    await message.add_reaction(EMOJI_GOOD_COMMAND)
                    message_sent, ed, ei = osuAPIService.get_top_5(username)
            await message.channel.send(message_sent)
            if ed != '':
                embed = discord.Embed()
                embed.description = ed
                embed.set_thumbnail(url=ei)
                await message.channel.send(embed=embed)

        if command.startswith('osurecent'):
            message_sent = "Error :/"  # If no conditions met
            if len(command) == len('osurecent'):
                await message.add_reaction(EMOJI_BAD_COMMAND)
                message_sent = "**Usage**: osurecent {**username**}"
                ed = ''
            elif command[len('osurecent')] == ' ':
                username = command[(len('osurecent') + 1):]
                if username == '':
                    await message.add_reaction(EMOJI_BAD_COMMAND)
                    ed = ''
                    message_sent = "**Missing argument**: Player username.\n **Usage**: osurecent {**username**}"
                else:
                    await message.add_reaction(EMOJI_GOOD_COMMAND)
                    message_sent, ed = osuAPIService.get_recent(username)
            await message.channel.send(message_sent)
            if ed != '':
                embed = discord.Embed()
                embed.description = ed
                await message.channel.send(embed=embed)
    else:
        if "727" in message.content:
            await message.channel.send("<a:WYSI:818240754866585630>")
            await message.channel.send(tenorAPIService.get_random_gif("wysi"))


def main():
    load_dotenv()
    client.run(getenv('BOT_TOKEN'))


if __name__ == '__main__':
    main()
