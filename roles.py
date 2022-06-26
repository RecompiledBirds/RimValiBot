import discord
import time
import discord.ext
from discord.utils import get
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions,  CheckFailure, check
import os
import data
import json

class ReactionRoleModule(commands.Cog,name="Reaction roles"):
  def __init__(self, bot):
    self.bot = bot
    self.name="Reaction roles"
    if not os.path.exists(data.jsonFile):
      with open(data.jsonFile,"w") as file:
        emptyData={}
        json.dump(emptyData,file)

  @commands.Cog.listener()
  async def on_raw_reaction_add(self,payload):
    guild = self.bot.get_guild(payload.guild_id)
    id=str(payload.message_id)
    user=payload.user_id
    emoji=payload.emoji
    server=str(payload.guild_id)
    channel=guild.get_channel(payload.channel_id).name
    dict={}
    wantedID=""
    with open(data.jsonFile,'r') as file:
      dict=json.load(file)
    if (server not in dict):
      return
    if channel in dict[server]:
      if not id in dict[server][channel]:
        return
      if not emoji.name in dict[server][channel][id]:
        return
      wantedID=dict[server][channel][id][emoji.name]
    else:
      if not "none" in dict[server]:
        return
      if not id in dict[server]["none"]:
        return
      if not emoji.name in dict[server]["none"][id]:
        return
      wantedID=dict[server]["none"][id][emoji.name]
    role = discord.utils.get(guild.roles,name=wantedID)
    member=self.bot.get_guild(payload.guild_id).get_member(user)
    print(wantedID)
    await member.add_roles(role)


  @commands.Cog.listener()
  async def on_raw_reaction_remove(self,payload):
    guild = self.bot.get_guild(payload.guild_id)
    id=str(payload.message_id)
    user=payload.user_id
    emoji=payload.emoji
    server=str(payload.guild_id)
    channel=guild.get_channel(payload.channel_id).name
    dict={}
    wantedID=""
    with open(data.jsonFile,'r') as file:
      dict=json.load(file)
    if (server not in dict):
      return
    if channel in dict[server]:
      if not dict[server][channel][id]:
        return
      if not emoji.name in dict[server][channel][id]:
        return
      wantedID=dict[server][channel][id][emoji.name]
    else:
      if not "none" in dict[server]:
        return
      if not id in dict[server]["none"]:
        return
      if not emoji.name in dict[server]["none"][id]:
        return
      wantedID=dict[server]["none"][id][emoji.name]
    role = discord.utils.get(guild.roles,name=wantedID)
    member=self.bot.get_guild(payload.guild_id).get_member(user)
    await member.remove_roles(role)

    
  @commands.command(name="addReactionRole")
  @has_permissions(administrator=True)
  async def AddRoleMessage(self,ctx, role: discord.Role, messageID: str, emoji: discord.PartialEmoji, channelName="none"):
  	rn=role.name
  	en=emoji.name
  	server=str(ctx.guild.id)
  	dict={}
  	with open(data.jsonFile,'r') as file:
      		dict=json.load(file)
  	print(dict)
  	if (server not in dict):
  		dict[server]={}
  	if channelName not in dict[server]:
  		dict[server][channelName]={}
  	if (messageID not in dict[server][channelName]):
  		dict[server][channelName][messageID]={}
  	
  	dict[server][channelName][messageID][en]=rn
  	
  	with open(data.jsonFile,'w') as file:
      		json.dump(dict,file)
  	await ctx.send(f"Added reaction role {rn} with reaction :{en}: to message!")
  	if channelName == "none":
  		msg= await ctx.channel.fetch_message(messageID)
  		await msg.add_reaction(emoji)
  	else:
  		chnl = discord.utils.get(ctx.guild.channels, name=channelName)
  		msg= await chnl.fetch_message(messageID)
  		await msg.add_reaction(emoji)


  @commands.command(name="removeReactionRole")
  @has_permissions(administrator=True)
  async def RemoveRoleMessage(self,ctx, messageID: str, emoji: discord.PartialEmoji,channelName="none"):
  	dict={}
  	server=str(ctx.guild.id)
  	with open(data.jsonFile,'r') as file:
  		dict=json.load(file)
  	if server not in dict:
  		return
  	if messageID not in dict[server][channelName]:
  		return
  	if emoji.name not in dict[server][channelName][messageID]:
  		return 
  	
  	del dict[server][channelName][messageID][emoji.name]
  	with open(data.jsonFile,'w') as file:
  		json.dump(dict,file)
  	if channelName == "none":
  		msg= await ctx.channel.fetch_message(messageID)
  		await msg.remove_reaction(emoji,self.bot.user)
  	else:
  		chnl = discord.utils.get(ctx.guild.channels, name=channelName)
  		msg= await chnl.fetch_message(messageID)
  		await msg.remove_reaction(emoji,self.bot.user)
  	await ctx.send("Removed reaction role!")


async def setup(bot):
  await bot.add_cog(ReactionRoleModule(bot))