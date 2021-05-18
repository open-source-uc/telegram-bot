import logging
from typing import Optional, Tuple

from telegram import (Bot, Chat, ChatMember, ChatMemberUpdated, ParseMode,
                      ReplyKeyboardMarkup, ReplyKeyboardRemove, Update)
from telegram.ext import CallbackContext, ConversationHandler, CommandHandler

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)


def start(update: Update, _: CallbackContext) -> int:
    reply_keyboard = [['El', 'Ella', 'Elle']]
    user = update.message.from_user
    update.message.reply_text(
        '¡Hola ' + user.first_name +
        ', soy el bot que te acompañara en tu inicio de desafios de Open SourceUC! '
        'Porfavor, escribe /cancel en el chat si te uniste por error o ya no quieres dar mas informacion.\n\n'
        'Antes de iniciar, ¿Con que pronombre te identificas?',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True),
    )
    # if update.message.reply_to_message.text is str:
    #    pronombre_data = update.message.text
    #    escribir_archivo('pronombres.csv', [user.first_name + " " + pronombre_data])

    # update.message.reply_text(
    #    '¡Excelente ' + user.first_name + '! Ahora que lo sabemos, podemos explicarte que necesitas hacer: INSERTE BIENVENIDA Y DESAFIO')


def cancel(update: Update, _: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(
        'Oh, ¿Ya te vas? Ojala podamos volver a hablar', reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
    },
    fallbacks=[CommandHandler('cancel', cancel)],
)
dispatcher.add_handler(conv_handler)