import discord
from discord.ext import commands
import json
import asyncio
import random
from colorama import Fore
import os

class GCName(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.task = None
        self.messages_file = "gcname_messages.json"
        self.config_file = "gcname_config.json"
        self.autopress_file = "autopress_config.json"
        self.autopress_tasks = {}
        self.autopress_messages = self.load_autopress()
        self.default_config = {
            "delay": 0.1,
            "counter_enabled": True,
            "random_order": True,
            "autopress_delay_min": 0.5,
            "autopress_delay_max": 3.5
        }
        self.config = self.load_config()
        self.messages = self.load_messages()

    def load_config(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                return json.load(f)
        self.save_config(self.default_config)
        return self.default_config

    def save_config(self, config):
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=4)

    def load_messages(self):
        if os.path.exists(self.messages_file):
            with open(self.messages_file, 'r') as f:
                return json.load(f)
        self.save_messages([
            "discord.gg/roster runs you LMFAO",
            "yo {user} wake the fuck up discord.gg/roster",
            "nigga your a bitch {user} discord.gg/roster",
            "{UPuser} STOP RUBBING YOUR NIPPLES LOL discord.gg/roster",
            "{UPuser} LOOOL HAILK DO SOMETHING RETARD discord.gg/roster",
            "{user} come die to prophet nigga discord.gg/roster",
            "{UPuser} ILL CAVE YOUR SKULL IN discord.gg/roster",
            "frail bitch discord.gg/roster",
            "{UPuser} I WILL KILL YOU LMFAO discord.gg/roster",
            "{user} nigga your slow as shit discord.gg/roster",
            "DONT FAIL THE CHECK {UPuser} LOL discord.gg/roster"
        ])
        return self.load_messages()

    def save_messages(self, messages):
        with open(self.messages_file, 'w') as f:
            json.dump(messages, f, indent=4)

    def load_autopress(self):
        if os.path.exists(self.autopress_file):
            with open(self.autopress_file, 'r') as f:
                return json.load(f)
        return {}

    def save_autopress(self):
        with open(self.autopress_file, 'w') as f:
            json.dump(self.autopress_messages, f, indent=4)

    @commands.group(invoke_without_command=True)
    async def gcname(self, ctx):
        if ctx.invoked_subcommand is None:
            message_count = len(self.messages)
            status = "RUNNING" if self.task else "STOPPED"
            
            await ctx.send(f"""```ansi
{Fore.CYAN}╔══════════════════════════════════════════════╗
{Fore.CYAN}║              {Fore.WHITE}GCNAME CONFIG                  {Fore.CYAN}║
{Fore.CYAN}╠══════════════════════════════════════════════╣
{Fore.CYAN}║                                              
{Fore.CYAN}║  {Fore.WHITE}Status      {Fore.CYAN}│ {Fore.GREEN if self.task else Fore.RED}{status}{Fore.CYAN}                        
{Fore.CYAN}║  {Fore.WHITE}Messages    {Fore.CYAN}│ {Fore.GREEN}{message_count} loaded{Fore.CYAN}                    
{Fore.CYAN}║  {Fore.WHITE}Delay       {Fore.CYAN}│ {Fore.GREEN}{self.config['delay']}s{Fore.CYAN}                        
{Fore.CYAN}║  {Fore.WHITE}Counter     {Fore.CYAN}│ {Fore.GREEN if self.config['counter_enabled'] else Fore.RED}{str(self.config['counter_enabled']).upper()}{Fore.CYAN}
{Fore.CYAN}║  {Fore.WHITE}Random      {Fore.CYAN}│ {Fore.GREEN if self.config['random_order'] else Fore.RED}{str(self.config['random_order']).upper()}{Fore.CYAN}
{Fore.CYAN}║                                              
{Fore.CYAN}╠══════════════════════════════════════════════╣
{Fore.CYAN}║  {Fore.WHITE}Commands:{Fore.CYAN}                                    
{Fore.CYAN}║  {Fore.YELLOW}• {Fore.WHITE}start <user> {Fore.CYAN}  - Start name changer         
{Fore.CYAN}║  {Fore.YELLOW}• {Fore.WHITE}stop {Fore.CYAN}        - Stop name changer          
{Fore.CYAN}║  {Fore.YELLOW}• {Fore.WHITE}add <msg> {Fore.CYAN}   - Add new message            
{Fore.CYAN}║  {Fore.YELLOW}• {Fore.WHITE}remove <id> {Fore.CYAN} - Remove message by ID       
{Fore.CYAN}║  {Fore.YELLOW}• {Fore.WHITE}list {Fore.CYAN}        - List all messages          
{Fore.CYAN}║  {Fore.YELLOW}• {Fore.WHITE}delay <sec> {Fore.CYAN} - Set delay between changes  
{Fore.CYAN}║  {Fore.YELLOW}• {Fore.WHITE}counter {Fore.CYAN}     - Toggle message counter     
{Fore.CYAN}║  {Fore.YELLOW}• {Fore.WHITE}random {Fore.CYAN}      - Toggle random order        
{Fore.CYAN}║  {Fore.YELLOW}• {Fore.WHITE}reset {Fore.CYAN}       - Reset all settings         
{Fore.CYAN}╚══════════════════════════════════════════════╝```""")

    @gcname.command()
    async def start(self, ctx, user: discord.User):
        if not isinstance(ctx.channel, discord.GroupChannel):
            await ctx.send("```This command can only be used in group chats```")
            return
            
        if self.task:
            await ctx.send("```Group chat name changer is already running```")
            return

        async def name_changer():
            counter = 1
            messages = self.messages.copy()
            
            while True:
                try:
                    if not messages:
                        messages = self.messages.copy()
                    
                    if self.config["random_order"]:
                        base_name = random.choice(messages)
                        if self.config["random_order"]:
                            messages.remove(base_name)
                    else:
                        base_name = messages[0]
                        messages = messages[1:] + [messages[0]]
                    
                    formatted_name = base_name.replace("{user}", user.name).replace("{UPuser}", user.name.upper())
                    new_name = f"{formatted_name} {counter}" if self.config["counter_enabled"] else formatted_name
                    
                    await ctx.channel._state.http.request(
                        discord.http.Route(
                            'PATCH',
                            '/channels/{channel_id}',
                            channel_id=ctx.channel.id
                        ),
                        json={'name': new_name}
                    )
                    
                    await asyncio.sleep(self.config["delay"])
                    counter += 1
                    
                except discord.HTTPException as e:
                    if e.code == 429:
                        retry_after = e.retry_after if hasattr(e, 'retry_after') else 1
                        await asyncio.sleep(retry_after)
                        continue
                    else:
                        await ctx.send(f"```Error: {str(e)}```")
                        break
                except asyncio.CancelledError:
                    break
                except Exception as e:
                    await ctx.send(f"```Error: {str(e)}```")
                    break

        self.task = asyncio.create_task(name_changer())
        await ctx.send("```Group chat name changer started```")

    @gcname.command()
    async def stop(self, ctx):
        if not self.task:
            await ctx.send("```Group chat name changer is not running```")
            return
            
        self.task.cancel()
        self.task = None
        await ctx.send("```Group chat name changer stopped```")

    @gcname.command()
    async def add(self, ctx, *, message):
        self.messages.append(message)
        self.save_messages(self.messages)
        await ctx.send(f"```Added message: {message}```")

    @gcname.command()
    async def remove(self, ctx, index: int):
        if 0 <= index < len(self.messages):
            removed = self.messages.pop(index)
            self.save_messages(self.messages)
            await ctx.send(f"```Removed message: {removed}```")
        else:
            await ctx.send("```Invalid message index```")

    @gcname.command()
    async def list(self, ctx):
        if not self.messages:
            await ctx.send("```No messages configured```")
            return
            
        message_list = "\n".join(f"{i}. {msg}" for i, msg in enumerate(self.messages))
        await ctx.send(f"```Messages:\n{message_list}```")

    @gcname.command()
    async def delay(self, ctx, delay: float):
        if delay < 0.1:
            await ctx.send("```Delay must be at least 0.1 seconds```")
            return
            
        self.config["delay"] = delay
        self.save_config(self.config)
        await ctx.send(f"```Delay set to {delay} seconds```")

    @gcname.command()
    async def counter(self, ctx):
        self.config["counter_enabled"] = not self.config["counter_enabled"]
        self.save_config(self.config)
        status = "enabled" if self.config["counter_enabled"] else "disabled"
        await ctx.send(f"```Message counter {status}```")

    @gcname.command()
    async def random(self, ctx):
        self.config["random_order"] = not self.config["random_order"]
        self.save_config(self.config)
        status = "enabled" if self.config["random_order"] else "disabled"
        await ctx.send(f"```Random message order {status}```")

    @gcname.command()
    async def reset(self, ctx):
        self.config = self.default_config.copy()
        self.save_config(self.config)
        await ctx.send("```Settings reset to default```")

    @commands.group(invoke_without_command=True)
    async def autopress(self, ctx, user: discord.Member = None):
        if ctx.invoked_subcommand is None:
            if not user:
                message_count = len(self.autopress_messages.get(str(ctx.author.id), []))
                status = "RUNNING" if ctx.author.id in self.autopress_tasks else "STOPPED"
                target = self.autopress_tasks.get(ctx.author.id, {}).get('target', None)
                
                await ctx.send(f"""```ansi
{Fore.CYAN}╔══════════════════════════════════════════════╗
{Fore.CYAN}║              {Fore.WHITE}AUTOPRESS CONFIG               {Fore.CYAN}║
{Fore.CYAN}╠══════════════════════════════════════════════╣
{Fore.CYAN}║                                              
{Fore.CYAN}║  {Fore.WHITE}Status      {Fore.CYAN}│ {Fore.GREEN if ctx.author.id in self.autopress_tasks else Fore.RED}{status}{Fore.CYAN}                        
{Fore.CYAN}║  {Fore.WHITE}Messages    {Fore.CYAN}│ {Fore.GREEN}{message_count} loaded{Fore.CYAN}                    
{Fore.CYAN}║  {Fore.WHITE}Target      {Fore.CYAN}│ {Fore.GREEN}{target.name if target else 'None'}{Fore.CYAN}
{Fore.CYAN}║  {Fore.WHITE}Min Delay   {Fore.CYAN}│ {Fore.GREEN}{self.config['autopress_delay_min']}s{Fore.CYAN}                        
{Fore.CYAN}║  {Fore.WHITE}Max Delay   {Fore.CYAN}│ {Fore.GREEN}{self.config['autopress_delay_max']}s{Fore.CYAN}
{Fore.CYAN}║                                              
{Fore.CYAN}╠══════════════════════════════════════════════╣
{Fore.CYAN}║  {Fore.WHITE}Commands:{Fore.CYAN}                                    
{Fore.CYAN}║  {Fore.YELLOW}• {Fore.WHITE}autopress <user> {Fore.CYAN}- Start autopressing       
{Fore.CYAN}║  {Fore.YELLOW}• {Fore.WHITE}add <msg> {Fore.CYAN}    - Add new message            
{Fore.CYAN}║  {Fore.YELLOW}• {Fore.WHITE}remove <id> {Fore.CYAN}  - Remove message by ID       
{Fore.CYAN}║  {Fore.YELLOW}• {Fore.WHITE}list {Fore.CYAN}         - List all messages          
{Fore.CYAN}║  {Fore.YELLOW}• {Fore.WHITE}clear {Fore.CYAN}        - Clear all messages         
{Fore.CYAN}║  {Fore.YELLOW}• {Fore.WHITE}stop {Fore.CYAN}         - Stop autopressing          
{Fore.CYAN}║  {Fore.YELLOW}• {Fore.WHITE}delay <min> <max> {Fore.CYAN}- Set delay range        
{Fore.CYAN}╚══════════════════════════════════════════════╝```""")
                return

            user_id = str(ctx.author.id)
            if user_id not in self.autopress_messages or not self.autopress_messages[user_id]:
                await ctx.send("```No messages configured. Use .autopress add <message> to add messages```")
                return

            if ctx.author.id in self.autopress_tasks:
                await ctx.send("```Autopress is already running```")
                return

            used_messages = set()
            messages_sent = 0

            async def send_message_loop():
                nonlocal used_messages, messages_sent
                while True:
                    available_messages = [msg for msg in self.autopress_messages[user_id] if msg not in used_messages]
                    if not available_messages:
                        used_messages.clear()
                        available_messages = self.autopress_messages[user_id]

                    message = random.choice(available_messages)
                    used_messages.add(message)

                    try:
                        full_message = f"{user.mention} {message.replace('{username}', user.display_name)}"
                        await ctx.send(full_message)
                        messages_sent += 1
                    except Exception as e:
                        print(f"Error sending message: {str(e)}")

                    await asyncio.sleep(random.uniform(
                        self.config['autopress_delay_min'],
                        self.config['autopress_delay_max']
                    ))

            task = asyncio.create_task(send_message_loop())
            self.autopress_tasks[ctx.author.id] = {
                'task': task,
                'target': user
            }
            await ctx.send(f"```Started autopressing {user.name}```")

    @autopress.command(name="delay")
    async def set_delay(self, ctx, min_delay: float, max_delay: float):
        if min_delay < 0.1 or max_delay < min_delay:
            await ctx.send("```Invalid delay range. Min must be ≥ 0.1 and max must be ≥ min```")
            return

        self.config['autopress_delay_min'] = min_delay
        self.config['autopress_delay_max'] = max_delay
        self.save_config(self.config)
        await ctx.send(f"```Delay range set to {min_delay}s - {max_delay}s```")

    @autopress.command(name="add")
    async def add_autopress(self, ctx, *, message: str):
        user_id = str(ctx.author.id)
        if user_id not in self.autopress_messages:
            self.autopress_messages[user_id] = []
        
        self.autopress_messages[user_id].append(message)
        self.save_autopress()
        await ctx.send(f"```Added message: {message}```")

    @autopress.command(name="remove")
    async def remove_autopress(self, ctx, index: int):
        user_id = str(ctx.author.id)
        if user_id not in self.autopress_messages or not self.autopress_messages[user_id]:
            await ctx.send("```No messages configured```")
            return
            
        if 1 <= index <= len(self.autopress_messages[user_id]):
            removed = self.autopress_messages[user_id].pop(index-1)
            self.save_autopress()
            await ctx.send(f"```Removed message: {removed}```")
        else:
            await ctx.send("```Invalid index. Use .autopress list to see message indices```")

    @autopress.command(name="list")
    async def list_autopress(self, ctx):
        user_id = str(ctx.author.id)
        if user_id not in self.autopress_messages or not self.autopress_messages[user_id]:
            await ctx.send("```No messages configured```")
            return
            
        message_list = "\n".join(f"{i+1}. {msg}" for i, msg in enumerate(self.autopress_messages[user_id]))
        await ctx.send(f"```Your configured messages:\n\n{message_list}```")

    @autopress.command(name="clear")
    async def clear_autopress(self, ctx):
        user_id = str(ctx.author.id)
        if user_id in self.autopress_messages:
            self.autopress_messages[user_id] = []
            self.save_autopress()
            await ctx.send("```Cleared all messages```")
        else:
            await ctx.send("```No messages configured```")

    @autopress.command(name="stop")
    async def stop_autopress(self, ctx):
        if ctx.author.id in self.autopress_tasks:
            self.autopress_tasks[ctx.author.id]['task'].cancel()
            del self.autopress_tasks[ctx.author.id]
            await ctx.send("```Stopped autopress```")
        else:
            await ctx.send("```Autopress is not running```")

def setup(bot):
    bot.add_cog(GCName(bot))
