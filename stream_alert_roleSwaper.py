import os
import discord
from discord.ext import commands
from twitchAPI import Twitch
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.types import AuthScope

intents = discord.Intents().all()
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='!',intents=intents)

# Set up the Twitch API client
twitch = Twitch(os.environ['test1'], os.environ['test2'])
auth = UserAuthenticator(twitch, [AuthScope.USER_READ_EMAIL, AuthScope.USER_READ_SUBSCRIPTIONS])
token, refresh_token = auth.authenticate()
twitch.set_user_authentication(token, [AuthScope.USER_READ_EMAIL, AuthScope.USER_READ_SUBSCRIPTIONS])

# Set up the Twitch notification system
async def twitch_notification(channel, streamer):
    while True:
        streams = twitch.get_streams(user_login=streamer)
        if len(streams['data']) > 0:
            print(f'{streamer} is now live')
            stream = streams['data'][0]
            message = f'{streamer} is now live! Watch at {stream["url"]}'
            await channel.send(message)
        await asyncio.sleep(60)

# Set up the Discord bot
@bot.event
async def on_ready():
    print(f'{bot.user} is ready')

@bot.command()
async def twitch(ctx, streamer_name: str, channel_name: str):
    channel = discord.utils.get(ctx.guild.channels, name=channel_name)
    if channel is None:
        await ctx.send(f'Channel #{channel_name} not found')
    else:
        await ctx.send(f'Twitch notifications for {streamer_name} will now be sent to #{channel.name}')
        await twitch_notification(channel, streamer_name)


