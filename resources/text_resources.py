HELP_TEXT_EN = f'''I am Cappuccino, a bot made by Lulu x Pix/PapuruHoshi.
I am currently under huge development (unless my creator is lazy).
Here are all of the commands currently available:
*\* [required] {{optional}} *
- **help**: Show this entire message
- **cuu**: Hiện danh sách câu lệnh của bot
- **bruh**: Bruh
- **chatting**: Send the "Chatting" embed
- **gif {{keyword}}**: Get a GIF from Tenor
- **hello**: Say hello to Cappuccino!
- **roll** {{range}}: Get a random number from 1 to 100, unless range specified
- **scramble**: Guess the scrambled word
- **osu top** [username]: Get the osu! top 50 plays of the user specified
- **osu best** [username]: Get the osu! top play of the user specified
- **osu recent** [username]: Get the osu! recent play of the user specified
'''

HELP_TEXT_VI = f'''Đây là Cappuccino, một bot tạo bởi Lulu x Pix/PapuruHoshi.
Bot đang được phát triển nên sẽ chưa có nhiều tính năng.
Các câu lệnh hiện đang có (**toàn bộ đầu ra của các câu lệnh đều là tiếng Anh**):
*\* [bắt buộc] {{không bắt buộc}} *
- **help**: Show command list
- **cuu**: Hiện tin nhắn này
- **bruh**: Bruh
- **chatting**: Gửi embed "Chatting"
- **gif {{từ khoá}}**: Tìm kiếm GIF trên Tenor
- **hello**: Chào hỏi!
- **roll** {{n}}: Trả về một số từ 1 tới n, mặc định n=100
- **scramble**: Sắp xếp lại từ tiếng Anh
- **osu top** [tên người chơi]: (osu!) Trả về 50 top plays của người chơi được ghi trong lệnh
- **osu best** [tên người chơi]: (osu!) Trả về top play của người chơi được ghi trong lệnh
- **osu recent** [tên người chơi]: (osu!) Trả về lượt chơi gần đây nhất của người chơi được ghi trong lệnh
'''

UNSET_USERNAME_WARNING = "**You have not set your osu! username!**" \
                         "\n Use `/osu set_username <username>` to set your username."

HELP_TEXTS = {"en": HELP_TEXT_EN, "vi": HELP_TEXT_VI}
