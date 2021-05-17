from telegram import Update, Chat, ChatMember, ParseMode, ChatMemberUpdated, Bot
from typing import Tuple, Optional
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackContext,
    ChatMemberHandler,
)
import basic
import logging

my_token = '1878681564:AAFooinZW8l7aVNAzFypkVxJsEgl72TdPrg'

bot = Bot(token=my_token)

while True:
    updater = Updater(my_token)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Keep track of which chats the bot is in
    dispatcher.add_handler(ChatMemberHandler(basic.track_chats, ChatMemberHandler.MY_CHAT_MEMBER))
    dispatcher.add_handler(CommandHandler("show_chats", basic.show_chats))

    # Handle members joining/leaving chats.
    dispatcher.add_handler(ChatMemberHandler(basic.greet_chat_members, ChatMemberHandler.CHAT_MEMBER))

    # Start the Bot
    # We pass 'allowed_updates' to *only* handle updates with '(my_)chat_member' or 'message'
    # If you want to handle *all* updates, pass Update.ALL_TYPES
    updater.start_polling(
        allowed_updates=[Update.MESSAGE, Update.CHAT_MEMBER, Update.MY_CHAT_MEMBER]
    )

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()
