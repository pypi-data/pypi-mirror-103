try:
    import asyncio
    import sys
    from termcolor import colored
    import sanic
    import aioconsole
    from sanic import Sanic
    import os
    import time
    from datetime import datetime
    import json
    from functools import partial
    import random as rand

    from colorama import Fore, Back, Style, init
    init(autoreset=True)

    import fortnitepy
    from fortnitepy.ext import commands
    import BenBotAsync
    import aiohttp
    import requests
    from flask import Flask, render_template
    import keep_alive
    from threading import Thread
    import discord, os

    from fortnitepy.ext import commands as fortnite_commands
    from discord.ext import commands as discord_commands

except ModuleNotFoundError as e:
    print(e)
    print(Fore.RED + f'[-] ' + Fore.RESET + 'Failed to import 1 or more modules. Run "INSTALL PACKAGES.bat')
    exit()




discord_bot = discord.Client

os.system('cls||clear')
sanic_app = sanic.Sanic(__name__)

intro = Fore.LIGHTYELLOW_EX + """
--------------------------------------------------------
Thanks For Using GuffBot
--------------------------------------------------------
"""

print(intro)

def lenPartyMembers():
    members = client.party.members
    return len(members)

def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn

def lenFriends():
    friends = client.friends
    return len(friends)

def getNewSkins():
    r = requests.get('https://benbotfn.tk/api/v1/files/added')

    response = r.json()

    cids = []

    for cid in [item for item in response if item.split('/')[-1].upper().startswith('CID_')]:
        cids.append(cid.split('/')[-1].split('.')[0])
    
    return cids

def getNewEmotes():
    r = requests.get('https://benbotfn.tk/api/v1/files/added')

    response = r.json()

    eids = []

    for cid in [item for item in response if item.split('/')[-1].upper().startswith('EID_')]:
        eids.append(cid.split('/')[-1].split('.')[0])
    
    return eids

def get_device_auth_details():
    if os.path.isfile('templates/auths.json'):
        with open('templates/auths.json', 'r') as fp:
            return json.load(fp)
    else:
        with open('templates/auths.json', 'w+') as fp:
            json.dump({}, fp)
    return {}

def store_device_auth_details(email, details):
    existing = get_device_auth_details()
    existing[email] = details

    with open('templates/auths.json', 'w') as fp:
        json.dump(existing, fp)

with open('config.json') as f:
    try:
        data = json.load(f)
    except json.decoder.JSONDecodeError as e:
        print(Fore.RED + ' [ERROR] ' + Fore.RESET + "There was an error in one of the bot's files! (config.json).")
        print(Fore.LIGHTRED_EX + f'\n {e}')
        exit(1)

with open('config.json') as f:
    try:
        info = json.load(f)
    except json.decoder.JSONDecodeError as e:
        print(Fore.RED + ' [ERROR] ' + Fore.RESET + "There was an error in one of the bot's files! (config.json) ")
        print(Fore.LIGHTRED_EX + f'\n {e}')
        exit(1)



def is_admin():
    async def predicate(ctx):
        return ctx.author.id in info['FullAccess']
    return commands.check(predicate)

async def get_authorization_code():
    while True:
        response = await aioconsole.ainput("Please Get an auth code from https://rebrand.ly/authcode sign in as and enter the response here: ")
        if "redirectUrl" in response:
            response = json.loads(response)
            if "?code" not in response["redirectUrl"]:
                print(colored("Invalid response.", "red"))
                continue
            code = response["redirectUrl"].split("?code=")[1]
            return code
        else:
            if "https://accounts.epicgames.com/fnauth" in response:
                if "?code" not in response:
                    print(colored("invalid response.", "red"))
                    continue
                code = response.split("?code=")[1]
                return code
            else:
                code = response
                return code

device_auth_details = get_device_auth_details().get(data['email'], {})

prefix = '!'

client = commands.Bot(
    command_prefix=prefix,
    case_insensitive=True,
    auth=fortnitepy.AdvancedAuth(
        prompt_authorization_code=True,
        delete_existing_device_auths=True,
        authorization_code=get_authorization_code,
        **device_auth_details
    ),
    status=data['status'],
    platform=fortnitepy.Platform(data['platform']),
)
description = 'GuffBot v2 Help'
discord_bot = discord_commands.Bot(
        command_prefix='!',
        description=description,
        case_insensitive=True,
        help_command=None
    )

@discord_bot.command(hidden = True)
async def help(ctx, *, command = None):
    "Get some dancing help"
    emb = discord.Embed(title = "GuffBot | Help")
    emb.set_thumbnail(url = "")
    if command:
        c = bot.get_command(command)
        if not c:
            emb = discord.Embed(description = "Nah, that's not a command", colour = discord.Colour.red())
            return await ctx.send(embed = emb)
        emb.description = f"**`{c.name} {c.signature}`**\n*{c.help}*"
        return await ctx.send(embed = emb)
    res = ""
    for a in discord_bot.commands:
        if a.name != "jishaku":
            if not a.hidden:
                res += f"**!{a.name}** {a.help}\n"
    emb.description = res
    await ctx.send(embed = emb)




@client.event
async def event_device_auth_generate(details, email):
    store_device_auth_details(email, details)

discord_bot_token =data['TOKEN']  # the discord bots token


@client.event
async def event_ready():
    os.system('cls||clear')
    print(intro)
    print(Fore.LIGHTBLUE_EX + 'Fortnite Client Ready As ' + Fore.LIGHTWHITE_EX + f'{client.user.display_name}')
    
    
    member = client.party.me

    await member.edit_and_keep(
        partial(
            fortnitepy.ClientPartyMember.set_outfit,
            variants = client.party.me.create_variants(material=data['style']),
            asset=data['cid'],
        ),
        partial(
            fortnitepy.ClientPartyMember.set_backpack,
            variants = client.party.me.create_variants(material=data['bidstyle']),
            asset=data['bid'],
        ),
        partial(
            fortnitepy.ClientPartyMember.set_pickaxe,
            asset=data['pid']
        ),
        partial(
            fortnitepy.ClientPartyMember.set_banner,
            icon=data['banner'],
            color=data['banner_color'],
            season_level=data['level']
        ),
        partial(
            fortnitepy.ClientPartyMember.set_battlepass_info,
            has_purchased=True,
            level=data['bp_tier']
        )
    )

    client.set_avatar(fortnitepy.Avatar(asset=data['icon'], background_colors=data['colors']))
    await discord_bot.start(discord_bot_token)

keep_alive.keep_alive()






      


@discord_bot.event
async def on_ready():
     
    print(Fore.LIGHTYELLOW_EX + f"Discord Client Ready As {discord_bot.user.name}#{discord_bot.user.discriminator}")
    activity = discord.Streaming(name=data['DiscordStatus'], url=data['TWITCH'])
    await discord_bot.change_presence(status=discord.Status.idle, activity=activity)
    print(Fore.LIGHTGREEN_EX + "All Clients Ready")
    print(Fore.LIGHTGREEN_EX + "Thx For Using GuffBot")

@client.event
async def event_party_invite(invite):
    if data['joinoninvite'].lower() == 'true':
        try:
            await invite.accept()
            print(Fore.LIGHTYELLOW_EX + '[GUFFBOT] ' + Fore.RESET + f'Accepted party invite from {invite.sender.display_name}')
        except Exception:
            pass
    elif data['joinoninvite'].lower() == 'false':
        if invite.sender.id in info['FullAccess']:
            await invite.accept()
            print(Fore.LIGHTYELLOW_EX + '[GUFFBOT] ' + Fore.RESET + 'Accepted party invite from ' + Fore.LIGHTGREEN_EX + f'{invite.sender.display_name}')
        else:
            print(Fore.LIGHTYELLOW_EX + ' [GUFFBOT] ' + Fore.RESET + f'Never accepted party invite from {invite.sender.display_name}')


@client.event
async def event_friend_request(request):
    if data['friendaccept'].lower() == 'true':
        try:
            await request.accept()
            print(f' [GUFFBOT] Accepted friend request from {request.display_name}' + Fore.LIGHTBLACK_EX + f' ({lenFriends()})')
        except Exception:
            pass
    elif data['friendaccept'].lower() == 'false':
        if request.id in info['FullAccess']:
            try:
                await request.accept()
                print(Fore.LIGHTYELLOW_EX + ' [GUFFBOT] ' + Fore.RESET + 'Accepted friend request from ' + Fore.LIGHTGREEN_EX + f'{request.display_name}' + Fore.LIGHTBLACK_EX + f' ({lenFriends()})')
            except Exception:
                pass
        else:
            print(f' [GUFFBOT] Never accepted friend request from {request.display_name}')


@client.event
async def event_party_member_join(member: fortnitepy.PartyMember) -> None:
    
    await client.party.send(
        data['joinmessage']
    )
    await client.party.me.set_emote(asset=data['eid'])
    


@client.event
async def event_party_member_leave(member):
    if client.user.display_name != member.display_name:
        try:
            if client.user.id in info['FullAccess']:
                print(Fore.LIGHTGREEN_EX + f' [GUFFBOT] {member.display_name}' + Fore.RESET + 'has left the lobby.')
            else:
                print(f' [GUFFBOT] {member.display_name} has left the lobby.' + Fore.LIGHTBLACK_EX + f' ({lenPartyMembers()})')
        except fortnitepy.HTTPException:
            pass


@client.event
async def event_party_message(message):
    if message.author.id in info['FullAccess']:
        name = Fore.LIGHTGREEN_EX + f'{message.author.display_name}'
    else:
        name = Fore.RESET + f'{message.author.display_name}'
    print(Fore.LIGHTGREEN_EX + ' [Party] ' + f'{name}' + Fore.RESET + f': {message.content}')


@client.event
async def event_friend_message(message):
    if message.author.id in info['FullAccess']:
        name = Fore.LIGHTMAGENTA_EX + f'{message.author.display_name}'
    else:
        name = Fore.RESET + f'{message.author.display_name}'
    print(Fore.LIGHTMAGENTA_EX + ' [Whisper] ' + f'{name}' + Fore.RESET + f': {message.content}')

    if message.content.upper().startswith('CID_'):
        await client.party.me.set_outfit(asset=message.content.upper())
        await message.reply(f'Skin set to: {message.content}')
    elif message.content.upper().startswith('BID_'):
        await client.party.me.set_backpack(asset=message.content.upper())
        await message.reply(f'Backpack set to: {message.content}')
    elif message.content.upper().startswith('EID_'):
        await client.party.me.set_emote(asset=message.content.upper())
        await message.reply(f'Emote set to: {message.content}')
    elif message.content.upper().startswith('PID_'):
        await client.party.me.set_pickaxe(asset=message.content.upper())
        await message.reply(f'Pickaxe set to: {message.content}')
    elif message.content.startswith('Playlist_'):
        try:
            await client.party.set_playlist(playlist=message.content)
            await message.reply(f'Playlist set to: {message.content}')
        except fortnitepy.Forbidden:
            await message.reply(f"I can not set gamemode because I am not party leader.")
    elif message.content.lower().startswith('prefix'):
        await message.reply(f'Current prefix: {prefix}')


@client.event
async def event_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f'That is not a command. Try {prefix}help')
    elif isinstance(error, IndexError):
        pass
    elif isinstance(error, fortnitepy.HTTPException):
        pass
    elif isinstance(error, commands.CheckFailure):
        await ctx.send("You don't have access to that command.")
    elif isinstance(error, TimeoutError):
        await ctx.send("You took too long to respond!")
    else:
        print(error)

# discord bot commands start here






