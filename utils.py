import discord
import requests
import random
import os
from var import game_list, insults_keywords, insults_output, greetings, custom_keywords, non_responsive_output

freeflashUrl = "https://freeflash.vercel.app"
headers = {
    "FREEFLASH_API_KEY": os.getenv('FREEFLASH_API_KEY')
}


def random_game_status():
    return discord.Game(name=random.choice(game_list))


def random_song_status():
    return discord.Activity(type=discord.ActivityType.listening, name="Spotify")


def get_insults(word):
    return random.choice(insults_output) + word


def get_insp_quote():
    json_res = requests.get(
        freeflashUrl+"/quote?mode=random", headers=headers).json()
    quote = json_res['q']
    # author = json_res['a']
    inspire = "{0}".format(quote)
    return inspire


def get_roasted(person):
    omit = ["天", "yoshii", "yoshi", "i", "me", "he", "she", "her",
            "him", "thien", "aden", "thein", "thienn", "adenn", "theinn"]
    repsonses = ["nah", "no", "try again", "wut"]
    if person.lower() in omit:
        return random.choice(repsonses)
    else:
        return requests.get(freeflashUrl+"/insult?who="+person.capitalize(), headers=headers).text


def get_photo_searcher_cat():
    cat_photo_res = requests.get(
        freeflashUrl+"/cat?mode=image", headers=headers).json()
    cat_photo_url = cat_photo_res['url']
    cat_photo_width = cat_photo_res['width']
    cat_photo_height = cat_photo_res['height']
    cat_fact = requests.get(freeflashUrl+"/cat?mode=fact",
                            headers=headers).json()['fact']
    embed = discord.Embed(
        title='Fun Fact 🐈',
        description=cat_fact,
        colour=discord.Colour.purple(),
        width=cat_photo_width,
        height=cat_photo_height
    )
    embed.set_image(url=cat_photo_url)
    embed.set_footer(text="")
    return embed


def get_joke():
    return requests.get(freeflashUrl+"/joke", headers=headers).json()['joke']


def get_google_searcher(search):
    payload = {
        "mode": "search",
        "search": search
    }
    try:
        res = requests.post(freeflashUrl+"/google",
                            json=payload, headers=headers).json()
        link = res['results'][0]['additional_links'][0]['href']
    except:
        link = "I can't find anything..."
    return link


def get_sentiment_analysis(text):
    response = requests.get(
        freeflashUrl+"/sentiment-analysis?text="+text, headers=headers).json()
    if response['ok']:
        return response['sentiment']
    else:
        return ""


def get_chatbot(search):
    payload = {
        "input": search
    }
    try:
        response = requests.post(
            freeflashUrl+"/yoshii", json=payload, headers=headers).json()
        if response:
            return response['output']
        else:
            return random.choice(greetings)
    except:
        return random.choice(greetings)


def get_custom_response(text, display_name):
    output = random.choice(non_responsive_output)
    for key in custom_keywords:
        if key in text:
            if key == "my name":
                output = f'Your name is {display_name}'
            elif key == "my real name":
                output = f'Your real name is {display_name}'

    return output
