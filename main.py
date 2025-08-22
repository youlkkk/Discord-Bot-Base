import os
import logging
import asyncio

import discord
from discord.ext import commands
from dotenv import load_dotenv

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

load_dotenv()

class Bot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        
        super().__init__(
            command_prefix='!',
            intents=intents,
            help_command=None
        )

    async def setup_hook(self):
        if os.path.exists("./cogs"):
            for filename in os.listdir("./cogs"):
                if filename.endswith(".py") and not filename.startswith("_"):
                    try:
                        await self.load_extension(f"cogs.{filename[:-3]}")
                        logger.info(f"Loaded cog: {filename[:-3]}")
                    except Exception as e:
                        logger.error(f"Error loading cog {filename}: {e}")

    async def on_ready(self):
        logger.info(f"Bot {self.user} is ready!")
        logger.info(f"Bot ID: {self.user.id}")
        
        await self.update_presence()

    async def update_presence(self):
        total_members = sum(guild.member_count for guild in self.guilds)
        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name=f"{len(self.guilds)} servers | {total_members} users"
            )
        )

    async def on_guild_join(self, guild):
        logger.info(f"Joined guild: {guild.name} ({guild.id})")
        await self.update_presence()

    async def on_guild_remove(self, guild):
        logger.info(f"Left guild: {guild.name} ({guild.id})")
        await self.update_presence()

    async def on_member_join(self, member):
        await self.update_presence()

    async def on_member_remove(self, member):
        await self.update_presence()

    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            return
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ You don't have permission to use this command.")
        else:
            logger.error(f"Command error: {error}")

async def main():
    bot = Bot()
    
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        logger.error("DISCORD_TOKEN not found in environment variables!")
        return
    
    try:
        await bot.start(token)
    except KeyboardInterrupt:
        await bot.close()
    except Exception as e:
        logger.error(f"Failed to start bot: {e}")

if __name__ == "__main__":
    asyncio.run(main())