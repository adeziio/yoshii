import discord
import os
import random
import requests
import json

client = discord.Client()

urface_keywords = [
  'poop',
  'huge',
  'dumb',
  'stupid',
  'ugly',
  'big',
  'sad'
]

greetings = [
  "Ooga! Yoshi boogie!",
  "Yoshi! Yoshi!",
  "YOSHI, FAIRY OF DRAGON FLAME!!!",
  "Hey! I still hungry!",
  "Oogabooga! I ready, and hungry!",
  "YOSHI TO RESCUE!!!"
]

def get_quote():
  res_data = json.loads(requests.get("https://zenquotes.io/api/random").text)
  quote = "\"{0}\" \n- {1}".format(res_data[0]['q'], res_data[0]['a'])
  return quote

@client.event
async def on_ready():
  print("Logged in as {0.user}".format(client))


@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.endswith("yoshii"):
    await message.channel.send(random.choice(greetings))
  
  for word in urface_keywords:
    if word in message.content:
      await message.channel.send("Your face is {}!".format(word))

  if message.content.startswith("yoshii") and "inspire" in message.content:
    await message.channel.send(get_quote())

client.run(os.getenv('BOT_TOKEN'))