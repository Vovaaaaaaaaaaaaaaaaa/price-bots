import requests
import telebot
import time
BOT_TOKEN="7555823015:AAG12zl1lefcTzB9P-Y_Y6Q5Blocr_z8m5c"

bot = telebot.TeleBot(BOT_TOKEN)
print('started')

@bot.message_handler(commands=['start', 'price'])
def send_welcome(message):
  #geting data from dexS api
  response = requests.get(
    "https://api.dexscreener.com/latest/dex/tokens/0xa093Df2A374a7D20Bd1ABa043F40a844F190383f",
    headers={},
  )
  data = response.json()
  pair = data["pair"]

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
  
bot.infinity_polling()
