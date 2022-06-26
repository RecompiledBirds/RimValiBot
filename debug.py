from discord.ext import commands
import discord
import data
import json
import os
import discord.ui as dui


class Debugger(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        if not os.path.exists(data.cogFile):
            with open(data.cogFile, "w") as file:
                emptyData = {}
                json.dump(emptyData, file)
        super().__init__()

    @commands.hybrid_command(name="test")
    async def Test(self, ctx: commands.Context) -> None:
        button = dui.Button(label="I'm a button!",
                            style=discord.ButtonStyle.green)

        async def button_callback(interaction: discord.Interaction):
            await interaction.response.send_message("Button pressed!")
        button.callback = button_callback
        view = dui.View()
        view.add_item(button)
        await ctx.send("hello world", view=view)

    @commands.hybrid_command(name="whatami")
    async def WhatAmI(self, ctx: commands.Context) -> None:
        embed = discord.Embed(
            title="Hey!",
            description=" I'm RimVali, a avali-themed bot. If you're curious about how I work, you can find my source code here: https://replit.com/@NeziThe/RimVali#main.py")
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="addcog")
    @commands.is_owner()
    async def AddCog(self, ctx: commands.Context, cog: str) -> None:
        downloaded = "local"
        path = "{dir}/{cogName}.py".format(dir=data.directory, cogName=cog)
        if(len(ctx.message.attachments) > 0):
            attachment = ctx.message.attachments[0]
            await attachment.save(path)
            await ctx.send("Downloading: " + attachment.name)
            print(f"Downloading: {attachment.name} to path: {path}")
            downloaded = "external"

        print(f"Loading: {path}")
        if(not os.path.exists(path)):
            await ctx.send("That file does not exist!")
            return
        with open(data.cogFile, "r") as file:
            cogs = json.load(file)
        cogs[path] = cog
        cogs[cog] = downloaded
        await self.bot.load_extension(cog)
        with open(data.cogFile, "w") as file:
            json.dump(cogs, file)

        await ctx.send("Loaded cog.")

    @commands.hybrid_command(name="removecog")
    @commands.is_owner()
    async def RemoveCog(self, ctx: commands.Context, cog: str) -> None:
        with open(data.cogFile, "r") as file:
            cogs = json.load(file)
        path = "{dir}/{cogName}.py".format(dir=data.cogFile, cogName=cog)
        print(f"Removing: {path}")
        if(cogs[cog] == "external"):
            os.remove(path)
            print(f"Deleted cog: {cog} at {path}")
        del cogs[path]
        del cogs[cog]
        await self.bot.unload_extension(cog)
        with open(data.cogFile, "w") as file:
            json.dump(cogs, file)
        await ctx.send("Removed cog.")

    @commands.hybrid_command(name="reloadcog")
    @commands.is_owner()
    async def ReloadCog(self, ctx: commands.Context, cog: str) -> None:
        await ctx.send(f"Reloading cog: {cog}")
        try:
            await self.bot.unload_extension(cog)
        except BaseException:
            print(f"Cog: {cog} was not loaded ,loading now..")
        await self.bot.load_extension(cog)
        print(f"Reloaded cog: {cog}")
        await ctx.send(f"Reloaded cog: {cog}")

    @commands.hybrid_command(name="reload")
    @commands.is_owner()
    async def Reload(self, ctx: commands.Context) -> None:
        await ctx.send("Reloading, please wait...")
        with open(data.cogFile, "r") as file:
            cogs = json.load(file)
        for cog in cogs:
            if(os.path.exists(cog)):
                try:
                    print(f"Reloading cog: {cog}")
                    await ctx.send(f"Reloading cog: {cog}")
                    try:
                        await self.bot.unload_extension(cogs[cog])
                    except BaseException:
                        print(
                            f"Cog: {cogs[cog]} was not loaded ,loading now..")
                    await self.bot.load_extension(cogs[cog])
                    print(f"Reloaded cog: {cog}")
                    await ctx.send(f"Reloaded cog: {cog}")
                except Exception as error:
                    await ctx.send("There was an error loading " + cog + ":\n" + f'**`ERROR:`** {type(error).__name__} - {error}')
        await ctx.send("All cogs have been reloaded.")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Debugger(bot))
