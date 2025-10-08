from discord.ext import commands
import discord
import json
import os
from typing import Literal
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

intents = discord.Intents.default()

bot = commands.Bot(command_prefix=None, intents=intents)

@bot.event
async def on_ready():
    print("StardewSavvy is ready!")
    # Set bot status
    await bot.change_presence(activity=discord.CustomActivity(name="Use /help for commands!"))
    
    # Sync slash commands
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} slash commands")
    except Exception as e:
        print(f"Failed to sync commands: {e}")

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

# Load fish data
with open('fish.json', 'r') as file:
    fish_data = json.load(file)

#####GIFT COMMAND#################################

@bot.tree.command(name='gift', description='Shows loved and liked gifts for a villager')
async def gift(ctx, townsperson: str):
    """Shows loved and liked gifts for a villager"""
    
    townsperson = townsperson.capitalize()
    if townsperson in townspeople_data:
        data = townspeople_data[townsperson]
        embed = discord.Embed(
            title=f"Gift Preferences for {townsperson}",
            color=0xFFD700
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
        
@bot.tree.command(name='char', description='Shows character profile including birthday')
async def char(ctx, townsperson: str):
    """Shows character profile including birthday"""
    
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
        
@bot.tree.command(name='build', description='Shows materials and cost for farm buildings')
async def build(ctx, *, building: str):
    """Shows materials and cost for farm buildings"""
    
    building = building.title()
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

@bot.tree.command(name='events', description='Shows events for a season or specific day')
async def events(ctx, season: str, day: int = None):
    """Shows events for a season or specific day"""
    
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

@bot.tree.command(name='house', description='Shows house upgrades or renovations')
async def house(ctx, category: Literal['upgrades', 'renovations']):
    """Shows house upgrades or renovations (use 'upgrades' or 'renovations')"""
    
    category = category.lower()
    
    if category == "upgrades":
        if "House Upgrades" in house_data:
            upgrades = house_data["House Upgrades"]
            embed = discord.Embed(
                title="House Upgrades",
                description="Sequential upgrades for your farmhouse (must be done in order)\n",
                color=0x8B4513
            )
            
            for upgrade in upgrades:
                cost_formatted = '\n'.join(f'- {item}' for item in upgrade["cost"])
                embed.add_field(
                    name=f"🏠 {upgrade['name']}",
                    value=f"{cost_formatted}\n*{upgrade['description']}*\n",
                    inline=False
                )
            
            # Create a button linking to the wiki
            button = discord.ui.Button(label="View All House Upgrades on Wiki", url="https://stardewvalleywiki.com/Farmhouse#Upgrades")
            view = discord.ui.View()
            view.add_item(button)
            
            await ctx.send(embed=embed, view=view)
        else:
            await ctx.send("House upgrade data not available.")
            
    elif category == "renovations":
        if "House Renovations" in house_data:
            renovations = house_data["House Renovations"]
            embed = discord.Embed(
                title="House Renovations",
                description="Optional room additions (requires House Upgrade 2)\n",
                color=0xA6571F
            )
            
            for renovation in renovations:
                embed.add_field(
                    name=renovation["name"],
                    value=renovation["cost"],
                    inline=True
                )
            
            # Create a button linking to the wiki
            button = discord.ui.Button(label="View All Renovations on Wiki", url="https://stardewvalleywiki.com/Farmhouse#Renovations")
            view = discord.ui.View()
            view.add_item(button)
            
            await ctx.send(embed=embed, view=view)
        else:
            await ctx.send("House renovation data not available.")

#####FISH COMMAND#################################

@bot.tree.command(name='fish', description='Shows detailed fish info (location, time, season, difficulty, prices)')
async def fish(ctx, *, fish_name: str):
    """Shows detailed fish info (location, time, season, difficulty, prices)"""
    
    # Find the fish (case-insensitive)
    fish_key = None
    for key in fish_data.keys():
        if key.lower() == fish_name.lower():
            fish_key = key
            break
    
    if fish_key is None:
        await ctx.send(f"Fish '{fish_name}' not found. Please check the spelling!")
        return
    
    fish_info = fish_data[fish_key]
    
    # Create embed
    embed = discord.Embed(
        title=f"{fish_info['name']}",
        color=0x4169E1  # Royal blue
    )
    
    # Set thumbnail
    if 'image' in fish_info and fish_info['image']:
        embed.set_thumbnail(url=fish_info['image'])
    
    # Add type field for ALL fish (at top, full width)
    if fish_info.get('type'):
        embed.add_field(name="🏷️ Type", value=fish_info['type'], inline=False)
    
    # Add location
    if fish_info.get('location'):
        if isinstance(fish_info['location'], list):
            location_text = ", ".join(fish_info['location'])
        else:
            location_text = fish_info['location']
        embed.add_field(name="📍 Location", value=location_text, inline=True)
    
    # Add time (if not null)
    if fish_info.get('time') is not None:
        embed.add_field(name="⏰ Time", value=fish_info['time'], inline=True)
    
    # Add season (if not null)
    if fish_info.get('season') is not None:
        if isinstance(fish_info['season'], list):
            season_text = ", ".join(fish_info['season'])
        else:
            season_text = fish_info['season']
        embed.add_field(name="🌸 Season", value=season_text, inline=True)
    
    # Add weather (if not null)
    if fish_info.get('weather') is not None:
        embed.add_field(name="🌤️ Weather", value=fish_info['weather'], inline=True)
    
    # Add difficulty (if not null)
    if fish_info.get('difficulty') is not None:
        embed.add_field(name="🎣 Difficulty", value=fish_info['difficulty'], inline=True)
    
    # Add XP (if not null)
    if fish_info.get('base_xp') is not None:
        embed.add_field(name="⭐ Base XP", value=fish_info['base_xp'], inline=True)
    
    # Add prices (at bottom, full width)
    if 'base_price' in fish_info:
        prices = fish_info['base_price']
        price_labels = ['Base', 'Silver', 'Gold', 'Iridium']
        valid_prices = []
        for i, price in enumerate(prices):
            if price is not None:
                valid_prices.append(f"{price_labels[i]}: {price}g")
        
        if valid_prices:
            price_text = "\n".join(valid_prices)
            price_text += "\n*Fisher Profession (+25%)*\n*Angler Profession (+50%)*"
            embed.add_field(name="💰 Sell Prices", value=price_text, inline=False)
    
    # Add wiki button
    view = discord.ui.View()
    wiki_button = discord.ui.Button(
        label="View All Fish on Wiki",
        url="https://stardewvalleywiki.com/Fish",
        style=discord.ButtonStyle.link
    )
    view.add_item(wiki_button)
    
    await ctx.send(embed=embed, view=view)

#####CROP COMMAND#################################

@bot.tree.command(name='crop', description='Shows detailed crop info (seasons, growth, prices, etc.)')
async def crop(ctx, *, crop_name: str):
    """Shows detailed crop info (seasons, growth, prices, etc.)"""
    
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
        embed.add_field(name="💰 Sell Prices", value=price_text, inline=True)
        
        # Seed sources
        if data.get("seed_sources"):
            seed_parts = []
            for source in data["seed_sources"]:
                seed_parts.append(source["source"])
            seed_text = '\n'.join(seed_parts)
            embed.add_field(name="🌰 Seed Sources", value=seed_text, inline=True)
        
        # Profit scenarios (alone at bottom)
        if data.get("profit_scenarios"):
            profit_text = '\n'.join(data["profit_scenarios"])
            embed.add_field(name="📈 Profit", value=profit_text, inline=False)
        
        # Create a button linking to the wiki
        button = discord.ui.Button(label="View All Crops on Wiki", url="https://stardewvalleywiki.com/Crops")
        view = discord.ui.View()
        view.add_item(button)
        
        await ctx.send(embed=embed, view=view)
    else:
        await ctx.send(f"No data available for '{crop_name}'.")

#####HELP COMMAND#################################

@bot.tree.command(name='help', description='Shows all available commands and their descriptions')
async def help_command(ctx):
    """Shows all available commands and their descriptions"""
    embed = discord.Embed(
        title="StardewSavvy Commands",
        description="Here are all the available commands to help you with Stardew Valley!",
        color=0x000000
    )
    
    # Add command fields
    embed.add_field(
        name="/gift",
        value="Shows loved and liked gifts for a villager\n*Usage: `/gift townsperson:Alex`*",
        inline=False
    )
    
    embed.add_field(
        name="/char", 
        value="Shows character profile including birthday\n*Usage: `/char townsperson:Abigail`*",
        inline=False
    )
    
    embed.add_field(
        name="/build",
        value="Shows materials and cost for farm buildings\n*Usage: `/build building:Barn`*", 
        inline=False
    )
    
    embed.add_field(
        name="/events",
        value="Shows events for a season or specific day\n*Usage: `/events season:Spring` or `/events season:Spring day:15`*",
        inline=False
    )
    
    embed.add_field(
        name="🏠 /house",
        value="Shows house upgrades or renovations\n*Usage: `/house category:upgrades`*",
        inline=False
    )
    
    embed.add_field(
        name="/fish",
        value="Shows detailed fish info (location, time, season, difficulty, prices)\n*Usage: `/fish fish_name:Pufferfish`*",
        inline=False
    )
    
    embed.add_field(
        name="/crop",
        value="Shows detailed crop info (seasons, growth, prices, etc.)\n*Usage: `/crop crop_name:Parsnip`*",
        inline=False
    )
    
    await ctx.send(embed=embed)


bot.run(os.getenv('BOT_TOKEN'))