import discord
import os
import requests
import json
import random
from replit import db
from keep_alive import keep_alive
import math
import random


client=discord.Client()

sad_words=["sad","depressed","angry","miserable","depressing","unhappy","pissed"]

starter_encouragements=["Cheer Up!","Hang in there","You are great","Look around the amazing world"]


if "responding" not in db.keys():
  db["responding"]=True

def update_encouragements(encouraging_message):
  if "encouragements" in db.keys():
    encouragements=db["encouragements"]
    if encouraging_message not in encouragements:
      encouragements.append(encouraging_message)
      db["encouragements"]=encouragements
  else:
    db["encouragements"]=[encouraging_message]

def delete_encouragements(index):
  encouragements=db["encouragements"]
  if len(encouragements)>index:
    del encouragements[index]
    db["encouragements"]=encouragements

def get_quote():
  response=requests.get("https://zenquotes.io/api/random")
  jsonData=json.loads(response.text)
  quote=(jsonData[0]['q']+" - "+ jsonData[0]['a'])
  return quote

def get_gif(keywords):
  url="https://g.tenor.com/v1/search?q={}&key=${}".format(keywords,os.getenv('TENORKEY'))
  response=requests.get(url)
  jsonData=json.loads(response.text)
  index=math.floor(random.random()*len(jsonData['results']))
  return jsonData['results'][index]['url']

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author==client.user:
    return
  msg=message.content
  
  if msg.startswith('$inspire'):
    await message.channel.send(get_quote())
  if db["responding"]:
    options=starter_encouragements
    if "encouragements" in db.keys():
      options+=db["encouragements"]
      
    if any(word in msg for word in sad_words):
      await message.channel.send(random.choice(options))
  
  if msg.startswith("$new"):
    encouraging_message=msg.split("$new ",1)[1]
    update_encouragements(encouraging_message)
    await message.channel.send("New encouraging message is added.")
  
  if msg.startswith("$del"):
    encouragements=[]
    if "encouragements" in db.keys():
      index=int(msg.split("$del ",1)[1])
      delete_encouragements(index)
      encouragements=db["encouragements"]
    await message.channel.send(encouragements)
  
  if msg.startswith("$list"):
    encouragements=[]
    if "encouragements" in db.keys():
      encouragements=db["encouragements"]
    await message.channel.send(encouragements)
  
  if msg.startswith("$responding"):
    value=msg.split("$responding ",1)[1]
    if value.lower()=="true":
      db["responding"]=True
    else:
      db["responding"]=False
    await message.channel.send("Responding is "+value)
   
  if msg.startswith("$gif"):
    keywords=msg.split("$gif ",1)[1]
    await message.channel.send(get_gif(keywords))




keep_alive()
client.run(os.getenv('TOKEN')) 

