#john_ bot created by Maishi

import os, requests, discord, emoji
from dotenv import load_dotenv

load_dotenv()
discord_token = os.getenv("DISCORD_TOKEN")
weather_api = os.getenv("WEATHER_API")

#bot set up

testing_server_list = [810369462627860531]

intends = discord.Intents.default()
intends.message_content = True

bot = discord.Bot()

@bot.event
async def on_ready():
    print('We have been logged on {0}'.format(bot.user))

#pong command

@bot.slash_command(guild_ids=testing_server_list,name="ping",description="Check the latency of the bot")
async def ping(ctx):
    embed = discord.Embed(title="PONG! 🏓", description="{0}ms".format(round(bot.latency*1000, 2)), color=0xFFFFFF)
    await ctx.respond(embed=embed)

#weather command

@bot.slash_command(guild_ids=testing_server_list,name="weather",description="How's the day in you city?")
async def ping(ctx: discord.ApplicationContext, city: str):
    key = 'http://api.weatherapi.com/v1/current.json?key={0}&q={1}&aqi=no'.format(weather_api,city)

    response = requests.get(key)

    if response.status_code == 200:
        data = response.json()

        city_name = data["location"]["name"]
        country = data["location"]["country"]
        emoji_country = emoji.emojize(":flag_for_{0}:".format(country.replace(" ", "_")), language='alias')
        condition = data["current"]["condition"]["text"]
        condition_image = "https:{0}".format(data["current"]["condition"]["icon"])
        temperature = "{0} °C | {1} °F".format(data["current"]["temp_c"],data["current"]["temp_f"])
        local_time = data["location"]["localtime"]
        last_updated = data["current"]["last_updated"]

        embed = discord.Embed(title=condition, color=0xFFFFFF)
        embed.set_author(name=f"{city_name} / {country} {emoji_country}")
        embed.set_thumbnail(url=condition_image)
        embed.add_field(name=temperature, value="Temperature", inline=True)
        embed.add_field(name=local_time,value="Local Time", inline=True)
        embed.set_footer(text=f"Last Update: {last_updated}")

        await ctx.respond(embed=embed)
    else:
        await ctx.respond("There was an error, sorry.")

bot.run(discord_token)