@discord_bot.command('botinfo', help='staartbot')
async def botinfo(ctx):
  embed = discord.Embed(
    title = f'{client.user.display_name}',
    description = ' ',
  )


  embed.set_footer(text='GuffBot v2 • By NotEason ')
  embed.set_thumbnail(url='https://static.wikia.nocookie.net/fortnite/images/b/be/Unpeely_-_Outfit_-_Fortnite.png/revision/latest?cb=20200721085555')
  embed.add_field(name = "Help",value = ' [Discord Server](https://discord.gg/TvY7jbzWnt)')
  embed.add_field(name = "Fortnite Commands", value = "!skin outfit : changes the outfit bot is wearing \n !emote emote : changes the emote bot is doing \n !backbling backbling : changes backbling \n !pickaxe pickaxe : changes pickaxe bot has equiped \n !banner id color level : changes the banners icon color and level \n !sitout : sitout \n !sitin : sitin \n !ready : ready \n !unready : unready \n !invite : invite ppl \n !join : join you\n !add : add people ", inline=False)
  embed.add_field(name = "Other cosmetic commands", value = "!pinkghoul : sets outfit to pink ghoul trooper \n !purpleskull : sets outfit to purple skull trooper \n !check :  equips checkered renegade style on the bot\n !dababy : turns bot into dababy", inline=False)
  embed.add_field(name = "General commands", value = "!kick user : kicks user \n !block user : blocks user that was mentioned \n !promote : promotes user mentioned \n !leave : leaves party and crys on its own in a lobby \n !hide all : hides all users in the party \n !send message : sends message to party chat", inline=False)
  embed.add_field(name = "Discord Bot Commands", value = "!shop : shows current item shop \n !item : shows the cosmetic details for mentioned item \n !map : shows fortnite map \n !brnews : shows fortnite br news \n !stop : boots the discord and fortnite bot offline", inline=False)
  embed.add_field(name = " CID", value = data['cid'], inline=True)
  embed.add_field(name = " BID", value = data['bid'], inline=True)
  embed.add_field(name = " PID", value = data['pid'], inline=True)
  embed.add_field(name = " BANNER", value = data['banner'], inline=True)
  embed.add_field(name = " BANNER COLOR", value = data['banner_color'], inline=True)
  embed.add_field(name = " LEVEL", value = data['level'], inline=True)
  embed.add_field(name = " STATUS", value = data['status'], inline=True)
  embed.add_field(name = " PLATFORM", value = data['platform'], inline=True)


  await ctx.send(embed=embed)



@discord_bot.command(name='shop', help='Fortnite Item Shop')
async def shop(ctx):
  embed = discord.Embed(title="Fortnite Item Shop", color=0x2c2ff3)
  embed.set_image(url="https://fortool.fr/cm/assets/shop/en.png")
  embed.set_footer(text="use code noteason #ad")
  await ctx.send(embed=embed)

@discord_bot.command(pass_context=True)
async def brnews(ctx, l = None):
 
    response = requests.get(f'https://fortnite-api.com/v2/news/br?language=en')

    geted = response.json()
        
    if response.status_code == 200:

        image = geted['data']['image']

        embed = discord.Embed(title="USE CODE NOTEASON")
        embed.set_image(url=image)

        await ctx.send(embed=embed)

    elif response.status_code == 400:
 
        error = geted['error']

        embed = discord.Embed(title='Error', 
                description=f'`{error}`')

        await ctx.send(embed=embed)

    elif response.status_code == 404:

        error =geted['error']

        embed = discord.Embed(title='Error', 
        description=f'``{error}``')

        await ctx.send(embed=embed)

@discord_bot.command()
async def map(ctx):
    embed = discord.Embed(title="Fortnite Map", color=0x2c2ff3)
    embed.set_image(url="https://media.fortniteapi.io/images/map.png?showPOI=true")
    embed.set_footer(text="use code noteason #ad")
    await ctx.send(embed=embed)




@discord_bot.command()
async def jaybatskin(ctx, *, content = None):
    if content is None:
        response = requests.get(f'https://fortnite-api.com/v2/cosmetics/br/search?name={content}')

        embed=discord.Embed(title=f"No skin was given, try: {prefix}skin (skin name)")
        embed.set_footer(text=f"use code noteason #ad •  made with ❤ ")
        await ctx.send(embed=embed)
    elif content.upper().startswith('CID_'):
        await client.party.me.set_outfit(asset=content.upper())
        embed.set_footer(text=f"use code noteason #ad •  made with ❤ ")
        embed=discord.Embed(title=f"Set Outfit To {content}")
        await ctx.send(embed=embed)
    else:
        try:
            cosmetic = await BenBotAsync.get_cosmetic(
                lang="en",
                searchLang="en",
                name=content,
                backendType="AthenaCharacter"
            )
            await client.party.me.set_outfit(asset=cosmetic.id)
            content = content.replace(" ", "+")
            embed=discord.Embed(title=f"Set Outfit To {cosmetic.name}")
            embed.set_thumbnail(url=response['data']['images']['icon'])
            embed.set_footer(text=f"use code noteason #ad •  made with ❤ ")
            await ctx.send(embed=embed)
        except BenBotAsync.exceptions.NotFound:
            embed=discord.Embed(title=f"could not find a skin named : {content}")
            embed.set_footer(text=f"use code noteason #ad •  made with ❤ ")
            await ctx.send(embed=embed)

@discord_bot.command()
async def skin(ctx, *, content = None):
    if content is None:
        embed=discord.Embed(title=f"No skin was given, try: {prefix}skin (skin name)")
        embed.set_footer(text=f"use code noteason #ad •  made with ❤ ")
        await ctx.send(embed=embed)
    elif content.upper().startswith('CID_'):
        await client.party.me.set_outfit(asset=content.upper())
        embed.set_footer(text=f"use code noteason #ad •  made with ❤ ")
        embed=discord.Embed(title=f"Set Outfit To {content}")
        await ctx.send(embed=embed)
    else:
        try:
            cosmetic = await BenBotAsync.get_cosmetic(
                lang="en",
                searchLang="en",
                name=content,
                backendType="AthenaCharacter"
            )
            await client.party.me.set_outfit(asset=cosmetic.id)
            embed=discord.Embed(title=f"Set Outfit To {cosmetic.name}")
            embed.set_footer(text=f"use code noteason #ad •  made with ❤ ")
            await ctx.send(embed=embed)
        except BenBotAsync.exceptions.NotFound:
            embed=discord.Embed(title=f"could not find a skin named : {content}")
            embed.set_footer(text=f"use code noteason #ad •  made with ❤ ")
            await ctx.send(embed=embed)


@discord_bot.command()
async def emote(ctx, *, content = None):
    if content is None:
        embed=discord.Embed(title=f"No emote was given, try: {prefix}emote (emote name)")
        embed.set_footer(text=f"use code noteason #ad •  made with ❤ ")
        await ctx.send(embed=embed)
    elif content.lower() == 'floss':
        await client.party.me.clear_emote()
        await client.party.me.set_emote(asset='EID_Floss')
        embed=discord.Embed(title="Emote set to: Floss")
        await ctx.send(embed=embed)
    elif content.lower() == 'none':
        await client.party.me.clear_emote()
        embed=discord.Embed(title="Emote set to: None")
        embed.set_footer(text=f"use code noteason #ad •  made with ❤ ")
        await ctx.send(embed=embed)
    elif content.upper().startswith('EID_'):
        await client.party.me.clear_emote()
        await client.party.me.set_emote(asset=content.upper())
        embed=discord.Embed(title=f"Emote set to: {content}")
        embed.set_footer(text=f"use code noteason #ad •  made with ❤ ")
        await ctx.send(embed=embed)
    else:
        try:
            cosmetic = await BenBotAsync.get_cosmetic(
                lang="en",
                searchLang="en",
                matchMethod="contains",
                name=content,
                backendType="AthenaDance"
            )
            await client.party.me.clear_emote()
            await client.party.me.set_emote(asset=cosmetic.id)
            embed=discord.Embed(title=f"Emote set to: {cosmetic.name}")
            embed.set_footer(text=f"use code noteason #ad •  made with ❤ ")
            await ctx.send(embed=embed)
        except BenBotAsync.exceptions.NotFound:
            embed=discord.Embed(title=f"Could not find an emote named: {content}")
            embed.set_footer(text=f"use code noteason #ad •  made with ❤ ")
            await ctx.send(embed=embed)

@discord_bot.command()
async def backbling(ctx, *, content = None):
    if content is None:
        embed=discord.Embed(title=f"No backbling was given, try: {prefix}backbling (backpack name)")
        embed.set_footer(text=f"use code noteason #ad •  made with ❤ ")
        await ctx.send(embed=embed)
    elif content.lower() == 'none':
        await client.party.me.clear_backpack()
        embed=discord.Embed(title="Backbling set to None")
        embed.set_footer(text=f"use code noteason #ad •  made with ❤ ")
        await ctx.send(embed=embed)
    elif content.upper().startswith('BID_'):
        await client.party.me.set_backpack(asset=content.upper())
        embed=discord.Embed(title=f"Backbling set to: {content}")
        embed.set_footer(text=f"use code noteason #ad •  made with ❤ ")
        await ctx.send(embed=embed)
    else:
        try:
            cosmetic = await BenBotAsync.get_cosmetic(
                lang="en",
                searchLang="en",
                matchMethod="contains",
                name=content,
                backendType="AthenaBackpack"
            )
            await client.party.me.set_backpack(asset=cosmetic.id)
            embed=discord.Embed(title=f"Backbling set to: {cosmetic.name}")
            embed.set_footer(text=f"use code noteason #ad •  made with ❤ ")
            await ctx.send(embed=embed)
        except BenBotAsync.exceptions.NotFound:
            embed=discord.Embed(title=f"Could not find a backpack named: {content}")
            embed.set_footer(text=f"use code noteason #ad •  made with ❤ ")
            await ctx.send(embed=embed)

@discord_bot.command()
async def pickaxe(ctx, *, content = None):
    if content is None:
        embed=discord.Embed(title=f"No pickaxe was given, try: {prefix}pickaxe (pickaxe name)")
        embed.set_footer(text=f"use code noteason #ad •  made with ❤ ")
        await ctx.send(embed=embed)
    elif content.upper().startswith('Pickaxe_'):
        await client.party.me.set_pickaxe(asset=content.upper())
        embed=discord.Embed(title=f"Pickaxe set to: {content}")
        embed.set_footer(text=f"use code noteason #ad •  made with ❤ ")
        await ctx.send(embed=embed)
    else:
        try:
            cosmetic = await BenBotAsync.get_cosmetic(
                lang="en",
                searchLang="en",
                matchMethod="contains",
                name=content,
                backendType="AthenaPickaxe"
            )
            await client.party.me.set_pickaxe(asset=cosmetic.id)
            embed=discord.Embed(title=f"Pickaxe set to: {cosmetic.name}")
            embed.set_footer(text=f"use code noteason #ad •  made with ❤ ")
            await ctx.send(embed=embed)
        except BenBotAsync.exceptions.NotFound:
            embed=discord.Embed(title=f"Could not find a pickaxe named: {content}")
            embed.set_footer(text=f"use code noteason #ad •  made with ❤ ")
            await ctx.send(embed=embed)

