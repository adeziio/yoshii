import re
import discord
import os
import random
from discord.ext import tasks
from var import greetings, goodbyes, whitelist, peacemaker, custom_keywords, insults_keywords, roast_blacklist
from utils import get_sentiment_analysis, get_insp_quote, get_roasted, get_photo_searcher_cat, get_joke, get_google_searcher, get_insults, random_game_status, random_song_status, get_chatbot, get_custom_response

client = discord.Client()
isActive = True


@client.event
async def on_ready():
    change_status.start()
    print("Logged in as {0.user}".format(client))


@client.event
async def on_message(message):
    global isActive

    text = message.content.lower()

    if isActive:
        # print(message.author.name, message.author.id, type(message.author.id))

        if message.author == client.user:
            return

        isBlacklisted = str(message.author.id) in roast_blacklist
        isWhitelisted = str(message.author.id) in whitelist

        if("yoshii" in text):
            async with message.channel.typing():
                text = text.replace("yoshii", "")
                text = re.sub(' +', ' ', text)
                text = text.strip()

                # Do not respond to blacklisted people
                if isBlacklisted:
                    await message.channel.send(get_insults(random.choice(insults_keywords)))
                    return

                # Sleep
                if ("go to sleep" in text) or ("offline" in text):
                    isActive = False
                    await client.change_presence(status=discord.Status.idle, activity=None)
                    await message.channel.send(random.choice(goodbyes))

                # Sentiment check
                elif get_sentiment_analysis(text) == 'negative' and not isWhitelisted:
                    await message.channel.send(random.choice(peacemaker))

                # Custom response
                elif any(item in text for item in custom_keywords):
                    if isBlacklisted:
                        await message.channel.send(get_custom_response(text, random.choice(insults_keywords)))
                    else:
                        await message.channel.send(get_custom_response(text, message.author.display_name))

                # Random inspirational quote
                elif ("inspire" in text) or ("inspirational" in text) or ("inspiration" in text):
                    await message.channel.send(get_insp_quote())

                # Manual roast
                elif ("roast" in text):
                    if not isBlacklisted:
                        await message.channel.send(get_roasted(" ".join(text.split(' ')[1:])))
                    else:
                        await message.channel.send(get_insults(random.choice(insults_keywords)))

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
        if("yoshii" in text):
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

client.run(os.getenv('YOSHII_TOKEN'))
