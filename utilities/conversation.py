import logging
from utilities.write_json import write_json
from typing import Optional, Tuple

from telegram import (Bot, Chat, ChatMember, ChatMemberUpdated, ParseMode,
                      ReplyKeyboardMarkup, ReplyKeyboardRemove, Update)
from telegram.ext import CallbackContext, ConversationHandler, CommandHandler
from telegram.ext.filters import Filters
from telegram.ext.messagehandler import MessageHandler

from threading import Thread

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)
global gender_words
global usuario


gender_words = {
    'El': 'comodo',
    'Ella': 'comoda',
    'Elle': 'comode'
}

usuario = {}

GENDER, PHOTO, LOCATION, BIO = range(4)


def start(update: Update, _: CallbackContext) -> int:
    reply_keyboard = [['El', 'Ella', 'Elle']]
    user = update.message.from_user
    usuario['Nombre'] = str(user.first_name)
    update.message.reply_text(
        '¡Hola ' + user.first_name +
        ', soy el bot que te acompañara en tu inicio de desafios de Open SourceUC! '
        'Porfavor, escribe /cancel en el chat si te uniste por error\n\n'
        'Antes de iniciar, ¿Con que pronombre te identificas?',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True),
    )

    return GENDER


def gender(update: Update, _: CallbackContext) -> int:
    user = update.message.from_user
    mensaje = update.message.text
    usuario['Pronombre'] = mensaje
    logger.info("Gender of %s: %s", user.first_name, update.message.text)
    update.message.reply_text(
        '¡Genial! ¿Te tinca me mandas una foto tuya? '
        'para ver como eres y poder tener registro en el equipo, o manda /skip si no te sientes ' +
        gender_words[mensaje] + '.',
        reply_markup=ReplyKeyboardRemove(),
    )

    return PHOTO


def photo(update: Update, _: CallbackContext) -> int:
    user = update.message.from_user
    mensaje = update.message.text
    photo_file = update.message.photo[-1].get_file()
    photo_file.download(user.first_name + '.jpg')
    logger.info("Foto de %s: %s", user.first_name, user.first_name + '.jpg')
    update.message.reply_text(
        '¡Increible! ¡Realmente fenomenal! Ahora, mandame tu ubicacion por favor, o manda /skip si no quieres.'
    )

    return LOCATION


def skip_photo(update: Update, _: CallbackContext) -> int:
    user = update.message.from_user
    mensaje = update.message.text
    logger.info("User %s did not send a photo.", user.first_name)
    update.message.reply_text(
        '¡Esta bien! Ahora, mandame tu ubicacion para la base de datos de Open Source UC (Para organizar eventos a futuro), o envia /skip.'
    )

    return LOCATION


def location(update: Update, _: CallbackContext) -> int:
    user = update.message.from_user
    mensaje = update.message.text
    user_location = update.message.location
    usuario['Lugar'] = [user_location.latitude,
                        user_location.longitude]  # Latitud y longitud
    logger.info(
        "Ubicacion de %s: %f / %f", user.first_name, user_location.latitude, user_location.longitude
    )
    update.message.reply_text(
        '¡Excelente! Esta informacion servira para eventos presenciales futuros. Ahora, cuentame un poco de ti, en un pequeño parrafo '
        'hablame sobre tus logros en la informatica, conocimiento y motivaciones de entrar a este equipo.'
    )

    return BIO


def skip_location(update: Update, _: CallbackContext) -> int:
    user = update.message.from_user
    mensaje = update.message.text
    logger.info("User %s did not send a location.", user.first_name)
    update.message.reply_text(
        '¡Ok, respetamos tu privacidad! Ahora, cuentame un poco de ti, en un pequeño parrafo '
        'hablame sobre tus logros en la informatica, conocimiento y motivaciones de entrar a este equipo.'
    )

    return BIO


def bio(update: Update, _: CallbackContext) -> int:
    user = update.message.from_user
    mensaje = update.message.text
    usuario['Biografia'] = mensaje
    logger.info("Bio of %s: %s", user.first_name, update.message.text)
    update.message.reply_text(
        '¡Gracias, ahora, te presento tu primer desafio en el equipo de OPEN SOURCE UC!: PROCEDE A PRESENTAR DESAFIO')

    return ConversationHandler.END


def cancel(update: Update, _: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(
        'Oh... ¿Te vas tan pronto? Ojala quieras volver a Open Source UC, si tuviste algun problema con el bot, no dudes en contactar a Dyotson '
        '(Max Militzer) para arreglarlo', reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


def send_to_json():
    thread = Thread(target=write_json, args=(usuario))
    thread.start()


conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        GENDER: [MessageHandler(Filters.regex('^(El|Ella|Elle)$'), gender)],
        PHOTO: [MessageHandler(Filters.photo, photo), CommandHandler('skip', skip_photo)],
        LOCATION: [
            MessageHandler(Filters.location, location),
            CommandHandler('skip', skip_location),
        ],
        BIO: [MessageHandler(Filters.text & ~Filters.command, bio)],
    },
    fallbacks=[CommandHandler('cancel', cancel)],
)
