import discord
import os
from discord.ext import commands

import command_vrac
import youtube_player as yt_player

intents = discord.Intents().all()
bot = commands.Bot(command_prefix='!', intents=intents)

# Add commands from command_vrac module
bot.add_command(command_vrac.clear)

# Add commands from youtube_player module
bot.add_command(yt_player.play_music)
bot.add_command(yt_player.show_queue)
bot.add_command(yt_player.pause_music)
bot.add_command(yt_player.resume_music)
bot.add_command(yt_player.skip_music)
bot.add_command(yt_player.leave_channel)
bot.add_command(yt_player.stop_music)


@bot.event
async def on_ready():
    print(f'{bot.user.name} is connected to Discord!')


# Handle errors gracefully
@bot.event
async def on_error(event, *args, **kwargs):
    print('An error occurred:', args[0])

token = os.getenv("BOT_TOKEN")
bot.run(token)