@discord_bot.command()
async def banner(ctx, args1 = None, args2 = None):
    if (args1 is not None) and (args2 is None):
        if args1.startswith('defaultcolor'):
            await client.party.me.set_banner(
                color = args1
            )
            embed=discord.Embed(title=f"Banner color set to: {args1}")
            embed.set_footer(text=f"use code noteason #ad •  made with ❤ ")
            await ctx.send(embed=embed)

        elif args1.isnumeric() == True:
            await client.party.me.set_banner(
                color = 'defaultcolor' + args1
            )
            embed=discord.Embed(title=f"Banner color set to: defaultcolor{args1}")
            embed.set_footer(text=f"use code noteason #ad •  made with ❤ ")
            await ctx.send(embed=embed)

        else:
            await client.party.me.set_banner(
                icon = args1
            )
            embed=discord.Embed(title=f"Banner Icon set to: {args1}")
            embed.set_footer(text=f"use code noteason #ad •  made with ❤ ")
            await ctx.send(embed=embed)

    elif (args1 is not None) and (args2 is not None):
        if args2.startswith('defaultcolor'):
            await client.party.me.set_banner(
                icon = args1,
                color = args2
            )
            embed=discord.Embed(title=f"Banner icon set to: {args1} -- Banner color set to: {args2}")
            embed.set_footer(text=f"use code noteason #ad •  made with ❤ ")
            await ctx.send(embed=embed)
        
        elif args2.isnumeric() == True:
            await client.party.me.set_banner(
                icon = args1,
                color = 'defaultcolor' + args2
            )
            embed=discord.Embed(title=f"Banner icon set to: {args1} -- Banner color set to: defaultcolor{args2}")
            embed.set_footer(text=f"use code noteason #ad •  made with ❤ ")
            await ctx.send(embed=embed)

        else:
            embed=discord.Embed(title=f"Not proper format. Try: {prefix}banner (Banner ID) (Banner Color ID)")
            embed.set_footer(text=f"use code noteason #ad •  made with ❤ ")
            await ctx.send(embed=embed)


copied_player = ""


@discord_bot.command()
async def send(ctx, *, message = None):
    if message is not None:
        await client.party.send(message)
        embed=discord.Embed(title=f"Sent 『{message}』  to party chat")
        embed.set_footer(text=f"use code noteason #ad •  made with ❤ ")
        await ctx.send(embed=embed)
    else:
        embed=discord.Embed(title=f"No message was given. Try: {prefix}send (message)")
        embed.set_footer(text=f"use code noteason #ad •  made with ❤ ")
        await ctx.send(embed=embed)

@discord_bot.command()
async def level(ctx, level = None):
    if level is None:
        embed=discord.Embed(title=f"No level was given. Try: {prefix}level (number)")
        embed.set_footer(text=f"use code noteason #ad •  made with ❤ ")
        await ctx.send(embed=embed)
    else:
        await client.party.me.set_banner(season_level=level)
        embed=discord.Embed(title=f"Level set to: {level}")
        embed.set_footer(text=f"use code noteason #ad •  made with ❤ ")
        await ctx.send(embed=embed)

@discord_bot.command()
async def pinkghoul(ctx):
    variants = client.party.me.create_variants(material=3)

    await client.party.me.set_outfit(
        asset='CID_029_Athena_Commando_F_Halloween',
        variants=variants
    )
    
    embed=discord.Embed(title="Skin set to: Pink Ghoul Trooper")
    embed.set_footer(text=f"use code noteason #ad •  made with ❤ ")
    await ctx.send(embed=embed)

@discord_bot.command()
async def purpleskull(ctx):
    variants = client.party.me.create_variants(clothing_color=1)

    await client.party.me.set_outfit(
        asset='CID_030_Athena_Commando_M_Halloween',
        variants = variants
    )
    
    embed=discord.Embed(title="Skin set to: Purple Skull Trooper")
    embed.set_footer(text=f"use code noteason #ad •  made with ❤ ")
    await ctx.send(embed=embed)

@discord_bot.command()
async def check(ctx):
    variants = client.party.me.create_variants(material=2)

    await client.party.me.set_outfit(
        asset='CID_028_Athena_Commando_F',
        variants=variants
    )

    embed=discord.Embed(title="Skin set to: Checkered Renegade")
    embed.set_footer(text=f"use code noteason #ad •  made with ❤ ")
    await ctx.send(embed=embed)

@discord_bot.command()
async def leave(ctx):
    await client.party.me.leave()
    embed=discord.Embed(title="Left party.")
    embed.set_footer(text=f"use code noteason #ad •  made with ❤ ")
    await ctx.send(embed=embed)



@discord_bot.command()
async def kick(ctx, *, member = None):
    if member is not None:
        if member.lower() == 'all':
            members = client.party.members

            for m in members:
                try:
                    member = await client.get_user(m)
                    await member.kick()
                except fortnitepy.Forbidden:
                    embed=discord.Embed(title="I am not party leader.")
                    embed.set_footer(text=f"use code noteason #ad •  made with ❤ ")
                    await ctx.send(embed=embed)

            embed=discord.Embed(title="Kicked everyone in the party")
            embed.set_footer(text=f"use code noteason #ad •  made with ❤ ")
            await ctx.send(embed=embed)

        else:
            try:
                user = await client.fetch_profile(member)
                member = client.party.members.get(user.id)
                if member is None:
                    embed=discord.Embed(title="Couldn't find that user. Are you sure they're in the party?")
                    embed.set_footer(text=f"use code noteason #ad •  made with ❤ ")
                    await ctx.send(embed=embed)

                await member.kick()
                embed=discord.Embed(title=f"Kicked: {member.display_name}")
                await ctx.send(embed=embed)
            except fortnitepy.Forbidden:
                embed=discord.Embed(title="I can't kick that user because I am not party leader")
                embed.set_footer(text=f"use code noteason #ad •  made with ❤ ")
                await ctx.send(embed=embed)
            except AttributeError:
                embed=discord.Embed(title="Couldn't find that user.")
                embed.set_footer(text=f"use code noteason #ad •  made with ❤ ")
                await ctx.send(embed=embed)
    else:
        embed=discord.Embed(title=f"No member was given. Try: {prefix}kick (user)")
        embed.set_footer(text=f"use code noteason #ad •  made with ❤ ")
        await ctx.send(embed=embed)

@discord_bot.command()
async def block(ctx, *, user = None):
    if user is not None:
        try:
            user = await client.fetch_profile(user)
            friends = client.friends

            if user.id in friends:
                try:
                    await user.block()
                    embed=discord.Embed(title=f"Blocked {user.display_name}")
                    embed.set_footer(text=f"use code noteason #ad •  made with ❤ ")
                    await ctx.send(embed=embed)
                except fortnitepy.HTTPException:
                    embed=discord.Embed(title="Something went wrong trying to block that user.")
                    embed.set_footer(text=f"use code noteason #ad •  made with ❤ ")
                    await ctx.send(embed=embed)

            elif user.id in client.blocked_users:
                embed=discord.Embed(title=f"I already have {user.display_name} blocked.")
                embed.set_footer(text=f"use code noteason #ad •  made with ❤ ")
                await ctx.send(embed=embed)
        except AttributeError:
            embed=discord.Embed(title=f"I can't find a player with that name.")
            embed.set_footer(text=f"use code noteason #ad •  made with ❤ ")
            await ctx.send(embed=embed)
    else:
        embed=discord.Embed(title=f"No user was given. Try: {prefix}block (friend)")
        embed.set_footer(text=f"use code noteason #ad •  made with ❤ ")
        await ctx.send(embed=embed)

@discord_bot.command()
async def promote(ctx, *, member = None):
    if member is None:
        user = await client.fetch_profile(ctx.message.author.id)
        member = client.party.members.get(user.id)
    if member is not None:
        user = await client.fetch_profile(member.display_name)
        member = client.party.members.get(user.id)
    try:
        await member.promote()
        embed=discord.Embed(title=f"Promoted: {member.display_name}")
        embed.set_footer(text=f"use code noteason #ad •  made with ❤ ")
        await ctx.send(embed=embed)
    except fortnitepy.Forbidden:
        embed=discord.Embed(title="Client is not party leader")
        embed.set_footer(text=f"use code noteason #ad •  made with ❤ ")
        await ctx.send(embed=embed)
    except fortnitepy.PartyError:
        embed=discord.Embed(title="That person is already party leader")
        embed.set_footer(text=f"use code noteason #ad •  made with ❤ ")
        await ctx.send(embed=embed)
    except fortnitepy.HTTPException:
        embed=discord.Embed(title="Something went wrong trying to promote that member")
        embed.set_footer(text=f"use code noteason #ad •  made with ❤ ")
        await ctx.send(embed=embed)
    except AttributeError:
        embed=discord.Embed(title=f"I could not find that user")
        embed.set_footer(text=f"use code noteason #ad •  made with ❤ ")
        await ctx.send(embed=embed)

@discord_bot.command()
async def hide(ctx, *, user = None):
    if client.party.me.leader:
        if user != "all":
            try:
                if user is None:
                    user = await client.fetch_profile(ctx.message.author.id)
                    member = client.party.members.get(user.id)
                else:
                    user = await client.fetch_profile(user)
                    member = client.party.members.get(user.id)

                raw_squad_assignments = client.party.meta.get_prop('Default:RawSquadAssignments_j')["RawSquadAssignments"]

                for m in raw_squad_assignments:
                    if m['memberId'] == member.id:
                        raw_squad_assignments.remove(m)

                await set_and_update_party_prop(
                    'Default:RawSquadAssignments_j',
                    {
                        'RawSquadAssignments': raw_squad_assignments
                    }
                )

                embed=discord.Embed(title=f"Hid {member.display_name}")
                embed.set_footer(text=f"use code noteason #ad •  made with ❤ ")
                await ctx.send(embed=embed)
            except AttributeError:
                embed=discord.Embed(title=f"I could not find that user.")
                embed.set_footer(text=f"use code noteason #ad •  made with ❤ ")
                await ctx.send(embed=embed)
            except fortnitepy.HTTPException:
                embed=discord.Embed(title=f"I am not party leader.")
                embed.set_footer(text=f"use code noteason #ad •  made with ❤ ")
                await ctx.send(embed=embed)
        else:
            try:
                await set_and_update_party_prop(
                    'Default:RawSquadAssignments_j',
                    {
                        'RawSquadAssignments': [
                            {
                                'memberId': client.user.id,
                                'absoluteMemberIdx': 1
                            }
                        ]
                    }
                )

                embed=discord.Embed(title=f"Hid everyone in the party.")
                embed.set_footer(text=f"use code noteason #ad •  made with ❤ ")
                await ctx.send(embed=embed)
            except fortnitepy.HTTPException:
                embed=discord.Embed(title=f"I am not party leader.")
                embed.set_footer(text=f"use code noteason #ad •  made with ❤ ")
                await ctx.send(embed=embed)
    else:
        embed=discord.Embed(title=f"I need party leader to do this!")
        embed.set_footer(text=f"use code noteason #ad •  made with ❤ ")
        await ctx.send(embed=embed)


@discord_bot.command()
async def ready(ctx):
    await client.party.me.set_ready(fortnitepy.ReadyState.READY)
    embed=discord.Embed(title=f"Ready!")
    embed.set_footer(text=f"use code noteason #ad •  made with ❤ ")
    await ctx.send(embed=embed)



@discord_bot.command()
async def unready(ctx):
    await client.party.me.set_ready(fortnitepy.ReadyState.NOT_READY)
    embed=discord.Embed(title=f"UnReady!")
    embed.set_footer(text=f"use code noteason #ad •  made with ❤ ")
    await ctx.send(embed=embed)


@discord_bot.command()
async def sitin(ctx):
    await client.party.me.set_ready(fortnitepy.ReadyState.NOT_READY)
    embed=discord.Embed(title=f"Sitting in!")
    embed.set_footer(text=f"use code noteason #ad •  made with ❤ ")
    await ctx.send(embed=embed)


