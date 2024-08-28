from datetime import datetime
from logging_config import logger
import discord

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

def create_arrivals_embed(airport_iata, arrivals, page_number, page_size):
    pages = (len(arrivals) + page_size - 1) // page_size
    embed = discord.Embed(
        title=f"Arrivals for {airport_iata}",
        description=f"Showing arrivals {page_number * page_size - page_size + 1} to {min(page_number * page_size, len(arrivals))}",
        color=discord.Color.blue(),
        timestamp=datetime.now()
    )
    
    start = (page_number - 1) * page_size
    end = start + page_size
    for i, arrival in enumerate(arrivals[start:end]):
        flight_callsign = get_nested(arrival, ['flight', 'identification', 'callsign'], '')
        flight_number = get_nested(arrival, ['flight', 'identification', 'number', 'default'], 'Not Found')
        aircraft_model = get_nested(arrival, ['flight', 'aircraft', 'model', 'text'], 'Not Found')
        arrival_estimated = convert_timestamp(get_nested(arrival, ['flight', 'time', 'estimated', 'arrival'], 0))
        flight_live_status = get_nested(arrival, ['flight', 'status', 'live'], False)
        
        value = f"Aircraft: {aircraft_model}\nEstimated Arrival: {arrival_estimated}"
               
        if flight_live_status:
            flightradar_url = f"https://www.flightradar24.com/{flight_callsign}"
            value += f"\n[See live]({flightradar_url})"
        
        flightradar_url = f"https://www.flightradar24.com/{flight_callsign}"
        
        embed.add_field(
            name=f"Flight {flight_number}",
            value=value,
            inline=True
        )
        if (i + 1) % 2 == 0:
            embed.add_field(name='\u200b', value='\u200b', inline=True)
    embed.set_footer(text=f"Page {page_number}/{pages}")
    
    return embed