import discord
import gspread
import asyncio
import os
from google.oauth2.service_account import Credentials

# Google Sheets setup
scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_file(
    "service_account.json",
    scopes=scope
)

gs = gspread.authorize(creds)
sheet = gs.open("Discord Members").sheet1

# store already logged users
saved_users = set()

# Discord setup
intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    guild = client.guilds[0]

    # load existing sheet data to avoid duplicates
    try:
        data = sheet.get_all_values()
        for row in data[1:]:
            if row:
                saved_users.add(row[0])
    except:
        pass

    print("Bot running")

    while True:
        guild = client.guilds[0]

        for member in guild.members:
            username = str(member)

            if username not in saved_users:
                sheet.append_row([username, str(member.joined_at)])
                saved_users.add(username)

        await asyncio.sleep(60)

client.run(os.getenv("MTUwMDI1NzIwNzU2MjkzMjM0NA.Gnj6F-.KOkoi37ZFC4MIDeJZJKTDE-_CPOBegGJ9--8s0"))