@discord_bot.command()
async def sitout(ctx):
    await client.party.me.set_ready(fortnitepy.ReadyState.SITTING_OUT)
    embed=discord.Embed(title=f"Sitting out!")
    embed.set_footer(text=f"use code noteason #ad •  made with ❤ ")
    await ctx.send(embed=embed)

@discord_bot.command()
async def dababy(ctx: fortnitepy.ext.commands.Context):
    await client.party.me.set_outfit("CID_887_Athena_Commando_M_ChOneSpitfire")
    await asyncio.sleep(0.10)
    await client.party.me.set_emote(asset="EID_JanuaryBop")
    embed=discord.Embed(title=f"LETS GO!")
    embed.set_footer(text=f"use code noteason #ad •  made with ❤ ")
    await ctx.send(embed=embed)  

@discord_bot.command()
async def join(ctx, *, member = None):
    try:
        if member is None:
            user = await client.fetch_profile(ctx.message.author.id)
            friend = client.get_friend(user.id)
        elif member is not None:
            user = await client.fetch_profile(member)
            friend = client.get_friend(user.id)

        await friend.join_party()
        embed=discord.Embed(title=f"Joined {friend.display_name}'s party.")
        embed.set_footer(text=f"use code noteason #ad •  made with ❤ ")
        await ctx.send(embed=embed)
    except fortnitepy.Forbidden:
        embed=discord.Embed(title=f"I can not join that party because it is private.")
        embed.set_footer(text=f"use code noteason #ad •  made with ❤ ")
        await ctx.send(embed=embed)
    except fortnitepy.PartyError:
        embed=discord.Embed(title=f"That user is already in the party.")
        embed.set_footer(text=f"use code noteason #ad •  made with ❤ ")
        await ctx.send(embed=embed)
    except fortnitepy.HTTPException:
        embed=discord.Embed(title=f"Something went wrong joining the party")
        embed.set_footer(text=f"use code noteason #ad •  made with ❤ ")
        await ctx.send(embed=embed)
    except AttributeError:
        embed=discord.Embed(title=f"I can not join that party. Are you sure I have them friended?")
        embed.set_footer(text=f"use code noteason #ad •  made with ❤ ")
        await ctx.send(embed=embed)

@discord_bot.command()
async def invite(ctx, *, member = None):
    if member == 'all':
        friends = client.friends
        invited = []

        try:
            for f in friends:
                friend = client.get_friend(f)

                if friend.is_online():
                    invited.append(friend.display_name)
                    await friend.invite()
            
            embed=discord.Embed(title=f"Invited {len(invited)} friends to the party.")
            embed.set_footer(text=f"use code noteason #ad •  made with ❤ ")
            await ctx.send(embed=embed)

        except Exception:
            pass

    else:
        try:
            if member is None:
                user = await client.fetch_profile(ctx.message.author.id)
                friend = client.get_friend(user.id)
            if member is not None:
                user = await client.fetch_profile(member)
                friend = client.get_friend(user.id)

            await friend.invite()
            embed=discord.Embed(title=f"Invited {friend.display_name} to the party.")
            embed.set_footer(text=f"use code noteason #ad •  made with ❤ ")
            await ctx.send(embed=embed)
        except fortnitepy.PartyError:
            embed=discord.Embed(title=f"That user is already in the party.")
            embed.set_footer(text=f"use code noteason #ad •  made with ❤ ")
            await ctx.send(embed=embed)
        except fortnitepy.HTTPException:
            embed=discord.Embed(title=f"Something went wrong inviting that user.")
            embed.set_footer(text=f"use code noteason #ad •  made with ❤ ")
            await ctx.send(embed=embed)
        except AttributeError:
            embed=discord.Embed(title=f"I can not invite that user. Are you sure I have them friended?")
            embed.set_footer(text=f"use code noteason #ad •  made with ❤ ")
            await ctx.send(embed=embed)
        except Exception:
            pass

@discord_bot.command()
async def add(ctx, *, member = None):
    if member is not None:
        try:
            user = await client.fetch_profile(member)
            friends = client.friends

            if user.id in friends:
                embed=discord.Embed(title=f"I already have {user.display_name} as a friend")
                embed.set_footer(text=f"use code noteason #ad •  made with ❤ ")
                await ctx.send(embed=embed)
            else:
                await client.add_friend(user.id)
                embed=discord.Embed(title=f"Sent a friend request to {user.display_name}")
                embed.set_footer(text=f"use code noteason #ad •  made with ❤ ")
                await ctx.send(embed=embed)
                print(Fore.GREEN + ' [GUFFBOT] ' + Fore.RESET + 'Sent a friend request to: ' + Fore.LIGHTBLACK_EX + f'{user.display_name}')

        except fortnitepy.HTTPException:
            await ctx.send("There was a problem trying to add this friend.")
        except AttributeError:
            embed=discord.Embed(title="I can't find a player with that name.")
            embed.set_footer(text=f"use code noteason #ad •  made with ❤ ")
            await ctx.send(embed=embed)
    else:
        
        embed=discord.Embed(title=f"No user was given. Try: {prefix}add (user)")
        embed.set_footer(text=f"use code noteason #ad •  made with ❤ ")
        await ctx.send(embed=embed)



@discord_bot.command()
async def admin(ctx, setting = None, *, user = None):
    if (setting is None) and (user is None):
        await ctx.send(f"Missing one or more arguments. Try: {prefix}admin (add, remove, list) (user)")
    elif (setting is not None) and (user is None):

        user = await client.fetch_profile(ctx.message.author.id)

        if setting.lower() == 'add':
            if user.id in info['FullAccess']:
                await ctx.send("You are already an admin")

            else:
                await ctx.send("Password?")
                response = await client.wait_for('friend_message', timeout=20)
                content = response.content.lower()
                if content == data['AdminPassword']:
                    info['FullAccess'].append(user.id)
                    with open('info.json', 'w') as f:
                        json.dump(info, f, indent=4)
                        await ctx.send(f"Correct. Added {user.display_name} as an admin.")
                        print(Fore.GREEN + " [GUFFBOT] " + Fore.LIGHTGREEN_EX + user.display_name + Fore.RESET + " was added as an admin.")
                else:
                    await ctx.send("Incorrect Password.")

        elif setting.lower() == 'remove':
            if user.id not in info['FullAccess']:
                await ctx.send("You are not an admin.")
            else:
                await ctx.send("Are you sure you want to remove yourself as an admin?")
                response = await client.wait_for('friend_message', timeout=20)
                content = response.content.lower()
                if (content.lower() == 'yes') or (content.lower() == 'y'):
                    info['FullAccess'].remove(user.id)
                    with open('info.json', 'w') as f:
                        json.dump(info, f, indent=4)
                        await ctx.send("You were removed as an admin.")
                        (Fore.BLUE + " [GUFFBOT] " + Fore.LIGHTBLUEprint_EX + user.display_name + Fore.RESET + " was removed as an admin.")
                elif (content.lower() == 'no') or (content.lower() == 'n'):
                    await ctx.send("You were kept as admin.")
                else:
                    await ctx.send("Not a correct reponse. Cancelling command.")
                
        elif setting == 'list':
            if user.id in info['FullAccess']:
                admins = []

                for admin in info['FullAccess']:
                    user = await client.fetch_profile(admin)
                    admins.append(user.display_name)

                await ctx.send(f"The bot has {len(admins)} admins:")

                for admin in admins:
                    await ctx.send(admin)

            else:
                await ctx.send("You don't have permission to this command.")

        else:
            await ctx.send(f"That is not a valid setting. Try: {prefix}admin (add, remove, list) (user)")
            
    elif (setting is not None) and (user is not None):
        user = await client.fetch_profile(user)

        if setting.lower() == 'add':
            if ctx.message.author.id in info['FullAccess']:
                if user.id not in info['FullAccess']:
                    info['FullAccess'].append(user.id)
                    with open('info.json', 'w') as f:
                        json.dump(info, f, indent=4)
                        await ctx.send(f"Correct. Added {user.display_name} as an admin.")
                        print(Fore.GREEN + " [GUFFBOT] " + Fore.LIGHTGREEN_EX + user.display_name + Fore.RESET + " was added as an admin.")
                else:
                    await ctx.send("That user is already an admin.")
            else:
                await ctx.send("You don't have access to add other people as admins. Try just: !admin add")
        elif setting.lower() == 'remove':
            if ctx.message.author.id in info['FullAccess']:
                if user.id in info['FullAccess']:
                    await ctx.send("Password?")
                    response = await client.wait_for('friend_message', timeout=20)
                    content = response.content.lower()
                    if content == data['AdminPassword']:
                        info['FullAccess'].remove(user.id)
                        with open('info.json', 'w') as f:
                            json.dump(info, f, indent=4)
                            await ctx.send(f"{user.display_name} was removed as an admin.")
                            print(Fore.BLUE + " [GUFFBOT] " + Fore.LIGHTBLUE_EX + user.display_name + Fore.RESET + " was removed as an admin.")
                    else:
                        await ctx.send("Incorrect Password.")
                else:
                    await ctx.send("That person is not an admin.")
            else:
                await ctx.send("You don't have permission to remove players as an admin.")
        else:
            await ctx.send(f"Not a valid setting. Try: {prefix}admin (add, remove) (user)")







@discord_bot.command()
async def item(ctx, cosnamee):
  r = requests.get(f'https://fortnite-api.com/v2/cosmetics/br/search/all?name={cosnamee}')
  rr = r.json()
  if rr['status'] == 200:
    for sub_dict in rr['data']:
      embed = discord.Embed(color=0x2c2ff3)
      embed.add_field(name='Name', value=f"``{sub_dict['name']}``", inline=False)
      embed.add_field(name='ID', value=f"``{sub_dict['id']}``", inline=False)
      embed.add_field(name='Rarity', value=f"``{sub_dict['description']}``", inline=False)
      embed.add_field(name='Type', value=f"``{sub_dict['type']['value']}``", inline=False)
      embed.add_field(name='Display Type', value=f"``{sub_dict['type']['displayValue']}``", inline=False)
      embed.add_field(name='Backend Value', value=f"``{sub_dict['type']['backendValue']}``", inline=False)
      embed.add_field(name='Rarity', value=f"``{sub_dict['rarity']['value']}``", inline=False)
      embed.add_field(name='Backend Rarity', value=f"``{sub_dict['rarity']['backendValue']}``", inline=False)
      embed.add_field(name='Series', value=f"``{sub_dict['series']}``", inline=False)
      if sub_dict['introduction'] == None:
        pass
      else:
        embed.add_field(name='Introduction', value=f"``{sub_dict['introduction']['text']}``", inline=False)
        embed.add_field(name='Display Asset Path', value=f"``{sub_dict['displayAssetPath']}``", inline=False)
        embed.add_field(name='Definition Path', value=f"``{sub_dict['definitionPath']}``", inline=False)
        embed.set_thumbnail(url=f"https://fortnite-api.com/images/cosmetics/br/{sub_dict['id'].lower()}/icon.png")
        embed.set_footer(text=f"use code noteason #ad")
        message = await ctx.send(embed=embed)
  else:
    embed = discord.Embed(color=0xff0f0f)
    embed.add_field(name='Error', value=f"``{rr['error']}``", inline=False)
    embed.set_footer(text=f"use code noteason #ad")
    message = await ctx.send(embed=embed)
    await asyncio.sleep(60)
    await message.delete()

