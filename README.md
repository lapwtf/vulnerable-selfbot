# Vul Selfbot

A powerful Discord selfbot with extensive automation and utility features. Created by @mwpv.

## ⚠️ Important Notice
Please be aware that using selfbots is against Discord's Terms of Service. Use at your own risk.

## Community
- Main Server: [discord.gg/lainbot](https://discord.gg/lainbot)
- Product Server: [discord.gg/lawful](https://discord.gg/lawful)

## Features

### Anti Group Chat System
- Advanced group chat protection
- Silent leave functionality
- Whitelist system
- Webhook logging
- Auto-fill capabilities with token management
- Customizable delays and settings

### Message Management
- Auto messenger system
- DM sniper functionality
- Message purging capabilities
- Custom ladder text generation

### Group Chat Utilities
- Group chat name management
- Auto-fill functionality
- Mass leave capabilities
- Group monitoring

### User Interaction
- Auto-react functionality
- Message purging
- User information fetching
- Avatar and banner viewing
- Mimic system

### Profile & Status
- Custom streaming status
- Status rotation
- Emoji rotation
- Banner and avatar commands
- Profile customization

### System Features
- Comprehensive help command system
- System stats display
- Performance monitoring
- Console management

## Setup

1. Create a `token.txt` file with your Discord token
2. Configure settings in `config.json`
3. Install required dependencies:
   ```bash
   pip install discord.py
   pip install colorama
   pip install psutil
   pip install aiohttp
   ```

## Configuration Files
- `config.json` - Main configuration
- `gc_settings.json` - Group chat settings
- `nuke_config.json` - Additional configuration

## Usage

The default command prefix is `#`. Use `#help` for a complete list of commands.

Common commands:
- `#antigc` - Manage group chat protection
- `#autofill` - Group chat auto-fill settings
- `#info` - Display bot information
- `#avatar` - View user avatars
- `#stream` - Set streaming status
- `#cls` - Clear console

## Technical Details
- Written in Python
- Uses discord.py library
- Modular cog-based command system
- Asynchronous operation
- Advanced logging capabilities

## Credits
- Created by: @mwpv
- Last Updated: 2025-01-05

## Disclaimer
This tool is for educational purposes only. Users are responsible for complying with Discord's Terms of Service and applicable laws.
