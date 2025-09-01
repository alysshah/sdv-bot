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

# Load house data
with open('house.json', 'r') as file:
    house_data = json.load(file)

# Load crop data
with open('crop.json', 'r') as file:
    crop_data = json.load(file)

#####GIFT COMMAND#################################

@bot.command(name='gift')
async def gift(ctx, townsperson: str = None):
    """Shows loved and liked gifts for a villager"""
    if townsperson is None:
        await ctx.send("Please provide a townsperson name. Example: `!gift Alex`")
        return
    
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
        embed.add_field(name="💝 Loves", value=loves_formatted, inline=True)
        embed.add_field(name="👍 Likes", value=likes_formatted, inline=True)

        # Create a button linking to the wiki
        button = discord.ui.Button(label="View All Gifts on Wiki", url="https://stardewvalleywiki.com/List_of_All_Gifts")
        view = discord.ui.View()
        view.add_item(button)

        await ctx.send(embed=embed, view=view)
    else:
        await ctx.send(f"No data available for {townsperson}.")

#####CHAR COMMAND#################################
        
@bot.command(name='char')
async def char(ctx, townsperson: str = None):
    """Shows character profile including birthday"""
    if townsperson is None:
        await ctx.send("Please provide a townsperson name. Example: `!char Abigail`")
        return
    
    townsperson = townsperson.capitalize()
    if townsperson in townspeople_data:
        data = townspeople_data[townsperson]
        embed = discord.Embed(
            title=f"Profile for {townsperson}",
            color=0x0f700b
        )
        #embed.set_author(name=townsperson, icon_url=data["image"])
        embed.set_thumbnail(url=data["image"])
        embed.add_field(name="🎂 Birthday", value=data["birthday"], inline=False)

        await ctx.send(embed=embed)
    else:
        await ctx.send(f"No data available for {townsperson}.")

#####BUILD COMMAND#################################
        
@bot.command(name='build')
async def build(ctx, *building: str):
    """Shows materials and cost for farm buildings"""
    if not building:
        await ctx.send("Please provide a building name. Example: `!build Barn`")
        return
    
    building = " ".join(building).title()
    if building in building_data:
        data = building_data[building]
        embed = discord.Embed(
            title=f"Cost for {building}",
            color=0xff0000
        )

        # Format the loves and likes as a bulleted list
        cost_formatted = '\n'.join(f'- {item}' for item in data["cost"])
        embed.add_field(name="🔨 Materials", value=cost_formatted, inline=False)
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
async def events(ctx, season=None, day=None):
    """Shows events for a season or specific day"""
    if season is None:
        await ctx.send("Please provide a season. Example: `!events Spring` or `!events Summer 15`")
        return
    
    season = season.capitalize()

    # If day parameter IS NOT provided --> show all events in season
    if day == None:
        if season in events_data:
            embed = discord.Embed(
                title=f"Happening in {season}",
                color=0x5c15ad
            )
            data = events_data[season]
            events_formatted = []
            for day in data:
                events_list = ', '.join(data[day])
                events_formatted.append(f'- {day}: {events_list}')
            events_formatted = '\n'.join(events_formatted)
            embed.add_field(name="🎉 Event(s)", value=events_formatted, inline=False)

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
                    embed.add_field(name="🎉 Event(s)", value=events_formatted, inline=False)
                else:
                    embed.add_field(name="🎉 Event(s)", value="No events", inline=False)

                await ctx.send(embed=embed)
        else:
            await ctx.send(f"No data available for this date.")

#####HOUSE COMMAND#################################

