import discord
from discord.ext import commands
import datetime
import asyncio
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
class HelpCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.pages = {} 
        self.current_page = {} 
        
        self.ascii_art = {
            1: f"""
                                {white}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣤⡀
                                ⠀ ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣸⣿⣿⡟
                                ⠀⣰⣶⣶⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⣶⣿⣿⣿⠏⠀
                                ⠀⠻⣿⣿⣷⣦⣄⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣴⣾⣿⣿⣿⣿⣿⣿⠀⠀
                                ⠀⠀⠀⣿⣿⣿⣿⣿⣿⣷⣶⣤⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀
                                ⠀⠀⠀⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⣴⣶⣾⣶⣾⣿⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀
                                ⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⡿⢿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀
                                ⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⢧⡹⣜⢣⣏⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⠆⠀⠀
                                ⠀⠀⠀⠀⠸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⡿⡟⡴⣋⣟⣷⣿⣿⣿⣿⣿⣿⣿⡯⠀⠀⠀⠀
                                ⠀⠀⠀⠀⠀⠀⠉⢹⣿⣿⣿⣿⣿⣿⣿⣿⠿⠿⢿⣿⣿⣷⣿⠟⠋⠉⠙⢻⣿⣿⣿⣿⡆⠀⠀⠀
                                ⠀⠀⠀⠀⠀⠀⠀⣻⣿⣿⣿⣿⣿⣿⢻⣁⠀⠀⠀⠀⠈⠉⠀⠀⠀{red}⢠⣼⣗{white}⠘⢿⣿⣿⡇⠀⠀⠀
                                ⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⠃⠈{red}⣿⣿⡇{white}⠀⠀⠀⠀⠀⠀⠀{red}⠸⣿⡿{white}⠀⢸⣿⣿⠃⠀⠀⠀
                                ⠀⠀⠀⠀⠀⠀⠀⠈⢿⣿⣿⣿⣿⡄⠀{red}⠙⠟⠃{white}⠀⠀⠀⠿⠗⡀⠀⠀⠀⠀⠀⣸⣿⠏⠀⠀⠀⠀
                                ⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣿⣿⣿⣷⣄⠀⠀⠀⠀⠀⠈⠚⠓⠁⠀⠀⠀⣠⣴⠟⠁⠀⠀⠀⠀⠀
                                ⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣈⣹⣿⣿⣿⣷⣦⣤⣤⣤⣤⣤⣤⣴⣶⣾⣿⣯⣤⣤⡄⠀⠀⠀⠀⠀
                                ⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣯⣿⡿⠛⠛⣿⣿⣿⣿⣿⠿⣿⣿⣿⣿⡉⢻⡟⠿⡷⠇⠀⠀⠀⠀⠀
                                ⠀⠀⠀⠀⠀⠀⠀⢀⡀⠀⠈⣿⡇⠀⢰⣨⣿⡟⠋⠀⠀⠀⠉⣿⣷⣧⠼⣷⠀⠀⠀⠀⠀⠀⠀⠀
                                ⠀⠀⠀⠀⠀⠀⠀⣽⣿⣿⣿⢿⣌⣀⡼⠛⠟⠃⠀⠀⠀⠀⠀⠈⠉⣿⡴⠟⠀⠀⠀⠀⠀⠀⠀⠀
                                ⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣷⣭⣿⡄⠀⠀⠀⠀⢀⠀⠀⠀⠀⢠⣿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀
                                ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠛⠻⣿⡿⠗⠀⠀⠀⢠⣿⡇⠀⠀⠀⠈⠻⣦⠀⠀⠀⠀⠀⠀⠀⠀⠀
                                ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣄⠀⠀⠀⢀⣸⡟⢷⣤⣀⣀⣀⣤⠟⠀⠀⠀⠀⠀⠀⠀⠀⠀
                                ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠛⠛⠛⠋⠁⠀⠀⠈⠉⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
""",

            2: f"""
                                ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                                ⠀⠀⠀⠀⠀⠀⠀⠀⠀⡤⠤⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠁⣬⡳⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                                ⠀⠀⠀⠀⠀⠀⠀⢠⠊⣰⠀⣦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡎⠀⢳⠈⢺⣦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                                ⠀⠀⠀⠀⠀⠀⢠⡃⡁⡇⠀⠈⠛⢤⡀⠀⠀⠀⠀⠀⣀⣀⣀⣀⡀⠀⠀⢀⠔⠋⠀⠀⢸⢼⡄⠈⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                                ⠀⠀⠀⠀⠀⠀⡏⣀⡏⡇⠀⠀⠉⠢⠈⣖⣉⡉⠉⣹⢧⣀⣀⠤⠬⠭⢹⣋⠀⠀⠀⠀⡜⠈⠹⣄⢹⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                                ⠀⠀⠀⠀⠀⢸⠻⡁⠀⢧⠀⠀⢀⡤⠚⠉⠀⠀⠀⠘⡾⣷⡀⠀⠀⠀⠀⠈⢍⡒⢤⣰⠃⠀⠀⣼⢸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                                ⠀⠀⠀⠀⠀⢸⢶⡃⠀⠈⣦⠞⠁⠀⢠⣮⣤⣴⣾⣿⣷⠹⣿⣿⣷⣿⣿⣶⣦⣷⣄⣈⡳⣄⠀⡬⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                                ⠀⠀⠀⠀⠀⠀⣠⣟⢀⡜⠁⠀⠀⢠⣿⣿⣿⣿⣿⣿⣽⣧⠹⣿⣿⣿⣯⣵⣾⣿⣶⣲⠃⠈⢳⣳⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                                ⠀⠀⠀⠀⠀⣸⠃⢸⠏⠀⠀⠀⢀⣿⣿⣿⠿⡿⢿⠿⠟⠛⢧⠙⢟⠉⠙⠛⠛⢻⠛⠻⡄⠀⢄⠹⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                                ⠀⠀⠀⠀⣰⡏⢀⠏⠀⠀⠀⠀⡜⠁⠀⠀⢠⡇⡜⠀⠀⠀⠀⠳⡌⢻⡀⠀⠀⠈⡆⠀⢸⡀⠈⠆⠹⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                                ⠀⠀⠀⢰⠻⠀⡼⠀⠀⠀⠀⢰⠃⠀⠀⢠⠇⡇⣷⠀⣧⠀⠦⠀⢸⢦⡹⣄⠀⠀⢧⠀⠀⡇⠠⠘⡄⢱⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                                ⠀⠀⠀⢼⡇⢀⠇⠀⠀⠀⠀⢸⠀⠀⣾⣸⠀⡇⡿⡀⣿⡆⠀⠀⢸⡀⣷⢮⣦⡀⢸⡆⠀⢸⠀⠀⢱⡀⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀
                                ⠀⠀⠀⣾⠀⢸⠀⠀⠀⠀⠀⠸⡆⢰⢹⡇⠀⢸⡇⢧⣷⣽⡄⠀⢸⣧⣻⣎⣿⡿⣾⣿⠀⢸⠀⠀⠀⢃⢸⠀⠀⠀⠀⠀⠀⠀⠀⠀
                                ⠀⠀⠀⡍⠀⡇⢀⠀⠀⠀⠀⠀⣷⢼⠬⣧⣀⣈⣷⠘⢧⣹⢿⣄⠈⣏⢻⣞⣿⣷⣼⠿⡷⣦⣀⠀⠀⠘⠌⡆⠀⠀⠀⠀⠀⠀⠀⠀
                                ⠀⠀⠀⡇⠀⡆⠀⣇⠀⠀⠀⠀⡿⣼⠀⠀⠀⠀⠙⣍⠉⠃⠀⠉⠓⠾⣉⣙⣈⣈⠃⠀⣷⠃⠉⠓⡦⣄⡀⣇⠀⠀⠀⠀⠀⠀⠀⠀
                                ⠀⠀⠀⡇⠀⡇⠀⠘⣆⠀⠀⠀⣇{red}⠙⠟⠛⣻⣿⡏⠉{white}⠀⠀⠀⠀⠀{red}⠈⠉⢛⣿⣟⡟⠋{white}⢸⠆⠀⣠⠇⠀⠈⡏⠙⠒⠲⠦⠤⠄⠀⠀
                                ⠀⠀⠀⡇⠀⡷⡀⠀⠘⣆⠀⠀⢹⠀⠀⠀{red}⠙⠛⠃{white}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀{red}⠛⠋⠀{white}⢸⠀⣠⠋⠀⠀⢀⡇⠀⠀⠀⠀⠀⠀⠀⠀
                                ⠀⠀⠀⠃⠀⣧⠱⡄⠀⠈⢧⡀⠘⣇⠀⣴⡶⡢⠾⠂⠀⠀⠀⠀⠀⠀⠀⠺⠊⢴⡷⢴⣏⡴⠃⠀⠀⢠⣾⠁⠀⠀⠀⠀⠀⠀⠀⠀
                                ⠀⠀⠀⢧⠀⢸⡀⠙⢄⠀⠀⠙⢦⣘⣆⠉⠀⠀⠀⠀⠀⠀⠀⠀⠈⠀⠀⠀⠀⠀⢀⢾⡟⠀⠀⠀⡴⠃⡞⠀⠀⠀⠀⠀⠀⠀⠀⠀
                                ⠀⠀⠀⢸⡀⠀⢳⡀⠈⠣⡀⠀⠈⢻⡙⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡼⠀⠀⢠⠞⠀⡼⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀
                                ⠀⠀⠀⢸⢃⠀⠀⠳⣄⠀⠈⢦⡀⠀⢧⣀⠀⠀⠀⠀⠀⠀⠉⠉⠀⠀⠀⠀⢀⡴⣾⠁⢀⡔⠁⢀⢾⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                                ⠀⠀⠀⡇⢸⡆⠀⠀⠈⡷⣦⡀⠙⢄⠘⣿⡝⠲⣤⣀⡀⠀⠀⠀⢀⣠⡴⠚⠁⣷⠇⡰⠋⣀⡴⠋⣸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                                ⠀⠀⡼⣡⢣⢷⠀⠀⢰⠀⡇⠈⠳⣄⠃⢹⣷⡿⠷⣄⣉⡉⠒⣊⡩⠿⣿⠀⠀⡟⣰⠕⣫⣾⠀⠀⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                                ⠀⣴⡵⠁⡜⠘⠀⣀⡦⠴⠥⢤⠤⢾⠳⣜⡏⡷⣤⠶⠤⣍⣷⣣⡤⠴⢻⢳⣶⣧⢣⠾⠖⠛⠒⠤⣼⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                                ⡾⠋⢀⡜⠀⢠⠏⠁⠀⠀⠀⠈⣦⠎⠀⠘⢿⡇⢸⠀⢐⣺⣧⣿⣋⣀⣼⣀⣿⢰⢳⠀⠰⡄⠀⠀⠀⠙⡷⣄⠀⠀⠀⠀⠀⠀⠀⠀
                                ⠀⣠⠎⠀⢠⠇⠀⠀⡄⠀⢀⠔⠃⠀⠀⢠⠟⡇⠈⡏⢡⣾⡿⠿⣿⡍⢹⡏⢹⡇⠈⠣⡀⡇⠀⠀⠀⠀⠘⡄⠉⠒⠒⠒⠢⣤⡶⠞
                                ⠞⠁⠀⠀⡸⠀⠀⠀⢸⣶⠋⢦⣀⣀⣴⡟⠀⢧⠀⡼⠼⣇⠀⠀⢀⠗⠛⣿⠘⣦⣀⠀⠈⢳⣄⠀⠀⠀⠀⢻⢿⣉⠉⠉⠉⠁⠀⠀      
""",

            3: f"""
{white}
                            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣤⣤⣴⠶⠶⠶⠶⠦⣤⣤⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣶⠾⠟⣿⣿⠾⠛⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠙⠻⢶⣤⣠⣤⣤⣄⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⡾⠟⠉⠀⠀⠸⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠛⢷⣀⠈⠙⠻⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⡾⠋⠀⠀⠀⢀⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣧⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣾⠏⠀⠀⠀⠀⢠⡿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⡀⠀⠀⠀⠈⠻⣦⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                            ⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⡟⠁⠀⠀⠀⠀⢀⡿⠁⠀⠀{red}⣰⣶⣦{white}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀{red}⣠⣄{white}⠀⠀⠀⠀⠀⢿⡀⠀⠀⠀⠀⠀⠙⠷⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                            ⠀⠀⠀⠀⠀⠀⣀⣴⠟⠋⠀⠀⠀⠀⠀⠀⣼⠇⠀⠀{red}⠐⣿⣿⡿{white}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀{red}⣴⣿⣿⡇{white}⠀⠀⠀⠀⢸⣇⠀⠀⠀⠀⠀⠀⠀⠈⠙⠳⣦⣄⡀⠀⠀⠀⠀⠀
                            ⠀⠀⠀⣀⣴⠾⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⢿⡇⠉⠁⠉⠈⠉⠀⠀⠀⠀⠀⠀⣠⢤⣀⠀⠀⠀⠀⠀{red}⠉⠿⠿⠁{white}⡀⠀⠀⠀⢸⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠻⢶⣄⠀⠀⠀
                            ⠀⣠⡾⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣷⣄⠤⠠⠐⢀⡀⠀⠀⠀⠀⠀⠋⠁⠉⠁⠀⠀⠀⠀⠀⠄⠀⠀⠀⢁⠀⠀⣼⢿⣦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⣷⡄⠀
                            ⢠⡿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⡟⠻⢶⣤⣴⡾⠷⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣦⣤⠀⠜⣀⣴⠟⠈⢿⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⣷⠀
                            ⣿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⡿⠁⠀⠀⣿⠃⠀⠀⢸⡟⠳⠶⠶⠶⢦⣶⣴⣶⣴⣶⣶⣿⠉⠀⠹⣷⣿⣿⣥⣄⡀⠀⢻⣦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇
                            ⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⠟⠁⠀⠀⠀⢿⣆⣠⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠳⠀⢀⣿⠟⠉⠉⠉⠛⣷⡄⠙⢷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⠇
                            ⠘⢷⣄⡀⠀⠀⠀⠀⠀⠀⢀⣠⣴⠟⠃⠀⠀⠀⠀⠀⠀⣼⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠰⠶⠿⣷⡀⠀⠀⣀⠀⠈⣿⡄⠀⠙⢷⣄⡀⠀⠀⠀⠀⠀⠀⣀⣼⠏⠀
                            ⠀⠀⠉⠛⠷⠶⠶⠶⠶⠾⠛⠋⠁⠀⠀⠀⠀⠀⠀⠀⣸⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣧⣤⣴⠏⠀⠀⣽⡇⠀⠀⠀⠈⠛⠿⠶⠶⠶⠶⠿⠋⠁⠀⠀
                            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⡇⠀⣠⣤⣄⠀⠀⠀⠀⠀⠀⠀⣀⣀⡀⠀⠀⠀⠀⠀⣼⡇⠀⠀⠀⠀⣴⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠹⣷⡾⠋⠀⠁⠀⠀⠀⠀⠀⢀⣾⠛⠉⠙⠓⠀⠀⢀⣴⠟⠛⠿⠾⠿⠛⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣷⠀⠀⠐⢶⣶⣶⣶⣶⣾⣿⡀⠀⠀⢶⡶⠛⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠹⣧⣀⣠⡿⠁⠀⠀⠀⠀⢹⣇⡀⣠⡾⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠁⠀⠀⠀⠀⠀⠀⠀⠙⠛⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
""",

            4: f"""
{white}
                            ⠀⢀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⣤⣄⠀
                            ⢰⣿⣿⣿⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⣿⣿⣿⡇
                            ⠘⢿⣿⣿⣧⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⣾⣿⣿⠛⠋⠀
                            ⠀⠀⠘⣿⣿⣿⣿⣿⣶⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⣶⣿⣿⣿⣿⣿⣿⠀⠀⠀
                            ⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣤⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀
                            ⠀⠀⠀⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣦⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⣿⡇⠀⠀⠀
                            ⠀⠀⠀⢸⣿⣿⣿⣿⣾⣿⣿⣻⣿⣿⣿⣿⣿⣿⣿⠀⠀⣀⣀⣀⣠⣤⣤⣤⣀⣀⣀⡀⢸⣿⣿⣿⣿⣿⣿⣿⢿⣻⣽⣾⣿⣿⣿⠁⠀⠀⠀
                            ⠀⠀⠀⠸⣿⣿⣿⣿⢿⣟⣿⣿⣿⣿⣽⣿⣿⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀
                            ⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣯⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿⣻⣿⣿⡟⠀⠀⠀⠀
                            ⠀⠀⠀⠀⣿⣿⣿⣿⣿⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿⣿⣻⣿⣯⣿⠿⠽⠿⢿⣿⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀
                            ⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣿⣾⣿⣿⣿⣿⡟⠉⠀⠀⠀⠀⠀⠈⢻⣿⣿⣾⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⠿⠁⠀⠀⠀⠀
                            ⠀⠀⠀⠀⠈⠛⠿⠿⣿⣿⣿⣿⣿⣿⣿⣽⣿⣿⣿⣿⢿⣻⣿⠀⣠⣄⠀⠀⠀⣠⣄⠀⣿⣿⣿⡿⣿⣿⣿⣿⣿⣿⣿⡉⠀⠀⠀⠀⠀⠀⠀
                            ⠀⠀⠀⠀⠀⠀⠀⢀⣿⣿⣿⣿⣿⣷⣿⣿⣿⡿⣿⣾⣿⣿⣿⡄⢿⡿⠀⠀⠀⠹⣿⢃⣿⣿⣿⣿⣿⣿⡿⣷⣿⣿⣿⣧⠀⠀⠀⠀⠀⠀⠀
                            ⠀⠀⠀⠀⠀⠀⠀⣸⣿⣿⣿⣿⣯⣿⣿⣿⣷⣿⣿⣿⣿⣿⣿⣿⣶⣤⠀⡖⣶⠠⣴⣿⣿⣿⣿⣟⣿⣷⣿⣿⣿⣿⣿⣿⡀⠀⠀⠀⠀⠀⠀
                            ⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⢿⣿⣿⣽⣿⠿⠛⠋⠉⠙⠛⠻⠿⣿⣿⣿⣿⣿⣿⡿⠟⠛⠉⠉⠛⢿⣿⣿⣿⣽⣿⣿⠄⠀⠀⠀⠀⠀⠀
                            ⠀⠀⠀⠀⠀⠀⠀⢿⣿⣿⣿⣿⣿⣿⣿⠟{red}⢡⣆⡀{white}⠀⠀⠀⠀⠀⠀⠀⠈⠉⠙⠉⠁⠀⠀⠀⠀{red}⣀⣴⡀{white}⠙⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀
                            ⠀⠀⠀⠀⠀⠀⠀⠸⣿⣿⣿⣟⣿⣿⠃⠀{red}⠈⣿⣿⣷⣶{white}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀{red}⢠⣶⣿⣿⣟{white}⠀⠀⢸⣿⣿⣿⡟⠀⠀⠀⠀⠀⠀⠀
                            ⠀⠀⠀⠀⠀⠀⠀⠀⢻⣿⣿⣿⣿⡏⠀⠀⠀{red}⢿⣿⣿⡿{white}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀{red}⠘⣿⣿⣿⡟{white}⠀⠀⢸⣿⣿⡿⠁⠀⠀⠀⠀⠀⠀⠀
                            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠹⣿⣿⣿⣿⠀⠀⠀{red}⠈⠉⠉{white}⠀⠀⠀⠀⠀⠰⣏⣹⡆⠀⠀⠀⠀{red}⠈⠉⠉{white}⠀⠀⢀⣾⣿⠟⠀⠀⠀⠀⠀⠀⠀⠀⠀
                            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠛⢿⣿⣧⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣧⣬⣥⡴⠃⠀⠀⠀⠀⠀⠀⢀⣤⡿⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣤⣄⠀⠈⢙⣻⣷⣶⣤⣤⣀⣀⣀⡴⠚⠛⠛⢿⡛⠛⠳⣄⣤⣤⣶⠾⠛⠉⣠⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⣧⣰⣸⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⠀⠀⠈⡧⠀⠀⣹⣿⣿⣿⣶⣶⣼⣇⠄⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                            ⠀⠀⠀⠀⠀{red}⢠⣤⣄⣀⣈⡉{white}⠁⠀⠀⠈⠉⢉⣽⣿⣿⣿⣿⣿⠷⠀⠀⣠⡼⣧⡄⠀⠉⠙⢿⡿⠿⠟⠋⠉⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                            ⠀⠀⠀⠀⠀{red}⢸⣿⣿⣿⣿⠋{white}⠀⠀⢠⡟⠉⢻⣿⡿⠿⠟⠋⠀⠀⢀⣼⠃⠀⠘⣧⠀⠀⠀⢸⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                            ⠀⠀⠀⠀⠀{red}⢸⣿⣿⣿⣿⣷⣄{white}⠀⠀⣻⡾⠋⠈⠛⠲⠶⠶⠶⠞⠋⠁⠀⠀⠀⠈⠳⠶⣶⠛⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                            ⠀⠀⠀⠀⠀⠀{red}⠁⠈⠻⢿⣿⣿⣿⣿⣿⣇{white}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣼⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀{red}⠈⠉⠉⠉⠀{white}⠹⣦⠀⠀⠀⠀⠀⠀⠀⠀⢀⡄⠀⠠⡴⢻⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⡇⠀⠀⠀⠀⠀⠀⠀⢤⣿⡀⠀⠀⠻⢷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⡆⠀⠀⠀⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⣇⣀⣀⣴⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠛⠶⠶⠶⠶⠶⠶⠖⠛⠉⠉⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
""",
            5:f"""
{white}            
                            ⠀⣀⣤⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⡶⠿⢶⡄
                            ⢸⡏⠀⠉⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢿⣄⠀⣸⡇
                            ⠈⠷⣤⣼⣯⣤⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣴⠶⠛⣿⠙⠉⠀
                            ⠀⠀⠀⢸⡇⠀⠉⠛⠳⢦⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣴⠾⠛⠉⠀⠀⠀⣿⠀⠀⠀
                            ⠀⠀⠀⢸⣧⠀⠀⠀⠀⠀⠈⠉⠛⠶⣤⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⡴⠞⠋⠉⠀⠀⠀⠀⠀⠀⠀⡟⠀⠀⠀
                            ⠀⠀⠀⠈⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠙⠳⣦⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⠞⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇⠀⠀⠀
                            ⠀⠀⠀⠀⢹⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇⠀⠀⠀
                            ⠀⠀⠀⠀⢸⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣸⣦⡤⠶⠖⠛⠛⠛⠛⠛⠙⠛⠛⠛⠒⠶⠾⣧⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⠁⠀⠀⠀
                            ⠀⠀⠀⠀⠈⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⠶⠛⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠛⠷⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀⣿⠀⠀⠀⠀
                            ⠀⠀⠀⠀⠀⣿⠀⠀⠀⠀⠀⠀⠀⣠⡾⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣶⡀⠀⠀⠀⠀⠀⠀⣿⠀⠀⠀⠀
                            ⠀⠀⠀⠀⠀⢻⡀⠀⠀⠀⠀⢀⣾⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⠶⠶⠲⠶⢦⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣦⠀⠀⠀⠀⢰⡇⠀⠀⠀⠀
                            ⠀⠀⠀⠀⠀⠸⣧⣀⡀⠀⣠⡟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⠟⢁⠀⠀⠀⠀⠀⠈⠻⣦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⣷⡤⠶⠞⠛⠁⠀⠀⠀⠀
                            ⠀⠀⠀⠀⠀⠀⠀⠉⠉⣹⠟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣏⠀⣾⡆⠀⠀⠀⢰⣦⠀⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣷⠀⠀⠀⠀⠀⠀⠀⠀
                            ⠀⠀⠀⠀⠀⠀⠀⠀⢠⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢿⣄⠿⠃⠀⠀⠀⠘⢛⣰⠟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡆⠀⠀⠀⠀⠀⠀⠀
                            ⠀⠀⠀⠀⠀⠀⠀⠀⣾⠁⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⡶⠶⣤⣄⡙⢳⣦⣶⣶⣶⣶⢛⣡⣤⠶⠶⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⠀⠀⠀⠀⠀⠀⠀
                            ⠀⠀⠀⠀⠀⠀⠀⠀⣿⠀⠀⠀⠀⠀⠀⢀⣴⢟⠋⠀⠀⠀⠀⠈⠙⠛⠶⣬⣭⠿⠟⠋⠉⠀⠀⠀⠀⠙⢷⣄⠀⠀⠀⠀⠀⠀⠀⣿⠀⠀⠀⠀⠀⠀⠀
                            ⠀⠀⠀⠀⠀⠀⠀⠀⣿⠀⠀⠀⠀⠀⣰⡟⠁{red}⣼⣷⣤⡀{white}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀{red}⣀⣴⣿⡿{white}⣧⠀⠀⠀⠀⠀⢀⡟⠀⠀⠀⠀⠀⠀⠀
                            ⠀⠀⠀⠀⠀⠀⠀⠀⢹⡆⠀⠀⠀⢰⡟⠀⠀{red}⢩⣿⣿⣿⣷{white}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀{red}⢰⣿⣿⣿⡏{white}⠀⠘⣧⠀⠀⠀⠀⣼⠃⠀⠀⠀⠀⠀⠀⠀
                            ⠀⠀⠀⠀⠀⠀⠀⠀⠈⢿⡄⠀⠀⢸⠁⠀⠀{red}⠸⣿⣿⣿⡏{white}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀{red}⢸⣿⣿⣿⡇{white}⠀⠀⣿⠀⠀⠀⣼⠏⠀⠀⠀⠀⠀⠀⠀⠀
                            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢻⣄⠀⢸⣇⠀⠀⠀{red}⠙⠛⠋{white}⠀⠀⠀⠀⠀⢰⣟⢙⣷⡄⠀⠀⠀⠀{red}⠙⠻⠛{white}⠀⠀⠀⡿⠀⣠⡾⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀
                            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠻⣦⣻⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣄⠩⠏⢁⣰⠀⠀⠀⠀⠀⠀⠀⠀⢀⣼⣣⠾⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢛⣷⣦⣄⣀⠀⢀⣠⡴⠶⣤⣍⠛⢛⣻⣥⣤⣄⡀⠀⢀⣀⣤⣶⠿⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⠀⣠⡴⠟⠉⠀⠈⠉⠛⣿⠁⠀⠀⠀⠙⣷⡟⠁⠀⠀⠈⢻⡞⠋⠉⠉⠻⢶⣄⠀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣟⠉⣻⡿⠶⠶⠶⢶⡤⠤⠤⢿⣄⠀⠀⠀⣠⡿⣧⡀⠀⠀⢀⣼⠧⠤⢤⣤⠤⠤⣽⣿⢉⢹⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠛⠛⠛⠀⠀⠀⠀⠘⣷⣄⠀⠀⠙⠃⠀⣺⡿⠀⠹⣟⡂⠀⠉⠁⠀⢀⣼⠏⠀⠀⠀⠙⠛⠛⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⠛⠶⠶⠶⡚⢋⡀⠀⠀⠉⣛⠶⠶⠶⠶⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
            """,
            6: f"""
{white}
                            ⠀⠀⠀⠀⠀⠀⠀⠀⣀⡤⠞⠉⣁⣤⢤⣼⣷⣴⣶⡄⠀⠀⠀⠀⠀⠀⠉⠛⢦⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                            ⠀⠀⠀⠀⠀⠀⢠⡾⣋⡤⢖⣾⣿⣿⡿⣿⡿⣿⡍⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠳⡈⠳⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                            ⠀⠀⠀⠀⠀⡰⠋⢰⣷⢿⣿⣿⣿⣾⡗⡿⣿⣿⣷⣶⣦⣤⣤⡀⠀⠀⠀⠀⠀⠀⢳⠀⠈⢧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                            ⠀⠀⠀⠀⣰⡇⠀⠀⣁⣸⣿⢿⣿⠵⠟⠙⠛⠋⠉⠉⠉⠛⠛⠛⠀⠀⠀⠀⠀⠀⠈⣇⠀⠀⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                            ⠀⠀⠀⢠⣿⠁⣠⢴⣯⡟⠛⣉⡤⠤⠐⠒⠒⠒⠒⠂⠤⠤⢤⣄⣀⡀⠀⠀⠀⠀⠀⢸⠀⠀⠸⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                            ⠀⠀⠀⢸⣿⡆⢹⡼⠁⣠⠞⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠑⠒⠤⣄⠀⠀⡄⠀⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                            ⠀⠀⠀⠘⣿⡇⠀⣠⠞⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠽⠓⣃⣀⣀⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                            ⠀⠀⠀⠀⣿⣧⠞⠁⠀⠤⠒⣋⣩⣭⣭⣭⣍⣀⣀⠠⠤⣀⡀⠀⠀⠀⠀⠔⢋⣥⣶⣿⣿⣿⣿⣿⡙⠒⠤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                            ⠀⠀⠀⠀⢹⡏⢠⠄⣠⣴⣿⣿⣿⣿⣿⡇⠙⣿⣿⣿⣷⣶⣭⣝⣂⣀⣤⣴⣿⣿⣿⠻⣿⣿⣿⠋⠁⠀⠀⠘⣷⢄⠀⠀⠀⠀⠀⠀⠀
                            ⠀⠀⠀⠀⢸⣿⢋⣼⣿⣿⣿⣿⣿⣿⡿⡇⠀⣿⣿⣿⣿⣿⣿⠟⠟⠛⢿⣿⣿⣿⣿⡴⣿⣿⣟⣀⡤⠐⠒⠚⠋⠛⠓⢄⡀⠀⠀⠀⠀
                            ⠀⠀⠀⠀⢸⣿⣾⣿⣿⣿⣿⣿⣿⢿⡗⡿⠃⢸⠃⠈⠀⠈⣿⣷⣶⣾⣿⠏⣿⣿⣿⣼⣿⣿⡟⠁⠀⠀⠀⠀⠀⠀⠀⠀⢳⡀⠀⠀⠀
                            ⠀⠀⠀⠀⢸⣿⢻⡿⢿⣿⣿⣿⣿⣼⣷⣾⡶⠸⠧⠒⠂⠴⠹⠊⠈⠁⠐⠃⣿⣿⣿⣿⣿⣿⢀⣀⣀⡤⠀⠀⠀⠀⠀⠀⠀⢳⠀⠀⠀
                            ⠀⠀⠀⣠⡾⢥⠤⠓⠚⠛⠿⣿⡝⡛⠋⣙⠀⠀⠀⡄⠀⠀⠀⠀⠀⠀⠀⢀⣿⣿⣿⣿⣿⡿⠟⠋⠉⠀⠀⠀⠀⠀⠀⠀⠀⠘⡄⠀⠀
                            ⠀⠀⢀⠜⡶⠉⠀⠀⠀⠀⠀⢀⣽⠿⠛⠉⠙⠒⠺⠥⣠⡀⠀⠀⠀⠀⡐⢋⣿⣿⣿⣿⣧⣤⡤⠖⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇⠀⠀
                            ⠀⠀⡾⠋⡄⠀⠀⠀⠀⠀⣰⣟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠉⠑⠒⠤⢮⣼⡞⣿⣿⣿⣿⣿⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣷⠀⠀
                            ⠀⠀⣧⠞⠀⠀⠀⠀⠀⢀⣿⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠛⠻⣮⡙⢳⣄⡀⠀⠀⠀⠀⠀⠀⠀⣀⣤⣴⣾⣿⠀⠀
                            ⠀⠀⣧⠶⠛⠛⠛⠛⠿⣿⣿⣿⣿⣷⣦⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠹⣧⢸⠛⢿⡆⠀⠀⠀⠀⢠⣾⣿⣿⣿⣿⣿⠀⠀
                            ⠀⣸⠁⠀⠀⠀⠀⠀⠀⠚⣿⣿⣿⣿⣿⣿⣟⡛⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣹⠀⠀⠀⠀⠀⠀⣤⣿⣿⣿⣿⣿⣿⣿⠀⠀
                            ⢠⡇⠀⠀⠀⠀⠀⠀⠀⠀⢿⣿⣿⣿⣿⣿⣿⣿⣶⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠛⠀⠀⠀⠀⢀⣼⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀
                            ⡏⡀⠀⢀⣀⣀⣀⣠⣤⣤⣤⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣦⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀
                            ⠻⣄⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⠛⠛⠛⠉⠛⠿⣷⣶⣦⣦⣤⣄⡀⠀⠀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡀⠀
                            ⠀⠙⣿⣿⣿⣿⣿⣿⣿⣿⠿⠟⠛⠋⢩⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⡿⠻⠿⣿⣿⣷⡿⠋⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀
                            ⠀⠀⠀⠙⠛⢻⠉⠉⠀⠀⠀⠀⠀⠀⢸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇⠀⠀⠀⠈⠉⠀⠀⠈⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀
                            ⠀⠀⠀⠀⠀⣇⣀⠀⠀⠀⠀⠀⠀⠀⢸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄
                            ⠀⠀⠀⠀⢰⠅⠈⠑⠀⠀⠀⠀⠀⠀⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡼⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧

            """,
            7: f"""
{white}
                                ⠀⠀⠀⠀⠀⣀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⡢⡀⠀⠀⠀⠀
                                ⠀⠀⠀⢄⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⠀⠀⠀⠀
                                ⠀⠀⢰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠀⠀⠀
                                ⠀⢨⣿⡿⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⠀⠀
                                ⠀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢀⠀
                                ⢈⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⠀
                                ⠸⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⡇⠀⢸⢹⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⡧⠀
                                ⠈⣿⣿⣿⣿⠧⠯⠟⠿⠧⠀⠀⠀⠸⠿⠿⢼⣿⠿⢿⣟⣿⣿⣿⣿⣿⣇⠀
                                ⠀⣿⣿⣿⣿⡿{red}⢰⠺⣿⠉⠂{white}⠀⠀⠀⠀⠀⠀{red}⠚⣷⣶⠢⡀{white}⢿⣿⣿⣿⡿⠉⠀
                                ⢐⢻⣿⣏⠙⠇{red}⠈⠒⠉⠁{white}⠀⠀⠀⠀⠀⠀⠀⠀{red}⠝⠻⠥⠁{white}⢰⡌⠹⠋⡀⡀⠀
                                ⠀⠉⢻⣿⣿⣦⡀⠐⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠆⠄⠸⢃⣰⡀⠱⠀⠀
                                ⠀⠀⠀⢹⣿⣿⡄⠀⠀⠀⠀⠀⠀⡀⡀⠀⠀⠀⠀⠀⠀⢀⣶⣿⣿⡟⠁⠀⠀
                                ⠀⠀⠘⣸⢿⣿⣿⣦⡀⠀⠀⠀⠀⠠⠄⠀⠀⠀⠀⠀⣠⣾⣿⣿⣿⣇⠀⠀⠀
                                ⠀⠀⠀⠉⠞⠿⠛⠿⠿⢶⣄⠀⠀⠀⠀⠀⠀⠀⣠⡾⠿⠿⣿⣿⡿⠅⠀⠀⠀
                                ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣿⣿⣶⣤⣤⣤⡴⠊⠀⡧⠀⠀⣿⣿⣇⠀⠀⠀⠀
                                ⠀⠀⠀⠀⠀⠀⠀⠀⣀⡞⠛⠿⣿⣿⠟⠋⠀⠀⠀⠱⣀⠈⣿⣿⡁⠀⠀⠀⠀
                                ⠀⠀⠀⠀⠀⢠⡠⠔⠋⠀⠀⠀⠈⠁⠀⠀⠀⠀⠀⠀⠙⠲⣿⣧⠀⠀⠀⠀⠀
                                ⢀⠔⠒⠀⠉⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡿⠀⠉⠚⠤⢔
            """

        }

        self.commands = {
            1: """
                            1.  [>.<] gcfill                    - Fills group chat with tokens
                            2.  [>.<] autofill                  - Fills group chat with tokens automatically
                            3.  [>.<] gcleaveall                - Leave all group chats with tokens
                            4.  [>.<] gcleave                   - Leave the group chat with tokens
                            5.  [>.<] antigc                    - Group chat spam protection
                            6.  [>.<] userinfo                  - Get user information
                            7.  [>.<] autoreact                 - Autoreact to a user's message
                            8.  [>.<] autoreactoff              - Stop autoreacting to a user's message
                            9.  [>.<] autotrap toggle <user>    - Prevent a user from leaving
                            10. [>.<] autotrapoff               - Stop preventing a user from leaving
                            11. [>.<] dreact                    - Rotate react on messages
                            12. [>.<] dreactoff                 - Stop rotating react on messages
""",
            2: """
                            13. [>.<] rstatus <amount>          - Rotate status
                            14. [>.<] stopstatus                - Stop rotating status
                            15. [>.<] remoji <type> <text>      - Rotate emoji status
                            16. [>.<] stopemoji                 - Stop rotating emoji status
                            17. [>.<] setname <name>            - Change global name
                            18. [>.<] stream <text>             - Set streaming status
                            19. [>.<] streamoff                 - Stop streaming status
                            20. [>.<] setbio <text>             - Customize bio
                            21. [>.<] setpronoun <text>         - Customize pronouns
                            22. [>.<] setpfp <link>             - Customize profile picture
                            23. [>.<] setbanner <link>          - Customize banner
                            24. [>.<] stealbio <user>           - Steal bio
                            25. [>.<] stealpronoun <user>       - Steal pronouns
                            26. [>.<] stealpfp <user>           - Steal profile picture
                            27. [>.<] stealbanner <user>        - Steal banner


""",
            3: """
                            28. [>.<] ar <user>                 - Auto reply to user
                            29. [>.<] arstop                    - Stop auto reply
                            30. [>.<] mimic <user>              - Show deleted messages
                            31. [>.<] mpurge <amount>           - Purge your messages
                            32. [>.<] avatar <user>             - Get user's avatar 
                            33. [>.<] banner <user>             - Get user's banner
""",
            4: """
                            34. [>.<] minicord prefix <text>        - Set start message addon
                            35. [>.<] minicord suffix <text>        - Set end message addon
                            36. [>.<] minicord delay <seconds>      - Set message delay
                            37. [>.<] minicord mirror               - Start mirroring messages
                            38. [>.<] minicord stop                 - End session
                            39. [>.<] minicord clear                - Clear console

""",
            5: """
                            40. [>.<] nuke message              - Set webhook spam message
                            41. [>.<] nuke name                 - Set server name
                            42. [>.<] nuke delay                - Set webhook spam delay
                            43. [>.<] nuke channels             - Set number of channels
                            44. [>.<] nuke roles                - Set number of roles
                            45. [>.<] nuke webhooks             - Set webhooks per channel
                            46. [>.<] nuke reset                - Reset all settings
                            47. [>.<] nuke start                - Start nuking
                            48. [>.<] nuke stop                 - Stop webhook spam
""",

            6: """
                            49. [>.<] gcname start <user>       - Start GC name changer
                            50. [>.<] gcname stop               - Stop GC name changer
                            51. [>.<] gcname add <msg>          - Add new name message
                            52. [>.<] gcname remove <id>        - Remove name message
                            53. [>.<] gcname list               - List all messages
                            54. [>.<] gcname delay <sec>        - Set change delay
                            55. [>.<] gcname counter            - Toggle counter
                            56. [>.<] gcname random             - Toggle random order
                            57. [>.<] gcname reset              - Reset settings
""",
            7: """
                            58. [>.<] autopress <user>         - Start autopressing user
                            59. [>.<] autopress add <msg>      - Add autopress message
                            60. [>.<] autopress remove <id>    - Remove message by ID
                            61. [>.<] autopress list           - List all messages
                            62. [>.<] autopress clear          - Clear all messages
                            63. [>.<] autopress stop           - Stop autopressing
                            64. [>.<] autopress delay <min>    - Set delay range

""", 
            8: """                            
                            65. [>.<] ladder                    - Start ladder spam              
                            66. [>.<] ladder stop               - Stop ladder spam               
                            67. [>.<] ladder add <msg>          - Add new ladder message         
                            68. [>.<] ladder remove <msg>       - Remove a ladder message        
                            69. [>.<] ladder list               - List all ladder messages       
                            70. [>.<] ladder delay <sec>        - Set message delay              
                            71. [>.<] ladder reset              - Reset to default messages      
                            72. [>.<] ladder clear              - Clear all messages       
""",

            9: """
                            73. [>.<] dmsnipe log <url>         - Set webhook URL                
                            74. [>.<] dmsnipe toggle            - Toggle dmsnipe on/off         
                            75. [>.<] dmsnipe edit              - Toggle edit snipe on/off      
                            76. [>.<] dmsnipe ignore <user/id>  - Ignore user/channel           
                            77. [>.<] dmsnipe clear             - Clear ignore lists      
                            78. [>.<] msgtime <min> <msg> on    - Start messaging    
                            79. [>.<] msgtime off               - Stop messaging     
                            80. [>.<] msgtime status            - Check status       
                            81. [>.<] msgtime list              - List messages      
                            82. [>.<] msgtime clear             - Clear messages     
                            83. [>.<] msgtime remove <num>      - Remove message    
            """
            
        }

    def get_page_content(self, page_num, total_pages):
        ascii_art = self.ascii_art.get(page_num, "")
        commands = self.commands.get(page_num, "")
        
        server_count = len(self.bot.guilds)
        friend_count = len([f for f in self.bot.user.friends]) if hasattr(self.bot.user, 'friends') else 0
        
        
        return f"""```ansi
{ascii_art}

{commands}

                                         {www}Page {page_num}/{total_pages} - Type {red}p#{www} to navigate.                 
                            Welcome [ {red}{self.bot.user}{www} ]        Servers: [ {red}{server_count}{www} ]        Friends: [ {red}{friend_count}{www} ]

Vulnerable SB              Options: {red}close{www} to exit, {red}reset{www} to return to first page      [ Made by {red}@mwpv{www} ]
```"""

    @commands.command()
    async def help(self, ctx):
        total_pages = len(self.pages)
        user_id = ctx.author.id
        
        self.current_page[user_id] = 1
        
        help_msg = await ctx.send(self.get_page_content(1, 8))
        self.pages[user_id] = help_msg

        def check(m):
            return m.author.id == ctx.author.id and (
                m.content.lower() in ['close', 'reset'] or 
                m.content.lower().startswith('p')
            )

        while True:
            try:
                msg = await self.bot.wait_for('message', timeout=120.0, check=check)
                
                if msg.content.lower() == 'close':
                    await help_msg.delete()
                    await msg.delete()
                    break
                    
                elif msg.content.lower() == 'reset':
                    self.current_page[user_id] = 1
                    await help_msg.edit(content=self.get_page_content(1, 8))
                    await msg.delete()
                    
                elif msg.content.lower().startswith('p'):
                    try:
                        page_num = int(msg.content[1:])
                        if 1 <= page_num <= 8:
                            self.current_page[user_id] = page_num
                            await help_msg.edit(content=self.get_page_content(page_num, 8))
                    except ValueError:
                        pass
                    await msg.delete()

            except asyncio.TimeoutError:
                await help_msg.delete()
                break

def setup(bot):
    bot.add_cog(HelpCommand(bot))
