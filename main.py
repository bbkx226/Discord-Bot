import discord
import os
import requests
import json
import random
from replit import db
from keep_alive import keep_alive
from discord.ext import commands, tasks
from random import choice
from random import randint
from datetime import datetime
import pytz

intents = discord.Intents.all()
client = commands.Bot(command_prefix='$', intents=intents)

status = [
    '(ﾉ◕ヮ◕)ﾉ*:･ﾟ✧Resting!✧ﾟ･: *ヽ(◕ヮ◕ヽ)', 'Eating!(ノಠ益ಠ)ノ彡┻━┻',
    '(☞ﾟヮﾟ)☞Sleeping!☜(ﾟヮﾟ☜)', 'Gambling! [̲̅$̲̅(̲̅5̲̅)̲̅$̲̅]',
    'Googling!(づ｡◕‿‿◕｡)づ', '(👍≖‿‿≖)👍Dreaming👍(≖‿‿≖👍)',
    'Fighting!(ง ͠° ͟ل͜ ͡°)ง'
]

player1 = ""
player2 = ""
turn = ""
gameOver = True

board = []

winningConditions = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7],
                     [2, 5, 8], [0, 4, 8], [2, 4, 6]]

if "responding" not in db.keys():
    db["responding"] = True


def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return (quote)


def get_weather(x):
    API_KEY = os.getenv("API_KEY")
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

    request_url = f"{BASE_URL}?q={x}&appid={API_KEY}"

    response = requests.get(request_url)
    if response.status_code == 200:
        data = response.json()
        weather = data['weather'][0]['description']
        temperature = data["main"]["temp"]
        temp = temperature - 273.15
        wind = data['wind']['speed']
        return (
            f"***Weather***: {weather} \n***Temperature***: {round(temp, 2)} celsius\n***Wind speed***: {wind} m/s"
        )
    else:
        return ("An error occured. ")


def get_random_love_message():
    url = "https://ajith-messages.p.rapidapi.com/getMsgs"

    querystring = {"category": "love"}

    headers = {
        "X-RapidAPI-Host": "ajith-messages.p.rapidapi.com",
        "X-RapidAPI-Key": os.getenv("X-RapidAPI-Key")
    }
    response = requests.request("GET",
                                url,
                                headers=headers,
                                params=querystring)
    data = response.json()
    message = data["Message"]
    return (f'***{message}***')


def get_greeting():
    response = requests.get("https://www.greetingsapi.com/random")
    data = response.json()
    greeting = data['greeting']
    lang = data['language']
    return (f'{greeting} | {lang}')


def update_encouragements(encouraging_message):
    if "encouragements" in db.keys():
        encouragements = db["encouragements"]
        encouragements.append(encouraging_message)
        db["encouragements"] = encouragements
    else:
        db["encouragements"] = [encouraging_message]


def delete_encouragment(index):
    encouragements = db["encouragements"]
    if len(encouragements) > index:
        del encouragements[index]
        db["encouragements"] = encouragements


@client.event
async def on_ready():
    change_status.start()
    print('We have logged in as {0.user}'.format(client))


@tasks.loop(seconds=60)
async def change_status():
    await client.change_presence(activity=discord.Game(choice(status)))


@client.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.channels, name='general')
    await channel.send(
        f'Welcome {member.mention}! See `$help` command for details!')


@client.command(name='ping', help='This command returns the latency')
async def ping(ctx):
    await ctx.send(f'*** Latency: {round(client.latency * 1000)}ms ༼ʘ̚ل͜ʘ̚༽')


@client.command(name='inspire', help='This command returns a random quote')
async def inspire(ctx):
    quote = get_quote()
    await ctx.channel.send(quote)


@client.command(name='weather',
                help='This command returns the weather of your city')
async def weather(ctx):
    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel

    await ctx.send("Enter a city name: ")
    msg1 = await client.wait_for("message", check=check)
    x = str(msg1.content)
    wea = get_weather(x)
    await ctx.channel.send(wea)


@client.command(name='love', help='This command returns random love message')
async def love(ctx):
    luv = get_random_love_message()
    await ctx.channel.send(luv)


@client.command(
    name='hello',
    help='This command returns a welcome message with random languange')
async def hello(ctx):
    greet = get_greeting()
    await ctx.channel.send(greet)


@client.command(name='reverse', help='This command returns a reverse number')
async def reverse(ctx):
    def check(msg):
        return msg.author == ctx.author and msg.content.isdigit() and \
               msg.channel == ctx.channel

    await ctx.send("Type a positive number")
    msg1 = await client.wait_for("message", check=check)

    x = int(msg1.content)
    reversed_num = 0
    while x > 0:
        reversed_num = reversed_num * 10 + x % 10
        x //= 10
    await ctx.channel.send(reversed_num)


