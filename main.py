import discord
import os
import random
from discord.ext import tasks
from var import greetings, goodbyes, whitelist, peacemaker, insults_keywords, roast_blacklist
from func import sentiment_analysis, get_insp_quote, get_roasted, photo_searcher_cat, get_joke, google_searcher, get_insults, random_game_status, random_song_status, get_chatbot

client = discord.Client()
isActive = True


@client.event
async def on_ready():
    change_status.start()
    print("Logged in as {0.user}".format(client))


@client.event
async def on_message(message):
    global isActive

    # Check status
    if(message.content.startswith("yoshii")):
        async with message.channel.typing():
            if "status" in message.content:
                await message.channel.send("I'm awake!" if isActive else "I'm asleep...zZzZzZ")
                return

            # Set awake or sleep
            if ("wake up" in message.content) or ("get up" in message.content) or ("online" in message.content):
                isActive = True
                await client.change_presence(status=discord.Status.online, activity=None)
                await message.channel.send(random.choice(greetings))
                return
            elif ("sleep" in message.content) or ("mute" in message.content) or ("offline" in message.content):
                isActive = False
                await client.change_presence(status=discord.Status.idle, activity=None)
                await message.channel.send(random.choice(goodbyes))
                return

    # Do these only when active
    if isActive:
        # print(message.author.name, message.author.id, type(message.author.id))
        # Prevent infinite loop
        if message.author == client.user:
            return
        if(message.content.startswith("yoshii")):
            async with message.channel.typing():
                text = " ".join(message.content.split(' ')[1:])

                if sentiment_analysis(text) == 'negative':
                    ran_num = random.randint(1, 4)
                    if ran_num == 1:
                        await message.channel.send(random.choice(peacemaker))

                # Random inspirational quote
                elif ("inspire" in text) or ("inspirational" in text) or ("inspiration" in text):
                    await message.channel.send(get_insp_quote())

                # Manual roast
                elif ("roast" in text):
                    if str(message.author.id) not in roast_blacklist:
                        await message.channel.send(get_roasted(" ".join(text.split(' ')[1:])))
                    else:
                        await message.channel.send("nah, ur banned")

                # Random cat photos
                elif ("cat" in text) or ("cat photo" in text) or ("cat photos" in text):
                    await message.channel.send(embed=photo_searcher_cat())

                # Random joke
                elif ("joke" in text):
                    await message.channel.send(get_joke())

                # Google search
                elif ("search up" in text) or ("look up" in text) or ("google" in text) or ("search" in text):
                    await message.channel.send(embed=google_searcher(text))

                # Default greetings
                elif text.endswith("yoshii"):
                    await message.channel.send(random.choice(greetings))

                # Default chatbot
                else:
                    await message.channel.send(get_chatbot(text))

        # Default roast
        else:
            for word in insults_keywords:
                if word in message.content.lower():
                    ran_num = random.randint(1, 2)
                    if ran_num == 1:
                        if (str(message.author.id) not in whitelist):
                            await message.channel.send(get_insults(word))


@tasks.loop(seconds=900)
async def change_status():
    ran_num = random.randint(1, 2)
    if ran_num == 1:
        # Setting `Playing ` status
        await client.change_presence(status=discord.Status.online, activity=random_game_status())
    if ran_num == 2:
        # Setting `Listening ` status
        await client.change_presence(activity=random_song_status())

client.run(os.getenv('YOSHII_TOKEN'))
