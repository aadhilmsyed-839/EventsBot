# Import Discord Python Libraries
import discord
from discord.ext import commands

# Import Other Necessary Libraries
from datetime import datetime as time
import pytz
import json
import os

class Configurations:
    
    def __init__(self):
        self.guild = None
        self.log_channel = None
        self.restricted_channels = []
        self.metar_embed_thumbnail_url = "https://media.istockphoto.com/id/537337166/photo/air-trafic-control-tower-and-airplance-at-paris-airport.jpg?b=1&s=612x612&w=0&k=20&c=kp14V8AXFNUh5jOy3xPQ_sxhOZLWXycdBL-eUGviMOQ="
        self.roles = {  # Role ID, Hours
            989232534313369630: 8,
            1110680241569017966: 5,
            1110680332879011882: 2,
            1112981412191146004: 1
        }
        
    def save(self, file_path="data/config.json"):
        data = {
            "restricted_channels": self.restricted_channels,
#            "roles": self.roles,
#            "metar_embed_thumbnail_url": self.metar_embed_thumbnail_url
        }
        with open(file_path, "w") as file: json.dump(data, file)
        
    def load(self, file_path="data/config.json"):
        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                data = json.load(file)
                self.restricted_channels = data.get("restricted_channels", [])
#                self.roles = data.get("roles", {})
#                self.metar_embed_thumbnail_url = data.get("metar_embed_thumbnail_url", None)


class FlightHours:
    def __init__(self):
    
        # Class Attributes
        self.flight_hours = {}          # Key: Member ID (str) | Value: Minutes (int)
        self.start_time = {}            # Key: Member ID (str) | Value: Time (datetime)
        self.event_history = {}         # Key: Event Name (str) | Value: ID of Members Joined (Set of str)
        self.member_history = {}        # Key: Member ID (str) | Value: Events Joined (Set of str)
        self.active_event = None
        self.voice_channels = []


    def log_start_time(self, member_id):

        # Add the member to the start time dictionary and the member history dictionary
        if str(member_id) not in self.start_time: self.start_time[str(member_id)] = time.now(pytz.utc)
        if str(member_id) not in self.member_history: self.member_history[str(member_id)] = set()
        
        # Add the member to the event history and the member to the event history
        self.event_history[self.active_event].add(str(member_id))
        self.member_history[str(member_id)].add(self.active_event)
        

    def log_end_time(self, member_id):
    
        if str(member_id) in self.start_time:
        
            # Calculate how long the member was in the voice channel for
            elapsed = time.now(pytz.utc) - self.start_time[str(member_id)]
            minutes_flown = (elapsed.total_seconds() // 60)
            
            # If the member is not in the flight hours dictionary, add them to it
            if str(member_id) not in self.flight_hours: self.flight_hours[str(member_id)] = 0
            
            # Add the elapsed minutes to the total flight hours for the member
            self.flight_hours[str(member_id)] += minutes_flown
            
            # Remove the start time entry for the member
            del self.start_time[str(member_id)]
            
            # Return the minutes flown
            return minutes_flown
            
        else: return 0 # Extra layer of protection

    def save(self, file_path="data/flight_hours.json"):
    
        # Convert non-parseable data types to parseable data types
        start_time_str = {k: v.isoformat() for k, v in self.start_time.items()}
        member_history_list = {k: list(v) for k, v in self.member_history.items()}
        event_history_list = {k: list(v) for k, v in self.event_history.items()}
        voice_channel_ids = [channel.id for channel in self.voice_channels]
        
        # Store the data in JSON format
        data = {
            "active_event": self.active_event,
            "voice_channels": voice_channel_ids,
            "flight_hours": self.flight_hours,
            "start_time": start_time_str,
            "member_history": self.member_history,
            "event_history": self.event_history
        }
        
        # Write the JSON data to the file
        with open(file_path, "w") as file: json.dump(data, file)
        
    def load(self, file_path="data/flight_hours.json"):
        if os.path.exists(file_path):
            with open(file_path, "r") as file:
            
                # Retrieve the JSON data from the file
                data = json.load(file)
                self.active_event = data.get("active_event", None)
                self.voice_channels = [config.guild.get_channel(vc_id) for vc_id in data.get("voice_channels", [])]
                self.flight_hours = data.get("flight_hours", {})
                self.start_time = {k: time.fromisoformat(v) for k, v in data.get("start_time", {}).items()}
                self.member_history = {k: set(v) for k, v in data.get("member_history", {}).items()}
                self.event_history = {k: set(v) for k, v in data.get("event_history", {}).items()}
                
                
    async def export(self, file_path):
        with open(file_path, "w") as file:
        
            # Iterate through the dictionary
            for member_id, minutes in self._flight_hours.items():
            
                # Check if the member exists
                member = None
                try: member = await config.guild.fetch_member(member_id)
                except Exception as e: member = None
                
                # Calculate the flight time
                hours, minutes = divmod(minutes, 60)
                
                # Write the flight time to the file
                if member: file.write(f"{member.name}: {hours} hours {minutes} minutes\n")


# Create Objects
config = Configurations()
flight_hours_manager = FlightHours()
