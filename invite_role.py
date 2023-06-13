import discord
from discord.ext import commands

intents = discord.Intents().all()
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='!',intents=intents)

# Dictionary to store role-invite link pairs
role_invites = {}

@bot.command()
async def invite_with_role(ctx, role_name: str):
    # Get the server the command was called in
    server = ctx.guild

    # Find the role by name
    role = discord.utils.get(server.roles, name=role_name)

    # Create an invite link that doesn't expire
    invite = await ctx.channel.create_invite(max_age=0)

    # Store the role-invite link pair in the dictionary
    role_invites[role.id] = invite.url

    # Send the invite link to the channel where the command was called
    await ctx.send(f'Here is the invite link: {invite}')

    # Add the role to anyone who joins using the invite link
    @bot.event
    async def on_member_join(member):
        if member.guild == server:
            await member.add_roles(role)

@bot.command()
async def list_role_invites(ctx):
    # Generate a list of role-invite link pairs
    role_invite_list = '\n'.join(f'{ctx.guild.get_role(role_id).name}: {invite_url}'
                                 for role_id, invite_url in role_invites.items())

    # Send the list to the channel where the command was called
    await ctx.send(f'Here are the roles that are linked to invite links:\n{role_invite_list}')

@bot.command()
@commands.has_permissions(manage_roles=True)  # only allow users with "manage roles" permission to use this command
async def unlink_invite(ctx, role_name: str):
    # Check if the role name is valid
    role = discord.utils.get(ctx.guild.roles, name=role_name)
    if not role:
        await ctx.send(f"Invalid role name: {role_name}")
        return

    # Check if there is an invite linked to the role
    if role.id not in role_invites:
        await ctx.send(f"No invite is linked to the role '{role_name}'")
        return

    # Delete the invite
    invite = await bot.fetch_invite(role_invites[role.id])
    await invite.delete(reason="Role unlinked from invite")

    # Remove the role from the linked roles dictionary
    del role_invites[role.id]

    await ctx.send(f"Invite and role '{role_name}' have been unlinked and deleted")


