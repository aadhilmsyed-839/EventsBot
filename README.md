# GeoFS Events CoPilot Discord Bot

Welcome to the GeoFS Events CoPilot! This bot is designed to enhance the [GeoFS Events Discord Server](https://discord.gg/nCWhNgN) by providing useful features and functionality, such as airport METAR information retrieval, flight hour tracking automation, role assignment automation, and other member commands such as dotspam, flight hours leaderboards, and individual flight times.

## Table of Contents

1. [Introduction](#introduction)
2. [Key Features](#key-features)
3. [File Structure](#file-structure)
4. [Contributing](#contributing)
5. [Usage Terms](#usage-terms)

## Introduction

The GeoFS Events CoPilot is your trusted companion in the world of Flight Simulation at GeoFS Events. It seamlessly integrates with the GeoFS Events Discord Server, providing a suite of indispensable tools and utilities designed to enhance the virtual flight experience.

## Key Features

Here's a glimpse of what the GeoFS Events CoPilot brings to the table:

- **Airport METAR Information**: Instantly retrieve real-time METAR data for any airport, ensuring you have up-to-date weather information for your flights.

- **Flight Hour Tracking Automation**: Say goodbye to manual record-keeping. The bot automates the logging of flight hours during events, ensuring that your valuable time is not gone to waste.

- **Role Assignment Automation**: Your hard-earned flight hours are rewarded with automated role assignments issued by server administrators.

- **Member Commands**: Don't worry. This bot also has many commands dedicated just for the members. From dotspam to flight hours leaderboards and individual flight time tracking, this bot is designed to be compatible for public use.

## File Structure

Here's an overview of the project's file structure to help you navigate the codebase:

- `events_bot.py`: The main/driver file of the program.
- `config.py`: Contains configuration settings and global variables.
- `commands` (Directory):
  - `metar.py`: Module for getting Airport METAR.
  - `member_commands.py`: Commands that can be issued by members.
  - `mod_commands.py`: Commands that can be issued by moderators.
  - `help.py`: Contains the help module for the bot. Members can call it to view info about the bot.
- `data` (Directory - contains sensitive information, excluded in .gitignore).
- `bot` (Directory):
  - `__init__.py`: Bot initialization file, contains bot object used by the rest of the program.
  - `events.py`: Implementation of `on_ready()` and `on_disconnect()` functions.
  - `logger` (Sub-directory):
    - `__init__.py`: Logger initialization file, contains logger object used by the rest of the program.
    - `formatter.py`: Module used to convert logger information into JSON format.
    - `parser.py`: Parses JSON file to CSV for exporting.
- `events` (Directory):
  - `flight_logs.py`: Contains module for automatically logging flight hours during events.
  - `send_saw.py`: Module that sends 'SAW' on deleted messages if not in a restricted channel.
  - `monthly_roles.py`: Module that updates roles based on each member's flight hours.

## Contributing

For contributions, please message `the._.pickle` on Discord.

## Usage Terms

This source code is provided solely for the purpose of running the GeoFS Events CoPilot Discord Bot in the context of the [GeoFS Events Discord Server](https://discord.gg/nCWhNgN). Any use, reproduction, modification, or distribution of this source code for other projects or purposes is strictly prohibited.

© GeoFS Flights Channel 2023. All Rights Reserved.

