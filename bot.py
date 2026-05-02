import discord
import gspread
import asyncio
from google.oauth2.service_account import Credentials

# Google setup
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

# track users already saved
saved_users = set()

intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    guild = client.guilds[0]

    # load existing sheet users
    records = sheet.get_all_values()
    for row in records[1:]:
        if row:
            saved_users.add(row[0])

    print("Bot running")

    while True:
        guild = client.guilds[0]

        for member in guild.members:
            name = str(member)

            if name not in saved_users:
                sheet.append_row([name, str(member.joined_at)])
                saved_users.add(name)

        await asyncio.sleep(60)