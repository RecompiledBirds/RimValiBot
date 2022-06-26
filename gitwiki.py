import git
import discord
import os
import discord.ext
from discord.ext import commands
import data
import json
import shutil
import asyncio
from discord.ext.commands import has_permissions, CheckFailure, check
import glob


def getArticleSections(path: str):
    sections = {}

    with open(path, 'r') as file:
        lastSection = ""
        print(path)
        lines = file.readlines()
        for line in lines:
            if(line.startswith("#")):
                lastSection = line
                sections[lastSection] = []
            else:
                if(len(sections) == 0):
                    sections[lastSection] = []
                sections[lastSection].append(line)
    return sections


class GitWiki(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        if not os.path.exists(data.gitWikiConfigFile):
            with open(data.gitWikiConfigFile, "w") as file:
                json.dump({}, file)

    @commands.command(name="attachToWiki")
    @has_permissions(administrator=True)
    async def attachToWiki(self, ctx: commands.Context, repoURL: str) -> None:

        path = f"{data.directory}/gits/{ctx.guild.id}"
        if(os.path.exists(path)):
            shutil.rmtree(path)
        await ctx.send(f"Attempting to attach to: {repoURL}")
        async with ctx.typing():
            git.Repo.clone_from(f"{repoURL}.wiki.git", path)
            dict = {}
            with open(data.gitWikiConfigFile, "r") as file:
                dict = json.load(file)
            with open(data.gitWikiConfigFile, "w") as file:
                dict[f"{ctx.guild.id}"] = path
                json.dump(dict, file)
            await ctx.send(f"Downloading {repoURL}.")
            # give the bot a moment
            await asyncio.sleep(30)
            print(f"Downloaded: {repoURL} to {path}")
            shutil.rmtree(f"{path}/.git")

    @commands.command(name="readarticle")
    async def readarticle(self, ctx: commands.Context, article: str) -> None:
        dict = {}
        with open(data.gitWikiConfigFile, "r") as file:
            dict = json.load(file)
        id = str(ctx.guild.id)
        if id not in dict:
            return

        path = f"{dict[id]}/{article}"

        if not path.endswith(".md"):
            path = f"{path}.md"
        print(f"Reading from {path}..")
        sections = getArticleSections(path)
        for section in sections:
            message = section
            for line in sections[section]:
                if(len(f"{message}\n{line}") >= 2000):
                    print(line)
                if(len(f"{message}\n{line}") >= 2000 or sections[section].index(line) == len(sections[section]) - 1):
                    if sections[section].index(
                            line) == len(sections[section]) - 1:
                        message = f"{message}\n{line}"
                    await ctx.send(message)

                else:
                    message = f"{message}\n{line}"

    @commands.command(name="getarticles")
    async def getarticles(self, ctx: commands.Context) -> None:
        async with ctx.typing():
            dict = {}
            with open(data.gitWikiConfigFile, "r") as file:
                dict = json.load(file)
            id = str(ctx.guild.id)
            if id not in dict:
                return

            path = dict[id]
            # dont need dict anymore, so just want to be sure it's done with.
            dict = {}
            files = glob.glob(f"{path}/*.md")
            message = "Articles:"
            for fp in files:
                print(files.index(fp), len(files) - 1)
                newstr = fp.replace(path, '')
                newstr = newstr[1:len(newstr) - 3]
                if len(
                        f"{message}\n-{newstr}") >= 2000 or files.index(fp) == len(files) - 1:
                    if files.index(fp) == len(files) - 1:
                        message = f"{message}\n-{newstr}"
                    await ctx.send(message)
                    message = "Articles:"
                else:
                    message = f"{message}\n-{newstr}"


async def setup(bot):
    await bot.add_cog(GitWiki(bot))
