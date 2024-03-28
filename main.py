import discord
from config import TOKEN
import json

bot = discord.Bot()

def save_meetings():
    with open("meetings.json", "w+") as file:
        json.dump(meetings, file)

def load_meetings():
    global meetings
    try:
        with open("meetings.json", "r") as file:
            meetings = json.load(file)
    except FileNotFoundError:
        meetings = []

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

guild_ids = ["1093730670708281464"]
@bot.slash_command(guild_ids=guild_ids)
async def hello(ctx):
    await ctx.respond("Hello!")
    
meetings = []
load_meetings()
print(meetings)

@bot.slash_command(guild_ids=guild_ids)
async def create_meeting(ctx, start_time, end_time, reoccurrence, location, role, description, title):
    # print(start_time, end_time, reoccurrence, location, role, description, title)
    # print(type(start_time), type(end_time), type(reoccurrence), type(location), type(role), type(description), type(title))
    meeting = {
        "start_time": start_time,
        "end_time": end_time,
        "reoccurrence": reoccurrence,
        "location": location,
        "role": role,
        "description": description,
        "title": title
    }
    meetings.append(meeting)
    save_meetings()

    embed = discord.Embed(title="New Meeting Created", color=discord.Color.green())
    embed.add_field(name="Title", value=title, inline=False)
    embed.add_field(name="Start Time", value=start_time, inline=False)
    embed.add_field(name="End Time", value=end_time, inline=False)
    embed.add_field(name="Reoccurrence", value=reoccurrence, inline=False)
    embed.add_field(name="Location", value=location, inline=False)
    embed.add_field(name="Role", value=role, inline=False)
    embed.add_field(name="Description", value=description, inline=False)

    await ctx.respond(embed=embed)

@bot.command()
async def list_meetings(ctx):
    embed = discord.Embed(title="Meeting Schedule", color=discord.Color.blue())

    if meetings:
        for i, meeting in enumerate(meetings, 1):
            embed.add_field(name=f"Meeting {i}: {meeting['title']}",
                            value=f"**Start Time:** {meeting['start_time']}\n**End Time:** {meeting['end_time']}\n**Location:** {meeting['location']}\n**Description:** {meeting['description']}",
                            inline=False)
    else:
        embed.description = "No meetings scheduled."

    await ctx.respond(embed=embed)

@bot.command()
async def delete_meeting(ctx, meeting_id: int):
    if 1 <= meeting_id <= len(meetings):
        deleted_meeting = meetings.pop(meeting_id - 1)
        save_meetings()
        await ctx.respond(f"Meeting '{deleted_meeting['title']}' deleted.")
    else:
        await ctx.respond("Invalid meeting ID.")

bot.run(TOKEN)