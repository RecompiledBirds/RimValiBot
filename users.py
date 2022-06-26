import discord
import time
import discord.ext
from discord.utils import get
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions,  CheckFailure, check
import os
import data
import json


class Users(commands.Cog, name="User information"):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def whois(self, ctx, member: discord.Member):
        id = str(member.id)
        mname = member.name
        creationDate = member.created_at.strftime("%b %d, %Y")
        pfp = member.avatar_url

        embed = discord.Embed(title=mname)
        embed.set_image(url=pfp)
        embed.add_field(name=f"ID: {id}", value="** **", inline=True)
        embed.add_field(
            name=f"Joined on: {creationDate}", value="** **", inline=True)
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Users(bot))
