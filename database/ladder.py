import discord
from discord.ext import commands
import json
import random
import asyncio
from colorama import Fore

class Ladder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.default_ladder_messages = [
            "I am above you",
            "You're beneath me", 
            "Bow down peasant",
            "Keep climbing",
            "Stay down there",
            "Looking down on you",
            "Higher than you'll ever be",
            "Keep trying to reach me"
        ]
        self.ladder_messages = self.default_ladder_messages.copy()
        self.ladder_delay = 0.2
        self.ladder_enabled = False
        self.ladder_task = None
        self.ladder_target = None
        self.load_ladder_messages()

    def save_ladder_messages(self):
        with open('ladder_messages.json', 'w') as f:
            json.dump(self.ladder_messages, f)

    def load_ladder_messages(self):
        try:
            with open('ladder_messages.json', 'r') as f:
                self.ladder_messages = json.load(f)
        except FileNotFoundError:
            self.ladder_messages = self.default_ladder_messages.copy()
            self.save_ladder_messages()

    @commands.group(invoke_without_command=True)
    async def ladder(self, ctx, user: discord.User = None):
        if ctx.invoked_subcommand is None:
            if self.ladder_enabled:
                await ctx.send("```Ladder spam is already running```")
                return
                
            self.ladder_enabled = True
            self.ladder_target = user
            
            async def ladder_spam():
                while self.ladder_enabled:
                    try:
                        message = random.choice(self.ladder_messages)
                        words = message.split()
                        
                        for word in words:
                            if self.ladder_target and random.random() < 0.2:
                                await ctx.send(f"{word} {self.ladder_target.mention}")
                            else:
                                await ctx.send(word)
                            await asyncio.sleep(self.ladder_delay)
                            
                        await asyncio.sleep(2.0)
                    except Exception as e:
                        print(f"Error sending ladder message: {e}")
            
            self.ladder_task = asyncio.create_task(ladder_spam())
            status = f"Ladder spam started"
            if self.ladder_target:
                status += f" targeting {self.ladder_target.name}"
            await ctx.send(f"```{status}```")

    @ladder.command(name="stop")
    async def ladder_stop(self, ctx):
        if not self.ladder_enabled:
            await ctx.send("```Ladder spam is not running```")
            return
            
        self.ladder_enabled = False
        self.ladder_target = None
        if self.ladder_task:
            self.ladder_task.cancel()
        await ctx.send("```Ladder spam stopped```")

    @ladder.command(name="add")
    async def ladder_add(self, ctx, *, message: str):
        if message in self.ladder_messages:
            await ctx.send("```This message already exists```")
            return
            
        self.ladder_messages.append(message)
        self.save_ladder_messages()
        await ctx.send(f"```Added: {message}```")

    @ladder.command(name="remove")
    async def ladder_remove(self, ctx, *, message: str):
        if message not in self.ladder_messages:
            await ctx.send("```Message not found```")
            return
            
        self.ladder_messages.remove(message)
        self.save_ladder_messages()
        await ctx.send(f"```Removed: {message}```")

    @ladder.command(name="list")
    async def ladder_list(self, ctx):
        messages = "\n".join(f"{i+1}. {msg}" for i, msg in enumerate(self.ladder_messages))
        await ctx.send(f"```Ladder Messages:\n\n{messages}```")

    @ladder.command(name="delay")
    async def ladder_delay_cmd(self, ctx, delay: float):
        if delay < 0.2:
            await ctx.send("```Delay must be at least 0.2 seconds```")
            return
            
        self.ladder_delay = delay
        await ctx.send(f"```Ladder delay set to {delay}s```")

    @ladder.command(name="reset")
    async def ladder_reset(self, ctx):
        self.ladder_messages = self.default_ladder_messages.copy()
        self.save_ladder_messages()
        await ctx.send("```Reset to default ladder messages```")

    @ladder.command(name="clear")
    async def ladder_clear(self, ctx):
        self.ladder_messages.clear()
        self.save_ladder_messages()
        await ctx.send("```Cleared all ladder messages```")

    @ladder.command(name="status")
    async def ladder_status(self, ctx):
        status = "ENABLED" if self.ladder_enabled else "DISABLED"
        await ctx.send(f"""```ansi
{Fore.CYAN}╔══════════════════════════════════════════════╗
{Fore.CYAN}║              {Fore.WHITE}LADDER CONFIG                  {Fore.CYAN}║
{Fore.CYAN}╠══════════════════════════════════════════════╣
{Fore.CYAN}║                                              
{Fore.CYAN}║  {Fore.WHITE}Status      {Fore.CYAN}│ {Fore.GREEN if self.ladder_enabled else Fore.RED}{status}{Fore.CYAN}                        
{Fore.CYAN}║  {Fore.WHITE}Messages    {Fore.CYAN}│ {Fore.GREEN}{len(self.ladder_messages)} messages{Fore.CYAN}                    
{Fore.CYAN}║  {Fore.WHITE}Delay       {Fore.CYAN}│ {Fore.GREEN}{self.ladder_delay}s{Fore.CYAN}                        
{Fore.CYAN}║  {Fore.WHITE}Target      {Fore.CYAN}│ {Fore.GREEN}{self.ladder_target.name if self.ladder_target else 'None'}{Fore.CYAN}                        
{Fore.CYAN}║                                              
{Fore.CYAN}╠══════════════════════════════════════════════╣
{Fore.CYAN}║  {Fore.WHITE}Commands:{Fore.CYAN}                                    
{Fore.CYAN}║  {Fore.YELLOW}• {Fore.WHITE}ladder {Fore.CYAN}      - Start ladder spam              
{Fore.CYAN}║  {Fore.YELLOW}• {Fore.WHITE}stop {Fore.CYAN}        - Stop ladder spam               
{Fore.CYAN}║  {Fore.YELLOW}• {Fore.WHITE}add {Fore.CYAN}         - Add new ladder message         
{Fore.CYAN}║  {Fore.YELLOW}• {Fore.WHITE}remove {Fore.CYAN}      - Remove a ladder message        
{Fore.CYAN}║  {Fore.YELLOW}• {Fore.WHITE}list {Fore.CYAN}        - List all ladder messages       
{Fore.CYAN}║  {Fore.YELLOW}• {Fore.WHITE}delay {Fore.CYAN}       - Set message delay              
{Fore.CYAN}║  {Fore.YELLOW}• {Fore.WHITE}reset {Fore.CYAN}       - Reset to default messages      
{Fore.CYAN}║  {Fore.YELLOW}• {Fore.WHITE}clear {Fore.CYAN}       - Clear all messages             
{Fore.CYAN}╚══════════════════════════════════════════════╝```""")

async def setup(bot):
    await bot.add_cog(Ladder(bot))
