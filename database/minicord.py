import discord
from discord.ext import commands
import aiohttp
import asyncio
import json
import os
from datetime import datetime
from typing import List, Dict

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

class TokenController(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.active_sessions: Dict[int, Dict] = {}
        self.config_file = 'data/token_controller.json'
        self.load_config()
        self.mirroring = set()
        self.console_messages = {}  
        
        if not os.path.exists('token.txt'):
            with open('token.txt', 'w') as f:
                f.write("# Put your tokens here, one per line\n")

    def load_config(self):
        if not os.path.exists('data'):
            os.makedirs('data')
            
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                self.config = json.load(f)
        else:
            self.config = {
                'prefix': '', 
                'suffix': '', 
                'delay': 0.5,  
                'ping_format': '<@{}>'  
            }
            self.save_config()

    def save_config(self):
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=4)

    async def fetch_user_info(self, token: str) -> dict:
        headers = {
            'Authorization': token,
            'Content-Type': 'application/json'
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get('https://discord.com/api/v9/users/@me', headers=headers) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return {
                        'username': data['username'],
                        'id': data['id'],
                        'discriminator': data['discriminator']
                    }
                return None

    async def verify_guild_access(self, token: str, guild_id: int) -> bool:
        headers = {
            'Authorization': token,
            'Content-Type': 'application/json'
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://discord.com/api/v9/guilds/{guild_id}/channels', headers=headers) as resp:
                if resp.status == 200:
                    return True
                else:
                    print(f"Token verification failed: {resp.status} - {await resp.text()}")
                    return False

    @commands.group(invoke_without_command=True)
    async def minicord(self, ctx):
        await ctx.send("```Enter server ID:```")
        try:
            guild_response = await self.bot.wait_for(
                'message',
                timeout=30.0,
                check=lambda m: m.author == ctx.author and m.channel == ctx.channel
            )
            guild_id = int(guild_response.content)

            try:
                guild = self.bot.get_guild(guild_id)
                guild_name = guild.name if guild else "Unknown Server"
                await ctx.send(f"""```ansi
{green}Server Selected{reset}
{red}⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯{reset}
{white}Name: {guild_name}
ID: {guild_id}{reset}```""")
            except Exception as e:
                print(f"Error fetching guild name: {e}")

            await ctx.send("```Enter channel ID:```")
            channel_response = await self.bot.wait_for(
                'message',
                timeout=30.0,
                check=lambda m: m.author == ctx.author and m.channel == ctx.channel
            )
            try:
                channel_id = int(channel_response.content)
                channel = self.bot.get_channel(channel_id)
                channel_name = channel.name if channel else "Unknown Channel"
                await ctx.send(f"""```ansi
{green}Channel Selected{reset}
{red}⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯{reset}
{white}Name: #{channel_name}
ID: {channel_id}{reset}```""")
            except ValueError:
                await ctx.send(f"""```ansi
{red}Error{reset}
{red}⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯{reset}
{white}Invalid channel ID. Please enter a valid number.{reset}```""")
                return

            tokens = self.load_tokens()
            if not tokens:
                await ctx.send("```No tokens found in token.txt```")
                return

            access_results = await asyncio.gather(*[
                self.verify_guild_access(token, guild_id) for token in tokens
            ])
            
            valid_tokens = [token for token, has_access in zip(tokens, access_results) if has_access]
            
            if not valid_tokens:
                await ctx.send(f"""```ansi
{red}Error{reset}
{red}⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯{reset}
{white}No tokens have access to this server.{reset}```""")
                return

            usernames = []
            for i, token in enumerate(valid_tokens, 1):
                user_info = await self.fetch_user_info(token)
                if user_info:
                    usernames.append(f"{i}. {user_info['username']}#{user_info['discriminator']}")

            token_list = "\n".join(usernames)
            await ctx.send(f"""```ansi
{magenta}Available Tokens{reset}
{red}⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯{reset}
{white}{token_list}{reset}

Select tokens (comma-separated numbers):```""")

            response = await self.bot.wait_for(
                'message',
                timeout=30.0,
                check=lambda m: m.author == ctx.author and m.channel == ctx.channel
            )
            
            selected_indices = [int(x.strip()) for x in response.content.split(',')]
            selected_tokens = [valid_tokens[i-1] for i in selected_indices if 0 < i <= len(valid_tokens)]

            session_id = ctx.author.id
            self.active_sessions[session_id] = {
                'tokens': selected_tokens,
                'guild_id': guild_id,
                'channel_id': channel_id,
                'source_channel_id': ctx.channel.id,
                'prefix': self.config['prefix'],
                'suffix': self.config['suffix'],
                'delay': self.config['delay']
            }

            await self.show_control_panel(ctx)

        except asyncio.TimeoutError:
            await ctx.send("```Operation timed out```")
        except ValueError as e:
            await ctx.send(f"""```ansi
{red}Error{reset}
{red}⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯{reset}
{white}Invalid input: {str(e)}{reset}```""")

    async def update_console(self, ctx, content):
        if ctx.author.id not in self.console_messages:
            msg = await ctx.send(content)
            self.console_messages[ctx.author.id] = msg
        else:
            try:
                await self.console_messages[ctx.author.id].edit(content=content)
            except discord.NotFound:
                msg = await ctx.send(content)
                self.console_messages[ctx.author.id] = msg

    @minicord.command(name='clear')
    async def clear_console(self, ctx):
        if ctx.author.id in self.console_messages:
            await self.console_messages[ctx.author.id].delete()
            del self.console_messages[ctx.author.id]
            await ctx.message.delete()

    async def show_control_panel(self, ctx):
        session = self.active_sessions.get(ctx.author.id)
        if not session:
            await self.update_console(ctx, "```No active session```")
            return

        console_text = f"""```ansi
{magenta}Token Controller Panel{reset}
{red}⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯{reset}
{white}Active Tokens: {len(session['tokens'])}
Server ID: {session['guild_id']}
Channel ID: {session['channel_id']}
Message Prefix: {session['prefix'] or 'None'}
Message Suffix: {session['suffix'] or 'None'}
Delay: {session['delay']}s
Mirror Mode: {'Active' if ctx.author.id in self.mirroring else 'Inactive'}{reset}

{green}Commands:{reset}
{white}minicord prefix <text> - Set start message addon
minicord suffix <text> - Set end message addon
minicord delay <seconds> - Set message delay
minicord mirror - Start mirroring messages
minicord stop - End session
minicord clear - Clear console{reset}```"""

        await self.update_console(ctx, console_text)

    @minicord.command(name='prefix')
    async def set_prefix(self, ctx, *, prefix: str):
        session = self.active_sessions.get(ctx.author.id)
        if session:
            session['prefix'] = prefix
            await self.show_control_panel(ctx)

    @minicord.command(name='suffix')
    async def set_suffix(self, ctx, *, suffix: str):
        session = self.active_sessions.get(ctx.author.id)
        if session:
            session['suffix'] = suffix
            await self.show_control_panel(ctx)

    @minicord.command(name='delay')
    async def set_delay(self, ctx, delay: float):
        if delay < 0.1:
            await self.update_console(ctx, "```Delay must be at least 0.1 seconds```")
            return
            
        session = self.active_sessions.get(ctx.author.id)
        if session:
            session['delay'] = delay
            await self.show_control_panel(ctx)

    @minicord.command(name='mirror')
    async def start_mirror(self, ctx):
        session = self.active_sessions.get(ctx.author.id)
        if not session:
            await ctx.send(f"""```ansi
{red}Error{reset}
{red}⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯{reset}
{white}No active session{reset}```""")
            return

        self.mirroring.add(ctx.author.id)
        await ctx.send(f"""```ansi
{green}Success{reset}
{red}⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯{reset}
{white}Mirror mode activated. All your messages will be repeated by the tokens.
Use .tokens stop to end the session.{reset}```""")

    @minicord.command(name='stop')
    async def stop_session(self, ctx):
        if ctx.author.id in self.active_sessions:
            del self.active_sessions[ctx.author.id]
            self.mirroring.discard(ctx.author.id)
            if ctx.author.id in self.console_messages:
                await self.console_messages[ctx.author.id].delete()
                del self.console_messages[ctx.author.id]
            await self.update_console(ctx, "```Session ended```")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or message.content.startswith('.'):
            return
        
        if message.author.id in self.mirroring:
            print(f"\nMessage received: {message.content}")
            print(f"Author ID: {message.author.id}")
            print(f"Channel ID: {message.channel.id}")
            
            session = self.active_sessions.get(message.author.id)
            if session and message.channel.id == session['source_channel_id']:
                print(f"Mirroring message with {len(session['tokens'])} tokens")
                content = message.content
                if session['prefix']:
                    content = f"{session['prefix']} {content}"
                if session['suffix']:
                    content = f"{content} {session['suffix']}"

                try:
                    for token in session['tokens']:
                        async with aiohttp.ClientSession() as client_session:
                            async with client_session.post(
                                f"https://canary.discord.com/api/v9/channels/{session['channel_id']}/messages",
                                headers={
                                    "authorization": token,
                                    "Content-Type": "application/json"
                                },
                                json={"content": content}
                            ) as resp:
                                if resp.status == 429:
                                    retry_after = (await resp.json()).get('retry_after', 1)
                                    print(f"Rate limited, waiting {retry_after}s")
                                    await asyncio.sleep(retry_after)
                                elif resp.status not in (200, 204):
                                    print(f"Error sending message with token {token[-4:]}")
                                else:
                                    print(f"Message sent with token ending in {token[-4:]}")
                    await asyncio.sleep(session['delay'])
                except Exception as e:
                    print(f"Error in mirroring: {str(e)}")

        await self.bot.process_commands(message)

    def load_tokens(self) -> List[str]:
        try:
            with open('token.txt', 'r') as f:
                return [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            print("token.txt not found")
            return []
        except Exception as e:
            print(f"Error loading tokens: {e}")
            return []

def setup(bot):
    bot.add_cog(TokenController(bot))
