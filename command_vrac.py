import discord
from discord.ext import commands
import asyncio

intents = discord.Intents().all()
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='!', intents=intents)


def is_mod(ctx):
    return ctx.author.guild.permissions.manage_messages


@bot.command()
async def clear(ctx):
    message_count = len([msg async for msg in ctx.channel.history()])
    if message_count == 0:
        clear_message = await ctx.send('The channel is already empty!')
        await asyncio.sleep(3)  # wait for 3 seconds
        await clear_message.delete()
    else:
        await ctx.channel.purge()
        empty_message = await ctx.send('The channel is now empty!')
        await asyncio.sleep(3)  # wait for 3 seconds
        await empty_message.delete()
