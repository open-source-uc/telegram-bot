from dotenv import load_dotenv
from os import getenv

from telegram import Update, Bot
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackContext,
    ChatMemberHandler,
    ConversationHandler,
    Filters,
    MessageHandler
)
import basic
import logging


def main():
    load_dotenv()
    my_token = getenv("TELEGRAM_API_TOKEN")
    print(my_token)

    bot = Bot(token=my_token)

    updater = Updater(my_token)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Keep track of which chats the bot is in
    dispatcher.add_handler(ChatMemberHandler(
        basic.track_chats, ChatMemberHandler.MY_CHAT_MEMBER))
    dispatcher.add_handler(CommandHandler("show_chats", basic.show_chats))

    # Handle members joining/leaving chats.
    dispatcher.add_handler(ChatMemberHandler(
        basic.greet_chat_members, ChatMemberHandler.CHAT_MEMBER))

    # Conversation starter
    # Starts the conversation with the user, asks them a gender question to be respectful
    # Ends when sends guide
    GENDER = range(1)
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', basic.start)],
        states={
        },
        fallbacks=[CommandHandler('cancel', basic.cancel)],
    )
    dispatcher.add_handler(conv_handler)

    # Start the Bot
    # We pass 'allowed_updates' to *only* handle updates with '(my_)chat_member' or 'message'
    # If you want to handle *all* updates, pass Update.ALL_TYPES
    updater.start_polling(
        allowed_updates=[Update.MESSAGE,
                         Update.CHAT_MEMBER, Update.MY_CHAT_MEMBER]
    )

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
