import discord
import os
from discord.ext import commands, tasks
from itertools import cycle

client = commands.Bot(command_prefix = "/")
client.remove_command('help')
status = cycle(['/help! | QUACK!','QUACK QUACK | I am a DUCK!','STILL FIXING THINGS! | QUACK'])







#events
@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.idle)
    change_status.start()
    print('I am now Online!')

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('Quack! Quack! Your Command Is Not Found!')
       

@tasks.loop(seconds=10)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))








#commands
@client.group(name="help", invoke_without_command=True, aliases=["Help", "HELP"])
async def helpcmd(ctx):
    embed = discord.Embed(title="**BOT COMMANDS!**", description="**LIST OF COMMANDS FROM THE BOT**", colour=discord.Colour.orange())
    
    embed.add_field(name="Miscellanious", value="/misc For the list of the miscellanious commands!")
    embed.add_field(name="Administrator", value="/admin For the list of the admin commands!")
    embed.add_field(name="Settings", value="/settings For the list of the settings commands!")
    
    
    await ctx.send(embed=embed)
    
@helpcmd.command(name='misc', aliases=['Misc', 'MISC'])
async def misc_cmd(ctx):
    await ctx.send('```••••••••••••••••Miscellanious•••••••••••••••```')
    await ctx.send('```HELP /help - Shows this Message!```')
    await ctx.send('```SAY /say - Says that you typed!```')
    
@helpcmd.command(name='admin',aliases=['Admin', 'ADMIN'])
async def admincmd(ctx):
    await ctx.send('```••••••••••••••••Administration••••••••••••••```')
    await ctx.send('```CLEAR /clear - clears the messages that was typed before```')
    await ctx.send('```KICK /kick - Kicks the mentioned user from the server```')
    await ctx.send('```BAN /ban - List of available ban command!```')
    
@helpcmd.command(name='settings', aliases=['Settings', 'SETTINGS', 'setting', 'Setting', 'SETTING'])
async def settingscmd(ctx):
    await ctx.send('```••••••••••••••••••Settings••••••••••••••••••```')
    await ctx.send('```PING /ping - shows the latency of the bot```')
  
@client.command()
async def say(ctx, *, msg):
    await ctx.channel.purge(limit=1)
    await ctx.send(msg)
 
@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')
    
@client.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount=3):
    await ctx.channel.purge(limit=amount)
    
@client.command()
@commands.has_permissions(administrator=True)
async def kick(ctx, member : discord.Member, *, reason='Misbehavior'):
    await member.kick(reason=reason)
    await ctx.send(f'Kicked {member.mention}')
    
@client.group(name='ban', invoke_without_command=True, aliases=['Ban', 'BAN'], )
async def bancmds(ctx):
    await ctx.send('```•••••••••••••••••Ban|Commands•••••••••••••••```')
    await ctx.send('```BAN ADD /ban add - Command will ban a mantioned user!```')
    await ctx.send('```BAN DEL /ban del - Command will unban a mantioned user!```')
    
@bancmds.command(name='add', aliases=['Add'])
@commands.has_permissions(administrator=True)
async def ban_add(ctx, member : discord.Member, *, reason='Misbehavior'):
    await member.ban(reason=reason)
    await ctx.send(f'Banned {member.mention}')
    
@bancmds.command(name='del', aliases=['Del'])
@commands.has_permissions(administrator=True)
async def ban_del(ctx, *, member):
    banned_users = await ctx.guild.bans()
    mamber_name, member_discriminator = member.split('#')
    
    for banned_entry in banned_users:
        user = banned_entry.user
        
        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.mention}')
            return

client.run(os.getenv('Token'))
