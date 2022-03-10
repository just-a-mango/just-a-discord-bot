import discord
from discord.ext import commands
import random
from discord.utils import get
from itertools import cycle
from better_profanity import profanity
import praw
import youtube_dl
import os
import shutil

reddit = praw.Reddit(
    client_id = "your client id",
    client_secret = "your client secret",
    username = "python_praw123",
    password = "python123",
    user_agent = "pythonpraw"
)

token = "your discord bot's token"

commands_prefix = '/'

client = commands.Bot(command_prefix=commands_prefix)

client.remove_command('help')

banned_words = [
    'piss',
    'idiot',
    'chungus',
    'arse',
    'ass',
    'bastard',
    'bitch',
    'bollocks',
    'bugger',
    'child-fucker',
    'christ on a bike',
    'christ on a cracker',
    'christ',
    'crap',
    'cunt',
    'damn',
    'effing',
    'frigger',
    'fuck',
    'goddamn',
    'godsdamn',
    'hell',
    'holy shit',
    'horseshit',
    'jesus christ',
    'jesus fuck',
    'jesus H. Christ',
    'Jesus Harold Christ',
    'Jesus wept',
    'Jesus, Mary and Joseph',
    'Judas Priest',
    'motherfucker',
    'nigga',
    'prick',
    'shit',
    'shit ass',
    'shitass',
    'slut',
    'son of a bitch',
    'son of a whore',
    'sweet Jesus',
    'twat'
]
profanity.add_censor_words(banned_words)

possible_answers = [
                "No swearing allowed! Read the rules!",
                "DO NOT SWEAR",
                "Hey! Don't swear! Have you read the rules ?",
                "Oh come on! You know you're not allowed to swear! If you don't, read the rules!!!",
                "STOP SWEARING",
                "N O    S W E A R I N G    A L L O W E D",
                "DON'T SWEAR"
            ]

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game("Your bot's game activity"))
    print("Bot is ready")

@client.event
async def on_message(msg):
    if profanity.contains_profanity(msg.content) == True:
        user = msg.author
        await user.send(random.choice(possible_answers))
        await msg.delete()
    if ":" == msg.content[0] and ":" == msg.content[-1]:
        emoji_name = msg.content[1:-1]
        for emoji in msg.guild.emojis:
            if emoji_name == emoji.name:
                await msg.channel.send(str(emoji))
                await msg.delete()
        

@client.event
async def on_command_error(ctx,error):
    if isinstance(error,commands.MissingPermissions):
        await ctx.send("You can't do that ;-;", delete_after = 3)
        await ctx.message.delete()
    elif isinstance(error,commands.MissingRequiredArgument):
        await ctx.send("You didn't enter all the required arguments...;-;", delete_after = 3)
        await ctx.message.delete()
    else:
        raise error

@client.command()
async def ping(ctx):
    await ctx.send(f"The current server latency is : {round(client.latency * 1000)}ms", delete_after = 7)

@client.command(aliases=['question', 'test'])
async def quesion(ctx, *, question):
    responses = [



        "It is certain.",

        "It is decidedly so.",

        "Without a doubt.",

        "Yes - definitely.",

        "You may rely on it.",

        "As I see it, yes.",

        "Most likely.",

        "Outlook good.",

        "Yes.",

        "Signs point to yes.",

        "Reply hazy, try again.",

        "Ask again later.",

        "Better not tell you now.",

        "Cannot predict now.",

        "Concentrate and ask again.",

        "Don't count on it.",

        "My reply is no.",

        "My sources say no.",

        "Outlook not so good.",

        "Very doubtful."
    ]
    await ctx.send(f'Ok. So....The question was : {question}\nAnd here is my answer : {random.choice(responses)}')



@client.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx,amount=10):
    await ctx.channel.purge(limit=amount)

@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member : discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'{member.mention} successfully kicked out from the server.')

@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member : discord.Member, *, reason="No fuckin' reason :rofl:"):
    await member.ban(reason=reason)
    await ctx.send(f'{member.mention} successfully banned from the server.')
    await member.send(f"O O F - You've been banned from {server} - Reason : {reason}")