@discord_bot.command('stop', help='kill bot')
async def stop(ctx):
  embed = discord.Embed(
    description = ("You Requested The Bot To Shut Down | Shutting Down"),
    colour = discord.Colour.green()
  )

  await ctx.send(embed=embed)
  sys.exit(1)






@discord_bot.event
async def on_message(message):
    if message.author.bot:
        return

    print(Fore.LIGHTBLUE_EX + '{0.author.display_name} | {0.content}'.format(message))
    await discord_bot.process_commands(message)

@client.event
async def event_friend_message(message, ctx):
        await ctx.send('Received fortnite message from {0.author.display_name} | Content "{0.content}"'.format(message))



















# discord bot commands end





@client.command()
async def skin(ctx, *, content = None):
    if content is None:
        await ctx.send(f'No skin was given, try: {prefix}skin (skin name)')
    elif content.upper().startswith('CID_'):
        await client.party.me.set_outfit(asset=content.upper())
        await ctx.send(f'Skin set to: {content}')
    else:
        try:
            cosmetic = await BenBotAsync.get_cosmetic(
                lang="en",
                searchLang="en",
                name=content,
                backendType="AthenaCharacter"
            )
            await client.party.me.set_outfit(asset=cosmetic.id)
            await ctx.send(f'Skin set to: {cosmetic.name}')
        except BenBotAsync.exceptions.NotFound:
            await ctx.send(f'Could not find a skin named: {content}')


@client.command()
async def backbling(ctx, *, content = None):
    if content is None:
        await ctx.send(f'No backpack was given, try: {prefix}backpack (backpack name)')
    elif content.lower() == 'none':
        await client.party.me.clear_backpack()
        await ctx.send('Backpack set to: None')
    elif content.upper().startswith('BID_'):
        await client.party.me.set_backpack(asset=content.upper())
        await ctx.send(f'Backpack set to: {content}')
    else:
        try:
            cosmetic = await BenBotAsync.get_cosmetic(
                lang="en",
                searchLang="en",
                matchMethod="contains",
                name=content,
                backendType="AthenaBackpack"
            )
            await client.party.me.set_backpack(asset=cosmetic.id)
            await ctx.send(f'Backpack set to: {cosmetic.name}')
        except BenBotAsync.exceptions.NotFound:
            await ctx.send(f'Could not find a backpack named: {content}')


@client.command()
async def emote(ctx, *, content = None):
    if content is None:
        await ctx.send(f'No emote was given, try: {prefix}emote (emote name)')
    elif content.lower() == 'floss':
        await client.party.me.clear_emote()
        await client.party.me.set_emote(asset='EID_Floss')
        await ctx.send(f'Emote set to: Floss')
    elif content.lower() == 'none':
        await client.party.me.clear_emote()
        await ctx.send(f'Emote set to: None')
    elif content.upper().startswith('EID_'):
        await client.party.me.clear_emote()
        await client.party.me.set_emote(asset=content.upper())
        await ctx.send(f'Emote set to: {content}')
    else:
        try:
            cosmetic = await BenBotAsync.get_cosmetic(
                lang="en",
                searchLang="en",
                matchMethod="contains",
                name=content,
                backendType="AthenaDance"
            )
            await client.party.me.clear_emote()
            await client.party.me.set_emote(asset=cosmetic.id)
            await ctx.send(f'Emote set to: {cosmetic.name}')
        except BenBotAsync.exceptions.NotFound:
            await ctx.send(f'Could not find an emote named: {content}')


@client.command()
async def pickaxe(ctx, *, content = None):
    if content is None:
        await ctx.send(f'No pickaxe was given, try: {prefix}pickaxe (pickaxe name)')
    elif content.upper().startswith('Pickaxe_'):
        await client.party.me.set_pickaxe(asset=content.upper())
        await ctx.send(f'Pickaxe set to: {content}')
    else:
        try:
            cosmetic = await BenBotAsync.get_cosmetic(
                lang="en",
                searchLang="en",
                matchMethod="contains",
                name=content,
                backendType="AthenaPickaxe"
            )
            await client.party.me.set_pickaxe(asset=cosmetic.id)
            await ctx.send(f'Pickaxe set to: {cosmetic.name}')
        except BenBotAsync.exceptions.NotFound:
            await ctx.send(f'Could not find a pickaxe named: {content}')


@client.command()
async def pet(ctx, *, content = None):
    if content is None:
        await ctx.send(f'No pet was given, try: {prefix}pet (pet name)')
    elif content.lower() == 'none':
        await client.party.me.clear_pet()
        await ctx.send('Pet set to: None')
    else:
        try:
            cosmetic = await BenBotAsync.get_cosmetic(
                lang="en",
                searchLang="en",
                matchMethod="contains",
                name=content,
                backendType="AthenaPet"
            )
            await client.party.me.set_pet(asset=cosmetic.id)
            await ctx.send(f'Pet set to: {cosmetic.name}')
        except BenBotAsync.exceptions.NotFound:
            await ctx.send(f'Could not find a pet named: {content}')


@client.command()
async def emoji(ctx, *, content = None):
    if content is None:
        await ctx.send(f'No emoji was given, try: {prefix}emoji (emoji name)')
    try:
        cosmetic = await BenBotAsync.get_cosmetic(
            lang="en",
            searchLang="en",
            matchMethod="contains",
            name=content,
            backendType="AthenaEmoji"
        )
        await client.party.me.clear_emoji()
        await client.party.me.set_emoji(asset=cosmetic.id)
        await ctx.send(f'Emoji set to: {cosmetic.name}')
    except BenBotAsync.exceptions.NotFound:
        await ctx.send(f'Could not find an emoji named: {content}')

    

@client.command()
async def current(ctx, setting = None):
    if setting is None:
        await ctx.send(f"Missing argument. Try: {prefix}current (skin, backpack, emote, pickaxe, banner)")
    elif setting.lower() == 'banner':
        await ctx.send(f'Banner ID: {client.party.me.banner[0]}  -  Banner Color ID: {client.party.me.banner[1]}')
    else:
        try:
            if setting.lower() == 'skin':
                    cosmetic = await BenBotAsync.get_cosmetic_from_id(
                        cosmetic_id=client.party.me.outfit
                    )

            elif setting.lower() == 'backpack':
                    cosmetic = await BenBotAsync.get_cosmetic_from_id(
                        cosmetic_id=client.party.me.backpack
                    )

            elif setting.lower() == 'emote':
                    cosmetic = await BenBotAsync.get_cosmetic_from_id(
                        cosmetic_id=client.party.me.emote
                    )

            elif setting.lower() == 'pickaxe':
                    cosmetic = await BenBotAsync.get_cosmetic_from_id(
                        cosmetic_id=client.party.me.pickaxe
                    )

            await ctx.send(f"My current {setting} is: {cosmetic.name}")
        except BenBotAsync.exceptions.NotFound:
            await ctx.send(f"I couldn't find a {setting} name for that.")



@client.command()
async def name(ctx, *, content=None):
    if content is None:
        await ctx.send(f'No ID was given, try: {prefix}name (cosmetic ID)')
    else:
        try:
            cosmetic = await BenBotAsync.get_cosmetic_from_id(
                cosmetic_id=content
            )
            await ctx.send(f'The name for that ID is: {cosmetic.name}')
            print(f' [GUFFBOT] The name for {cosmetic.id} is: {cosmetic.name}')
        except BenBotAsync.exceptions.NotFound:
            await ctx.send(f'Could not find a cosmetic name for ID: {content}')



@client.command()
async def cid(ctx, *, content = None):
    if content is None:
        await ctx.send(f'No skin was given, try: {prefix}cid (skin name)')
    else:
        try:
            cosmetic = await BenBotAsync.get_cosmetic(
                lang="en",
                searchLang="en",
                matchMethod="contains",
                name=content,
                backendType="AthenaCharacter"
            )
            await ctx.send(f'The CID for {cosmetic.name} is: {cosmetic.id}')
            print(f' [GUFFBOT] The CID for {cosmetic.name} is: {cosmetic.id}')
        except BenBotAsync.exceptions.NotFound:
            await ctx.send(f'Could not find a skin named: {content}')
        

@client.command()
async def bid(ctx, *, content):
    if content is None:
        await ctx.send(f'No backpack was given, try: {prefix}bid (backpack name)')
    else:
        try:
            cosmetic = await BenBotAsync.get_cosmetic(
                lang="en",
                searchLang="en",
                matchMethod="contains",
                name=content,
                backendType="AthenaBackpack"
            )
            await ctx.send(f'The BID for {cosmetic.name} is: {cosmetic.id}')
            print(f' [GUFFBOT] The BID for {cosmetic.name} is: {cosmetic.id}')
        except BenBotAsync.exceptions.NotFound:
            await ctx.send(f'Could not find a backpack named: {content}')



@client.command()
async def eid(ctx, *, content):
    if content is None:
        await ctx.send(f'No emote was given, try: {prefix}eid (emote name)')
    elif content.lower() == 'floss':
        await ctx.send(f'The EID for Floss is: EID_Floss')
    else:
        try:
            cosmetic = await BenBotAsync.get_cosmetic(
                lang="en",
                searchLang="en",
                matchMethod="contains",
                name=content,
                backendType="AthenaDance"
            )
            await ctx.send(f'The EID for {cosmetic.name} is: {cosmetic.id}')
            print(f' [GUFFBOT] The EID for {cosmetic.name} is: {cosmetic.id}')
        except BenBotAsync.exceptions.NotFound:
            await ctx.send(f'Could not find an emote named: {content}')


@client.command()
async def pid(ctx, *, content):
    if content is None:
        await ctx.send(f'No pickaxe was given, try: {prefix}pid (pickaxe name)')
    else:
        try:
            cosmetic = await BenBotAsync.get_cosmetic(
                lang="en",
                searchLang="en",
                matchMethod="contains",
                name=content,
                backendType="AthenaPickaxe"
            )
            await ctx.send(f'The PID for {cosmetic.name} is: {cosmetic.id}')
            print(f' [GUFFBOT] The PID for {cosmetic.name} is: {cosmetic.id}')
        except BenBotAsync.exceptions.NotFound:
            await ctx.send(f'Could not find a pickaxe named: {content}')



@client.command()
async def random(ctx, content = None):

    skins = await BenBotAsync.get_cosmetics(
        lang="en",
        backendType="AthenaCharacter"
    )

    skin = rand.choice(skins)

    backpacks = await BenBotAsync.get_cosmetics(
        lang="en",
        backendType="AthenaBackpack"
    )

    backpack = rand.choice(backpacks)

    emotes = await BenBotAsync.get_cosmetics(
        lang="en",
        backendType="AthenaDance"
    )

    emote = rand.choice(emotes)

    pickaxes = await BenBotAsync.get_cosmetics(
        lang="en",
        backendType="AthenaPickaxe"
    )

    pickaxe = rand.choice(pickaxes)

    
    if content is None:
        me = client.party.me
        await me.set_outfit(asset=skin.id)
        await me.set_backpack(asset=backpack.id)
        await me.set_pickaxe(asset=pickaxe.id)

        await ctx.send(f'Loadout randomly set to: {skin.name}, {backpack.name}, {pickaxe.name}')
    else:
        if content.lower() == 'skin':
            await client.party.me.set_outfit(asset=skin.id)
            await ctx.send(f'Skin randomly set to: {skin.name}')

        elif content.lower() == 'backpack':
            await client.party.me.set_backpack(asset=backpack.id)
            await ctx.send(f'Backpack randomly set to: {backpack.name}')

        elif content.lower() == 'emote':
            await client.party.me.set_emote(asset=emote.id)
            await ctx.send(f'Emote randomly set to: {emote.name}')

        elif content.lower() == 'pickaxe':
            await client.party.me.set_pickaxe(asset=pickaxe.id)
            await ctx.send(f'Pickaxe randomly set to: {pickaxe.name}')

        else:
            await ctx.send(f"I don't know that, try: {prefix}random (skin, backpack, emote, pickaxe - og, exclusive, unreleased")



