import logging
from pathlib import Path
from threading import Thread

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import CallbackContext, CommandHandler, ConversationHandler
from telegram.ext.filters import Filters
from telegram.ext.messagehandler import MessageHandler

from osuc_companion.settings import CONVERSATIONS, GENDER_WORDS, MAINTAINER, USERS_AVATAR_PATH
from osuc_companion.utilities.write_json import write_json

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)

gender_words = GENDER_WORDS

"""
Define the conversation handler states.
"""
GENDER, PHOTO, LOCATION, BIO = range(4)


def add_skip_message(text: str) -> str:
    return text + " " + CONVERSATIONS["skip_message"]


def start(update: Update, context: CallbackContext) -> int:
    reply_keyboard = [["El", "Ella", "Elle"]]
    user = update.message.from_user
    context.user_data["nombre"] = str(user.first_name)
    update.message.reply_text(
        CONVERSATIONS["start_message"].format(user.first_name, MAINTAINER)
        + " "
        + CONVERSATIONS["ask_gender"],
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
    )

    return GENDER


def gender(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    mensaje = update.message.text
    context.user_data["pronombre"] = mensaje
    logger.info("Gender of %s: %s", user.first_name, update.message.text)
    update.message.reply_text(
        f"{CONVERSATIONS['ask_photo']} {CONVERSATIONS['skip_message']}",
        reply_markup=ReplyKeyboardRemove(),
    )

    return PHOTO


def photo(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    mensaje = update.message.text
    photo_file = update.message.photo[-1].get_file()
    avatar = Path(USERS_AVATAR_PATH, user.first_name).with_suffix(".jpg")
    photo_file.download(custom_path=str(avatar))
    logger.info("Foto de %s: %s", user.first_name, avatar.stem)
    update.message.reply_text(add_skip_message(CONVERSATIONS["ask_city"]))

    return LOCATION


def skip_photo(update: Update, _: CallbackContext) -> int:
    user = update.message.from_user
    mensaje = update.message.text
    logger.info("User %s did not send a photo.", user.first_name)
    update.message.reply_text(add_skip_message(CONVERSATIONS["ask_region"]))

    return LOCATION


def location(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    mensaje = update.message.text
    context.user_data["ubicacion"] = mensaje
    logger.info("Ubicacion enviada")
    update.message.reply_text(CONVERSATIONS["ask_bio"])

    return BIO


def skip_location(update: Update, _: CallbackContext) -> int:
    user = update.message.from_user
    mensaje = update.message.text
    update.message.reply_text(
        f"{CONVERSATIONS['privacy_message']} {CONVERSATIONS['ask_bio']}"
    )

    return BIO


def bio(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    mensaje = update.message.text
    context.user_data["biografia"] = mensaje
    logger.info("Bio of %s: %s", user.first_name, update.message.text)
    update.message.reply_text(CONVERSATIONS["end_message"])
    send_to_json(context)
    return ConversationHandler.END


def cancel(update: Update, _: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(
        CONVERSATIONS["cancel_message"].format(MAINTAINER),
        reply_markup=ReplyKeyboardRemove(),
    )

    return ConversationHandler.END


def send_to_json(context):
    thread = Thread(target=write_json, args=(context.user_data,))
    thread.start()


conv_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        GENDER: [MessageHandler(Filters.regex("^(El|Ella|Elle)$"), gender)],
        PHOTO: [
            MessageHandler(Filters.photo, photo),
            CommandHandler("skip", skip_photo),
        ],
        LOCATION: [
            MessageHandler(Filters.text, location),
            CommandHandler("skip", skip_location),
        ],
        BIO: [MessageHandler(Filters.text & ~Filters.command, bio)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)
