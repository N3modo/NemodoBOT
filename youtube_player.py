import discord
import pytube

from discord.ext import commands

intents = discord.Intents().all()
bot = commands.Bot(command_prefix='!', intents=intents)
current_queue = []
currently_playing = 0

is_playlist = lambda x: "list=" in x


def extract_audio_url(video):
    return video.streams.filter(only_audio=True).first().url


# Function to download audio from YouTube
def get_audio(url):
    try:
        if is_playlist(url):
            return pytube.Playlist(url).videos
        else:
            return [pytube.YouTube(url)]
    except pytube.exceptions.PytubeError as e:
        print(f"Error extracting audio stream: {e}")


def reschedule_play(exception, voice_client):
    global current_queue, currently_playing
    if exception:
        print("Reschedule exception: ", exception)
        return
    if currently_playing >= len(current_queue):
        return
    currently_playing += 1
    schedule_play(voice_client)


def schedule_play(voice_client):
    global current_queue, currently_playing
    if currently_playing >= len(current_queue):
        return

    audio_url = extract_audio_url(current_queue[currently_playing])
    audio_source = discord.FFmpegPCMAudio(audio_url,
                                          before_options=" -reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 1")
    voice_client.play(audio_source, after=lambda e: reschedule_play(e, voice_client))


@bot.event
async def on_ready():
    print(f'{bot.user.name} is connected to Discord!')


@bot.command(name='play')
async def play_music(ctx, *, url):
    global current_queue, currently_playing
    voice_client = ctx.voice_client

    if not ctx.author.voice:
        await ctx.send("You are not connected to a voice channel!")
        return

    voice_channel = ctx.author.voice.channel

    if voice_client is None:
        await voice_channel.connect()
        voice_client = ctx.voice_client
        print(f"Bot joined voice channel: {voice_channel.name}")
    elif voice_client.channel != voice_channel:
        await voice_client.move_to(voice_channel)
        print(f"Bot moved to voice channel: {voice_channel.name}")

    last_queue_len = len(current_queue)
    current_queue += get_audio(url)
    print(f"Added {len(current_queue) - last_queue_len} video(s) to the queue")

    if not voice_client.is_playing():
        currently_playing = last_queue_len
        schedule_play(voice_client)
        print("Started playing music")


@bot.command(name='queue')
async def show_queue(ctx):
    global current_queue, currently_playing
    if not current_queue:
        await ctx.send("La file d'attente est vide.")
    else:
        queue_list = []
        for i, video in enumerate(current_queue, start=currently_playing + 1):
            queue_list.append(f"{i}. {video.title}")
        queue_message = "\n".join(queue_list)
        await ctx.send(f"File d'attente des chansons:\n{queue_message}")



@bot.command(name='pause')
async def pause_music(ctx):
    voice_client = ctx.voice_client
    if voice_client is not None and voice_client.is_playing():
        voice_client.pause()
        print("Music paused")


@bot.command(name='resume')
async def resume_music(ctx):
    voice_client = ctx.voice_client
    if voice_client is not None and voice_client.is_paused():
        voice_client.resume()
        print("Music resumed")


@bot.command(name='skip')
async def skip_music(ctx):
    global currently_playing, current_queue
    voice_client = ctx.voice_client
    if voice_client is not None and voice_client.is_playing():
        voice_client.stop()
    else:
        await ctx.send("Aucune musique n'est actuellement en cours de lecture.")



@bot.command(name='stop')
async def stop_music(ctx):
    global currently_playing, current_queue
    voice_client = ctx.voice_client
    if voice_client is not None:
        if voice_client.is_playing() or voice_client.is_paused():
            voice_client.stop()
            current_queue.clear()
            currently_playing = 0
            await ctx.send("La lecture de musique a été arrêtée et la file d'attente a été effacée.")
        await voice_client.disconnect()
        await ctx.send("Le bot a quitté le canal vocal.")


@bot.command(name='leave')
async def leave_channel(ctx):
    voice_client = ctx.voice_client
    if voice_client is not None:
        await voice_client.disconnect()
        print("Bot left the voice channel")