@bot.command(name='house')
async def house(ctx, category: str = None):
    """Shows house upgrades or renovations (use 'upgrades' or 'renovations')"""
    if category is None:
        await ctx.send("Please specify either `upgrades` or `renovations`. Example: `!house upgrades`")
        return
    
    category = category.lower()
    
    try:
        if category == "upgrades":
            upgrades = house_data["House Upgrades"]
            embed = discord.Embed(
                title="House Upgrades",
                description="Sequential upgrades for your farmhouse (must be done in order)",
                color=0x8B4513
            )
            
            for i, upgrade in enumerate(upgrades, 1):
                cost_formatted = ', '.join(upgrade["cost"])
                embed.add_field(
                    name=f"{upgrade['name']} - {cost_formatted}",
                    value=upgrade["description"],
                    inline=False
                )
            
            # Create a button linking to the wiki
            button = discord.ui.Button(label="View All House Upgrades on Wiki", url="https://stardewvalleywiki.com/Farmhouse#Upgrades")
            view = discord.ui.View()
            view.add_item(button)
            
            await ctx.send(embed=embed, view=view)
            
        elif category == "renovations":
            renovations = house_data["House Renovations"]
            embed = discord.Embed(
                title="House Renovations",
                description="Optional room additions (requires House Upgrade 2)",
                color=0xA6571F
            )
            
            for renovation in renovations:
                cost = renovation["cost"] if isinstance(renovation["cost"], str) else ', '.join(renovation["cost"])
                # Use shorter field names and values for grid layout (inline fields)
                embed.add_field(
                    name=renovation['name'],
                    value=cost,
                    inline=True
                )
            
            # Create a button linking to the wiki
            button = discord.ui.Button(label="View All Renovations on Wiki", url="https://stardewvalleywiki.com/Farmhouse#Renovations")
            view = discord.ui.View()
            view.add_item(button)
            
            await ctx.send(embed=embed, view=view)
            
        else:
            await ctx.send("Please specify either `upgrades` or `renovations`. Example: `!house upgrades`")
    
    except Exception as e:
        await ctx.send(f"Error: {str(e)}")
        print(f"House command error: {e}")

#####CROP COMMAND#################################

@bot.command(name='crop')
async def crop(ctx, *, crop_name: str = None):
    """Shows detailed crop info (seasons, growth, prices, etc.)"""
    if crop_name is None:
        await ctx.send("Please provide a crop name. Example: `!crop Parsnip`")
        return
    
    # Handle case-insensitive matching
    crop_name_formatted = None
    for key in crop_data.keys():
        if key.lower() == crop_name.lower():
            crop_name_formatted = key
            break
    
    if crop_name_formatted and crop_name_formatted in crop_data:
        data = crop_data[crop_name_formatted]
        embed = discord.Embed(
            title=f"Crop Info: {data['name']}",
            color=0x6FDE4B
        )
        
        # Set thumbnail image
        embed.set_thumbnail(url=data["image"])
        
        # Seasons
        seasons_text = ', '.join(data["seasons"])
        embed.add_field(name="🌱 Seasons", value=seasons_text, inline=True)
        
        # Growth time
        embed.add_field(name="⏱️ Growth Time", value=data["growth_time"], inline=True)
        
        # Prices
        prices = data["prices"]
        price_parts = []
        if "base" in prices:
            price_parts.append(f"Base: {prices['base']}g")
        if "silver" in prices:
            price_parts.append(f"Silver: {prices['silver']}g")
        if "gold" in prices:
            price_parts.append(f"Gold: {prices['gold']}g")
        if "iridium" in prices:
            price_parts.append(f"Iridium: {prices['iridium']}g")
        
        price_text = '\n'.join(price_parts)
        embed.add_field(name="💰 Sell Prices", value=price_text, inline=False)
        
        # Seed sources
        if data.get("seed_sources"):
            seed_parts = []
            for source in data["seed_sources"]:
                seed_parts.append(source["source"])
            seed_text = '\n'.join(seed_parts)
            embed.add_field(name="🌰 Seed Sources", value=seed_text, inline=True)
        
        # Profit scenarios
        if data.get("profit_scenarios"):
            profit_text = '\n'.join(data["profit_scenarios"])
            embed.add_field(name="📈 Profit", value=profit_text, inline=True)
        
        # Create a button linking to the wiki
        button = discord.ui.Button(label="View All Crops on Wiki", url="https://stardewvalleywiki.com/Crops")
        view = discord.ui.View()
        view.add_item(button)
        
        await ctx.send(embed=embed, view=view)
    else:
        await ctx.send(f"No data available for '{crop_name}'.")


bot.run(os.getenv('BOT_TOKEN'))