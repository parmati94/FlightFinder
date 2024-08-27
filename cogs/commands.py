import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime
from services.CustomFlightRadarAPI import CustomFlightRadarAPI
from utils.helpers import convert_timestamp

class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.fr_api = CustomFlightRadarAPI()
        airlines = self.fr_api.get_airlines()
        self.airlines_dict = {}
        for airline in airlines:
            key = airline['Code'] if airline['Code'] else airline['ICAO']
            self.airlines_dict[key] = airline
        
    @app_commands.command(name="ping", description="Sends the bot's latency.")
    async def ping_slash(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"Pong! Latency is {self.bot.latency}")
    
    @app_commands.command(name="flight", description="Retrieve flight information via flight number.")
    async def flight_slash(self, interaction: discord.Interaction, flight_number: str):
        flight_number = flight_number.upper()
        airline_code = flight_number[:2]
        airline_icao = self.airlines_dict.get(airline_code, {}).get('ICAO', None)
        
        flight = self.fr_api.get_flight(airline_icao, flight_number)
        if not flight:
            await interaction.response.send_message(f"Flight {flight_number} not found.")
            return
        
        flight.set_flight_details(self.fr_api.get_flight_details(flight))
        
        estimated_arrival = convert_timestamp(flight.time_details['estimated']['arrival'])
        scheduled_departure = convert_timestamp(flight.time_details['scheduled']['departure'])
        real_departure = convert_timestamp(flight.time_details['real']['departure'])

        embed = discord.Embed(
            title=f"Flight Information for {flight_number}",
            description=f"Details for flight {flight_number}",
            color=discord.Color.blue(),
            timestamp=datetime.now()
        )
        
        flightradar_url = f"https://www.flightradar24.com/{flight.callsign}"

        embed.add_field(name="Airline ICAO", value=airline_icao, inline=True)
        embed.add_field(name="Scheduled Departure", value=scheduled_departure, inline=True)
        embed.add_field(name="Real Departure", value=real_departure, inline=True)
        embed.add_field(name="Estimated Arrival", value=estimated_arrival, inline=True)
        embed.add_field(name="Origin Airport", value=flight.origin_airport_iata, inline=True)
        embed.add_field(name="Destination Airport", value=flight.destination_airport_iata, inline=True)
        embed.add_field(name="Flight URL", value=f"[{flight_number}]({flightradar_url})", inline=True)

        if flight.aircraft_model:
            embed.add_field(name="Aircraft", value=flight.aircraft_model, inline=True)

        thumbnails = flight.aircraft_images.get("thumbnails")
        if thumbnails and isinstance(thumbnails, list) and len(thumbnails) > 0:
            first_thumbnail = thumbnails[0]
            if isinstance(first_thumbnail, dict) and "src" in first_thumbnail:
                embed.set_thumbnail(url=first_thumbnail["src"])

        embed.set_footer(text="Flight data provided by FlightRadar24")

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    print("Setting up Commands cog")
    await bot.add_cog(Commands(bot))
    print("Commands cog has been added")