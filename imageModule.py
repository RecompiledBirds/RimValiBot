from discord.ext import commands
import discord
import data
import json
import random
import os

def UploadImage(ctx,author,title,url,link):
    images={}
    with open(data.imageDataFile, "r") as file:
      images = json.load(file)

    if not f"{author}{title}" in images:
      images[f"{author}{title}" ]={}
    images[f"{author}{title}" ]={
      "athrURL":link,
      "imgURL":url,
      "author":author,
      "title":title,
      "userThatAddedID":str(ctx.message.author.id),
      "userThatAdded":ctx.message.author.name
    }
    with open(data.imageDataFile,"w") as file:
        json.dump(images,file)




      
class ImageModule(commands.Cog, name="Avali Images"):
  def __init__(self, bot:commands.Bot)->None:
    self.bot = bot
    if not os.path.exists(data.imageDataFile):
      with open(data.imageDataFile,"w") as file:
        emptyData={}
        json.dump(emptyData,file)
    super().__init__()

  

  @commands.hybrid_command(name="avali",description="Get a avali image!")
  async def getImage(self,ctx: commands.Context)->None:
    images={}
    with open(data.imageDataFile, "r") as file:
      images = json.load(file)
    if(len(images)==0):
      ctx.send("I have no avali right now. :(")
      return
    imageToUse = random.choice(tuple(images))
    color=random.choice(tuple(data.colors))
    embed=discord.Embed(title=f"{images[imageToUse]['title']} by {images[imageToUse]['author']}",url=images[imageToUse]['athrURL'],color=data.colors[color])
    embed.set_image(url=images[imageToUse]['imgURL'])
    await ctx.send(embed=embed)

  @commands.hybrid_command(name="avalicount")
  async def avalicount(self,ctx: commands.Context)->None:
    images={}
    with open(data.imageDataFile, "r") as file:
      images = json.load(file)
    count=len(images)
    await ctx.send(f"I have {count} avali!")
  @commands.hybrid_command(name="addimage",description="Add an avali to my database!")
  async def addImage(self, ctx:commands.Context, author: str, title: str, link: str)->None:
    if(len(ctx.message.attachments)==0):
      embed = discord.Embed(title="Image not found",description="I cannot find an attached image..", color=data.colors['RED'])
      await ctx.send(embed=embed)
      return
    file_url = ctx.message.attachments[0].url
    UploadImage(ctx,author,title,file_url,link)
    embed = discord.Embed(title="Image uploaded",description="I have added this image to my database.", color=data.colors['GREEN'])
    await ctx.send(embed=embed)
async def setup(bot:commands.Bot)->None:
  await bot.add_cog(ImageModule(bot))