@client.command()
async def point(ctx, *, content = None):
    if content is None:
        await client.party.me.clear_emote()
        await client.party.me.set_emote(asset='EID_IceKing')
        await ctx.send(f'Pointing with: {client.party.me.pickaxe}')
    
    else:
        if content.upper().startswith('Pickaxe_'):
            await client.party.me.set_pickaxe(asset=content.upper())
            await client.party.me.clear_emote()
            asyncio.sleep(0.25)
            await client.party.me.set_emote(asset='EID_IceKing')
            await ctx.send(f'Pointing with: {content}')
        else:
            try:
                cosmetic = await BenBotAsync.get_cosmetic(
                    lang="en",
                    searchLang="en",
                    matchMethod="contains",
                    name=content,
                    backendType="AthenaPickaxe"
                )
                await client.party.me.set_pickaxe(asset=cosmetic.id)
                await client.party.me.clear_emote()
                await client.party.me.set_emote(asset='EID_IceKing')
                await ctx.send(f'Pointing with: {cosmetic.name}')
            except BenBotAsync.exceptions.NotFound:
                await ctx.send(f'Could not find a pickaxe named: {content}')





@client.command()
async def check(ctx):
    variants = client.party.me.create_variants(material=2)

    await client.party.me.set_outfit(
        asset='CID_028_Athena_Commando_F',
        variants=variants
    )

    await ctx.send('Skin set to: Checkered Renegade')

@client.command()
async def surgeon(ctx):
    variants = client.party.me.create_variants(parts=2)

    await client.party.me.set_outfit(
        asset='CID_216_Athena_Commando_F_Medic',
        variants=variants
    )

    await ctx.send('Skin set to: Field Surgeon (No Helmet).')

@client.command()
async def pinkghoul(ctx):
    variants = client.party.me.create_variants(material=3)

    await client.party.me.set_outfit(
        asset='CID_029_Athena_Commando_F_Halloween',
        variants=variants
    )

    await ctx.send('Skin set to: Pink Ghoul Trooper')


@client.command()
async def wildcat(ctx):
    variants = client.party.me.create_variants(material=3)

    await client.party.me.set_outfit(
        asset='CID_757_Athena_Commando_F_WildCat',
        variants=variants
    )

    await ctx.send('Skin set to: wildcat ')


@client.command()
async def purpleskull(ctx):
    variants = client.party.me.create_variants(clothing_color=1)

    await client.party.me.set_outfit(
        asset='CID_030_Athena_Commando_M_Halloween',
        variants = variants
    )

    await ctx.send('Skin set to: Purple Skull Trooper')


@client.command()
async def purpleportal(ctx):
    variants = client.party.me.create_variants(
        item='AthenaBackpack',
        particle_config='Particle',
        particle=1
    )

    await client.party.me.set_backpack(
        asset='BID_105_GhostPortal',
        variants=variants
    )

    await ctx.send('Backpack set to: Purple Ghost Portal')


@client.command()
async def goldpeely(ctx):
    variants = client.party.me.create_variants(progressive=4)

    await client.party.me.set_outfit(
        asset='CID_701_Athena_Commando_M_BananaAgent',
        variants=variants,
        enlightenment=(2, 350)
    )

    await ctx.send('Skin set to: Golden Peely')

@client.command()
async def hatlessrecon(ctx):
    variants = client.party.me.create_variants(parts=2)

    await client.party.me.set_outfit(
        asset='CID_022_Athena_Commando_F',
        variants=variants
    )

    await ctx.send('Skin set to: Hatless Recon Expert')



@client.command()
async def hologram(ctx):
    await client.party.me.set_outfit(
        asset='CID_VIP_Athena_Commando_M_GalileoGondola_SG'
    )
    
    await ctx.send("Skin set to: Hologram")



@client.command()
async def itemshop(ctx):
    previous_skin = client.party.me.outfit

    store = await client.fetch_item_shop()

    await ctx.send("Equipping all item shop skins + emotes")

    for cosmetic in store.featured_items + store.daily_items:
        for grant in cosmetic.grants:
            if grant['type'] == 'AthenaCharacter':
                await client.party.me.set_outfit(asset=grant['asset'])
                await asyncio.sleep(5)
            elif grant['type'] == 'AthenaDance':
                await client.party.me.clear_emote()
                await client.party.me.set_emote(asset=grant['asset'])
                await asyncio.sleep(5)

    await client.party.me.clear_emote()
    
    await ctx.send("Done!")

    await asyncio.sleep(1.5)

    await client.party.me.set_outfit(asset=previous_skin)



@client.command()
async def new(ctx, content = None):
    newSkins = getNewSkins()
    newEmotes = getNewEmotes()

    previous_skin = client.party.me.outfit

    if content is None:
        await ctx.send(f'There are {len(newSkins) + len(newEmotes)} new skins + emotes')

        for cosmetic in newSkins + newEmotes:
            if cosmetic.startswith('CID_'):
                await client.party.me.set_outfit(asset=cosmetic)
                await asyncio.sleep(4)
            elif cosmetic.startswith('EID_'):
                await client.party.me.clear_emote()
                await client.party.me.set_emote(asset=cosmetic)
                await asyncio.sleep(4)

    elif 'skin' in content.lower():
        await ctx.send(f'There are {len(newSkins)} new skins')

        for skin in newSkins:
            await client.party.me.set_outfit(asset=skin)
            await asyncio.sleep(4)

    elif 'emote' in content.lower():
        await ctx.send(f'There are {len(newEmotes)} new emotes')

        for emote in newEmotes:
            await client.party.me.clear_emote()
            await client.party.me.set_emote(asset=emote)
            await asyncio.sleep(4)

    await client.party.me.clear_emote()
    
    await ctx.send('Done!')

    await asyncio.sleep(1.5)

    await client.party.me.set_outfit(asset=previous_skin)

    if (content is not None) and ('skin' or 'emote' not in content.lower()):
        ctx.send(f"Not a valid option. Try: {prefix}new (skins, emotes)")



@client.command()
async def ready(ctx):
    await client.party.me.set_ready(fortnitepy.ReadyState.READY)
    await ctx.send('Ready!')



@client.command()
async def unready(ctx):
    await client.party.me.set_ready(fortnitepy.ReadyState.NOT_READY)
    await ctx.send('Unready!')


@client.command()
async def sitin(ctx):
    await client.party.me.set_ready(fortnitepy.ReadyState.NOT_READY)
    await ctx.send('Sitting in')


@client.command()
async def sitout(ctx):
    await client.party.me.set_ready(fortnitepy.ReadyState.SITTING_OUT)
    await ctx.send('Sitting out')



@client.command()
async def tier(ctx, tier = None):
    if tier is None:
        await ctx.send(f'No tier was given. Try: {prefix}tier (tier number)') 
    else:
        await client.party.me.set_battlepass_info(
            has_purchased=True,
            level=tier
        )

        await ctx.send(f'Battle Pass tier set to: {tier}')



@client.command()
async def level(ctx, level = None):
    if level is None:
        await ctx.send(f'No level was given. Try: {prefix}level (number)')
    else:
        await client.party.me.set_banner(season_level=level)
        await ctx.send(f'Level set to: {level}')



@client.command()
async def banner(ctx, args1 = None, args2 = None):
    if (args1 is not None) and (args2 is None):
        if args1.startswith('defaultcolor'):
            await client.party.me.set_banner(
                color = args1
            )
            
            await ctx.send(f'Banner color set to: {args1}')

        elif args1.isnumeric() == True:
            await client.party.me.set_banner(
                color = 'defaultcolor' + args1
            )

            await ctx.send(f'Banner color set to: defaultcolor{args1}')

        else:
            await client.party.me.set_banner(
                icon = args1
            )

            await ctx.send(f'Banner Icon set to: {args1}')

    elif (args1 is not None) and (args2 is not None):
        if args2.startswith('defaultcolor'):
            await client.party.me.set_banner(
                icon = args1,
                color = args2
            )

            await ctx.send(f'Banner icon set to: {args1} -- Banner color set to: {args2}')
        
        elif args2.isnumeric() == True:
            await client.party.me.set_banner(
                icon = args1,
                color = 'defaultcolor' + args2
            )

            await ctx.send(f'Banner icon set to: {args1} -- Banner color set to: defaultcolor{args2}')

        else:
            await ctx.send(f'Not proper format. Try: {prefix}banner (Banner ID) (Banner Color ID)')


copied_player = ""


@client.command()
async def stop(ctx):
    global copied_player
    if copied_player != "":
        copied_player = ""
        await ctx.send(f'Stopped copying all users.')
        return
    else:
        try:
            await client.party.me.clear_emote()
        except RuntimeWarning:
            pass



@client.command()
async def copy(ctx, *, username = None):
    global copied_player

    if username is None:
        user = await client.fetch_profile(ctx.message.author.id)
        member = client.party.members.get(user.id)

    elif 'stop' in username:
        copied_player = ""
        await ctx.send(f'Stopped copying all users.')
        return

    elif username is not None:
        try:
            user = await client.fetch_profile(username)
            member = client.party.members.get(user.id)
        except AttributeError:
            await ctx.send("Could not get that user.")
            return
    try:
        copied_player = member

        await client.party.me.edit_and_keep(
                partial(
                    fortnitepy.ClientPartyMember.set_outfit,
                    asset=member.outfit,
                    variants=member.outfit_variants
                ),
                partial(
                    fortnitepy.ClientPartyMember.set_backpack,
                    asset=member.backpack,
                    variants=member.backpack_variants
                ),
                partial(
                    fortnitepy.ClientPartyMember.set_pickaxe,
                    asset=member.pickaxe,
                    variants=member.pickaxe_variants
                ),
                partial(
                    fortnitepy.ClientPartyMember.set_banner,
                    icon=member.banner[0],
                    color=member.banner[1],
                    season_level=member.banner[2]
                ),
                partial(
                    fortnitepy.ClientPartyMember.set_battlepass_info,
                    has_purchased=member.battlepass_info[0],
                    level=member.battlepass_info[1]
                )
            )

        await ctx.send(f"Now copying: {member.display_name}")
    except AttributeError:
        await ctx.send("Could not get that user.")

@client.event()
async def event_party_member_outfit_change(member, before, after):
    if member == copied_player:
        await client.party.me.edit_and_keep(
            partial(
                fortnitepy.ClientPartyMember.set_outfit,
                asset=after,
                variants=member.outfit_variants
            )
        )

@client.event()
async def event_party_member_outfit_variants_change(member, before, after):
    if member == copied_player:
        await client.party.me.edit_and_keep(
            partial(
                fortnitepy.ClientPartyMember.set_outfit,
                variants=member.outfit_variants
            )
        )

@client.event()
async def event_party_member_backpack_change(member, before, after):
    if member == copied_player:
        if after is None:
            await client.party.me.clear_backpack()
        else:
            await client.party.me.edit_and_keep(
                partial(
                    fortnitepy.ClientPartyMember.set_backpack,
                    asset=after,
                    variants=member.backpack_variants
                )
            )

@client.event()
async def event_party_member_backpack_variants_change(member, before, after):
    if member == copied_player:
        await client.party.me.edit_and_keep(
            partial(
                fortnitepy.ClientPartyMember.set_backpack,
                variants=member.backpack_variants
            )
        )

