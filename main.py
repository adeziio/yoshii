import discord
import os
import random
from keep_alive import keep_alive
from discord.ext import tasks
from var import greetings, goodbyes, whitelist, peacemaker, insults_keywords, roast_blacklist
from func import sentiment_analysis, get_insp_quote, get_roasted, photo_searcher_cat, get_joke, google_searcher, get_insults, random_game_status, random_song_status

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
  if message.content.startswith("yoshii status"):
    await message.channel.send("I'm awake!" if isActive else "I'm asleep...zZzZzZ")

  # Set awake or sleep
  if message.content.startswith("yoshii wake up"):
    isActive = True
    await message.channel.send(random.choice(greetings))
  elif message.content.startswith("yoshii sleep"):
    isActive = False
    await client.change_presence(status=discord.Status.idle, activity=None)
    await message.channel.send(random.choice(goodbyes))

  # Do these only when active
  if isActive:
    # print(message.author.name, message.author.id, type(message.author.id))
    # Prevent infinite loop
    if message.author == client.user:
      return

    elif sentiment_analysis(message.content) == 'negative' and (str(message.author.id) not in whitelist):
      ran_num = random.randint(1,4)
      if ran_num == 1:
        await message.channel.send(random.choice(peacemaker))

    # Add to insults_keywords
    elif message.content.startswith("yoshii add "):
      await message.channel.send(message.content.split(' ')[-1] + " added to keywords")
      if message.content.split(' ')[-1] not in insults_keywords:
        insults_keywords.append(message.content.split(' ')[-1])

    # Remove from insults_keywords
    elif message.content.startswith("yoshii remove "):
      await message.channel.send(message.content.split(' ')[-1] + " removed from keywords")
      if message.content.split(' ')[-1] in insults_keywords:
        insults_keywords.remove(message.content.split(' ')[-1])

    # Random inspirational quotes
    elif message.content.startswith("yoshii inspire "):
      await message.channel.send(get_insp_quote(message.content.split(' ')[2:]))

    # Random roasts
    elif message.content.startswith("yoshii roast "):
      if str(message.author.id) not in roast_blacklist:
        await message.channel.send(get_roasted(message.content.split(' ')[2:]))
      else:
        await message.channel.send("nah, ur banned")
    
    # Random cat photos
    elif message.content.startswith("yoshii cat"):
      await message.channel.send(embed=photo_searcher_cat())

    # Random joke
    elif message.content.startswith("yoshii tell a joke"):
      await message.channel.send(get_joke())

    # Output the list of insults_keywords
    elif message.content.startswith("yoshii keywords"):
      await message.channel.send(insults_keywords)
    
    # Default greetings
    elif message.content.endswith("yoshii"):
      await message.channel.send(random.choice(greetings))

    # Google search
    elif message.content.startswith("yoshii "):
      await message.channel.send(embed=google_searcher(message.content.split(' ')[1:]))
    
    # Last condition
    else:
      for word in insults_keywords:
        if word in message.content.lower():
          ran_num = random.randint(1, 1)
          if ran_num == 1:
            if (str(message.author.id) not in whitelist):
              await message.channel.send(get_insults(word))

@tasks.loop(seconds=900)
async def change_status():
  ran_num = random.randint(1,2)
  if ran_num == 1:
    # Setting `Playing ` status
    await client.change_presence(status=discord.Status.online, activity=random_game_status())
  if ran_num == 2:
    # Setting `Listening ` status
    await client.change_presence(activity=random_song_status())

keep_alive()
client.run(os.getenv('BOT_TOKEN'))