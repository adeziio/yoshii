import re
import discord
import os
import random
from datetime import date
from discord.ext import tasks
from var import greetings, goodbyes, whitelist, peacemaker, custom_keywords, insults_keywords
from server import keep_alive
from dotenv import load_dotenv, find_dotenv
from utils import get_sentiment_analysis, get_insp_quote, get_roasted, get_photo_searcher_cat, get_joke, get_google_searcher, \
    get_insults, random_game_status, random_song_status, get_chatbot, get_custom_response, update_karma_point, get_karma, get_karma_point, \
    get_karma_ranking

load_dotenv(find_dotenv())

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
isActive = True


@client.event
async def on_ready():
    change_status.start()
    print("Name\t: {0.user}".format(client))
    print("Version\t: 2.0.0")
    print("Status\t: active")


@client.event
async def on_message(message):
    # print(message.author.id, message.author, message.guild.id,
    #       message.guild.name, message.author.display_name)
    global isActive

    text = message.content.lower()

    if (date.today().month == 12):
        try:
            update_karma_point(message.author.id,
                               message.guild.id, get_sentiment_analysis(text))
        except Exception:
            None

    if isActive:
        if message.author == client.user:
            return

        isWhitelisted = str(message.author.id) in whitelist

        if ("yoshii" in text or client.user in message.mentions):
            async with message.channel.typing():
                text = text.replace("yoshii", "")
                text = re.sub(' +', ' ', text)
                text = text.strip()

                # Sleep
                if ("go to sleep" in text) or ("offline" in text):
                    isActive = False
                    await client.change_presence(status=discord.Status.idle, activity=None)
                    await message.channel.send(random.choice(goodbyes))

                # Check karma
                elif ("karma" in text or "naughty list" in text):
                    if (date.today().month == 12):
                        if ("my" in text):
                            if ("point" in text):
                                await message.channel.send(get_karma_point(message.author.id, message.guild.id))
                            else:
                                await message.channel.send(get_karma(message.author.id, message.guild.id, "Your"))
                        elif ("your" in text or "ur" in text):
                            if ("point" in text):
                                await message.channel.send(get_karma_point(client.user.id, message.guild.id))
                            else:
                                await message.channel.send(get_karma(client.user.id, message.guild.id, "My"))
                        elif ("ranking" in text or "leaderboard" in text or "naughty list" in text):
                            karma_ranking = get_karma_ranking(
                                message.guild.id, text)
                            if (len(karma_ranking) > 0):
                                serverName = await client.fetch_guild(int(message.guild.id))
                                title = f""
                                description = f""

                                colour = discord.Colour.orange()
                                embed = discord.Embed(
                                    title=title,
                                    description=description,
                                    colour=colour,
                                )
                                row = ""
                                for i in range(len(karma_ranking)):
                                    user = await client.fetch_user(int(karma_ranking[i]['id'].split('-')[0]))
                                    user_name = user.name
                                    karma_point = int(
                                        karma_ranking[i]['karma_point'])
                                    emoji = "😐"
                                    if (karma_point > 0):
                                        emoji = "😇"
                                    elif (karma_point < 0):
                                        emoji = "💀"
                                    else:
                                        emoji = "😐"
                                    row += f"{emoji} {user_name}  ({karma_point})" + "\n"
                                embed.add_field(name=f"🎄🎅 Yoshii's Naughty List {int(karma_ranking[i]['karma_year'])} 🎅🎄",
                                                value=row, inline=True)
                                embed.set_footer(
                                    text=f"")
                                await message.channel.send(embed=embed)
                            else:
                                await message.channel.send("Karma Ranking does not exist.")
                        else:
                            await message.channel.send("I'm not sure what you're asking.")
                    else:
                        await message.channel.send("This feature is only available during the Christmas season 🎅")

                # Sentiment check
                elif get_sentiment_analysis(text) == 'negative' and not isWhitelisted:
                    await message.channel.send(random.choice(peacemaker))

                # Custom response
                elif any(item in text for item in custom_keywords):
                    await message.channel.send(get_custom_response(text, message.author.display_name))

                # Random inspirational quote
                elif ("inspire" in text) or ("inspirational" in text) or ("inspiration" in text):
                    await message.channel.send(get_insp_quote())

                # Manual roast
                elif ("roast" in text):
                    await message.channel.send(get_roasted(" ".join(text.split(' ')[1:])))

                # Random cat photos
                elif ("cat" in text) or ("cat photo" in text) or ("cat photos" in text):
                    await message.channel.send(embed=get_photo_searcher_cat())

                # Random joke
                elif ("joke" in text):
                    await message.channel.send(get_joke())

                # Google search
                elif ("search up" in text) or ("look up" in text) or ("google" in text) or ("search" in text):
                    await message.channel.send(get_google_searcher(text))

                # Default chatbot
                else:
                    await message.channel.send(get_chatbot(text))

        # Default roast
        else:
            for word in insults_keywords:
                if word in text.lower():
                    ran_num = random.randint(1, 2)
                    if ran_num == 1:
                        if not isWhitelisted:
                            async with message.channel.typing():
                                await message.channel.send(get_insults(word))

    # Not active
    else:
        if ("yoshii" in text):
            async with message.channel.typing():
                if ("wake up" in text) or ("get up" in text) or ("online" in text):
                    isActive = True
                    await client.change_presence(status=discord.Status.online, activity=None)
                    await message.channel.send(random.choice(greetings))
                else:
                    await message.channel.send("I'm sleeping...zzZ...ZzZZ")
                    await message.channel.send("Wake me up or go away!")


@tasks.loop(seconds=900)
async def change_status():
    global isActive
    isActive = True
    ran_num = random.randint(1, 2)
    if ran_num == 1:
        # Setting `Playing ` status
        await client.change_presence(status=discord.Status.online, activity=random_game_status())
    if ran_num == 2:
        # Setting `Listening ` status
        await client.change_presence(activity=random_song_status())

keep_alive()
client.run(os.getenv('YOSHII_TOKEN'))
