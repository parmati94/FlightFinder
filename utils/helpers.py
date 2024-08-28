from datetime import datetime
from logging_config import logger
import discord
import asyncio

def convert_timestamp(timestamp):
    if timestamp is None:
        return None
    time_str = datetime.fromtimestamp(timestamp).strftime('%I:%M %p')
    return time_str.lstrip('0')

def get_nested(data, keys, default=None):
    SENTINEL = object()
    for key in keys:
        if not isinstance(data, dict):
            print(f"Expected dict but got {type(data)} for key {key}. Returning default: {default}")
            return default
        data = data.get(key, SENTINEL)
        if data is SENTINEL:
            return default
        if data is None or data == '':
            return default
    return data

async def handle_reactions(bot, message, user, items, page_size, create_embed_callback, airport_iata, flight_type):
    page_number = 1
    total_pages = (len(items) + page_size - 1) // page_size

    def check(reaction, reaction_user):
        return reaction_user == user and str(reaction.emoji) in ["⬅️", "➡️", "🔄"] and reaction.message.id == message.id

    while True:
        try:
            reaction, reaction_user = await bot.wait_for("reaction_add", timeout=600.0, check=check)

            if str(reaction.emoji) == "➡️" and page_number < total_pages:
                page_number += 1
            elif str(reaction.emoji) == "⬅️" and page_number > 1:
                page_number -= 1
            elif str(reaction.emoji) == "🔄":
                page_number = 1

            embed = create_embed_callback(airport_iata, items, page_number, page_size, flight_type)
            await message.edit(embed=embed)
            await message.remove_reaction(reaction, reaction_user)

        except asyncio.TimeoutError:
            break

def create_arrivals_or_departures_embed(airport_iata, flights, page_number, page_size, flight_type):
    logger.info(f"Creating {flight_type} embed for {airport_iata}, page #{page_number}")
    pages = (len(flights) + page_size - 1) // page_size
    embed = discord.Embed(
        title=f"{flight_type.capitalize() + 's'} for {airport_iata}",
        description=f"Showing {flight_type} {page_number * page_size - page_size + 1} to {min(page_number * page_size, len(flights))}",
        color=discord.Color.blue(),
        timestamp=datetime.now()
    )
    
    start = (page_number - 1) * page_size
    end = start + page_size
    for i, flight in enumerate(flights[start:end]):
        flight_callsign = get_nested(flight, ['flight', 'identification', 'callsign'], '')
        flight_number = get_nested(flight, ['flight', 'identification', 'number', 'default'], 'Not Found')
        aircraft_model = get_nested(flight, ['flight', 'aircraft', 'model', 'text'], 'Not Found')
        estimated_time = convert_timestamp(get_nested(flight, ['flight', 'time', 'estimated', flight_type], 0))
        flight_live_status = get_nested(flight, ['flight', 'status', 'live'], False)
        
        value = f"Aircraft: {aircraft_model}\nEstimated {flight_type.capitalize()}: {estimated_time}"
               
        if flight_live_status:
            flightradar_url = f"https://www.flightradar24.com/{flight_callsign}"
            value += f"\n[See live]({flightradar_url})"
        
        embed.add_field(
            name=f"Flight {flight_number}",
            value=value,
            inline=True
        )
        if (i + 1) % 2 == 0:
            embed.add_field(name='\u200b', value='\u200b', inline=True)
    embed.set_footer(text=f"Page {page_number}/{pages}")
    
    return embed