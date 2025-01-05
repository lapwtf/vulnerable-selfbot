import discord
from discord.ext import commands
import json
import aiohttp
from datetime import datetime
import logging
from typing import Union
from colorama import Fore

class DMSnipe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = self.load_config()
        logging.basicConfig(level=logging.INFO)

    def load_config(self):
        try:
            with open('dmsnipe_config.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            config = {
                'webhook_url': None,
                'enabled': False,
                'edit_snipe': False,
                'ignored_users': [],
                'ignored_channels': []
            }
            self.save_config(config)
            return config

    def save_config(self, config=None):
        if config is None:
            config = self.config
        with open('dmsnipe_config.json', 'w') as f:
            json.dump(config, f, indent=4)

    @commands.group(invoke_without_command=True)
    async def dmsnipe(self, ctx):
        await ctx.send("```run '.help dmsnipe' for more info```")

    @dmsnipe.command()
    async def log(self, ctx, webhook_url: str = None):
        if webhook_url is None:
            await ctx.send("```Please add a webhook URL```")
            return
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(webhook_url) as resp:
                    if resp.status == 200:
                        self.config['webhook_url'] = webhook_url
                        self.save_config()
                        await ctx.send("```Webhook set successfully```")
                    else:
                        await ctx.send("```Invalid webhook URL```")
        except:
            await ctx.send("```Invalid webhook URL```")

    @dmsnipe.command()
    async def toggle(self, ctx, state: str = None):
        if state not in ['on', 'off']:
            await ctx.send("```Please choose 'on' or 'off'```")
            return
        
        self.config['enabled'] = state == 'on'
        self.save_config()
        await ctx.send(f"```DMSnipe {state}```")

    @dmsnipe.command()
    async def edit(self, ctx, state: str = None):
        if state not in ['on', 'off']:
            await ctx.send("```Please choose 'on' or 'off'```")
            return
        
        self.config['edit_snipe'] = state == 'on'
        self.save_config()
        await ctx.send(f"```Edit sniping {state}```")

    @dmsnipe.command()
    async def ignore(self, ctx, target: Union[discord.User, discord.TextChannel] = None):
        if target is None:
            await ctx.send("```Please mention a user or channel to ignore```")
            return
        
        target_id = target.id
        if isinstance(target, discord.User):
            if target_id not in self.config['ignored_users']:
                self.config['ignored_users'].append(target_id)
                await ctx.send(f"```Now ignoring user: {target.name}```")
            else:
                self.config['ignored_users'].remove(target_id)
                await ctx.send(f"```No longer ignoring user: {target.name}```")
        else:
            if target_id not in self.config['ignored_channels']:
                self.config['ignored_channels'].append(target_id)
                await ctx.send(f"```Now ignoring channel: {target.name}```")
            else:
                self.config['ignored_channels'].remove(target_id)
                await ctx.send(f"```No longer ignoring channel: {target.name}```")
        self.save_config()

    @dmsnipe.command()
    async def clear(self, ctx):
        self.config['ignored_users'] = []
        self.config['ignored_channels'] = []
        self.save_config()
        await ctx.send("```Cleared all ignore lists```")

    @dmsnipe.command()
    async def status(self, ctx):
        status = "ENABLED" if self.config['enabled'] else "DISABLED"
        edit_status = "ENABLED" if self.config['edit_snipe'] else "DISABLED"
        webhook_status = "SET" if self.config['webhook_url'] else "NOT SET"
        
        await ctx.send(f"""```ansi
{Fore.CYAN}╔══════════════════════════════════════════════╗
{Fore.CYAN}║              {Fore.WHITE}DMSNIPE CONFIG                {Fore.CYAN}║
{Fore.CYAN}╠══════════════════════════════════════════════╣
{Fore.CYAN}║                                              
{Fore.CYAN}║  {Fore.WHITE}Status      {Fore.CYAN}│ {Fore.GREEN if self.config['enabled'] else Fore.RED}{status}{Fore.CYAN}                        
{Fore.CYAN}║  {Fore.WHITE}Edit Snipe  {Fore.CYAN}│ {Fore.GREEN if self.config['edit_snipe'] else Fore.RED}{edit_status}{Fore.CYAN}                        
{Fore.CYAN}║  {Fore.WHITE}Webhook     {Fore.CYAN}│ {Fore.GREEN if self.config['webhook_url'] else Fore.RED}{webhook_status}{Fore.CYAN}                        
{Fore.CYAN}║  {Fore.WHITE}Ignored     {Fore.CYAN}│ {Fore.GREEN}{len(self.config['ignored_users'])} users, {len(self.config['ignored_channels'])} channels{Fore.CYAN}                        
{Fore.CYAN}║                                              
{Fore.CYAN}╠══════════════════════════════════════════════╣
{Fore.CYAN}║  {Fore.WHITE}Commands:{Fore.CYAN}                                    
{Fore.CYAN}║  {Fore.YELLOW}• {Fore.WHITE}log <url>  {Fore.CYAN}   - Set webhook URL                
{Fore.CYAN}║  {Fore.YELLOW}• {Fore.WHITE}toggle     {Fore.CYAN}   - Toggle dmsnipe on/off         
{Fore.CYAN}║  {Fore.YELLOW}• {Fore.WHITE}edit       {Fore.CYAN}   - Toggle edit snipe on/off      
{Fore.CYAN}║  {Fore.YELLOW}• {Fore.WHITE}ignore     {Fore.CYAN}   - Ignore user/channel           
{Fore.CYAN}║  {Fore.YELLOW}• {Fore.WHITE}clear      {Fore.CYAN}   - Clear ignore lists            
{Fore.CYAN}╚══════════════════════════════════════════════╝```""")

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.guild is not None:
            return
            
        if not self.config['enabled'] or not self.config['webhook_url']:
            return
            
        if message.author.bot or message.author.id in self.config['ignored_users']:
            return
            
        if message.channel.id in self.config['ignored_channels']:
            return

        embed = discord.Embed(
            title="Message Deleted",
            description=message.content,
            color=0x2F3136,
            timestamp=datetime.utcnow()
        )
        
        channel_type = "Group DM" if isinstance(message.channel, discord.GroupChannel) else "DM"
        
        embed.description = f"""**Content:**
{message.content}

**Author:** {message.author} ({message.author.id})
**Channel Type:** {channel_type}
**Channel:** {message.channel} ({message.channel.id})
{f'**Attachments:**\n' + '\n'.join([a.url for a in message.attachments]) if message.attachments else ''}"""

        try:
            webhook = discord.Webhook.from_url(self.config['webhook_url'], adapter=discord.AsyncWebhookAdapter(aiohttp.ClientSession()))
            await webhook.send(embed=embed)
            logging.info(f"Webhook sent successfully for message delete in {channel_type}")
        except Exception as e:
            logging.error(f"Failed to send webhook for message delete: {e}")

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.guild is not None:
            return
            
        if not self.config['enabled'] or not self.config['edit_snipe'] or not self.config['webhook_url']:
            return
            
        if before.author.bot or before.author.id in self.config['ignored_users']:
            return
            
        if before.channel.id in self.config['ignored_channels']:
            return
            
        if before.content == after.content:
            return

        channel_type = "Group DM" if isinstance(before.channel, discord.GroupChannel) else "DM"

        embed = discord.Embed(
            title="Message Edited",
            color=0x2F3136,
            timestamp=datetime.utcnow()
        )
        
        embed.description = f"""**Before:**
{before.content}

**After:**
{after.content}

**Author:** {before.author} ({before.author.id})
**Channel Type:** {channel_type}
**Channel:** {before.channel} ({before.channel.id})"""

        try:
            webhook = discord.Webhook.from_url(self.config['webhook_url'], adapter=discord.AsyncWebhookAdapter(aiohttp.ClientSession()))
            await webhook.send(embed=embed)
            logging.info(f"Webhook sent successfully for message edit in {channel_type}")
        except Exception as e:
            logging.error(f"Failed to send webhook for message edit: {e}")

async def setup(bot):
    await bot.add_cog(DMSnipe(bot))