@client.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split("#")
    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'{user.mention} was successfully unbanned')
            return


@client.command()
@commands.has_permissions(ban_members=True)
async def unbanall(ctx):
    banned_users = await ctx.guild.bans()
    for ban_entry in banned_users:
        user = ban_entry.user
        await ctx.guild.unban(user)
        await ctx.send(f'{user.mention} was successfully unbanned')
        return



@client.command()
async def meme(ctx,subred = "memes"):
    subreddit = reddit.subreddit(subred)
    all_subs = []
    top = subreddit.top(limit = 50)
    for submission in top:
        all_subs.append(submission)

    random_sub = random.choice(all_subs)
    name = random_sub.title
    url = random_sub.url
    em = discord.Embed(title = name)
    em.set_image(url = url)
    await ctx.send(embed = em)

@client.command(pass_context=True)
async def help(ctx):
    embed = discord.Embed(
        colour = discord.Colour.gold()
    )
    embed.set_author(name='Help')
    embed.add_field(name='/ping', value='Returns the current server latency in ms', inline=False)
    embed.add_field(name='/question <question>', value='Returns the answer to your question!', inline=False)
    embed.add_field(name='/clear <amount(10 by default)>', value='Deletes messages. If number is not specified, the default is 10', inline=False)
    embed.add_field(name='/kick <member>', value='Kicks a member', inline=False)
    embed.add_field(name='/ban <member>', value='Bans a member', inline=False)
    embed.add_field(name='/unban <member>', value='Unbans a banned member', inline=False)
    embed.add_field(name='/unbanall', value='Unbans all the banned members', inline=False)
    embed.add_field(name='/meme <subreddit(memes by default)>', value='Posts a random funny meme', inline=False)
    embed.add_field(name='/play <url>', value="If you're in a voice channel, the bot will play the audio from the specified URL", inline=False)
    embed.add_field(name='/pause', value="Pauses the current audio", inline=False)
    embed.add_field(name='/resume', value="Pauses the current audio", inline=False)
    embed.add_field(name='/join', value="Joins your current voice channel", inline=False)
    embed.add_field(name='/leave', value="Leaves your current voice channel", inline=False)
    embed.add_field(name='/stop', value="Stops the current audio", inline=False)
    embed.add_field(name='/queue <url>', value="Puts a song in the song queue", inline=False)
    await ctx.send(embed=embed)

@client.command(pass_context=True)
@commands.has_role("DJ")
async def join(ctx):
    global voice
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()

    await voice.disconnect()

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
        print(f"The bot has connected to {channel}\n")

    await ctx.send(f"The awesome😝, 😝beautiful, and 😝intelligent bot that I am joined {channel}")

@client.command(pass_context=True)
@commands.has_role("DJ")
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.disconnect()
        print(f"The bot has left {channel}")
        await ctx.send(f"Left {channel}")
    else:
        print("Bot was told to leave voice channel, but was not in one")
        await ctx.send("Don't think I am in a voice channel...💢🗯️😡")

