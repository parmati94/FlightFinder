import discord
from discord.ext import commands
from config import TOKEN
from services.CustomFlightRadarAPI import CustomFlightRadarAPI
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
        print(f'S:  {s}')
        print(f'Synced {len(s)} commands')
            
    except Exception as e:
        print(f'Error syncing commands: {e}')
        
    print(f'Logged in as {bot.user.name}')

async def main():
    try:
        async with bot:
            print("Loading extension 'cogs.commands'...")
            await bot.load_extension('cogs.commands')
            print("Extension 'cogs.commands' loaded successfully.")
             # Check loaded extensions
            print("Loaded extensions:")
            for ext in bot.extensions:
                print(f' - {ext}')
            print("Starting bot...")
            await bot.start(TOKEN)
    except Exception as e:
        print(f'Failed to start bot: {e}')

if __name__ == "__main__":
    asyncio.run(main())