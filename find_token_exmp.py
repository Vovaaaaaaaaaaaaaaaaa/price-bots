import requests
import telebot
import time
BOT_TOKEN=""

bot = telebot.TeleBot(BOT_TOKEN)
print('started')

coin_dict = {}

class Coin:
    def __init__(self, ca):
        self.ca = ca

@bot.message_handler(commands=['start'])
def send_welcome(message):
  sent_msg = bot.send_message(message.chat.id, "Send me CA of the token you want to track \n\nIf you want to change the token to track , send /new_ca")  
  bot.register_next_step_handler(sent_msg, ca_handler)

@bot.message_handler(commands=['new_ca'])
def send_welcome(message):
  sent_msg = bot.send_message(message.chat.id, "Send me CA of the token you want to track \n\nIf you want to change the token to track , send /new_ca")  
  bot.register_next_step_handler(sent_msg, ca_handler)

def ca_handler(message):
    ca = message.text
    coin = Coin(ca)
    coin_dict[message.chat.id] = coin

    response = requests.get(
    "https://api.dexscreener.com/latest/dex/tokens/" + ca,
    headers={},
    )
    
    if response :
      data = response.json()
      pair = data["pairs"][0]

      name = pair["baseToken"]["name"]
      price = str(pair["priceUsd"])

      sent_msg = bot.send_message(message.chat.id, f"Found. {name} • {price}$ \n\nNow you can use /price !")
      return(pair)

    else:
       sent_msg = bot.send_message(message.chat.id, f"I can not find any matching coins, please check that you sent me right contract adress of the token(also check that it is TOKEN adress and not adress fo the POOL) and send me new CA")
       bot.register_next_step_handler(sent_msg, ca_handler)
    
@bot.message_handler(commands=['price'])
def send_welcome(message):
  #sent_msg = bot.send_message(message.chat.id, "Send me CA of the token you want to track \n\nIf you want to change the token to track , send /new_ca")  
  coin = coin_dict[message.chat.id]

  response = requests.get(
  "https://api.dexscreener.com/latest/dex/tokens/" + coin.ca,
  headers={},
  )
  
  if response :
    data = response.json()
    pair = data["pairs"][0]

    name = str(pair["baseToken"]["name"])
    price = str(pair["priceUsd"])
    intprice = float(pair["priceUsd"])
    mc = str(pair["marketCap"])
    change1hpr = str(pair["priceChange"]["h1"])
    intchange = pair["priceChange"]["h1"]
    vol24h = str(pair["volume"]["h24"])
    url = str(pair["url"])

    if intchange > 0:
      change1h = intchange * (intprice / 100)
      bot.send_message(message.chat.id, f'{name} • {price}$ \n\n<tg-emoji emoji-id="5368324170671202286">💎</tg-emoji>Market cap: {mc}$ \n<tg-emoji emoji-id="5368324170671202286">📈</tg-emoji>1h change: {round(change1h, 6)}$ • {change1hpr}% \n<tg-emoji emoji-id="5368324170671202286">📊</tg-emoji>24h volume: {vol24h} \n\n<tg-emoji emoji-id="5368324170671202286">🔗</tg-emoji><a href="{url}">DexS link</a>', disable_web_page_preview=True, parse_mode='HTML')

    elif intchange < 0:
      change1h = intchange * (intprice / 100)
      bot.send_message(message.chat.id, f'{name} • {price}$ \n\n<tg-emoji emoji-id="5368324170671202286">💎</tg-emoji>Market cap: {mc}$ \n<tg-emoji emoji-id="5368324170671202286">📈</tg-emoji>1h change: {round(change1h, 6)}$ • {change1hpr}% \n<tg-emoji emoji-id="5368324170671202286">📊</tg-emoji>24h volume: {vol24h} \n\n<tg-emoji emoji-id="5368324170671202286">🔗</tg-emoji><a href="{url}">DexS link</a>', disable_web_page_preview=True, parse_mode='HTML')


    else:
      bot.send_message(message.chat.id, f'{name} • {price}$ \n\n<tg-emoji emoji-id="5368324170671202286">💎</tg-emoji>Market cap: {mc}$ \n<tg-emoji emoji-id="5368324170671202286">📈</tg-emoji>1h change: 0$ • 0% \n<tg-emoji emoji-id="5368324170671202286">📊</tg-emoji>24h volume: {vol24h} \n\n<tg-emoji emoji-id="5368324170671202286">🔗</tg-emoji><a href="{url}">DexS link</a>', disable_web_page_preview=True, parse_mode='HTML')
    
  else:
    sent_msg = bot.send_message(message.chat.id, f"I can not find any matching coins, please check that you sent me right contract adress of the token(also check that it is TOKEN adress and not adress fo the POOL) and send me new CA")
    bot.register_next_step_handler(sent_msg, ca_handler)
  


  
bot.infinity_polling()