import random
import webpage
import discord
from discord.ext import tasks, commands
from discord import File
import os
import youtube_dl
import asyncio
players = {}


bot = commands.Bot(command_prefix='!')



#----------------------------------
@bot.event
async def on_ready():
    print("Online:")
    print(bot.user.name)
    print("-------")


@bot.command(name='randoom')
async def random_gex(ctx):
    if os.path.exists('textlist.txt'):
        lines = open('textlist.txt', encoding='utf-8').read().splitlines()
        text = random.choice(lines)

        image = os.listdir('./images/')
        imgString = random.choice(image)
        path = "./images/" + imgString

    await ctx.send(file=File(path))
    await ctx.send(text)


#--------------------------------------------

musics = {}
ytdl = youtube_dl.YoutubeDL()


class Video:
    def __init__(self, link):
        video = ytdl.extract_info(link, download=False)
        video_format = video["formats"][0]
        self.url = video["webpage_url"]
        self.stream_url = video_format["url"]

@bot.command()
async def leave(ctx):
    client = ctx.guild.voice_client
    await client.disconnect()
    musics[ctx.guild] = []

@bot.command()
async def resume(ctx):
    client = ctx.guild.voice_client
    if client.is_paused():
        client.resume()


@bot.command()
async def pause(ctx):
    client = ctx.guild.voice_client
    if not client.is_paused():
        client.pause()


@bot.command()
async def skip(ctx):
    client = ctx.guild.voice_client
    client.stop()


def play_song(client, queue, song):
    source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(song.stream_url
        , before_options = "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"))

    def next(_):
        if len(queue) > 0:
            new_song = queue[0]
            del queue[0]
            play_song(client, queue, new_song)
        else:
            asyncio.run_coroutine_threadsafe(client.disconnect(), bot.loop)

    client.play(source, after=next)


@bot.command()
async def play(ctx, url):
    print("play")
    client = ctx.guild.voice_client

    if client and client.channel:
        video = Video(url)
        musics[ctx.guild].append(video)
    else:
        channel = ctx.author.voice.channel
        video = Video(url)
        musics[ctx.guild] = []
        client = await channel.connect()
        play_song(client, musics[ctx.guild], video)

#-----------------------------------------------------------















webpage.keep_alive()
bot.run(os.getenv('TOKEN'))