@client.event()
async def event_party_member_emote_change(member, before, after):
    if member == copied_player:
        if after is None:
            await client.party.me.clear_emote()
        else:
            await client.party.me.edit_and_keep(
                partial(
                    fortnitepy.ClientPartyMember.set_emote,
                    asset=after
                )
            )

@client.event()
async def event_party_member_pickaxe_change(member, before, after):
    if member == copied_player:
        await client.party.me.edit_and_keep(
            partial(
                fortnitepy.ClientPartyMember.set_pickaxe,
                asset=after,
                variants=member.pickaxe_variants
            )
        )

@client.event()
async def event_party_member_pickaxe_variants_change(member, before, after):
    if member == copied_player:
        await client.party.me.edit_and_keep(
            partial(
                fortnitepy.ClientPartyMember.set_pickaxe,
                variants=member.pickaxe_variants
            )
        )

@client.event()
async def event_party_member_banner_change(member, before, after):
    if member == copied_player:
        await client.party.me.edit_and_keep(
            partial(
                fortnitepy.ClientPartyMember.set_banner,
                icon=member.banner[0],
                color=member.banner[1],
                season_level=member.banner[2]
            )
        )

@client.event()
async def event_party_member_battlepass_info_change(member, before, after):
    if member == copied_player:
        await client.party.me.edit_and_keep(
            partial(
                fortnitepy.ClientPartyMember.set_battlepass_info,
                has_purchased=member.battlepass_info[0],
                level=member.battlepass_info[1]
            )
        )

async def set_and_update_party_prop(schema_key: str, new_value: str):
    prop = {schema_key: client.party.me.meta.set_prop(schema_key, new_value)}
    await client.party.patch(updated=prop)


@client.command()
async def hide(ctx, *, user = None):
    if client.party.me.leader:
        if user != "all":
            try:
                if user is None:
                    user = await client.fetch_profile(ctx.message.author.id)
                    member = client.party.members.get(user.id)
                else:
                    user = await client.fetch_profile(user)
                    member = client.party.members.get(user.id)

                raw_squad_assignments = client.party.meta.get_prop('Default:RawSquadAssignments_j')["RawSquadAssignments"]

                for m in raw_squad_assignments:
                    if m['memberId'] == member.id:
                        raw_squad_assignments.remove(m)

                await set_and_update_party_prop(
                    'Default:RawSquadAssignments_j',
                    {
                        'RawSquadAssignments': raw_squad_assignments
                    }
                )

                await ctx.send(f"Hid {member.display_name}")
            except AttributeError:
                await ctx.send("I could not find that user.")
            except fortnitepy.HTTPException:
                await ctx.send("I am not party leader.")
        else:
            try:
                await set_and_update_party_prop(
                    'Default:RawSquadAssignments_j',
                    {
                        'RawSquadAssignments': [
                            {
                                'memberId': client.user.id,
                                'absoluteMemberIdx': 1
                            }
                        ]
                    }
                )

                await ctx.send("Hid everyone in the party.")
            except fortnitepy.HTTPException:
                await ctx.send("I am not party leader.")
    else:
        await ctx.send("I need party leader to do this!")


@client.command()
async def unhide(ctx):
    if client.party.me.leader:
        user = await client.fetch_profile(ctx.message.author.id)
        member = client.party.members.get(user.id)

        await member.promote()

        await ctx.send("Unhid all players.")

    else:
        await ctx.send("I am not party leader.")



@client.command()
async def avatar(ctx, *, skin = None):
    if skin is None:
        await ctx.send(f'No skin was given. Try: {prefix}avatar (skin name, cid)')
    elif skin.upper().startswith('CID_'):
        try:
            cosmetic = await BenBotAsync.get_cosmetic_from_id(
                cosmetic_id=skin.upper()
            )
            client.set_avatar(fortnitepy.Avatar(asset=cosmetic.id))
            await ctx.send(f'Avatar set to: {cosmetic.id}')
        except BenBotAsync.exceptions.NotFound:
            await ctx.send(f'Could not find the ID: {skin}')
    else:
        try:
            cosmetic = await BenBotAsync.get_cosmetic(
                lang="en",
                searchLang="en",
                name=skin,
                backendType="AthenaCharacter"
            )
            client.set_avatar(fortnitepy.Avatar(asset=cosmetic.id))
            await ctx.send(f'Avatar set to: {cosmetic.name}')
        except BenBotAsync.exceptions.NotFound:
            await ctx.send(f'Could not find a skin named: {skin}')


@commands.dm_only()
@client.command()
async def send(ctx, *, message = None):
    if message is not None:
        await client.party.send(message)
        await ctx.send(f'Sent "{message}" to party chat')
    else:
        await ctx.send(f'No message was given. Try: {prefix}send (message)')



@client.command()
async def whisper(ctx, member = None, *, message = None):
    if (member is not None) and (message is not None):
        try:
            user = await client.fetch_profile(member)
            friend = client.get_friend(user.id)

            if friend.is_online():
                await friend.send(message)
                await ctx.send("Message sent.")
            else:
                await ctx.send("That friend is offline.")
        except AttributeError:
            await ctx.send("I couldn't find that friend.")
        except fortnitepy.HTTPException:
            await ctx.send("Something went wrong sending the message.")
    else:
        await ctx.send(f"Command missing one or more arguments. Try: {prefix}whisper (friend) (message)")



@client.command()
async def match(ctx, players = None):
    time = datetime.utcnow()
    if players is not None:
        if 'auto' in players.lower():
            if client.party.me.in_match():
                left = client.party.me.match_players_left
            else:
                left = 100
            await client.party.me.set_in_match(players_left=left, started_at=time)

            await asyncio.sleep(rand.randint(20, 30))

            while client.party.me.match_players_left > 5 and client.party.me.in_match():
                await client.party.me.set_in_match(players_left=client.party.me.match_players_left - rand.randint(3, 5), started_at=time),

                await asyncio.sleep(rand.randint(8, 18))

            while (client.party.me.match_players_left <= 5) and (client.party.me.match_players_left > 3):
                await client.party.me.set_in_match(players_left=client.party.me.match_players_left - rand.randint(1, 2), started_at=time)

                await asyncio.sleep(rand.randint(12, 20))

            while (client.party.me.match_players_left <= 3) and (client.party.me.match_players_left > 1):
                await client.party.me.set_in_match(players_left=client.party.me.match_players_left - 1, started_at=time)

                await asyncio.sleep(rand.randint(12, 20))

            await asyncio.sleep(6)
            await client.party.me.clear_in_match()

        elif 'leave' in players.lower():
            await client.party.me.clear_in_match()

        else:
            try:
                await client.party.me.set_in_match(players_left=int(players), started_at=time)
            except ValueError:
                await ctx.send(f"Invalid usage. Try: {prefix}match (0-255)")
                pass

    else:
        await ctx.send(f'Incorrect usage. Try: {prefix}match (auto, #, leave)')


@client.command()
async def status(ctx, *, status = None):
    if status is not None:
        await client.set_status(status)
        await ctx.send(f'Set status to: {status}')
        print(Fore.GREEN + ' [GUFFBOT] ' + Fore.RESET + 'Changed status to: ' + Fore.LIGHTBLACK_EX + f'{status}')
    else:
        await ctx.send(f'No status was given. Try: {prefix}status (status message)')


@client.command()
async def leave(ctx):
    await client.party.me.leave()
    await ctx.send('Left party.')



@client.command()
async def kick(ctx, *, member = None):
    if member is not None:
        if member.lower() == 'all':
            members = client.party.members

            for m in members:
                try:
                    member = await client.get_user(m)
                    await member.kick()
                except fortnitepy.Forbidden:
                    await ctx.send("I am not party leader.")

            await ctx.send("Kicked everyone in the party")

        else:
            try:
                user = await client.fetch_profile(member)
                member = client.party.members.get(user.id)
                if member is None:
                    await ctx.send("Couldn't find that user. Are you sure they're in the party?")

                await member.kick()
                await ctx.send(f'Kicked: {member.display_name}')
            except fortnitepy.Forbidden:
                await ctx.send("I can't kick that user because I am not party leader")
            except AttributeError:
                await ctx.send("Couldn't find that user.")
    else:
        await ctx.send(f'No member was given. Try: {prefix}kick (user)')


@client.command()
async def promote(ctx, *, member = None):
    if member is None:
        user = await client.fetch_profile(ctx.message.author.id)
        member = client.party.members.get(user.id)
    if member is not None:
        user = await client.fetch_profile(member.display_name)
        member = client.party.members.get(user.id)
    try:
        await member.promote()
        await ctx.send(f"Promoted: {member.display_name}")
    except fortnitepy.Forbidden:
        await ctx.send("Client is not party leader")
    except fortnitepy.PartyError:
        await ctx.send("That person is already party leader")
    except fortnitepy.HTTPException:
        await ctx.send("Something went wrong trying to promote that member")
    except AttributeError:
        await ctx.send("I could not find that user")



@client.command()
async def privacy(ctx, setting = None):
    if setting is not None:
        try:
            if setting.lower() == 'public':
                await client.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
                await ctx.send(f"Party Privacy set to: Public")
            elif setting.lower() == 'friends':
                await client.party.set_privacy(fortnitepy.PartyPrivacy.FRIENDS)
                await ctx.send(f"Party Privacy set to: Friends Only")
            elif setting.lower() == 'private':
                await client.party.set_privacy(fortnitepy.PartyPrivacy.PRIVATE)
                await ctx.send(f"Party Privacy set to: Private")
            else:
                await ctx.send("That is not a valid privacy setting. Try: Public, Friends, or Private")
        except fortnitepy.Forbidden:
            await ctx.send("I can not set the party privacy because I am not party leader.")
    else:
        await ctx.send(f"No privacy setting was given. Try: {prefix}privacy (Public, Friends, Private)")


@client.command()
async def join(ctx, *, member = None):
    try:
        if member is None:
            user = await client.fetch_profile(ctx.message.author.id)
            friend = client.get_friend(user.id)
        elif member is not None:
            user = await client.fetch_profile(member)
            friend = client.get_friend(user.id)

        await friend.join_party()
        await ctx.send(f"Joined {friend.display_name}'s party.")
    except fortnitepy.Forbidden:
        await ctx.send("I can not join that party because it is private.")
    except fortnitepy.PartyError:
        await ctx.send("That user is already in the party.")
    except fortnitepy.HTTPException:
        await ctx.send("Something went wrong joining the party")
    except AttributeError:
        await ctx.send("I can not join that party. Are you sure I have them friended?")
        


@client.command()
async def invite(ctx, *, member = None):
    if member == 'all':
        friends = client.friends
        invited = []

        try:
            for f in friends:
                friend = client.get_friend(f)

                if friend.is_online():
                    invited.append(friend.display_name)
                    await friend.invite()
            
            await ctx.send(f"Invited {len(invited)} friends to the party.")

        except Exception:
            pass

    else:
        try:
            if member is None:
                user = await client.fetch_profile(ctx.message.author.id)
                friend = client.get_friend(user.id)
            if member is not None:
                user = await client.fetch_profile(member)
                friend = client.get_friend(user.id)

            await friend.invite()
            await ctx.send(f"Invited {friend.display_name} to the party.")
        except fortnitepy.PartyError:
            await ctx.send("That user is already in the party.")
        except fortnitepy.HTTPException:
            await ctx.send("Something went wrong inviting that user.")
        except AttributeError:
            await ctx.send("I can not invite that user. Are you sure I have them friended?")
        except Exception:
            pass



