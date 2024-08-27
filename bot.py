import discord
from discord.ext import commands
from config import TOKEN
from services.CustomFlightRadarAPI import CustomFlightRadarAPI
from logging_config import logger
import asyncio

intents = discord.Intents.default()
# intents.message_content = True
bot = commands.Bot(command_prefix=';', intents=intents)

fr_api = CustomFlightRadarAPI()

@bot.event
async def on_ready():
    global airlines_dict
    try:
        s = await bot.tree.sync()
        logger.info(f'S:  {s}')
        logger.info(f'Synced {len(s)} commands')
            
    except Exception as e:
        logger.info(f'Error syncing commands: {e}')
        
    logger.info(f'Logged in as {bot.user.name}')

async def main():
    try:
        async with bot:
            logger.info("Loading extension 'cogs.commands'...")
            await bot.load_extension('cogs.commands')
            logger.info("Extension 'cogs.commands' loaded successfully.")
             # Check loaded extensions
            logger.info("Loaded extensions:")
            for ext in bot.extensions:
                logger.info(f' - {ext}')
            logger.info("Starting bot...")
            await bot.start(TOKEN)
    except Exception as e:
        logger.info(f'Failed to start bot: {e}')

if __name__ == "__main__":
    asyncio.run(main())