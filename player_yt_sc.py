import discord
from discord.ext import commands
import asyncio
import soundcloud
from soundcloud_lib import resolve
from youtube_search_python import SearchVideos
from pytube import YouTube

bot = commands.Bot(command_prefix='!')
client = soundcloud.Client(client_id='YOUR_CLIENT_ID')

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command(name='join')
async def join_channel(ctx):
    if not ctx.author.voice:
        await ctx.send("You are not connected to a voice channel")
        return
    voice_channel = ctx.author.voice.channel
    if ctx.voice_client is None:
        await voice_channel.connect()
    else:
        await ctx.voice_client.move_to(voice_channel)

@bot.command(name='leave')
async def leave_channel(ctx):
    if ctx.voice_client is not None:
        await ctx.voice_client.disconnect()

@bot.command(name='play')
async def play_music(ctx, *, query):
    if not ctx.author.voice:
        await ctx.send("You are not connected to a voice channel")
        return
    voice_channel = ctx.author.voice.channel
    voice_client = ctx.voice_client
    if voice_client is None:
        try:
            await voice_channel.connect()
        except discord.ClientException:
            await ctx.send("I'm already in a voice channel!")
            return
        voice_client = ctx.voice_client
    if 'soundcloud.com' in query:
        try:
            track = resolve(query, client_id=client.client_id)
            stream_url = client.get(track['stream_url'], allow_redirects=False).location
        except:
            await ctx.send("Error: could not find SoundCloud track")
            return
    else:
        try:
            search = SearchVideos(query, offset=1, mode="json", max_results=1)
            result = search.result()
            url = eval(result)[0]['link']
            video = YouTube(url)
            stream = video.streams.filter(only_audio=True).first()
            stream_url = stream.url
        except:
            await ctx.send("Error: could not find YouTube video")
            return

    voice_client.play(discord.FFmpegPCMAudio(stream_url))
    while voice_client.is_playing():
        await asyncio.sleep(1)

@bot.command(name='pause')
async def pause_music(ctx):
    voice_client = ctx.voice_client
    if voice_client is not None and voice_client.is_playing():
        voice_client.pause()

@bot.command(name='resume')
async def resume_music(ctx):
    voice_client = ctx.voice_client
    if voice_client is not None and voice_client.is_paused():
        voice_client.resume()



