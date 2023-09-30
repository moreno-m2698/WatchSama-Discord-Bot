import discord
import time

from discord.ext import commands

from watchsama.tools.WatchSamaEmbed import WatchSamaEmbed


def __init__(bot):
    ping(bot)
    stop(bot)
    info(bot)
    user_Info(bot)
    server_Info(bot)

def stop(bot: discord.Client):
    @bot.command()
    async def stop(ctx: commands.Context) -> discord.Message:
        #Need to add check so that this cant be called outside of test guild
        await ctx.send(f'Goodbye {ctx.author.name}!')
        await bot.close()

def info(bot: discord.Client):
    @bot.command()
    async def info(ctx: commands.Context) -> discord.Message:
        embed = WatchSamaEmbed(title="WatchSama", url = 'https://github.com/moreno-m2698/Watchsama-Discord-Bot', description='Developers: keopi.')
        await ctx.send(embed=embed)


def ping(bot:discord.Client):
    @bot.command()
    async def ping(ctx:commands.Context) -> discord.Message:
        await ctx.send(f'Pong! {round(bot.latency * 1000)} ms')

def user_Info(bot:discord.Client):
    @bot.command(aliases = ['uinfo', 'whois'])
    async def userinfo(ctx:commands.Context, member: discord.Member = None):
        if member == None:
            member = ctx.message.author
        embed = WatchSamaEmbed(title="User Info:", description=f"Here is user {member.display_name}'s info:", timestamp=ctx.message.created_at)
        embed.set_thumbnail(url=member.avatar)
        embed.add_field(name='ID', value=member.id)
        embed.add_field(name='Username', value = member.name)
        embed.add_field(name='Nickname', value = member.display_name)
        embed.add_field(name="Status", value=member.status)
        embed.add_field(name='Joined at', value = member.joined_at.strftime("%a, %B %#d, %Y, %I:%M %p "))
        embed.add_field(name="Bot?", value = member.bot)
        await ctx.send(embed=embed)

def server_Info(bot:discord.Client):
    @bot.command(aliases = ['sinfo', 'server'])
    async def serverinfo(ctx: commands.Context):

        guild = ctx.guild
        embed = WatchSamaEmbed(title="Server Info:", description=f"Here is the server info for {guild.name}:", timestamp=ctx.message.created_at)
        if guild.icon != None:
            embed.set_thumbnail(url = guild.icon)
        embed.add_field(name="Member Count", value = guild.member_count)
        embed.add_field(name= "Channels", value = f'{len(guild.text_channels)} : text | {len(guild.voice_channels)} : voice')

        if guild.banner != None:
            embed.set_image(url = guild.banner.url)

        await ctx.send(embed=embed)
        
    