@client.command(name='time', help='This command returns current time')
async def time(ctx):
    await ctx.channel.send(datetime.now(pytz.timezone('Asia/Shanghai')))


@client.command(name='officials',
                help='This command returns members of ATSM Club')
async def officials(ctx):
    await ctx.channel.send('''
  ----------------------------------------------------------
|Head Of Public Relations & British Relations|
𝓓𝓮𝓻𝓮𝓴 𝓗𝓮𝓷𝓰

|Head Of Acquisitions & Technology|
𝓑𝓻𝓪𝓷𝓭𝓸𝓷 𝓑𝓪𝓷

|Head Of Engineering & Korean Relations|
𝓚𝓪𝓷𝓰 𝓦𝓮𝓲 𝓒𝓱𝓮𝓷𝓰

|Head Of Analytics & Australian Relations|
𝓦𝓮𝓲 𝓧𝓾𝓷 𝓢𝓸𝓲

|Head Of Security & Singaporean Relations|
𝓗𝓪𝓸 𝓨𝓾𝓷 𝓣𝓮𝔂

|Head Of Investments & Finance|
𝓚𝓲𝓽 𝓒𝓱𝓸𝓷𝓰 𝓢𝓮𝓸𝔀

|Head Of Education & Taiwanese Relations|
𝓝𝓲𝓬𝓱𝓸𝓵𝓪𝓼 𝓣𝓪𝓷𝓰

|Head Of Human Resource & Communications|
𝓨𝓲𝔂𝓪𝓷𝓰 𝓣𝓪𝓷

|Head Of Arts & Japanese Relations|
𝓡𝓾𝓲 𝓑𝓲𝓷 𝓛𝓸𝔀

|Head Of Statistics & Data Science|
𝓨𝓲𝓴 𝓢𝓮𝓷𝓰 𝓛𝓲𝓶

|Head Of Health & Chinese Relations|
𝓢𝓲 𝓙𝓲𝓮 𝓝𝓰

|Head Of Auditing & Accounting|
𝓚𝓪𝓲 𝓙𝓾𝓷 𝓝𝓰

|Head Of Entertainment & Canadian Relations|
𝓙𝓲𝓷𝓰 𝓧𝓲𝓪𝓷𝓰 𝓞𝓷𝓰
--------------------©2021 ATSM,Inc-------------------------
  ''')


@client.command(name='die', help='This command returns a random last words')
async def die(ctx):
    responses = [
        'Then I die happy.', 'To the strongest.', 'Do not disturb my circles.',
        'You too, my child?', 'Yet I was once your Emperor.',
        'Shoot, Walter, in the devil\'s name!',
        'I see my God. He calls me to Him.',
        'I am a dead man! Lord, have mercy upon me!'
    ]
    await ctx.send(choice(responses))


@client.command(name='credits', help='This command return the credits')
async def credits(ctx):
    await ctx.send('👉Made by ***BBKX***,')
    await ctx.send('👉Learnt from Youtube and Github,')
    await ctx.send(
        '👉Any advice to improve my bot, please email to bbkx226@gmail.com. Appreciate!***'
    )


@client.command(name='rd', help='This command returns a random number')
async def rd(ctx):
    def check(msg):
        return msg.author == ctx.author and msg.content.isdigit() and \
               msg.channel == ctx.channel

    await ctx.send("Type a positive number")
    msg1 = await client.wait_for("message", check=check)
    await ctx.send("Type a second, larger positive number")
    msg2 = await client.wait_for("message", check=check)
    x = int(msg1.content)
    y = int(msg2.content)
    if x < y:
        value = random.randint(x, y)
        await ctx.send(f"You got {value}.")
    else:
        await ctx.send(
            ":warning: Please ensure the first number is smaller than the second number."
        )


@client.command(name='cheer',
                help='This command returns a random motivational word.')
