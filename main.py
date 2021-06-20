from telegram import Update
from telegram.ext import ChatMemberHandler, CommandHandler, Updater

from osuc_companion.bot.chats import show_chats, track_chats
from osuc_companion.bot.conversation import conv_handler
from osuc_companion.bot.greet_users import greet_chat_members

from osuc_companion.settings import TELEGRAM_API_TOKEN


def main():
    my_token = TELEGRAM_API_TOKEN

    updater = Updater(my_token)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Keep track of which chats the bot is in
    dispatcher.add_handler(ChatMemberHandler(
        track_chats, ChatMemberHandler.MY_CHAT_MEMBER))
    dispatcher.add_handler(CommandHandler("show_chats", show_chats))

    # Handle members joining/leaving chats.
    dispatcher.add_handler(ChatMemberHandler(
        greet_chat_members, ChatMemberHandler.CHAT_MEMBER))

    # Start the Bot
    # We pass 'allowed_updates' to *only* handle updates
    # with '(my_)chat_member' or 'message'
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
