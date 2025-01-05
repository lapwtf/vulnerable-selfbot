import discord
from discord.ext import commands
from colorama import Fore
import random
import requests
from collections import defaultdict
import os
import json
import aiohttp
import asyncio
import re
from colorama import Fore, Style, init
import datetime
import platform
import psutil
import colorama
from colorama import Fore
import time
import sys

intents = discord.Intents.default()
intents.members = True
intents.reactions = True
intents.messages = True
bot = commands.Bot(command_prefix='#', intents=intents, self_bot=True)
black = "\033[30m"
red = "\033[31m"
green = "\033[32m"
yellow = "\033[33m"
blue = "\033[34m"
magenta = "\033[35m"
cyan = "\033[36m"
white = "\033[37m"
reset = "\033[0m"  
pink = "\033[38;2;255;192;203m"
white = "\033[37m"
blue = "\033[34m"
black = "\033[30m"
light_green = "\033[92m" 
light_yellow = "\033[93m" 
light_magenta = "\033[95m" 
light_cyan = "\033[96m"  
light_red = "\033[91m"  
light_blue = "\033[94m"  


gr = Fore.LIGHTGREEN_EX
rd = Fore.LIGHTRED_EX
bot.remove_command('help')
autoreply_tasks = {}
status_changing_task = None
autogc_enabled = False
help_message = None
help_author = None
help_expiry = None
status_rotation_active = False
emoji_rotation_active = False
current_status = ""
current_emoji = ""
autoreplies = [
"# P R O P H E T   runs u"
]

def get_system_info():
    cpu_usage = psutil.cpu_percent()
    memory = psutil.virtual_memory()
    memory_used = f"{memory.used / (1024 ** 3):.1f}GB"
    memory_total = f"{memory.total / (1024 ** 3):.1f}GB"
    return {
        'cpu': cpu_usage,
        'memory_used': memory_used,
        'memory_total': memory_total,
        'os': platform.system(),
        'python_version': platform.python_version()
    }

Cogs = [
    'database.help_command',
    'database.profile',
    'database.antigc',
    'database.nuke',
    'database.minicord',
    'database.ladder',
    'database.dmsnipe',
    'database.automessenger'
]

def loading_animation():
    word = "VULNERABLE"
    frames = []
    colors = [Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.BLUE, Fore.MAGENTA]
    
    for i in range(len(word)):
        frame = ""
        for j in range(len(word)):
            if j <= i:
                frame += f"{Fore.GREEN}{word[j]}"
            else:
                frame += f"{Fore.WHITE}{word[j]}"
        frames.append(frame)
    
    for color in colors:
        frames.append(f"{color}{word}")
    
    return frames

os.system('cls')

frames = loading_animation()
total_cogs = len(Cogs)
loaded_cogs = 0

