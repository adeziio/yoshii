import discord
import os
import random
import requests
from keep_alive import keep_alive

client = discord.Client()

isActive = True

insults_keywords = [
  'crazy',
  'funny',
  'poop',
  'huge',
  'dumb',
  'stupid',
  'stoopid',
  'ugly',
  'big',
  'sad',
  'fat',
  'apple',
  'weird',
  'scary'
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
  "Oogabooga! I ready, and hungry!",
  "YOSHI TO RESCUE!!!"
]

goodbyes = [
  "Scooze me!",
  "This means war!",
  "Nooooooo",
  "Ohhhh.... Yoshi no feel good!",
  "Aww, do I have to go to bed so soon?",
  "Night, Mama Luigi!",
  "Hey! I still hungry!",
]

roast_blacklist = [
  "I'm Not Short",
  "ruen-"
]

# ---------------------------------------------------------------------------------------------------------------------------

def get_insults(word):
  return random.choice(insults_output) + word

def get_insp_quote(person):
  omit = ["i", "me", "he", "she", "her", "him"]
  json_res = requests.get("https://zenquotes.io/api/random").json()
  quote = json_res[0]['q']
  # author = json_res[0]['a']
  inspire = "{0}".format(quote)
  return person.capitalize() + ". " + inspire if person.lower() not in omit else "" + inspire

def get_roasted(person):
  omit = ["yoshii", "yoshi", "i", "me", "he", "she", "her", "him", "thien", "aden", "thein", "thienn", "adenn", "theinn"]
  repsonses = ["nah", "no", "try again", "wut"]
  if person.lower() in omit:
    return random.choice(repsonses)
  else:
    return requests.get("https://insult.mattbas.org/api/en/insult.txt?who="+person.capitalize()).text

def photo_searcher_cat():
  cat_photo_res = requests.get("https://api.thecatapi.com/v1/images/search").json()[0]
  cat_photo_url = cat_photo_res['url']
  cat_photo_width = cat_photo_res['width']
  cat_photo_height = cat_photo_res['height']
  cat_fact =  requests.get("https://catfact.ninja/fact").json()['fact']
  embed = discord.Embed(
          title = 'Fun Fact 🐈',
          description = cat_fact,
          colour = discord.Colour.purple(),
          width = cat_photo_width,
          height = cat_photo_height
          )
  embed.set_image(url=cat_photo_url)
  embed.set_footer(text="")
  return embed

def get_joke():
  return requests.get("https://v2.jokeapi.dev/joke/Any?type=single").json()['joke']

def google_searcher(searchList):
  newSearch = ""
  for search in searchList:
    newSearch += search + "+"
  headers = {
    'x-rapidapi-host': "google-search3.p.rapidapi.com",
    'x-rapidapi-key': os.getenv('GOOGLE_SEARCH_TOKEN')
    }
  search_image = requests.get("https://google-search3.p.rapidapi.com/api/v1/images/q="+newSearch, headers=headers).json()['image_results'][0]
  search = requests.get("https://google-search3.p.rapidapi.com/api/v1/search/q="+newSearch, headers=headers).json()['results'][0]
  image_url = search_image['image']['src']
  search_title = search['title']
  search_link = search['link']
  search_description = search['description']

  embed = discord.Embed(
          title = search_title,
          description = search_description,
          url = search_link,
          colour = discord.Colour.blue()
          )
  embed.set_image(url=image_url)
  embed.set_footer(text="")
  return embed

# ---------------------------------------------------------------------------------------------------------------------------

@client.event
async def on_ready():
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
    await message.channel.send(random.choice(goodbyes))

  # Do these only when active
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
    
    # Random cat photos
    elif message.content.startswith("yoshii cat"):
      await message.channel.send(embed=photo_searcher_cat())

    # Random joke
    elif message.content.startswith("yoshii tell a joke"):
      await message.channel.send(get_joke())

     # Google search
    elif message.content.startswith("yoshii search "):
      await message.channel.send(embed=google_searcher(message.content.split(' ')[2:]))

    # Output the list of insults_keywords
    elif message.content.startswith("yoshii keywords"):
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
            if (message.author.name != "adeziio"):
              await message.channel.send(get_insults(word))
# ---------------------------------------------------------------------------------------------------------------------------
keep_alive()
client.run(os.getenv('BOT_TOKEN'))