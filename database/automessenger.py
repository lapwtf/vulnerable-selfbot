import discord
from discord.ext import commands, tasks
import asyncio
import json
import os
from datetime import datetime, timedelta
import aiohttp
from colorama import Fore

class AutoMessenger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.message_tasks = {}
        self.message_configs = {}
        self.config_file = "configs/auto_messenger.json"
        self.load_configs()

    def load_configs(self):
        if not os.path.exists("configs"):
            os.makedirs("configs")
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    self.message_configs = json.load(f)
        except Exception as e:
            print(f"Error loading auto messenger configs: {e}")
            self.message_configs = {}

    def save_configs(self):
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.message_configs, f, indent=4)
        except Exception as e:
            print(f"Error saving auto messenger configs: {e}")

    async def send_messages(self, channel_id, messages, interval):
        channel = self.bot.get_channel(channel_id)
        if not channel:
            return
        
        message_index = 0
        while channel_id in self.message_tasks:
            if isinstance(messages, list):
                message = messages[message_index]
                message_index = (message_index + 1) % len(messages)
            else:
                message = messages
            
            try:
                await channel.send(message)
            except Exception as e:
                print(f"Error sending message: {e}")
                
            await asyncio.sleep(interval * 60)

    @commands.command(name="msgtime")
    async def msgtime(self, ctx, time: float = None, *args):
        if not args:
            await ctx.send("```Please provide proper arguments. Use `.msgtime help` for usage information.```")
            return

        if args[0].lower() == "help":
            await ctx.send(f"""```ansi
{Fore.CYAN}╔══════════════════════════════════════════════╗
{Fore.CYAN}║            {Fore.WHITE}AUTO MESSENGER HELP              {Fore.CYAN}║
{Fore.CYAN}╠══════════════════════════════════════════════╣
{Fore.CYAN}║                                              
{Fore.CYAN}║  {Fore.YELLOW}• {Fore.WHITE}msgtime <min> <msg> on {Fore.CYAN}- Start messaging    
{Fore.CYAN}║  {Fore.YELLOW}• {Fore.WHITE}msgtime off {Fore.CYAN}          - Stop messaging     
{Fore.CYAN}║  {Fore.YELLOW}• {Fore.WHITE}msgtime status {Fore.CYAN}       - Check status       
{Fore.CYAN}║  {Fore.YELLOW}• {Fore.WHITE}msgtime list {Fore.CYAN}         - List messages      
{Fore.CYAN}║  {Fore.YELLOW}• {Fore.WHITE}msgtime clear {Fore.CYAN}        - Clear messages     
{Fore.CYAN}║  {Fore.YELLOW}• {Fore.WHITE}msgtime remove <num> {Fore.CYAN}  - Remove message    
{Fore.CYAN}║                                              
{Fore.CYAN}╚══════════════════════════════════════════════╝```""")
            return

        if args[0].lower() == "off":
            if ctx.channel.id in self.message_tasks:
                self.message_tasks[ctx.channel.id].cancel()
                del self.message_tasks[ctx.channel.id]
                if str(ctx.channel.id) in self.message_configs:
                    del self.message_configs[str(ctx.channel.id)]
                    self.save_configs()
                await ctx.send("```Auto messenger stopped```")
            else:
                await ctx.send("```No auto messenger running```")
            return

        if args[0].lower() == "status":
            if ctx.channel.id in self.message_tasks:
                config = self.message_configs.get(str(ctx.channel.id), {})
                messages = config.get('messages', [])
                interval = config.get('interval', 0)
                status = "ENABLED" if ctx.channel.id in self.message_tasks else "DISABLED"
                
                await ctx.send(f"""```ansi
{Fore.CYAN}╔══════════════════════════════════════════════╗
{Fore.CYAN}║           {Fore.WHITE}AUTO MESSENGER STATUS             {Fore.CYAN}║
{Fore.CYAN}╠══════════════════════════════════════════════╣
{Fore.CYAN}║                                              
{Fore.CYAN}║  {Fore.WHITE}Status      {Fore.CYAN}│ {Fore.GREEN if ctx.channel.id in self.message_tasks else Fore.RED}{status}{Fore.CYAN}                        
{Fore.CYAN}║  {Fore.WHITE}Interval    {Fore.CYAN}│ {Fore.GREEN}{interval} minutes{Fore.CYAN}                    
{Fore.CYAN}║  {Fore.WHITE}Messages    {Fore.CYAN}│ {Fore.GREEN}{len(messages)} configured{Fore.CYAN}                
{Fore.CYAN}║  {Fore.WHITE}Channel     {Fore.CYAN}│ {Fore.GREEN}#{ctx.channel.name}{Fore.CYAN}                    
{Fore.CYAN}║                                              
{Fore.CYAN}╚══════════════════════════════════════════════╝```""")
            else:
                await ctx.send("```No auto messenger running```")
            return

        if args[0].lower() == "list":
            config = self.message_configs.get(str(ctx.channel.id), {})
            messages = config.get('messages', [])
            if messages:
                msg_list = "\n".join(f"{i+1}. {msg}" for i, msg in enumerate(messages))
                await ctx.send(f"""```ansi
{Fore.CYAN}╔══════════════════════════════════════════════╗
{Fore.CYAN}║           {Fore.WHITE}CONFIGURED MESSAGES              {Fore.CYAN}║
{Fore.CYAN}╠══════════════════════════════════════════════╣
{Fore.CYAN}║
{Fore.GREEN}{msg_list}
{Fore.CYAN}║
{Fore.CYAN}╚══════════════════════════════════════════════╝```""")
            else:
                await ctx.send("```No messages configured```")
            return

        if args[0].lower() == "clear":
            if str(ctx.channel.id) in self.message_configs:
                del self.message_configs[str(ctx.channel.id)]
                self.save_configs()
                if ctx.channel.id in self.message_tasks:
                    self.message_tasks[ctx.channel.id].cancel()
                    del self.message_tasks[ctx.channel.id]
                await ctx.send("```All messages cleared```")
            else:
                await ctx.send("```No messages to clear```")
            return

        if args[0].lower() == "remove":
            if len(args) < 2:
                await ctx.send("```Please specify the message number```")
                return
            try:
                index = int(args[1]) - 1
                config = self.message_configs.get(str(ctx.channel.id), {})
                messages = config.get('messages', [])
                if 0 <= index < len(messages):
                    removed_msg = messages.pop(index)
                    config['messages'] = messages
                    self.message_configs[str(ctx.channel.id)] = config
                    self.save_configs()
                    await ctx.send(f"```Removed: {removed_msg}```")
                else:
                    await ctx.send("```Invalid message number```")
            except ValueError:
                await ctx.send("```Please provide a valid number```")
            return

        if not time or time <= 0:
            await ctx.send("```Please provide a valid time interval```")
            return

        messages = ' '.join(args[:-1]) if args[-1].lower() == "on" else ' '.join(args)
        message_list = [msg.strip() for msg in messages.split(',')]

        if args[-1].lower() != "on":
            await ctx.send("```Please end command with 'on' to start```")
            return

        if ctx.channel.id in self.message_tasks:
            self.message_tasks[ctx.channel.id].cancel()

        self.message_configs[str(ctx.channel.id)] = {
            'messages': message_list,
            'interval': time
        }
        self.save_configs()

        task = asyncio.create_task(self.send_messages(ctx.channel.id, message_list, time))
        self.message_tasks[ctx.channel.id] = task
        
        await ctx.send(f"```Auto messenger started ({time} min interval)```")

    async def purge_messages_from_channel(self, channel_id, keyword, user_id):
        deleted_count = 0
        last_message_id = None
        
        while True:
            try:
                params = {'limit': 100}
                if last_message_id:
                    params['before'] = last_message_id
                
                async with aiohttp.ClientSession() as session:
                    async with session.get(
                        f'https://canary.discord.com/api/v10/channels/{channel_id}/messages',
                        params=params,
                        headers={
                            'Authorization': self.bot.http.token,
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                            'X-Super-Properties': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzEyMC4wLjAuMCBTYWZhcmkvNTM3LjM2IiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTIwLjAuMC4wIiwib3NfdmVyc2lvbiI6IjEwIiwicmVmZXJyZXIiOiIiLCJyZWZlcnJpbmdfZG9tYWluIjoiIiwicmVmZXJyZXJfY3VycmVudCI6IiIsInJlZmVycmluZ19kb21haW5fY3VycmVudCI6IiIsInJlbGVhc2VfY2hhbm5lbCI6InN0YWJsZSIsImNsaWVudF9idWlsZF9udW1iZXIiOjI1MzUyOSwiY2xpZW50X2V2ZW50X3NvdXJjZSI6bnVsbH0='
                        },
                        timeout=aiohttp.ClientTimeout(total=10)
                    ) as resp:
                        if resp.status != 200:
                            if resp.status == 429:
                                retry_after = (await resp.json()).get('retry_after', 5)
                                await asyncio.sleep(retry_after)
                                continue
                            return deleted_count
                        
                        messages = await resp.json()
                
                if not messages:
                    break
                    
                last_message_id = messages[-1]['id']
                
                to_delete = [msg for msg in messages 
                           if msg['author']['id'] == str(user_id) 
                           and keyword.lower() in msg['content'].lower()]
                
                for msg in to_delete:
                    try:
                        await asyncio.sleep(0.5)
                        async with aiohttp.ClientSession() as session:
                            async with session.delete(
                                f'https://canary.discord.com/api/v10/channels/{channel_id}/messages/{msg["id"]}',
                                headers={
                                    'Authorization': self.bot.http.token,
                                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                                    'X-Super-Properties': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzEyMC4wLjAuMCBTYWZhcmkvNTM3LjM2IiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTIwLjAuMC4wIiwib3NfdmVyc2lvbiI6IjEwIiwicmVmZXJyZXIiOiIiLCJyZWZlcnJpbmdfZG9tYWluIjoiIiwicmVmZXJyZXJfY3VycmVudCI6IiIsInJlZmVycmluZ19kb21haW5fY3VycmVudCI6IiIsInJlbGVhc2VfY2hhbm5lbCI6InN0YWJsZSIsImNsaWVudF9idWlsZF9udW1iZXIiOjI1MzUyOSwiY2xpZW50X2V2ZW50X3NvdXJjZSI6bnVsbH0='
                                },
                                timeout=aiohttp.ClientTimeout(total=10)
                            ) as resp:
                                if resp.status == 204:
                                    deleted_count += 1
                                elif resp.status == 429:
                                    retry_after = (await resp.json()).get('retry_after', 1)
                                    await asyncio.sleep(retry_after)
                    except Exception as e:
                        continue
                
                if len(messages) < 100:
                    break
                    
                await asyncio.sleep(1)
                
            except Exception:
                continue
                
        return deleted_count

    @commands.command(name="purgekw")
    async def purgekw(self, ctx, keyword: str):
        try:
            await ctx.message.delete()
        except:
            pass

        deleted_count = 0
        last_message_id = None
        status_msg = await ctx.send("```Purging messages...```")
        
        while True:
            try:
                params = {'limit': 100}
                if last_message_id:
                    params['before'] = last_message_id
                
                async with aiohttp.ClientSession() as session:
                    async with session.get(
                        f'https://canary.discord.com/api/v10/channels/{ctx.channel.id}/messages',
                        params=params,
                        headers={
                            'Authorization': self.bot.http.token,
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                        }
                    ) as resp:
                        if resp.status != 200:
                            await status_msg.edit(content=f"```Error fetching messages: {resp.status}```")
                            return
                        
                        messages = await resp.json()
                
                if not messages:
                    break
                    
                last_message_id = messages[-1]['id']
                
                to_delete = [msg for msg in messages 
                           if msg['author']['id'] == str(ctx.author.id) 
                           and keyword.lower() in msg['content'].lower()]
                
                for msg in to_delete:
                    try:
                        await asyncio.sleep(0.5)
                        async with aiohttp.ClientSession() as session:
                            async with session.delete(
                                f'https://canary.discord.com/api/v10/channels/{ctx.channel.id}/messages/{msg["id"]}',
                                headers={
                                    'Authorization': self.bot.http.token,
                                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                                }
                            ) as resp:
                                if resp.status == 204:
                                    deleted_count += 1
                                    await status_msg.edit(content=f"```Purging... ({deleted_count} deleted)```")
                                elif resp.status == 429:
                                    retry_after = (await resp.json()).get('retry_after', 1)
                                    await asyncio.sleep(retry_after)
                    except Exception as e:
                        continue
                
                if len(messages) < 100:
                    break
                    
                await asyncio.sleep(1)
                
            except Exception as e:
                await status_msg.edit(content=f"```Error during purge: {e}```")
                return

        try:
            await status_msg.edit(content=f"```Purged {deleted_count} messages containing '{keyword}'```")
            await asyncio.sleep(3)
            await status_msg.delete()
        except:
            pass

    @commands.command(name="purgekwdm")
    async def purgekwdm(self, ctx, keyword: str):
        try:
            await ctx.message.delete()
        except:
            pass

        total_deleted = 0
        status_msg = await ctx.send("```Purging messages from DMs...```")

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    'https://canary.discord.com/api/v10/users/@me/channels',
                    headers={
                        'Authorization': self.bot.http.token,
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                    }
                ) as resp:
                    if resp.status == 200:
                        channels = await resp.json()
                        for channel in channels:
                            if channel['type'] == 1:  # DM channel
                                deleted = await self.purge_messages_from_channel(channel['id'], keyword, ctx.author.id)
                                total_deleted += deleted
                                await status_msg.edit(content=f"```Purging... ({total_deleted} deleted)```")

        except Exception as e:
            await status_msg.edit(content=f"```Error during DM purge: {str(e)}```")
            return

        try:
            await status_msg.edit(content=f"```Purged {total_deleted} messages containing '{keyword}' from DMs```")
            await asyncio.sleep(3)
            await status_msg.delete()
        except:
            pass

    @commands.command(name="purgekwserver")
    async def purgekwserver(self, ctx, keyword: str):
        try:
            await ctx.message.delete()
        except:
            pass

        total_deleted = 0
        status_msg = await ctx.send("```Purging messages from servers...```")

        for guild in self.bot.guilds:
            try:
                for channel in guild.text_channels:
                    try:
                        deleted = await self.purge_messages_from_channel(channel.id, keyword, ctx.author.id)
                        total_deleted += deleted
                        await status_msg.edit(content=f"```Purging... ({total_deleted} deleted)```")
                    except:
                        continue
            except:
                continue

        try:
            await status_msg.edit(content=f"```Purged {total_deleted} messages containing '{keyword}' from servers```")
            await asyncio.sleep(3)
            await status_msg.delete()
        except:
            pass

async def setup(bot):
    await bot.add_cog(AutoMessenger(bot))
