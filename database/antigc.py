import discord
from discord.ext import commands
import json
import aiohttp
import asyncio
from datetime import datetime
import os
import random
from colorama import Fore, Style

black = "\033[30m"
red = "\033[31m"
green = "\033[32m"
yellow = "\033[33m"
blue = "\033[34m"
magenta = "\033[35m"
cyan = "\033[36m"
white = "\033[37m"
www = "\033[37m"
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


def loads_tokens(file_path):
    try:
        with open(file_path, 'r') as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        return []

class AntiGC(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.gc_protection_enabled = False
        self.silent_leave = True
        self.whitelist = set()
        self.webhook_url = None
        self.log_to_file = False
        self.log_file = "gc_logs.txt"
        self.autofill_active = False
        self.autofill_tokens = 12
        self.autofill_delay = 3
        self.autofill_whitelist = set()
        self.load_settings()

    def load_settings(self):
        try:
            with open('gc_settings.json', 'r') as f:
                settings = json.load(f)
                self.gc_protection_enabled = settings.get('enabled', False)
                self.silent_leave = settings.get('silent', True)
                self.whitelist = set(settings.get('whitelist', []))
                self.webhook_url = settings.get('webhook_url', None)
                self.log_to_file = settings.get('log_to_file', False)
                self.autofill_active = settings.get('autofill', False)
                self.autofill_tokens = settings.get('autofill_tokens', 12)
                self.autofill_delay = settings.get('autofill_delay', 3)
                self.autofill_whitelist = set(settings.get('autofill_whitelist', []))
        except FileNotFoundError:
            self.save_settings()

    def save_settings(self):
        settings = {
            'enabled': self.gc_protection_enabled,
            'silent': self.silent_leave,
            'whitelist': list(self.whitelist),
            'webhook_url': self.webhook_url,
            'log_to_file': self.log_to_file,
            'autofill': self.autofill_active,
            'autofill_tokens': self.autofill_tokens,
            'autofill_delay': self.autofill_delay,
            'autofill_whitelist': list(self.autofill_whitelist)
        }
        with open('gc_settings.json', 'w') as f:
            json.dump(settings, f, indent=4)

    async def log_event(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] {message}"

        if self.webhook_url:
            try:
                async with aiohttp.ClientSession() as session:
                    webhook = discord.Webhook.from_url(self.webhook_url, session=session)
                    await webhook.send(f"```{log_message}```")
            except Exception as e:
                print(f"Webhook logging failed: {e}")

        if self.log_to_file:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(f"{log_message}\n")

    @commands.group(invoke_without_command=True)
    async def antigc(self, ctx):
        if ctx.invoked_subcommand is None:
            status = "ENABLED" if self.gc_protection_enabled else "DISABLED"
            silent = "ENABLED" if self.silent_leave else "DISABLED"
            logging = "WEBHOOK" if self.webhook_url else "FILE" if self.log_to_file else "DISABLED"
            autofill = "ENABLED" if self.autofill_active else "DISABLED"
            
            await ctx.send(f"""```ansi
{Fore.CYAN}╔══════════════════════════════════════════════╗
{Fore.CYAN}║             {Fore.WHITE}ANTI GROUP CHAT                  {Fore.CYAN}║
{Fore.CYAN}╠══════════════════════════════════════════════╣
{Fore.CYAN}║                                              
{Fore.CYAN}║  {Fore.WHITE}Protection  {Fore.CYAN}│ {Fore.GREEN if self.gc_protection_enabled else Fore.RED}{status}{Fore.CYAN}                        
{Fore.CYAN}║  {Fore.WHITE}Silent Mode {Fore.CYAN}│ {Fore.GREEN if self.silent_leave else Fore.RED}{silent}{Fore.CYAN}                        
{Fore.CYAN}║  {Fore.WHITE}Logging     {Fore.CYAN}│ {Fore.GREEN if logging != "DISABLED" else Fore.RED}{logging}{Fore.CYAN}                        
{Fore.CYAN}║  {Fore.WHITE}Whitelist   {Fore.CYAN}│ {Fore.GREEN}{len(self.whitelist)} users{Fore.CYAN}                        
{Fore.CYAN}║  {Fore.WHITE}Autofill    {Fore.CYAN}│ {Fore.GREEN if self.autofill_active else Fore.RED}{autofill}{Fore.CYAN}                        
{Fore.CYAN}║  {Fore.WHITE}Tokens      {Fore.CYAN}│ {Fore.GREEN}{self.autofill_tokens}{Fore.CYAN}                        
{Fore.CYAN}║  {Fore.WHITE}Delay       {Fore.CYAN}│ {Fore.GREEN}{self.autofill_delay}s{Fore.CYAN}                        
{Fore.CYAN}║                                              
{Fore.CYAN}╠══════════════════════════════════════════════╣
{Fore.CYAN}║  {Fore.WHITE}Commands:{Fore.CYAN}                                    
{Fore.CYAN}║  {Fore.YELLOW}• {Fore.WHITE}toggle {Fore.CYAN}     - Toggle protection on/off            
{Fore.CYAN}║  {Fore.YELLOW}• {Fore.WHITE}silent {Fore.CYAN}     - Toggle silent leave                
{Fore.CYAN}║  {Fore.YELLOW}• {Fore.WHITE}whitelist {Fore.CYAN}  - Manage whitelist                
{Fore.CYAN}║  {Fore.YELLOW}• {Fore.WHITE}webhook {Fore.CYAN}    - Configure webhook logging         
{Fore.CYAN}║  {Fore.YELLOW}• {Fore.WHITE}logging {Fore.CYAN}    - Set logging mode                  
{Fore.CYAN}║  {Fore.YELLOW}• {Fore.WHITE}autofill {Fore.CYAN}   - Auto fill group chats            
{Fore.CYAN}╚══════════════════════════════════════════════╝```""")

    @antigc.group()
    async def autofill(self, ctx):
        if ctx.invoked_subcommand is None:
            status = "ENABLED" if self.autofill_active else "DISABLED"
            whitelist = len(self.autofill_whitelist)
            
            await ctx.send(f"""```ansi
{Fore.CYAN}╔══════════════════════════════════════════════╗
{Fore.CYAN}║              {Fore.WHITE}AUTOFILL CONFIG                 {Fore.CYAN}║
{Fore.CYAN}╠══════════════════════════════════════════════╣
{Fore.CYAN}║                                              
{Fore.CYAN}║  {Fore.WHITE}Status      {Fore.CYAN}│ {Fore.GREEN if self.autofill_active else Fore.RED}{status}{Fore.CYAN}                        
{Fore.CYAN}║  {Fore.WHITE}Tokens      {Fore.CYAN}│ {Fore.GREEN}{self.autofill_tokens} tokens{Fore.CYAN}                        
{Fore.CYAN}║  {Fore.WHITE}Delay       {Fore.CYAN}│ {Fore.GREEN}{self.autofill_delay}s{Fore.CYAN}                        
{Fore.CYAN}║  {Fore.WHITE}Whitelist   {Fore.CYAN}│ {Fore.GREEN}{whitelist} users{Fore.CYAN}                        
{Fore.CYAN}║                                              
{Fore.CYAN}╠══════════════════════════════════════════════╣
{Fore.CYAN}║  {Fore.WHITE}Commands:{Fore.CYAN}                                    
{Fore.CYAN}║  {Fore.YELLOW}• {Fore.WHITE}toggle {Fore.CYAN}     - Enable/disable autofill          
{Fore.CYAN}║  {Fore.YELLOW}• {Fore.WHITE}tokens {Fore.CYAN}     - Set token count (1-50)          
{Fore.CYAN}║  {Fore.YELLOW}• {Fore.WHITE}delay {Fore.CYAN}      - Set join delay (1-10s)          
{Fore.CYAN}║  {Fore.YELLOW}• {Fore.WHITE}whitelist {Fore.CYAN}  - Manage autofill whitelist       
{Fore.CYAN}║  {Fore.YELLOW}• {Fore.WHITE}status {Fore.CYAN}     - View detailed settings          
{Fore.CYAN}╚══════════════════════════════════════════════╝```""")

    @autofill.command(name="toggle")
    async def autofill_toggle(self, ctx):
        self.autofill_active = not self.autofill_active
        self.save_settings()
        status = "enabled" if self.autofill_active else "disabled"
        await ctx.send(f"```Autofill {status}```")
        await self.log_event(f"Autofill {status} by {ctx.author}")

    @autofill.command(name="tokens")
    async def autofill_tokens_cmd(self, ctx, amount: int):
        if not 1 <= amount <= 50:
            await ctx.send("```Token amount must be between 1 and 50```")
            return
        self.autofill_tokens = amount
        self.save_settings()
        await ctx.send(f"```Set autofill token count to {amount}```")

    @autofill.command(name="delay")
    async def autofill_delay_cmd(self, ctx, seconds: float):
        if not 1 <= seconds <= 10:
            await ctx.send("```Delay must be between 1 and 10 seconds```")
            return
        self.autofill_delay = seconds
        self.save_settings()
        await ctx.send(f"```Set autofill delay to {seconds}s```")

    @autofill.group(name="whitelist")
    async def autofill_whitelist(self, ctx):
        if ctx.invoked_subcommand is None:
            whitelist = [str(uid) for uid in self.autofill_whitelist]
            await ctx.send(f"```Current whitelist: {', '.join(whitelist) if whitelist else 'None'}```")

    @autofill_whitelist.command(name="add")
    async def autofill_whitelist_add(self, ctx, user: discord.User):
        self.autofill_whitelist.add(user.id)
        self.save_settings()
        await ctx.send(f"```Added {user.name} to autofill whitelist```")

    @autofill_whitelist.command(name="remove")
    async def autofill_whitelist_remove(self, ctx, user: discord.User):
        if user.id in self.autofill_whitelist:
            self.autofill_whitelist.remove(user.id)
            self.save_settings()
            await ctx.send(f"```Removed {user.name} from autofill whitelist```")
        else:
            await ctx.send("```User not in whitelist```")

    @autofill.command(name="status")
    async def autofill_status(self, ctx):
        status = "ENABLED" if self.autofill_active else "DISABLED"
        whitelist = [str(uid) for uid in self.autofill_whitelist]
        await ctx.send(f"""```
Autofill Status: {status}
Token Count: {self.autofill_tokens}
Join Delay: {self.autofill_delay}s
Whitelisted Users: {', '.join(whitelist) if whitelist else 'None'}
```""")

    @antigc.command()
    async def toggle(self, ctx):
        self.gc_protection_enabled = not self.gc_protection_enabled
        self.save_settings()
        await ctx.send(f"```Anti group chat protection is now {'enabled' if self.gc_protection_enabled else 'disabled'}```")
        await self.log_event(f"Anti-GC protection {'enabled' if self.gc_protection_enabled else 'disabled'} by {ctx.author}")

    @antigc.command()
    async def silent(self, ctx):
        self.silent_leave = not self.silent_leave
        self.save_settings()
        await ctx.send(f"```Silent leave is now {'enabled' if self.silent_leave else 'disabled'}```")

    @antigc.group()
    async def whitelist(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("```Usage: antigc whitelist <add/remove/list> [user]```")

    @whitelist.command(name="add")
    async def whitelist_add(self, ctx, user: discord.User):
        self.whitelist.add(user.id)
        self.save_settings()
        await ctx.send(f"```Added {user.name} to whitelist```")
        await self.log_event(f"{user.name} added to whitelist by {ctx.author}")

    @whitelist.command(name="remove")
    async def whitelist_remove(self, ctx, user: discord.User):
        if user.id in self.whitelist:
            self.whitelist.remove(user.id)
            self.save_settings()
            await ctx.send(f"```Removed {user.name} from whitelist```")
            await self.log_event(f"{user.name} removed from whitelist by {ctx.author}")
        else:
            await ctx.send(f"```{user.name} is not in whitelist```")

    @whitelist.command(name="list")
    async def whitelist_list(self, ctx):
        if not self.whitelist:
            await ctx.send("```No users in whitelist```")
            return
        
        users = []
        for user_id in self.whitelist:
            user = self.bot.get_user(user_id)
            users.append(f"• {user.name if user else user_id}")
        
        await ctx.send(f"```Whitelisted Users:\n{chr(10).join(users)}```")

    @antigc.command()
    async def webhook(self, ctx, url: str = None):
        if url is None:
            self.webhook_url = None
            await ctx.send("```Webhook logging disabled```")
        else:
            try:
                async with aiohttp.ClientSession() as session:
                    webhook = discord.Webhook.from_url(url, session=session)
                    await webhook.send("```Anti-GC webhook test```")
                self.webhook_url = url
                self.save_settings()
                await ctx.send("```Webhook logging enabled and tested```")
            except:
                await ctx.send("```Invalid webhook URL```")

    @antigc.group()
    async def logging(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("```Usage: antigc logging <file/webhook/off>```")

    @logging.command(name="file")
    async def logging_file(self, ctx):
        self.log_to_file = True
        self.webhook_url = None
        self.save_settings()
        await ctx.send("```Logging set to file mode```")

    @logging.command(name="webhook")
    async def logging_webhook(self, ctx, url: str):
        try:
            async with aiohttp.ClientSession() as session:
                webhook = discord.Webhook.from_url(url, session=session)
                await webhook.send("```Anti-GC webhook test```")
            self.webhook_url = url
            self.log_to_file = False
            self.save_settings()
            await ctx.send("```Logging set to webhook mode```")
        except:
            await ctx.send("```Invalid webhook URL```")

    @logging.command(name="off")
    async def logging_off(self, ctx):
        self.log_to_file = False
        self.webhook_url = None
        self.save_settings()
        await ctx.send("```Logging disabled```")

    @commands.Cog.listener()
    async def on_private_channel_create(self, channel):
        if not isinstance(channel, discord.GroupChannel):
            return

        if self.autofill_active:
            try:
                async for msg in channel.history(limit=1):
                    if msg.author.id not in self.autofill_whitelist:
                        return
            except:
                pass

            print(f"{Fore.CYAN}[DEBUG] Detected new group chat")
            try:
                tokens_file_path = 'token.txt'
                tokens = loads_tokens(tokens_file_path)

                if not tokens:
                    print(f"{Fore.RED}[ERROR] No tokens found in the file")
                    return

                limited_tokens = tokens[:self.autofill_tokens]
                await self.log_event(f"Starting autofill with {len(limited_tokens)} tokens")

                async def add_token_to_gc(token):
                    try:
                        async with aiohttp.ClientSession() as session:
                            headers = {
                                'Authorization': token,
                                'Content-Type': 'application/json'
                            }

                            async with session.put(
                                f'https://discord.com/api/v9/channels/{channel.id}/recipients/{self.bot.user.id}',
                                headers=headers,
                                json={}
                            ) as resp:
                                if resp.status == 204:
                                    print(f'{Fore.GREEN}[SUCCESS] Added token to group chat')
                                elif resp.status == 429:
                                    retry_after = random.uniform(1, self.autofill_delay)
                                    print(f"{Fore.YELLOW}[RATELIMIT] Sleeping for {retry_after:.2f}s")
                                    await asyncio.sleep(retry_after)
                                else:
                                    print(f"{Fore.RED}[ERROR] Failed to add token: {resp.status}")

                    except Exception as e:
                        print(f"{Fore.RED}[ERROR] Autofill error: {str(e)}")

                tasks = [add_token_to_gc(token) for token in limited_tokens]
                await asyncio.gather(*tasks, return_exceptions=True)
                await self.log_event("Autofill complete")

            except Exception as e:
                print(f"{Fore.RED}[ERROR] Autofill error: {str(e)}")
                await self.log_event(f"Autofill error: {str(e)}")

        if self.gc_protection_enabled:
            try:
                async for msg in channel.history(limit=1):
                    if msg.author.id in self.whitelist:
                        await self.log_event(f"Allowed GC from whitelisted user: {msg.author.name}")
                        return
            except:
                pass

            try:
                headers = {
                    'Authorization': self.bot.http.token,
                    'Content-Type': 'application/json'
                }
                params = {
                    'silent': str(self.silent_leave).lower()
                }
                
                async with aiohttp.ClientSession() as session:
                    async with session.delete(
                        f'https://discord.com/api/v9/channels/{channel.id}',
                        headers=headers,
                        params=params
                    ) as resp:
                        if resp.status == 200:
                            await self.log_event(f"Left group chat: {channel.id}")
                        elif resp.status == 429:
                            retry_after = int(resp.headers.get("Retry-After", 1))
                            await self.log_event(f"Rate limited. Retrying after {retry_after}s")
                            await asyncio.sleep(retry_after)
                        else:
                            await self.log_event(f"Failed to leave GC. Status: {resp.status}")
            except Exception as e:
                await self.log_event(f"Error leaving GC: {e}")

def setup(bot):
    bot.add_cog(AntiGC(bot))
