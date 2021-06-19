import logging
from osuc_companion.settings import USERS_AVATAR_PATH
from pathlib import Path
from osuc_companion.utilities.write_json import write_json

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

gender_words = {
    'El': 'comodo',
    'Ella': 'comoda',
    'Elle': 'comode'
}

GENDER, PHOTO, LOCATION, BIO = range(4)


def start(update: Update, context: CallbackContext) -> int:
    reply_keyboard = [['El', 'Ella', 'Elle']]
    user = update.message.from_user
    context.user_data['nombre'] = str(user.first_name)
    update.message.reply_text(
        '¡Hola ' + user.first_name +
        ', soy el bot que te acompañara en tu inicio de desafios de Open SourceUC! '
        'Porfavor, escribe /cancel en el chat si te uniste por error\n\n'
        'Antes de iniciar, ¿Con que pronombre te identificas?',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True),
    )

    return GENDER


def gender(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    mensaje = update.message.text
    context.user_data['pronombre'] = mensaje
    logger.info("Gender of %s: %s", user.first_name, update.message.text)
    update.message.reply_text(
        '¡Genial! ¿Te tinca me mandas una foto tuya? '
        'para ver como eres y poder tener registro en el equipo, o manda /skip si no te sientes ' +
        gender_words[mensaje] + '.',
        reply_markup=ReplyKeyboardRemove(),
    )

    return PHOTO


def photo(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    mensaje = update.message.text
    photo_file = update.message.photo[-1].get_file()
    avatar = Path(USERS_AVATAR_PATH, user.first_name).with_suffix('.jpg')
    photo_file.download(custom_path=str(avatar))
    logger.info("Foto de %s: %s", user.first_name, avatar.stem)
    update.message.reply_text(
        '¡Increible! ¡Realmente fenomenal! Ahora, escribeme tu ciudad por favor, o manda /skip si no quieres.'
    )

    return LOCATION


def skip_photo(update: Update, _: CallbackContext) -> int:
    user = update.message.from_user
    mensaje = update.message.text
    logger.info("User %s did not send a photo.", user.first_name)
    update.message.reply_text(
        '¡Esta bien! Ahora, escribeme tu ciudad para la base de datos de Open Source UC (Para organizar eventos a futuro), o envia /skip.'
    )

    return LOCATION


def location(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    mensaje = update.message.text
    context.user_data['ubicacion'] = mensaje
    logger.info(
        "Ubicacion enviada"
    )
    update.message.reply_text(
        '¡Excelente! Esta informacion servira para eventos presenciales futuros. Ahora, cuentame un poco de ti, en un pequeño parrafo '
        'hablame sobre tus logros en la informatica, conocimiento y motivaciones de entrar a este equipo.'
    )

    return BIO


def skip_location(update: Update, _: CallbackContext) -> int:
    user = update.message.from_user
    mensaje = update.message.text
    update.message.reply_text(
        '¡Ok, respetamos tu privacidad! Ahora, cuentame un poco de ti, en un pequeño parrafo '
        'hablame sobre tus logros en la informatica, conocimiento y motivaciones de entrar a este equipo.'
    )

    return BIO


def bio(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    mensaje = update.message.text
    context.user_data['biografia'] = mensaje
    logger.info("Bio of %s: %s", user.first_name, update.message.text)
    update.message.reply_text(
        '¡Gracias, ahora, te presento tu primer desafio en el equipo de OPEN SOURCE UC!: PROCEDE A PRESENTAR DESAFIO')
    send_to_json(context)
    return ConversationHandler.END


def cancel(update: Update, _: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(
        'Oh... ¿Te vas tan pronto? Ojala quieras volver a Open Source UC, si tuviste algun problema con el bot, no dudes en contactar a Dyotson '
        '(Max Militzer) para arreglarlo', reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


def send_to_json(context):
    thread = Thread(target=write_json, args=(context.user_data,))
    thread.start()


conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        GENDER: [MessageHandler(Filters.regex('^(El|Ella|Elle)$'), gender)],
        PHOTO: [MessageHandler(Filters.photo, photo), CommandHandler('skip', skip_photo)],
        LOCATION: [
            MessageHandler(Filters.text, location),
            CommandHandler('skip', skip_location),
        ],
        BIO: [MessageHandler(Filters.text & ~Filters.command, bio)],
    },
    fallbacks=[CommandHandler('cancel', cancel)],
)
