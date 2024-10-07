import discord
import urllib.request
import json
import re

client = discord.Client()

citycodes = {
    "土浦": '080020',
    "水戸": '080010',
    "札幌": '016010',
    "仙台": '040010',
    "東京": '130010',
    "横浜": '140010',
    "名古屋": '230010',
    "大阪": '270000',
    "広島": '340010',
    "福岡": '400010',
    "鹿児島": '460010',
    "那覇": '471010'
}

@client.event
async def on_ready():
  print("logged in as " + client.user.name)

@client.event
async def on_message(message):
  if message.author != client.user:

    reg_res = re.compile(u"(.+)").search(message.content)
    if reg_res:

      if reg_res.group(1) in citycodes.keys():

        citycode = citycodes[reg_res.group(1)]
        resp = urllib.request.urlopen('https://weather.tsukumijima.net/api/forecast?city=%s'%citycode).read()
        resp = json.loads(resp.decode('utf-8'))

        msg = resp['location']['city']
        msg += "の天気は、\n"
        for f in resp['forecasts']:
          msg += f['dateLabel'] + "が" + f['telop'] + "\n"
        msg += "です。"

        await client.send_message(message.channel, message.author.mention + msg)

      else:
        await client.send_message(message.channel, "そこの天気はわかりません...")

client.run("https://discord.com/oauth2/authorize?client_id=1292749758401744896&permissions=0&integration_type=0&scope=bot")
