#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#By CamelJuno 🐪

import discord
import requests
import random
import json
import base64
import string
import time

client = discord.Client()

def getJUNOGecko():
  headers = {
    'Host': 'api.coingecko.com',
    'Accept': '*/*'
  }
  a = requests.get('https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=juno-network',headers=headers,timeout=10)
  if a.status_code == 200:
    z = json.loads(a.text)[0]['current_price']
    if z == None:
      getJUNOGecko()
    else:
      return z
  else:
    getJUNOGecko()

def getNETA2JUNO():
  headers = {
    'Host': 'rpc-juno.itastakers.com',
    'Content-Type': 'application/json',
  }
  jsonData = {"jsonrpc":"2.0","id":genId(),"method":"abci_query","params":{"path":"/cosmwasm.wasm.v1.Query/SmartContractState","data":"0a3f6a756e6f3165386e366368376d736b7334383765637a6e796561676d7a64356d6c327071397467656471743275363376726130713072396d71726a7936797312377b22746f6b656e325f666f725f746f6b656e315f7072696365223a7b22746f6b656e325f616d6f756e74223a2231303030303030227d7d","prove":False}}
  a = requests.post('https://rpc-juno.itastakers.com/',headers=headers,json=jsonData,timeout=10)
  if a.status_code == 200:
    a = round(float(base64.b64decode(json.loads(a.text)['result']['response']['value']).split('"token1_amount":"'.encode('utf-8'),1)[1].split('"}'.encode('utf-8'),1)[0])/1000000,2)
    return a
  else:
    getNETA2JUNO()

def genId():
  res = ''
  for i in range(12):
    res = res+random.choice(string.digits)
  return int(res)

@client.event
async def on_ready():
  print(f'You have logged in as {client}')
  guild = client.get_guild(guildID)
  member = guild.get_member(memberID)
  while(True):
    try:
      NETAPrice = round(getJUNOGecko()*getNETA2JUNO(),2)
      await member.edit(nick="NETA $"+str(NETAPrice))
      time.sleep(1)
      await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=str(NETA2JUNO)+" JUNO"))
      print(str(JUNO2UST*NETA2JUNO))
      time.sleep(60)
    except:
      continue

guildID = 0
memberID = 0
BOT_TOKEN = 'PLACE_AUTH_TOKEN_HERE'
client.run(BOT_TOKEN)