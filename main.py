import discord
import os
import requests
import json
import random
from replit import db

client=discord.Client()

sad_words=["sad","depressed","angry","miserable","depressing","unhappy","pissed"]

starter_encouragements=["Cheer Up!","Hang in there","You are great","Look around the amazing world"]

def update_encouragements(encouraging_message):
  if "encouragements" in db.keys():
    encouragements=db["encouragements"]
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
    await message.channel.send("Updated encouragements are"+ encouragements)

client.run(os.getenv('TOKEN')) 