@client.command()
async def add(ctx, *, member = None):
    if member is not None:
        try:
            user = await client.fetch_profile(member)
            friends = client.friends

            if user.id in friends:
                await ctx.send(f"I already have {user.display_name} as a friend")
            else:
                await client.add_friend(user.id)
                await ctx.send(f'Sent a friend request to {user.display_name}')
                print(Fore.GREEN + ' [GUFFBOT] ' + Fore.RESET + 'Sent a friend request to: ' + Fore.LIGHTBLACK_EX + f'{user.display_name}')

        except fortnitepy.HTTPException:
            await ctx.send("There was a problem trying to add this friend.")
        except AttributeError:
            await ctx.send("I can't find a player with that name.")
    else:
        await ctx.send(f"No user was given. Try: {prefix}add (user)")



@client.command()
async def remove(ctx, *, friend = None):
    if friend is not None:
        if friend.lower() == 'all':
            await ctx.send("Are you sure you want to remove ALL of the client's friends? (yes/no)")
            response = await client.wait_for('friend_message', timeout=15)
            content = response.content.lower()

            if 'yes' in content.lower():
                await ctx.send("Admin password?")
                res1 = await client.wait_for('friend_message', timeout=15)
                content1 = res1.content.lower()

                if content1.lower() == data['AdminPassword']:
                    try:
                        await client.remove_all_friends()
                        await ctx.send(f'Successfully removed all friends.')
                        print(Fore.GREEN + ' [GUFFBOT] ' + Fore.RESET + "Removed all of the client's friends")
                    except fortnitepy.HTTPException:
                        await ctx.send("There was an error trying to remove all friends")
                else:
                    ctx.send("That password is not correct. Kept all of the client's friends")
            elif 'no' in content.lower():
                await ctx.send('Kept all friends.')
            else:
                await ctx.send('That is not a valid response. Kept all friends.')

        else:
            try:
                user = await client.fetch_profile(friend)
                friends = client.friends

                if user.id in friends:
                    await client.remove_or_decline_friend(user.id)
                    await ctx.send(f'Successfully removed {user.display_name} as a friend.')
                    print(Fore.GREEN + ' [GUFFBOT] ' + Fore.RESET + 'Removed ' + Fore.LIGHTBLACK_EX + f'{user.display_name}' + Fore.RESET + ' as a friend.')
                else:
                    await ctx.send(f"I don't have {user.display_name} added as a friend.")
            except fortnitepy.HTTPException:
                await ctx.send("There was an error trying to remove that friend.")
            except AttributeError:
                await ctx.send("I can't find a player with that name.")
    else:
        await ctx.send(f"No user was given. Try: {prefix}remove (friend)")



@client.command()
async def block(ctx, *, user = None):
    if user is not None:
        try:
            user = await client.fetch_profile(user)
            friends = client.friends

            if user.id in friends:
                try:
                    await user.block()
                    await ctx.send(f"Blocked {user.display_name}")
                except fortnitepy.HTTPException:
                    await ctx.send("Something went wrong trying to block that user.")

            elif user.id in client.blocked_users:
                await ctx.send(f"I already have {user.display_name} blocked.")
        except AttributeError:
            await ctx.send("I can't find a player with that name.")
    else:
        await ctx.send(f"No user was given. Try: {prefix}block (friend)")



@client.command()
async def blocked(ctx):

    blockedusers = []

    for b in client.blocked_users:
        user = client.get_blocked_user(b)
        blockedusers.append(user.display_name)
    
    await ctx.send(f'Client has {len(blockedusers)} users blocked:')
    for x in blockedusers:
        if x is not None:
            await ctx.send(x)



@client.command()
async def unblock(ctx, *, user = None):
    if user is not None:
        try:
            member = await client.fetch_profile(user)
            blocked = client.blocked_users
            if member.id in blocked:
                try:
                    await client.unblock_user(member.id)
                    await ctx.send(f'Successfully unblocked {member.display_name}')
                except fortnitepy.HTTPException:
                    await ctx.send('Something went wrong trying to unblock that user.')
            else:
                await ctx.send('That user is not blocked')
        except AttributeError:
            await ctx.send("I can't find a player with that name.")
    else:
        await ctx.send(f'No user was given. Try: {prefix}unblock (blocked user)')
    


@client.command()
async def friends(ctx):
    cfriends = client.friends
    onlineFriends = []
    offlineFriends = []

    try:
        for f in cfriends:
            friend = client.get_friend(f)
            if friend.is_online():
                onlineFriends.append(friend.display_name)
            else:
                offlineFriends.append(friend.display_name)
        
        await ctx.send(f"Client has: {len(onlineFriends)} friends online and {len(offlineFriends)} friends offline")
        await ctx.send("(Check cmd for full list of friends)")

        print(" [GUFFBOT] Friends List: " + Fore.GREEN + f'{len(onlineFriends)} Online ' + Fore.RESET + "/" + Fore.LIGHTBLACK_EX + f' {len(offlineFriends)} Offline ' + Fore.RESET + "/" + Fore.LIGHTWHITE_EX + f' {len(onlineFriends) + len(offlineFriends)} Total')
        
        for x in onlineFriends:
            if x is not None:
                print(Fore.GREEN + " " + x)
        for x in offlineFriends:
            if x is not None:
                print(Fore.LIGHTBLACK_EX + " " + x)
    except Exception:
        pass



@client.command()
async def members(ctx):
    pmembers = client.party.members
    partyMembers = []
    
    for m in pmembers:
        member = client.get_user(m)
        partyMembers.append(member.display_name)
    
    await ctx.send(f"There are {len(partyMembers)} members in {client.user.display_name}'s party:")
    for x in partyMembers:
        if x is not None:
            await ctx.send(x)



@client.command()
@is_admin()
async def id(ctx, *, user = None):
    if user is not None:
        user = await client.fetch_profile(user)
    
    elif user is None:
        user = await client.fetch_profile(ctx.message.author.id)

    try:
        await ctx.send(f"{user}'s Epic ID is: {user.id}")
        print(Fore.GREEN + ' [GUFFBOT] ' + Fore.RESET + f"{user}'s Epic ID is: " + Fore.LIGHTBLACK_EX + f'{user.id}')
    except AttributeError:
        await ctx.send("I couldn't find an Epic account with that name.")



@client.command()
@is_admin()
async def user(ctx, *, user = None):
    if user is not None:
        user = await client.fetch_profile(user)

        try:
            await ctx.send(f"The ID: {user.id} belongs to: {user.display_name}")
            print(Fore.GREEN + ' [GUFFBOT] ' + Fore.RESET + f'The ID: {user.id} belongs to: ' + Fore.LIGHTBLACK_EX + f'{user.display_name}')
        except AttributeError:
            await ctx.send(f"I couldn't find a user that matches that ID")
    else:
        await ctx.send(f'No ID was given. Try: {prefix}user (ID)')



@client.command()
async def admin(ctx, setting = None, *, user = None):
    if (setting is None) and (user is None):
        await ctx.send(f"Missing one or more arguments. Try: {prefix}admin (add, remove, list) (user)")
    elif (setting is not None) and (user is None):

        user = await client.fetch_profile(ctx.message.author.id)

        if setting.lower() == 'add':
            if user.id in info['FullAccess']:
                await ctx.send("You are already an admin")

            else:
                await ctx.send("Password?")
                response = await client.wait_for('friend_message', timeout=20)
                content = response.content.lower()
                if content == data['AdminPassword']:
                    info['FullAccess'].append(user.id)
                    with open('info.json', 'w') as f:
                        json.dump(info, f, indent=4)
                        await ctx.send(f"Correct. Added {user.display_name} as an admin.")
                        print(Fore.GREEN + " [GUFFBOT] " + Fore.LIGHTGREEN_EX + user.display_name + Fore.RESET + " was added as an admin.")
                else:
                    await ctx.send("Incorrect Password.")

        elif setting.lower() == 'remove':
            if user.id not in info['FullAccess']:
                await ctx.send("You are not an admin.")
            else:
                await ctx.send("Are you sure you want to remove yourself as an admin?")
                response = await client.wait_for('friend_message', timeout=20)
                content = response.content.lower()
                if (content.lower() == 'yes') or (content.lower() == 'y'):
                    info['FullAccess'].remove(user.id)
                    with open('info.json', 'w') as f:
                        json.dump(info, f, indent=4)
                        await ctx.send("You were removed as an admin.")
                        print(Fore.BLUE + " [GUFFBOT] " + Fore.LIGHTBLUE_EX + user.display_name + Fore.RESET + " was removed as an admin.")
                elif (content.lower() == 'no') or (content.lower() == 'n'):
                    await ctx.send("You were kept as admin.")
                else:
                    await ctx.send("Not a correct reponse. Cancelling command.")
                
        elif setting == 'list':
            if user.id in info['FullAccess']:
                admins = []

                for admin in info['FullAccess']:
                    user = await client.fetch_profile(admin)
                    admins.append(user.display_name)

                await ctx.send(f"The bot has {len(admins)} admins:")

                for admin in admins:
                    await ctx.send(admin)

            else:
                await ctx.send("You don't have permission to this command.")

        else:
            await ctx.send(f"That is not a valid setting. Try: {prefix}admin (add, remove, list) (user)")
            
    elif (setting is not None) and (user is not None):
        user = await client.fetch_profile(user)

        if setting.lower() == 'add':
            if ctx.message.author.id in info['FullAccess']:
                if user.id not in info['FullAccess']:
                    info['FullAccess'].append(user.id)
                    with open('info.json', 'w') as f:
                        json.dump(info, f, indent=4)
                        await ctx.send(f"Correct. Added {user.display_name} as an admin.")
                        print(Fore.GREEN + " [GUFFBOT] " + Fore.LIGHTGREEN_EX + user.display_name + Fore.RESET + " was added as an admin.")
                else:
                    await ctx.send("That user is already an admin.")
            else:
                await ctx.send("You don't have access to add other people as admins. Try just: !admin add")
        elif setting.lower() == 'remove':
            if ctx.message.author.id in info['FullAccess']:
                if user.id in info['FullAccess']:
                    await ctx.send("Password?")
                    response = await client.wait_for('friend_message', timeout=20)
                    content = response.content.lower()
                    if content == data['AdminPassword']:
                        info['FullAccess'].remove(user.id)
                        with open('info.json', 'w') as f:
                            json.dump(info, f, indent=4)
                            await ctx.send(f"{user.display_name} was removed as an admin.")
                            print(Fore.BLUE + " [GUFFBOT] " + Fore.LIGHTBLUE_EX + user.display_name + Fore.RESET + " was removed as an admin.")
                    else:
                        await ctx.send("Incorrect Password.")
                else:
                    await ctx.send("That person is not an admin.")
            else:
                await ctx.send("You don't have permission to remove players as an admin.")
        else:
            await ctx.send(f"Not a valid setting. Try: {prefix}admin (add, remove) (user)")

#old bot life support

if (data['email'] and data['password']) and (data['email'] != "" and data['password'] != ""):
    try:
        client.run()
    except fortnitepy.errors.AuthException as e:
        print(Fore.RED + ' [ERROR] ' + Fore.RESET + f'{e}')
    except ModuleNotFoundError:

        print(Fore.RED + f'[-] ' + Fore.RESET + 'Failed to import 1 or more modules. Run "INSTALL PACKAGES.bat')
        exit()
else:
    print(Fore.RED + ' [ERROR] ' + Fore.RESET + 'Can not log in, as no accounts credentials were provided.')
