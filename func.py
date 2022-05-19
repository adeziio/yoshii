import discord
import os
import requests
import json
import random
from var import game_list, insults_output, greetings

def random_game_status():
  return discord.Game(name=random.choice(game_list))

def random_song_status():
  return discord.Activity(type=discord.ActivityType.listening, name="Spotify")

def get_insults(word):
  return random.choice(insults_output) + word

def get_insp_quote():
  json_res = requests.get("https://zenquotes.io/api/random").json()
  quote = json_res[0]['q']
  # author = json_res[0]['a']
  inspire = "{0}".format(quote)
  return inspire

def get_roasted(person):
  omit = ["天", "yoshii", "yoshi", "i", "me", "he", "she", "her", "him", "thien", "aden", "thein", "thienn", "adenn", "theinn"]
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

def google_searcher(search):
  headers = {
    'x-rapidapi-host': "google-search3.p.rapidapi.com",
    'x-rapidapi-key': os.getenv('RAPID_API_KEY')
  }
  try:
    search_image = requests.get("https://google-search3.p.rapidapi.com/api/v1/images/q="+search, headers=headers).json()['image_results'][0]
    image_url = search_image['image']['src']
  except:
    image_url = ""
  
  try:
    search = requests.get("https://google-search3.p.rapidapi.com/api/v1/search/q="+search, headers=headers).json()['results'][0]
    search_title = search['title']
    search_link = search['link']
    search_description = search['description']
  except:
    search_title = ""
    search_description = ""
    search_link = ""

  embed = discord.Embed(
          title = search_title,
          description = search_description,
          url = search_link,
          colour = discord.Colour.blue()
          )
  embed.set_image(url=image_url)
  embed.set_footer(text="")
  return embed

def sentiment_analysis(text):
  url = "https://text-analysis12.p.rapidapi.com/sentiment-analysis/api/v1.1"
  payload = {
    "language": "english",
    "text": text
  }
  headers = {
    'content-type': "application/json",
    'x-rapidapi-host': "text-analysis12.p.rapidapi.com",
    'x-rapidapi-key': os.getenv("RAPID_API_KEY")
  }

  response = requests.post(url, data=json.dumps(payload), headers=headers).json()
  if response['ok']:
    return response['sentiment']
  else:
    return ""

def get_chatbot(search):
  search = search.lower().replace("yoshii", "RoboMatic")
  search = search.lower().replace("+", "%2B")
  url = "https://robomatic-ai.p.rapidapi.com/api.php"
  
  payload = "in=" + search + "F&op=in&cbot=1&SessionID=RapidAPI1&ChatSource=RapidAPI&cbid=1&key=" + os.getenv("ROBOMATIC_KEY")
  headers = {
      'content-type': "application/x-www-form-urlencoded",
      'x-rapidapi-host': "robomatic-ai.p.rapidapi.com",
      'x-rapidapi-key': os.getenv("RAPID_API_KEY")
      }
  
  response = requests.request("POST", url, data=payload, headers=headers).json()
  if response:
    try:
      resMsg = response['out']
      resMsg = resMsg.replace("I said it before, ", "")
      resMsg = resMsg.replace("RoboMatic", "yoshii")
      resMsg = resMsg.replace("Ehab Elagizy", "Aden Tran")
      resMsg = resMsg.replace("back in 2001", "back in 2021")
      resMsg = resMsg.replace("since 1995", "since 2021")
      resMsg = resMsg.replace("Later in 2011", "In 2021")
      resMsg = resMsg.replace("Egyptian", "Vietnamese")
      return resMsg
    except Exception:
      return random.choice(greetings)
  else:
    return random.choice(greetings)