@client.command(pass_context=True)
@commands.has_role("DJ")
async def play(ctx, url: str):
    global voice
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()

    await voice.disconnect()

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
        print(f"The bot has connected to {channel}\n")

    await ctx.send(f"The awesome😝, 😝beautiful, and 😝intelligent bot that I am joined {channel}")

    def check_queue():
        Queue_infile = os.path.isdir("./Queue")
        if Queue_infile is True:
            DIR = os.path.abspath(os.path.realpath("Queue"))
            length = len(os.listdir(DIR))
            still_q = length - 1
            try:
                first_file = os.listdir(DIR)[0]
            except:
                print("No more queued song(s)\n")
                queues.clear()
                return
            main_location = os.path.dirname(os.path.realpath(__file__))
            song_path = os.path.abspath(os.path.realpath("Queue") + "\\" + first_file)
            if length != 0:
                print("Song done, playing next queued\n")
                print(f"Songs still in queue: {still_q}")
                song_there = os.path.isfile("song.mp3")
                if song_there:
                    os.remove("song.mp3")
                shutil.move(song_path, main_location)
                for file in os.listdir("./"):
                    if file.endswith(".mp3"):
                        os.rename(file, 'song.mp3')

                voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: check_queue())
                voice.source = discord.PCMVolumeTransformer(voice.source)
                voice.source.volume = 0.07

            else:
                queues.clear()
                return

        else:
            queues.clear()
            print("No songs were queued before the ending of the last song\n")



    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
            queues.clear()
            print("Removed old song file")
    except PermissionError:
        print("Trying to delete song file, but it's being played")
        await ctx.send("ERROR: Music playing(yup, that sounds really bad...😬)")
        return


    Queue_infile = os.path.isdir("./Queue")
    try:
        Queue_folder = "./Queue"
        if Queue_infile is True:
            print("Removed old Queue Folder")
            shutil.rmtree(Queue_folder)
    except:
        print("No old Queue folder")
    possible_waits = [
        "Gimme a sec, I'm getting everything ready...😉",
        "Getting everything ready...😉",
        "Getting everything setup...😉",
        "Just wait a sec, I'm getting everything ready...😉",
        "Getting everything ready properly...😉",
        "Getting everything setup properly...😉",
        "Look! A Wumpus(getting everything ready..)👁️!!!",
        "Look! A Wumpus!!👁️",
        "Look! That's a Wumpus!!!👁️",
        "Look! A wumpus(getting everything setup...)👁️!!!"
    ]
    await ctx.send(f"{random.choice(possible_waits)}")

    voice = get(client.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print("Downloading audio now\n")
        ydl.download([url])

    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            name = file
            print(f"Renamed File: {file}\n")
            os.rename(file, "song.mp3")

    voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: check_queue())
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.07

    nname = name.rsplit("-", 2)
    await ctx.send(f"Ok so here's what I'm gonna play right now(it's that song right ?) : {nname[0]}")
    print("playing\n")

@client.command(pass_context=True)
@commands.has_role("DJ")
async def pause(ctx):

    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_playing():
        print("Music paused")
        voice.pause()
        await ctx.send("Music paused...That's too bad...🙍")
    else:
        print("Music not playing failed pause")
        await ctx.send("Music not playing failed pause...(oh shit, that's an error...😬)")

@client.command(pass_context=True)
@commands.has_role("DJ")
async def resume(ctx):

    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_paused():
        print("Resumed music")
        voice.resume()
        await ctx.send("Resumed music...🕺WWOOOA💃OAOOOOAO💃AOAOAOOAO💃AOAO🕺")
    else:
        print("Music is not paused")
        await ctx.send("Music is not paused(doesn't sound good...😬)")

@client.command(pass_context=True)
@commands.has_role("DJ")
async def stop(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)

    queues.clear()

    if voice and voice.is_playing():
        print("Music stopped")
        voice.stop()
        await ctx.send("The current music was stopped...😔")
    else:
        print("No music playing failed to stop")
        await ctx.send("Dude, there wasn't anything playing! WHY ?! 💢🗯️😡")

queues = {}

@client.command(pass_context=True)
@commands.has_role("DJ")
async def queue(ctx, url: str):
    Queue_infile = os.path.isdir("./Queue")
    if Queue_infile is False:
        os.mkdir("Queue")
    DIR = os.path.abspath(os.path.realpath("Queue"))
    q_num = len(os.listdir(DIR))
    q_num += 1
    add_queue = True
    while add_queue:
        if q_num in queues:
            q_num += 1
        else:
            add_queue = False
            queues[q_num] = q_num

    queue_path = os.path.abspath(os.path.realpath("Queue") + f"\song{q_num}.%(ext)s")

    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'outtmpl': queue_path,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print("Downloading audio now\n")
        ydl.download([url])
    await ctx.send("K I'm adding this " + str(q_num) + " to the 💃song🕺 queue")

    print("Song added to queue\n")

client.run(token)
