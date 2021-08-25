import discord
import os
import random
import requests
import json
from keep_alive import keep_alive

client = discord.Client()

isActive = True

insults_keywords = [
  'gay',
  'poop',
  'huge',
  'dumb',
  'stupid',
  'ugly',
  'big',
  'sad',
  'fat',
  'apple',
  'weird',
  'scary',
  ':face_vomiting:',
  ':skull:',
  ':moyai:'
]

insults_output = [
  "ur face is ",
  "u look like a ",
  "boi ur forehead is ",
  "ur mum is ",
  "boi ur face is ",
  "boi ya look like a "
]

greetings = [
  "Ooga! Yoshi boogie!",
  "Yoshi! Yoshi!",
  "YOSHI, FAIRY OF DRAGON FLAME!!!",
  "Hey! I still hungry!",
  "Oogabooga! I ready, and hungry!",
  "YOSHI TO RESCUE!!!"
]

goodbyes = [
  "Scooze me!",
  "This means war!",
  "Nooooooo",
  "Ohhhh.... Yoshi no feel good!",
  "Aww, do I have to go to bed so soon?",
  "Night, Mama Luigi!"
]

def get_insults(word):
  return random.choice(insults_output) + word

def get_insp_quote():
  res_data = json.loads(requests.get("https://zenquotes.io/api/random").text)
  quote = "\"{0}\" \n- {1}".format(res_data[0]['q'], res_data[0]['a'])
  return quote

@client.event
async def on_ready():
  print("Logged in as {0.user}".format(client))

@client.event
async def on_message(message):
  global isActive

  # Check status 
  if message.content.startswith("yoshii") and "status" in message.content:
    await message.channel.send("I'm awake!" if isActive else "I'm asleep...zZzZzZ")

  # Set awake or sleep
  if message.content.startswith("yoshii") and "awake" in message.content:
    isActive = True
    await message.channel.send(random.choice(greetings))
  elif message.content.startswith("yoshii") and "sleep" in message.content:
    isActive = False
    await message.channel.send(random.choice(goodbyes))

  if isActive:
    if message.author == client.user:
      return

    elif message.content.startswith("yoshii") and "add " in message.content:
      await message.channel.send(message.content.split(' ')[-1] + " added to keywords")
      if message.content.split(' ')[-1] not in insults_keywords:
        insults_keywords.append(message.content.split(' ')[-1])

    elif message.content.startswith("yoshii") and "remove " in message.content:
      await message.channel.send(message.content.split(' ')[-1] + " removed from keywords")
      if message.content.split(' ')[-1] in insults_keywords:
        insults_keywords.remove(message.content.split(' ')[-1])

    elif message.content.startswith("yoshii") and "inspire" in message.content:
      await message.channel.send(get_insp_quote())

    elif message.content.startswith("yoshii") and "keywords" in message.content:
      await message.channel.send(insults_keywords)
    
    elif message.content.endswith("yoshii"):
      await message.channel.send(random.choice(greetings))

    else:
      for word in insults_keywords:
        if word in message.content.lower():
          ran_num = random.randint(1, 2)
          if ran_num == 1:
            await message.channel.send(get_insults(word))

# keep_alive()
client.run(os.getenv('BOT_TOKEN'))