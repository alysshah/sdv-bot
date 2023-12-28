from discord.ext import commands
import discord
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print("StardewSavvy is ready!")

# Load townspeople data
with open('townspeople.json', 'r') as file:
    townspeople_data = json.load(file)

# Load building data
with open('building.json', 'r') as file:
    building_data = json.load(file)

# Load events data
with open('events.json', 'r') as file:
    events_data = json.load(file)

#####GIFT COMMAND#################################

@bot.command(name='gift')
async def gift(ctx, townsperson: str):
    townsperson = townsperson.capitalize()
    if townsperson in townspeople_data:
        data = townspeople_data[townsperson]
        embed = discord.Embed(
            title=f"Gift Preferences for {townsperson}",
            color=0x1e31bd
        )
        #embed.set_author(name=townsperson, icon_url=data["image"])
        embed.set_thumbnail(url=data["image"])

        # Format the loves and likes as a bulleted list
        loves_formatted = '\n'.join(f'- {item}' for item in data["loves"])
        likes_formatted = '\n'.join(f'- {item}' for item in data["likes"])
        embed.add_field(name="Loves", value=loves_formatted, inline=True)
        embed.add_field(name="Likes", value=likes_formatted, inline=True)

        # Create a button linking to the wiki
        button = discord.ui.Button(label="View All Gifts on Wiki", url="https://stardewvalleywiki.com/List_of_All_Gifts")
        view = discord.ui.View()
        view.add_item(button)

        await ctx.send(embed=embed, view=view)
    else:
        await ctx.send(f"No data available for {townsperson}.")

#####CHAR COMMAND#################################
        
@bot.command(name='char')
async def char(ctx, townsperson: str):
    townsperson = townsperson.capitalize()
    if townsperson in townspeople_data:
        data = townspeople_data[townsperson]
        embed = discord.Embed(
            title=f"Profile for {townsperson}",
            color=0x0f700b
        )
        #embed.set_author(name=townsperson, icon_url=data["image"])
        embed.set_thumbnail(url=data["image"])
        embed.add_field(name="Birthday", value=data["birthday"], inline=False)

        await ctx.send(embed=embed)
    else:
        await ctx.send(f"No data available for {townsperson}.")

#####BUILD COMMAND#################################
        
@bot.command(name='build')
async def build(ctx, *building: str):
    building = " ".join(building).title()
    if building in building_data:
        data = building_data[building]
        embed = discord.Embed(
            title=f"Cost for {building}",
            color=0xff0000
        )

        # Format the loves and likes as a bulleted list
        cost_formatted = '\n'.join(f'- {item}' for item in data["cost"])
        embed.add_field(name="Materials", value=cost_formatted, inline=False)
        embed.set_thumbnail(url=data["image"])

        # Create a button linking to the wiki
        button = discord.ui.Button(label="View All Buildings on Wiki", url="https://stardewvalleywiki.com/Carpenter%27s_Shop#Farm_Buildings")
        view = discord.ui.View()
        view.add_item(button)

        await ctx.send(embed=embed, view=view)
    else:
        await ctx.send(f"No data available for {building}.")

#####EVENT COMMAND#################################

@bot.command(name='events')
async def events(ctx, season, day=None): 
    season = season.capitalize()

    # If day parameter IS NOT provided --> show all events in season
    if day == None:
        if season in events_data:
            embed = discord.Embed(
                title=f"Happening in {season}",
                color=0x5c15ad
            )
            data = events_data[season]
            events_formatted = " "
            for day in data:
                events_formatted += '\n'.join(f'- {day}: {event}\n' for event in data[day])
            embed.add_field(name="Event(s)", value=events_formatted, inline=False)

            await ctx.send(embed=embed)
        else:
            await ctx.send(f"Please provide an existing season")
    
    # If day paramter IS provided --> only show events on that specific day
    else:
        if season in events_data:
            if int(day) > 28 or int(day) < 0:
                await ctx.send(f"Not a valid date.")
            else:
                embed = discord.Embed(
                    title=f"Happening on {season} {day}",
                    color=0x5c15ad
                )
                data = events_data[season]
                if day in data:
                    events_formatted = '\n'.join(f'- {item}' for item in data[day])
                    embed.add_field(name="Event(s)", value=events_formatted, inline=False)
                else:
                    embed.add_field(name="Event(s)", value="No events", inline=False)

                await ctx.send(embed=embed)
        else:
            await ctx.send(f"No data available for this date.")


bot.run(os.getenv('BOT_TOKEN'))