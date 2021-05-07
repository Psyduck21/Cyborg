from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import datetime
import time
import keyboard
import discord
from discord.ext import commands
import dhooks
from dhooks import Webhook, Embed

class zoom(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        meeting_link = "https://us04web.zoom.us/j/79830005057?pwd=T0M3UjNpamxQWmdwMkR4K3VUVG5YUT09"
    @commands.command()
    async def _join(self, ctx, meeting_link:str):
            self.bot = webdriver.Chrome("D:/Discord Stuff/bots/cyborg/Zoom_meeting stuff/chromedriver.exe")
            self.bot.get(meeting_link)
            time.sleep(3)
            keyboard.send("tab", do_press=True, do_release=True)
            keyboard.send("tab", do_press=True, do_release=True)
            keyboard.send("enter", do_press=True, do_release=True)
            time.sleep(3)

            self.bot.quit()

            hook = Webhook(
            "https://discord.com/api/webhooks/774299510683467807/Hiqq9wY5-537P4Vi11WBz6zgwwDNdMkMRqnWfetuPYsscIc43PkMbgPR6FZHOGgoCYBM")
            embed = Embed(description='I have joined 11am class . :sunglasses:',
                        color=0x5cdbf0,
                        timestamp='now')
            hook.send(embed=embed)
        
            

def setup(bot):
    bot.add_cog(zoom(bot))
    print("zoom bot added")