for cog in Cogs:
    try:
        bot.load_extension(cog)
        loaded_cogs += 1
        
        percentage = int((loaded_cogs / total_cogs) * 100)
        
        bar_length = 20
        filled_length = int(bar_length * loaded_cogs // total_cogs)
        bar = f"{Fore.GREEN}{'█' * filled_length}{Fore.RED}{'░' * (bar_length - filled_length)}"
        
        frame = frames[loaded_cogs % len(frames)]
        
        os.system('cls')
        print(f"""
                                        {Fore.CYAN}╔══════════════════════════════════════════════╗
                                        {Fore.CYAN}║                                              ║
                                        {Fore.CYAN}║     ╦  ╦╦ ╦╦  ╔╗╔╔═╗╦═╗╔═╗╔╗ ╦  ╔═╗          ║
                                        {Fore.CYAN}║     ╚╗╔╝║ ║║  ║║║║╣ ╠╦╝╠═╣╠╩╗║  ║╣           ║
                                        {Fore.CYAN}║      ╚╝ ╚═╝╩═╝╝╚╝╚═╝╩╚═╩ ╩╚═╝╩═╝╚═╝          ║
                                        {Fore.CYAN}║                                              ║
                                        {Fore.CYAN}╠══════════════════════════════════════════════╣
                                        {Fore.CYAN}║  {Fore.WHITE}Loading Cogs: {bar} {Fore.GREEN+'OK ' if percentage == 100 else f'{percentage}%'}{Fore.CYAN}      ║
                                        {Fore.CYAN}║  {Fore.WHITE}Current: {Fore.YELLOW}{cog.split('.')[-1]:<20}{Fore.CYAN}               ║
                                        {Fore.CYAN}╚══════════════════════════════════════════════╝
""")
        time.sleep(0.4)
        
    except Exception as e:
        print(f"{Fore.RED}[ERROR]{Fore.RESET} Failed to load {cog}: {e}")
time.sleep(0.4)
print(f"""                                          {Fore.GREEN}[VULNERABLE] {Fore.CYAN}Checking and Loading Tokens....""")

www = Fore.WHITE
mkk = Fore.BLUE
b = Fore.BLACK
ggg = Fore.LIGHTGREEN_EX
y = Fore.LIGHTYELLOW_EX 
pps = Fore.LIGHTMAGENTA_EX
c = Fore.LIGHTCYAN_EX
lr = Fore.LIGHTRED_EX
qqq = Fore.MAGENTA
lbb = Fore.LIGHTBLUE_EX
mll = Fore.LIGHTBLUE_EX
mjj = Fore.RED
yyy = Fore.YELLOW
autoreact_users = {}
dreact_users = {}

config_file = "config.json"

if not os.path.exists(config_file):
    with open(config_file, 'w') as f:
        json.dump({"token": ""}, f)

with open(config_file, 'r') as f:
    config = json.load(f)
    TOKEN = config.get("token")

if not TOKEN:
    input("Token not found. Please provide a token.")
    exit()


init(autoreset=True)

def get_system_info():
    cpu_usage = psutil.cpu_percent()
    memory = psutil.virtual_memory()
    memory_used = f"{memory.used / (1024 ** 3):.1f}GB"
    memory_total = f"{memory.total / (1024 ** 3):.1f}GB"
    return {
        'cpu': cpu_usage,
        'memory_used': memory_used,
        'memory_total': memory_total,
        'os': platform.system(),
        'python_version': platform.python_version()
    }

async def check_token(token):
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get('https://discord.com/api/v9/users/@me', headers=headers) as response:
                return response.status == 200
    except:
        return False

async def validate_tokens():
    tokens_file_path = 'token.txt'
    tokens = open(tokens_file_path, 'r').read().splitlines()
    
    async with aiohttp.ClientSession() as session:
        tasks = []
        for token in tokens:
            headers = {
                'Authorization': token,
                'Content-Type': 'application/json',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }
            task = session.get('https://discord.com/api/v9/users/@me', headers=headers)
            tasks.append(task)
        
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        
        valid_count = sum(1 for resp in responses if not isinstance(resp, Exception) and resp.status == 200)
        invalid_count = len(tokens) - valid_count
        
        return valid_count, invalid_count

@bot.event
async def on_ready():
    valid_tokens, invalid_tokens = await validate_tokens()
    os.system('cls')
    print(f"""
                {Fore.CYAN}+------------------------------------------------+
                {Fore.CYAN}|{Fore.WHITE}              VULNERABLE SELFBOT                 {Fore.CYAN}
                {Fore.CYAN}|{Fore.WHITE}              ================                   {Fore.CYAN}
                {Fore.CYAN}+------------------------------------------------+
                {Fore.CYAN}| {Fore.WHITE}Creator{Fore.CYAN}: {Fore.MAGENTA}Lappy @mwpv                                   {Fore.CYAN}
                {Fore.CYAN}| {Fore.WHITE}Version{Fore.CYAN}: {Fore.GREEN}2.0                                      {Fore.CYAN}
                {Fore.CYAN}| {Fore.WHITE}Discord{Fore.CYAN}: {Fore.BLUE}discord.gg/roster                         {Fore.CYAN}
                {Fore.CYAN}+------------------------------------------------+
                {Fore.CYAN}| {Fore.WHITE}Selfbot Info{Fore.CYAN}:                                        
                {Fore.CYAN}| {Fore.WHITE}Made For{Fore.CYAN}: {Fore.YELLOW}swatlarps {Fore.WHITE}
                {Fore.CYAN}| {Fore.WHITE}Valid Tokens{Fore.CYAN}: {Fore.GREEN}{valid_tokens}
                {Fore.CYAN}| {Fore.WHITE}Invalid Tokens{Fore.CYAN}: {Fore.RED}{invalid_tokens}        
                {Fore.CYAN}| {Fore.WHITE}User{Fore.CYAN}: {Fore.GREEN}{bot.user}{Fore.CYAN}                         
                {Fore.CYAN}+------------------------------------------------+
""")

@bot.command()
async def gcfill(ctx):
    tokens_file_path = 'token.txt'
    tokens = loads_tokens(tokens_file_path)

    if not tokens:
        await ctx.send("```No tokens found in the file. Please check the token file.```")
        return

    limited_tokens = tokens[:12]
    group_channel = ctx.channel

    async def add_token_to_gc(token):
        try:
            user_client = discord.Client(intents=intents)
            
            @user_client.event
            async def on_ready():
                try:
                    await group_channel.add_recipients(user_client.user)
                    print(f'Added {user_client.user} to the group chat')
                except Exception as e:
                    print(f"Error adding user with token {token[-4:]}: {e}")
                finally:
                    await user_client.close()

            await user_client.start(token, bot=False)
            
        except Exception as e:
            print(f"Failed to process token {token[-4:]}: {e}")

    tasks = [add_token_to_gc(token) for token in limited_tokens]
    await asyncio.gather(*tasks, return_exceptions=True)
    
    await ctx.send(f"```Attempted to add {len(limited_tokens)} tokens to the group chat```")

@bot.command()
async def gcleave(ctx):
    tokens_file_path = 'token.txt'
    tokens = open(tokens_file_path, 'r').read().splitlines()
    
    if not tokens:
        await ctx.send("```No tokens found in the file```")
        return
        
    channel_id = ctx.channel.id

    async def leave_gc(token):
        headers = {
            'Authorization': token,
            'Content-Type': 'application/json'
        }
        
        async with aiohttp.ClientSession() as session:
            try:
                url = f'https://discord.com/api/v9/channels/{channel_id}'
                async with session.delete(url, headers=headers) as response:
                    if response.status == 200:
                        print(f'Token {token[-4:]} left the group chat successfully')
                    elif response.status == 429:
                        retry_after = float((await response.json()).get('retry_after', 1))
                        print(f"Rate limited for token {token[-4:]}, waiting {retry_after}s")
                        await asyncio.sleep(retry_after)
                    else:
                        print(f"Error for token {token[-4:]}: Status {response.status}")
                        
            except Exception as e:
                print(f"Failed to process token {token[-4:]}: {e}")
            
            await asyncio.sleep(0.5) 

    tasks = [leave_gc(token) for token in tokens]
    await asyncio.gather(*tasks, return_exceptions=True)
    
    await ctx.send("```Attempted to make all tokens leave the group chat```")


@bot.command()
async def gcleaveall(ctx):
    tokens_file_path = 'token.txt'
    tokens = open(tokens_file_path, 'r').read().splitlines()
    
    if not tokens:
        await ctx.send("```No tokens found in the file```")
        return

    async def leave_all_gcs(token):
        headers = {
            'Authorization': token,
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        
        left_count = 0
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get('https://discord.com/api/v9/users/@me/channels', headers=headers) as resp:
                    if resp.status == 200:
                        channels = await resp.json()
                        group_channels = [channel for channel in channels if channel.get('type') == 3]
                        
                        for channel in group_channels:
                            try:
                                channel_id = channel['id']
                                async with session.delete(f'https://discord.com/api/v9/channels/{channel_id}', headers=headers) as leave_resp:
                                    if leave_resp.status == 200:
                                        left_count += 1
                                        print(f'Token {token[-4:]} left group chat {channel_id}')
                                    elif leave_resp.status == 429:
                                        retry_after = float((await leave_resp.json()).get('retry_after', 1))
                                        print(f"Rate limited for token {token[-4:]}, waiting {retry_after}s")
                                        await asyncio.sleep(retry_after)
                                    else:
                                        print(f"Error leaving GC {channel_id} for token {token[-4:]}: Status {leave_resp.status}")
                                
                                await asyncio.sleep(0.5)  
                                
                            except Exception as e:
                                print(f"Error processing channel for token {token[-4:]}: {e}")
                                continue
                                
                        return left_count
                    else:
                        print(f"Failed to get channels for token {token[-4:]}: Status {resp.status}")
                        return 0
                        
            except Exception as e:
                print(f"Failed to process token {token[-4:]}: {e}")
                return 0

    status_msg = await ctx.send("```Starting group chat leave operation...```")
    
    tasks = [leave_all_gcs(token) for token in tokens]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    total_left = sum(r for r in results if isinstance(r, int))
    
    await status_msg.edit(content=f"""```ansi
Group Chat Leave Operation Complete
Total tokens processed: {len(tokens)}
Total group chats left: {total_left}```""")



noleave_users = {}


async def monitor_group_chats(ctx, group_chat_id):
    await bot.wait_until_ready() 

    headers = {
        'Authorization': bot.http.token,
        'Content-Type': 'application/json'
    }

    while not bot.is_closed():
        if group_chat_id in noleave_users:
            async with aiohttp.ClientSession() as session:
                async with session.get(f'https://discord.com/api/v9/channels/{group_chat_id}', headers=headers) as resp:
                    if resp.status == 200:
                        group_data = await resp.json()
                        current_member_ids = {int(recip['id']) for recip in group_data.get('recipients', [])}

                        for member in list(noleave_users[group_chat_id]):
                            if member.id not in current_member_ids:
                                try:
                                    if member.id == ctx.author.id:  
                                        continue
                                    async with session.put(
                                        f'https://discord.com/api/v9/channels/{group_chat_id}/recipients/{member.id}',
                                        headers=headers
                                    ) as add_resp:
                                        if add_resp.status == 204:
                                            print(f"Re-added {member.username} to group chat")
                                        elif add_resp.status == 429:
                                            retry_after = int(add_resp.headers.get('Retry-After', 1))
                                            await asyncio.sleep(retry_after)
                                except Exception as e:
                                    print(f"Error adding user: {e}")

        await asyncio.sleep(0.1)

class SimpleUser:
    def __init__(self, data):
        self.id = int(data['id'])
        self.username = data['username']
        self.discriminator = data.get('discriminator', '0')

@bot.command(name="autotrap")
async def autotrap(ctx, action: str, user_input: str = None):
    global noleave_users

    group_chat_id = ctx.channel.id

    if group_chat_id not in noleave_users:
        noleave_users[group_chat_id] = set()

    if action == "toggle":
        if user_input:
            if user_input.startswith('<@') and user_input.endswith('>'):
                user_id = user_input[2:-1].replace('!', '')
            else:
                user_id = user_input

            try:
                user_id = int(user_id)
                headers = {
                    'Authorization': bot.http.token,
                    'Content-Type': 'application/json'
                }
                
                async with aiohttp.ClientSession() as session:
                    async with session.get(f'https://discord.com/api/v9/users/{user_id}', headers=headers) as resp:
                        if resp.status == 200:
                            user_data = await resp.json()
                            member_obj = SimpleUser(user_data)
                            
                            if member_obj.id in [u.id for u in noleave_users[group_chat_id]]:
                                noleave_users[group_chat_id] = {u for u in noleave_users[group_chat_id] if u.id != member_obj.id}
                                await ctx.send(f"```{member_obj.username} is now allowed to leave.```")
                            else:
                                noleave_users[group_chat_id].add(member_obj)
                                await ctx.send(f"```{member_obj.username} cannot leave this group chat.```")
                        else:
                            await ctx.send("```User not found.```")
            except ValueError:
                await ctx.send("```Invalid user ID format.```")
            except Exception as e:
                await ctx.send(f"```Error: {str(e)}```")
        else:
            await ctx.send("```Please specify a user (mention or ID).```")

    elif action == "list":
        if noleave_users[group_chat_id]:
            user_list = ", ".join([f"<@{user.id}>" for user in noleave_users[group_chat_id]])
            await ctx.send(f"```Users prevented from leaving: \n{user_list}```")
        else:
            await ctx.send("```No users are prevented from leaving this group chat.```")

    elif action == "clear":
        noleave_users[group_chat_id].clear()
        await ctx.send("```All users are now allowed to leave this group chat.```")
    else:
        await ctx.send("```Invalid action. Use `toggle`, `list`, or `clear`.```")

    if not hasattr(bot, 'monitor_task'):
        bot.monitor_task = bot.loop.create_task(monitor_group_chats(ctx, group_chat_id))

@bot.command()
async def ar(ctx, user: discord.User):
    channel_id = ctx.channel.id

    await ctx.send(f"```Autoreply for {user.mention} has started.```")

    async def send_autoreply(message):
        while True:  
            try:
                random_reply = random.choice(autoreplies)
                await message.reply(random_reply)
                print(f"Successfully replied to {user.name}")
                break  
            except discord.errors.HTTPException as e:
                if e.status == 429:  
                    try:
                        response_data = await e.response.json()
                        retry_after = response_data.get('retry_after', 1)
                    except:
                        retry_after = 1 
                    print(f"Rate limited, waiting {retry_after} seconds...")
                    await asyncio.sleep(retry_after)
                else:
                    print(f"HTTP Error: {e}, retrying...")
                    await asyncio.sleep(1)
            except Exception as e:
                print(f"Error sending message: {e}, retrying...")
                await asyncio.sleep(1)

    async def reply_loop():
        def check(m):
            return m.author == user and m.channel == ctx.channel

        while True:
            try:
                message = await bot.wait_for('message', check=check)
                asyncio.create_task(send_autoreply(message))
                await asyncio.sleep(0.1)  
            except Exception as e:
                print(f"Error in reply loop: {e}")
                await asyncio.sleep(1)
                continue


    task = bot.loop.create_task(reply_loop())
    autoreply_tasks[(user.id, channel_id)] = task

@bot.command()
async def arstop(ctx):
    channel_id = ctx.channel.id
    tasks_to_stop = [key for key in autoreply_tasks.keys() if key[1] == channel_id]
    
    if tasks_to_stop:
        for user_id in tasks_to_stop:
            task = autoreply_tasks.pop(user_id)
            task.cancel()
        await ctx.send("```Autoreply has been stopped.```")
    else:
        await ctx.send("```No active autoreply tasks in this channel.```")


@bot.command()
async def mimic(ctx, user: discord.Member):
    if not hasattr(bot, 'mimic_tasks'):
        bot.mimic_tasks = {}
        
    if user.id in bot.mimic_tasks:
        bot.mimic_tasks[user.id].cancel()
        del bot.mimic_tasks[user.id]
        await ctx.send(f"```Stopped mimicking {user.name}```")
        return

    headers = {
        "authorization": bot.http.token,
        "content-type": "application/json"
    }

    last_message_id = None
    cached_messages = {}
    
    blocked_content = [
        "underage", "minor", "year old", "yo", "years old",
        "10", "11", "9", "8", "7", "6", "5", "4", "3", "1", "2",
        "12", "13", "14", "mute",
        "/kick", "/mute", ".kick", ".mute",
        "-kick", "-mute", "$kick", "ban",
        "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten",
        "eleven", "twelve", "thirteen", "self-bot", "self bot",
        "nsfw", "porn", "hentai", "nude", "nudes"
    ]

    async def mimic_task():
        nonlocal last_message_id
        
        while user.id in bot.mimic_tasks:
            try:
                params = {'after': last_message_id} if last_message_id else {'limit': 1}
                response = requests.get(
                    f"https://discord.com/api/v9/channels/{ctx.channel.id}/messages",
                    headers=headers,
                    params=params
                )
                
                if response.status_code == 200:
                    messages = response.json()
                    
                    for msg in reversed(messages):
                        if msg['author']['id'] == str(user.id):
                            content = msg.get('content', '').lower()
                            
                            if any(word in content for word in blocked_content):
                                continue
                            
                            content = msg.get('content', '')
                            
                            while content.startswith('.'):
                                content = content[1:].lstrip()  
                            
                            if not content:
                                continue
                                
                            if content[:3].count('.') > 1:
                                continue

                            if content.startswith(('!', '?', '-', '$', '/', '>', '<')):
                                continue
                            
                            if not content and msg.get('referenced_message'):
                                content = f"Reply to: {msg['referenced_message'].get('content', '[Content Hidden]')}"
                            elif not content and msg.get('mentions'):
                                content = f"Mentioned: {', '.join(m['username'] for m in msg['mentions'])}"
                            elif not content:
                                if msg.get('embeds'):
                                    embed = msg['embeds'][0]
                                    content = embed.get('description', embed.get('title', '[Embed]'))
                                elif msg.get('attachments'):
                                    content = '[' + ', '.join(a['filename'] for a in msg['attachments']) + ']'
                                else:
                                    continue
                                    
                            if any(word in content.lower() for word in blocked_content):
                                continue
                            
                            if msg['id'] not in cached_messages:
                                cached_messages[msg['id']] = True
                                
                                payload = {
                                    "content": content,
                                    "tts": False
                                }
                                
                                if msg.get('embeds'):
                                    payload['embeds'] = msg['embeds']
                                
                                requests.post(
                                    f"https://discord.com/api/v9/channels/{ctx.channel.id}/messages",
                                    headers=headers,
                                    json=payload
                                )
                                
                                await asyncio.sleep(0.5)
                            
                            last_message_id = msg['id']
                            
            except Exception as e:
                print(f"Mimic Error: {e}")
                
            await asyncio.sleep(1)

    task = bot.loop.create_task(mimic_task())
    bot.mimic_tasks[user.id] = task
    await ctx.send(f"```Started mimicking {user.name}```")


@bot.command()
async def swat(ctx, user: discord.User = None):
    if not user:
        await ctx.send("```Usage: $swat <@user>```")
        return

    locations = ["bedroom", "basement", "attic", "garage", "bathroom", "kitchen"]
    bomb_types = ["pipe bomb", "pressure cooker bomb", "homemade explosive", "IED", "chemical bomb"]
    police_units = ["SWAT team", "bomb squad", "tactical unit", "special forces", "counter-terrorism unit"]
    arrest_methods = ["broke down the door", "surrounded the house", "breached through windows", "used tear gas", "sent in K9 units"]
    
    location = random.choice(locations)
    bomb = random.choice(bomb_types)
    unit = random.choice(police_units)
    method = random.choice(arrest_methods)
    
    await ctx.send(f"```911, whats your ermgiance?📱\n{user.display_name}: you have 10minutes to come before i kill everyone in this house.\n911: Excuse me sir? Whats your name, and what are you planning on doing..\n<@{user.id}>: my name dose not mattter, i have a {bomb} inisde of my {location}, there are 4 people in the house.```")
    asyncio.sleep(1)
    await ctx.send(f"```911: Calling the {unit}. There is a possible {bomb} attack inside of <@{user.id}> residance.\nPolice Unit: On that ma'am, will send all units as fast as possible.```")
    asyncio.sleep(1)
    await ctx.send(f"```Police Unit: {user.display_name} WE HAVE YOU SURROUNDED, COME OUT PEACEFULLY\n<@{user.id}>: im a fucking loser```")
    story = f"```BREAKING NEWS: {user.display_name} was found dead after killing himself after police received an anonymous tip about a {bomb} in their {location}. The {unit} {method} and found multiple explosive devices.```"
    
    await ctx.send(story)



@bot.command()
async def autoreact(ctx, user: discord.User, emoji: str):
    autoreact_users[user.id] = emoji
    await ctx.send(f"```Now auto-reacting with {emoji} to {user.name}'s messages```")

@bot.command()
async def autoreactoff(ctx, user: discord.User):
    if user.id in autoreact_users:
        del autoreact_users[user.id]
        await ctx.send(f"```Stopped auto-reacting to {user.name}'s messages```")
    else:
        await ctx.send("```This user doesn't have autoreact enabled```")        

@bot.command()
async def dreact(ctx, user: discord.User, *emojis):
    if not emojis:
        await ctx.send("```Please provide at least one emoji```")
        return
        
    dreact_users[user.id] = [list(emojis), 0]  # [emojis_list   , and then current index cuz why not >.< - if you see this ily - lap]
    await ctx.send(f"```Now alternating reactions with {len(emojis)} emojis on {user.name}'s messages```")

@bot.command()
async def dreactoff(ctx, user: discord.User):
    if user.id in dreact_users:
        del dreact_users[user.id]
        await ctx.send(f"```Stopped reacting to {user.name}'s messages```")
    else:
        await ctx.send("```This user doesn't have dreact enabled```")   
@bot.command()
async def mpurge(ctx, limit: int):
    
    await ctx.message.delete() 
    

    async for message in ctx.channel.history(limit=limit):
        if message.author == ctx.author:  
            try:
                await message.delete()
            except discord.HTTPException:
                print(f"Failed to delete message {message.id} due to a rate limit or permission issue.")
    

    await ctx.send(f"```Purged {limit} of your messages.```", delete_after=5)





@bot.command(name="banner")
async def userbanner(ctx, user: discord.User):
    headers = {
        "Authorization": bot.http.token,
        "Content-Type": "application/json"
    }
    
    url = f"https://discord.com/api/v9/users/{user.id}/profile"
    
    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            banner_hash = data.get("user", {}).get("banner")
            
            if banner_hash:
                banner_format = "gif" if banner_hash.startswith("a_") else "png"
                banner_url = f"https://cdn.discordapp.com/banners/{user.id}/{banner_hash}.{banner_format}?size=1024"
                await ctx.send(f"```{user.display_name}'s banner:``` [Birth Sb]({banner_url})")
            else:
                await ctx.send(f"{user.mention} does not have a banner set.")
        else:
            await ctx.send(f"Failed to retrieve banner: {response.status_code} - {response.text}")
    
    except Exception as e:
        await ctx.send(f"An error occurred: {e}") 
@bot.command(aliases=['av', 'pfp'])
async def avatar(ctx, user: discord.Member = None):
    if user is None:
        user = ctx.author

    avatar_url = str(user.avatar_url_as(format='gif' if user.is_avatar_animated() else 'png'))

    await ctx.send(f"```{user.name}'s pfp```\n[Cozy Sb]({avatar_url})")

async def change_status():
    await bot.wait_until_ready()
    while True:
        for status in statuses:
            await bot.change_presence(activity=discord.Streaming(name=status, url="https://www.twitch.tv/ex"))
            await asyncio.sleep(10) 





@bot.command()
async def stream(ctx, *, statuses_list: str):
    global status_changing_task
    global statuses
    
    statuses = statuses_list.split(',')
    statuses = [status.strip() for status in statuses]
    
    if status_changing_task:
        status_changing_task.cancel()
    
    status_changing_task = bot.loop.create_task(change_status())
    await ctx.send(f"```Set Status to {statuses_list}```")

@bot.command()
async def streamoff(ctx):
    global status_changing_task
    
    if status_changing_task:
        status_changing_task.cancel()
        status_changing_task = None
        await bot.change_presence(activity=None)  
        await ctx.send(f'status rotation stopped')
    else:
        await ctx.send(f'status rotation is not running')

@bot.command(name='rstatus')
async def rotate_status(ctx, *, statuses: str):
    global status_rotation_active, current_status, current_emoji
    await ctx.message.delete()
    
    status_list = [s.strip() for s in statuses.split(',')]
    
    if not status_list:
        await ctx.send("```Please separate statuses by commas.```", delete_after=3)
        return
    
    current_index = 0
    status_rotation_active = True
    
    async def update_status_emoji():
        json_data = {
            'custom_status': {
                'text': current_status,
                'emoji_name': current_emoji
            }
        }

        custom_emoji_match = re.match(r'<a?:(\w+):(\d+)>', current_emoji)
        if custom_emoji_match:
            name, emoji_id = custom_emoji_match.groups()
            json_data['custom_status']['emoji_name'] = name
            json_data['custom_status']['emoji_id'] = emoji_id
        else:
            json_data['custom_status']['emoji_name'] = current_emoji

        async with aiohttp.ClientSession() as session:
            try:
                async with session.patch(
                    'https://discord.com/api/v9/users/@me/settings',
                    headers={'Authorization': bot.http.token, 'Content-Type': 'application/json'},
                    json=json_data
                ) as resp:
                    await resp.read()
            finally:
                await session.close()

    await ctx.send(f"```Status rotation started```")
    
    try:
        while status_rotation_active:
            current_status = status_list[current_index]
            await update_status_emoji()
            await asyncio.sleep(8)
            current_index = (current_index + 1) % len(status_list)
                
    finally:
        current_status = ""
        await update_status_emoji()
        status_rotation_active = False

@bot.command(name='remoji')
async def rotate_emoji(ctx, *, emojis: str):
    global emoji_rotation_active, current_emoji, status_rotation_active
    await ctx.message.delete()
    
    emoji_list = [e.strip() for e in emojis.split(',')]
    
    if not emoji_list:
        await ctx.send("```Please separate emojis by commas.```", delete_after=3)
        return
    
    current_index = 0
    emoji_rotation_active = True
    
    async def update_status_emoji():
        json_data = {
            'custom_status': {
                'text': current_status,
                'emoji_name': current_emoji
            }
        }
        
        custom_emoji_match = re.match(r'<a?:(\w+):(\d+)>', current_emoji)
        if custom_emoji_match:
            name, emoji_id = custom_emoji_match.groups()
            json_data['custom_status']['emoji_name'] = name
            json_data['custom_status']['emoji_id'] = emoji_id
        else:
            json_data['custom_status']['emoji_name'] = current_emoji

        async with aiohttp.ClientSession() as session:
            try:
                async with session.patch(
                    'https://discord.com/api/v9/users/@me/settings',
                    headers={'Authorization': bot.http.token, 'Content-Type': 'application/json'},
                    json=json_data
                ) as resp:
                    await resp.read()
            finally:
                await session.close()

    await ctx.send(f"```Emoji rotation started```")
    
    try:
        while emoji_rotation_active:
            current_emoji = emoji_list[current_index]
            await update_status_emoji()
            await asyncio.sleep(8)
            current_index = (current_index + 1) % len(emoji_list)
                
    finally:
        current_emoji = ""
        await update_status_emoji()
        emoji_rotation_active = False

@bot.command(name='stopstatus')
async def stop_rotate_status(ctx):
    global status_rotation_active
    status_rotation_active = False
    await ctx.send("```Status rotation stopped.```", delete_after=3)

@bot.command(name='stopemoji')
async def stop_rotate_emoji(ctx):
    global emoji_rotation_active
    emoji_rotation_active = False
    await ctx.send("```Emoji rotation stopped.```", delete_after=3)


@bot.command()
async def info(ctx):
    valid_tokens, invalid_tokens = await validate_tokens()
    await ctx.send(f"""```ansi
                {cyan}+------------------------------------------------+
                {cyan}|{white}              VULNERABLE SELFBOT                 {cyan}
                {cyan}|{white}              ================                   {cyan}
                {cyan}+------------------------------------------------+
                {cyan}| {white}Creator{cyan}: {magenta}Lappy @mwpv                                   {cyan}
                {cyan}| {white}Version{cyan}: {green}2.0                                      {cyan}
                {cyan}| {white}Discord{cyan}: {blue}/roster                         {cyan}
                {cyan}+------------------------------------------------+
                {cyan}| {white}Selfbot Info{cyan}:                                        
                {cyan}| {white}Made For{cyan}: {yellow}swatlarps                                {cyan}
                {cyan}| {white}Valid Tokens{cyan}: {green}{valid_tokens}                                    {cyan}
                {cyan}| {white}Invalid Tokens{cyan}: {red}{invalid_tokens}                                  {cyan}
                {cyan}| {white}User{cyan}: {green}{bot.user}                              {cyan}
                {cyan}+------------------------------------------------+```""")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        if message.content.startswith('.'):
            await bot.process_commands(message)
        return

    for user_id, emoji in autoreact_users.items():
        if message.author.id == user_id:
            try:
                await message.add_reaction(emoji)
            except Exception as e:
                print(e)

    for user_id, data in dreact_users.items():
        if message.author.id == user_id:
            emojis = data[0]
            current_index = data[1]
            try:
                await message.add_reaction(emojis[current_index])
                data[1] = (current_index + 1) % len(emojis)
            except Exception as e:
                print(e)

    await bot.process_commands(message)




@bot.command()
async def cls(ctx):
    os.system('cls')  
    print(main)
    await ctx.send(f"```Cleared Display UI```")

bot.run(TOKEN, bot=False)