async def cheer(ctx):
    starter_encouragements = [
        "Cheer up!", "Hang in there.", "You are a great person / bot!",
        "A word of encouragement during a failure is worth more than an hour of praise after success.",
        "When you get to your wits end, you will find, God lives there.",
        "This too shall pass.", "The best revenge is massive success.",
        "It is time for us all to stand and cheer for the doer, the achiever – the one who recognizes the challenges and does something about it.",
        "Fall seven times, stand up eight.",
        "Character cannot be developed in ease and quiet. Only through experience of trial and suffering can the soul be strengthened, ambition inspired, and success achieved.",
        "He who has a why to live can bear almost any how.",
        "Defeat may serve as well as victory to shake the soul and let the glory out.",
        "God uses suffering as a whetstone, to make men sharp with.",
        "Perhaps everything terrible is in its deepest being something helpless that wants help from us.",
        "If the wind will not serve, take to the oars.",
        "Never regret something that once made you smile.",
        "Applause is the spur of noble minds, the end and aim of weak ones.",
        "When you come to the end of your rope, tie a knot and hang on."
    ]
    await ctx.send(choice(starter_encouragements))


@client.command(name='server', help='This command returns server information')
async def server(ctx):
    name = str(ctx.guild.name)
    description = str(ctx.guild.description)

    owner = str(ctx.guild.owner)
    id = str(ctx.guild.id)
    region = str(ctx.guild.region)
    memberCount = str(ctx.guild.member_count)

    icon = str(ctx.guild.icon_url)

    embed = discord.Embed(title=name + " Server Information",
                          description=description,
                          color=discord.Color.blue())
    embed.set_thumbnail(url=icon)
    embed.add_field(name="Owner", value=owner, inline=True)
    embed.add_field(name="Server ID", value=id, inline=True)
    embed.add_field(name="Region", value=region, inline=True)
    embed.add_field(name="Member Count", value=memberCount, inline=True)

    await ctx.send(embed=embed)


@client.command(
    name='tictactoe',
    help='Play game by entering $tictactoe @first_user @second_user')
async def tictactoe(ctx, p1: discord.Member, p2: discord.Member):
    global count
    global player1
    global player2
    global turn
    global gameOver

    if gameOver:
        global board
        board = [
            ":white_large_square:", ":white_large_square:",
            ":white_large_square:", ":white_large_square:",
            ":white_large_square:", ":white_large_square:",
            ":white_large_square:", ":white_large_square:",
            ":white_large_square:"
        ]
        turn = ""
        gameOver = False
        count = 0

        player1 = p1
        player2 = p2

        # print the board
        line = ""
        for x in range(len(board)):
            if x == 2 or x == 5 or x == 8:
                line += " " + board[x]
                await ctx.send(line)
                line = ""
            else:
                line += " " + board[x]

        # determine who goes first
        num = random.randint(1, 2)
        if num == 1:
            turn = player1
            await ctx.send("It is <@" + str(player1.id) + ">'s turn.")
        elif num == 2:
            turn = player2
            await ctx.send("It is <@" + str(player2.id) + ">'s turn.")
    else:
        await ctx.send(
            "A game is already in progress! Finish it before starting a new one."
        )


@client.command(name='place',
                help='This command executes your move in \'Tic Tac Toe\'.')
async def place(ctx, pos: int):
    global turn
    global player1
    global player2
    global board
    global count
    global gameOver

    if not gameOver:
        mark = ""
        if turn == ctx.author:
            if turn == player1:
                mark = ":regional_indicator_x:"
            elif turn == player2:
                mark = ":o2:"
            if 0 < pos < 10 and board[pos - 1] == ":white_large_square:":
                board[pos - 1] = mark
                count += 1

                # print the board
                line = ""
                for x in range(len(board)):
                    if x == 2 or x == 5 or x == 8:
                        line += " " + board[x]
                        await ctx.send(line)
                        line = ""
                    else:
                        line += " " + board[x]

                checkWinner(winningConditions, mark)
                print(count)
                if gameOver == True:
                    await ctx.send(mark + " wins!")
                elif count >= 9:
                    gameOver = True
                    await ctx.send("It's a tie!")

                # switch turns
                if turn == player1:
                    turn = player2
                elif turn == player2:
                    turn = player1
            else:
                await ctx.send(
                    "Be sure to choose an integer between 1 and 9 (inclusive) and an unmarked tile."
                )
        else:
            await ctx.send("It is not your turn.")
    else:
        await ctx.send("Please start a new game using the #tictactoe command.")


def checkWinner(winningConditions, mark):
    global gameOver
    for condition in winningConditions:
        if board[condition[0]] == mark and board[
                condition[1]] == mark and board[condition[2]] == mark:
            gameOver = True


@tictactoe.error
async def tictactoe_error(ctx, error):
    print(error)
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please mention 2 players for this command.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send(
            "Please make sure to mention/ping players (ie. <@688534433879556134>)."
        )


@place.error
async def place_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please enter a position you would like to mark.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Please make sure to enter an integer.")


keep_alive()
client.run(os.getenv("TOKEN"))
