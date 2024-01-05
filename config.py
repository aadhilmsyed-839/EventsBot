##############################################
# GLOBAL VARIABLES
##############################################

# Channel for Logging Bot Information
from bot import bot
log_channel = bot.get_guild(553718744233541656).get_channel(1184292134258479176)

# List of restricted announcement channels
restricted_channels = []

# Dictionary of Flight Hours
flight_hours = {}

# Dictionary to Store Amount of Time in Voice Channel
start_time = {}

# Flag to Indicate whether an Event is active or not
is_event_active = False

# Voice Channel of the Event
voice_channel = None

# Define role IDs for different tiers
roles = { # Role ID, Hours
    989232534313369630: 8,
    1110680241569017966: 5,
    1110680332879011882: 3,
    1112981412191146004: 1
}

# Embed Thumbnail for METAR commands
metar_embed_thumbnail_url = "https://media.istockphoto.com/id/537337166/photo/air-trafic-control-tower-and-airplance-at-paris-airport.jpg?b=1&s=612x612&w=0&k=20&c=kp14V8AXFNUh5jOy3xPQ_sxhOZLWXycdBL-eUGviMOQ="
