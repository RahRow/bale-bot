from poll import Updater

TOKEN = "1436034831:YPhRWhXUze7d7SiqaLRxIrJJbvpHHPjlKJFI2kqi"

updater = Updater(TOKEN)

async def callback(message):
    print(message)

updater.start_polling(callback)


