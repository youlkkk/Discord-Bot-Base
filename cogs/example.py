import discord
from discord import app_commands
from discord.ext import commands
from helpers import create_embed

class ExampleCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        
        if self.bot.user.mentioned_in(message):
            embed = create_embed(
                title="Greetings!",
                description="👋 Hello! I'm a Discord bot!",
                color=discord.Color.green()
            )
            await message.channel.send(embed=embed)

    @commands.command(name="ping")
    async def ping(self, ctx):
        latency = round(self.bot.latency * 1000)
        embed = create_embed(
            title="Pong! 🏓",
            description=f"Bot latency: {latency}ms",
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed)

    @app_commands.command(name="hello", description="Say hello")
    async def hello(self, interaction: discord.Interaction):
        embed = create_embed(
            title="Greetings! 👋",
            description=f"Hello, {interaction.user.mention}!",
            color=discord.Color.gold()
        )
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(ExampleCog(bot))