from telegram import Update
from telegram.ext import ChatMemberHandler, CommandHandler, Updater

from osuc_companion.bot.conversation import conv_handler

from osuc_companion.settings import TELEGRAM_API_TOKEN_2


def main():
    my_token = TELEGRAM_API_TOKEN_2

    updater = Updater(my_token)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Conversation starter
    # Starts the conversation with the user,
    # asks them a gender question to be respectful
    # Ends when sends guide
    dispatcher.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
