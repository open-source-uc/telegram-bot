import telegram
import basic

my_token = '1878681564:AAFooinZW8l7aVNAzFypkVxJsEgl72TdPrg'
bot = telegram.Bot(token=my_token)

mensaje = bot.get_me()
print(mensaje)
