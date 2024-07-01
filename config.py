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
            989232534313369630: 5,
            1110680241569017966: 3,
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
        self._flight_hours = {}
        self._start_time = {}
        self._is_event_active = False
        self._voice_channel = None

    @property
    def flight_hours(self): return self._flight_hours

    @property
    def start_time(self): return self._start_time

    @property
    def is_event_active(self): return self._is_event_active

    @property
    def voice_channel(self): return self._voice_channel

    @is_event_active.setter
    def is_event_active(self, value): self._is_event_active = value

    @voice_channel.setter
    def voice_channel(self, channel): self._voice_channel = channel

    def log_start_time(self, member_id):
        if str(member_id) not in self._start_time: self._start_time[str(member_id)] = time.now(pytz.utc)

    def log_end_time(self, member_id):
        if str(member_id) in self._start_time:
            elapsed = time.now(pytz.utc) - self._start_time[str(member_id)]
            if str(member_id) not in self._flight_hours:
                self._flight_hours[str(member_id)] = 0
            self._flight_hours[str(member_id)] += (elapsed.total_seconds() // 60)
            del self._start_time[str(member_id)]
            return elapsed.total_seconds() // 60
        return 0
        
    def save(self, file_path="data/flight_hours.json"):
        start_time_str = {k: v.isoformat() for k, v in self._start_time.items()}
        data = {
            "is_event_active": self._is_event_active,
            "voice_channel": self._voice_channel.id if self._voice_channel else None,
            "flight_hours": self._flight_hours,
            "start_time": start_time_str
        }
        with open(file_path, "w") as file: json.dump(data, file)
        
    def load(self, file_path="data/flight_hours.json"):
        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                data = json.load(file)
                self._is_event_active = data.get("is_event_active", False)
                self._voice_channel = data.get("voice_channel", None)
                self._flight_hours = data.get("flight_hours", {})
                self._start_time = {k: time.fromisoformat(v) for k, v in data.get("start_time", {}).items()}
                
    async def export(self, file_path):
        with open(file_path, "w") as file:
            for member_id, minutes in self._flight_hours.items():
                member = await config.guild.fetch_member(member_id)
                hours, minutes = divmod(minutes, 60)
                file.write(f"{member.name}: {hours} hours & {minutes} minutes\n")

# Create Objects
config = Configurations()
flight_hours_manager = FlightHours()
