import discord
from discord.ext import commands

intents = discord.Intents().all()
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='!', intents=intents)

# global variables to store selected role and emoji
selected_role = None
selected_emoji = None


@bot.event
async def on_ready():
    print('Bot is ready!')


@bot.command()
async def add_role_reaction(ctx, message_id: int, role: discord.Role):
    global selected_role, selected_emoji
    selected_role = role
    message = await ctx.fetch_message(message_id)
    await ctx.send(f"React to this message to choose your emoji: {message.jump_url}")

    def check(reaction, user):
        return user == ctx.author and reaction.message.id == message.id

    print('ok1')
    reaction, user = await bot.wait_for('reaction_add', check=check)
    print(selected_emoji,selected_role)
    selected_emoji = reaction.emoji
    print('ok2')
    try:
        await message.add_reaction(selected_emoji)
        await ctx.send("Reaction added successfully!")
        print('ok3')
    except:
        await ctx.send("Failed to add reaction. Please check the bot's permissions and try again.")
        print("ok4")


@bot.event
async def on_raw_reaction_add(payload):
    global selected_role, selected_emoji
    if selected_emoji and str(payload.emoji) == selected_emoji:
        guild = bot.get_guild(payload.guild_id)
        role = selected_role
        if role:
            member = guild.get_member(payload.user_id)
            await member.add_roles(role)

token = os.getenv("BOT_TOKEN")
bot.run(token)

