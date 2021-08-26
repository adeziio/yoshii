import discord
import os
import random
import requests
import json
from keep_alive import keep_alive

client = discord.Client()

isActive = True

insults_keywords = [
  'funny',
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

roast_blacklist = [
  "I'm Not Short",
  "ruen-"
]

def get_insults(word):
  return random.choice(insults_output) + word

def get_insp_quote(person):
  omit = ["i", "me", "he", "she", "her", "him"]
  res_data = json.loads(requests.get("https://zenquotes.io/api/random").text)
  quote = res_data[0]['q']
  # author = res_data[0]['a']
  inspire = "{0}".format(quote)
  return person.capitalize() + ". " + inspire if person.lower() not in omit else "" + inspire

def get_roasted(person):
  omit = ["i", "me", "he", "she", "her", "him", "thien", "aden", "thein", "thienn", "adenn", "theinn"]
  repsonses = ["nah", "no", "try again", "wut"]
  if person.lower() in omit:
    return random.choice(repsonses)
  else:
    return requests.get("https://insult.mattbas.org/api/en/insult.txt?who="+person.capitalize()).text

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
  if message.content.startswith("yoshii wake up"):
    isActive = True
    await message.channel.send(random.choice(greetings))
  elif message.content.startswith("yoshii sleep") and message.author.name == "Adezi":
    isActive = False
    await message.channel.send(random.choice(goodbyes))

  if isActive:
    # print(message.author.name)
    # Prevent infinite loop
    if message.author == client.user:
      return

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
      await message.channel.send(get_insp_quote(message.content.split(' ')[-1]))

    # Random roasts
    elif message.content.startswith("yoshii roast ") and message.author.name not in roast_blacklist:
      await message.channel.send(get_roasted(message.content.split(' ')[-1]))

    # Output the list of insults_keywords
    elif message.content.startswith("yoshii keywords?"):
      await message.channel.send(insults_keywords)
    
    # Default greetings
    elif message.content.endswith("yoshii"):
      await message.channel.send(random.choice(greetings))

    # Last condition
    # Listening for insults_keywords
    else:
      for word in insults_keywords:
        if word in message.content.lower():
          ran_num = random.randint(1, 1)
          if ran_num == 1:
            await message.channel.send(get_insults(word))

keep_alive()
client.run(os.getenv('BOT_TOKEN'))