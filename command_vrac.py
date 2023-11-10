import discord
import os
from discord.ext import commands
import asyncio

env_prefix = os.getenv("BOT_CMD_PREFIX")
bot_prefix = env_prefix if env_prefix is not None else '!'


def is_mod(ctx):
    return ctx.author.guild.permissions.manage_messages


async def clear(ctx):
    print("channel cleared")
    await ctx.channel.purge()


async def command_prefix(this_bot: commands.Bot, message: discord.Message) -> str:
    global bot_prefix
    if not (not isinstance(message.channel, discord.channel.DMChannel)
            and not isinstance(message.channel, discord.channel.GroupChannel)):
        print(this_bot.user.name + " has received a message through DM")
        return ''
    return bot_prefix


async def change_prefix(ctx, *, new_prefix: str):
    global bot_prefix
    p = new_prefix.split()
    msg = "Prefix changed to : '" + p[0] + "'"
    if len(p) == 1:
        bot_prefix = p[0]
    else:
        bot_prefix = p
        msg += "  (or '" + '\',\''.join(p[1:]) + "')"
    await ctx.send(msg)


async def command_prefix(this_bot: commands.Bot, message: discord.Message) -> str:
    global bot_prefix
    if not (not isinstance(message.channel, discord.channel.DMChannel)
            and not isinstance(message.channel, discord.channel.GroupChannel)):
        print(this_bot.user.name + " has received a message through DM")
        return ''
    return bot_prefix


async def change_prefix(ctx, *, new_prefix: str):
    global bot_prefix
    p = new_prefix.split()
    msg = "Prefix changed to : '" + p[0] + "'"
    if len(p) == 1:
        bot_prefix = p[0]
    else:
        bot_prefix = p
        msg += "  (or '" + '\',\''.join(p[1:]) + "')"
    await ctx.send(msg)
