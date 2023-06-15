import discord
import os
from discord.ext import commands

import command_vrac
import youtube_player as yt_player


async def on_ready():
    print(f'{bot.user.name} is connected to Discord!')


# Handle errors gracefully
async def on_error(event, *args, **kwargs):
    print('An error occurred:', args[0])


if __name__ == "__main__":
    intents = discord.Intents().all()
    bot = commands.Bot(command_prefix=command_vrac.command_prefix, intents=intents)
    # Add commands from command_vrac module
    bot.command(name='clear')(command_vrac.clear)
    bot.command(name='change_prefix')(command_vrac.change_prefix)

    # Add commands from youtube_player module
    bot.command(name='play')(yt_player.play_music)
    bot.command(name='queue')(yt_player.show_queue)
    bot.command(name='pause')(yt_player.pause_music)
    bot.command(name='resume')(yt_player.resume_music)
    bot.command(name='skip')(yt_player.skip_music)
    bot.command(name='leave')(yt_player.leave_channel)
    bot.command(name='stop')(yt_player.stop_music)
    bot.event(on_ready)
    bot.event(on_error)
    token = os.getenv("BOT_TOKEN")
    if token is None:
        print("Environment variable \"BOT_TOKEN\" must be defined")
        exit(1)
    bot.run(token)
