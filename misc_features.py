from discord.ext import commands
import discord
import data
import random
import asyncio


class MiscFeatures(commands.Cog):
  #cant change status in init?
  #this is hacky but it works
  tick=200
  def __init__(self, bot:commands.Bot)->None:
    self.bot = bot
    super().__init__()
    

  @commands.Cog.listener()
  async def on_message(self,ctx)->None:
    if(self.tick>=random.randint(90,120)):
      choice = random.choice(data.status_messages)
      activity=discord.Game(choice)
      await self.bot.change_presence(status=discord.Status.online,activity=activity)
    
    await asyncio.sleep(20)
    self.tick=self.tick+1

async def setup(bot:commands.Bot)->None:
  await bot.add_cog(MiscFeatures(bot))