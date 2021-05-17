from telegram import Update, Chat, ChatMember, ParseMode, ChatMemberUpdated, Bot, ReplyKeyboardMarkup, ReplyKeyboardRemove
from typing import Tuple, Optional
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackContext,
    ChatMemberHandler,
    ConversationHandler
)
import logging

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)


def escribir_archivo(nombre_archivo, lista):
    for linea in lista:
        with open(nombre_archivo, 'a') as archivo:
            archivo.write('\n' + linea)


def send(msg, chat_id, token):
    """
    Send a mensage to a telegram user specified on chatId
    chat_id must be a number!
    """
    bot = Bot(token=token)
    bot.sendMessage(chat_id=chat_id, text=msg)


def extract_status_change(
    chat_member_update: ChatMemberUpdated,
) -> Optional[Tuple[bool, bool]]:
    """Takes a ChatMemberUpdated instance and extracts whether the 'old_chat_member' was a member
    of the chat and whether the 'new_chat_member' is a member of the chat. Returns None, if
    the status didn't change."""
    status_change = chat_member_update.difference().get("status")
    old_is_member, new_is_member = chat_member_update.difference().get("is_member",
                                                                       (None, None))

    if status_change is None:
        return None

    old_status, new_status = status_change
    was_member = (
        old_status
        in [
            ChatMember.MEMBER,
            ChatMember.CREATOR,
            ChatMember.ADMINISTRATOR,
        ]
        or (old_status == ChatMember.RESTRICTED and old_is_member is True)
    )
    is_member = (
        new_status
        in [
            ChatMember.MEMBER,
            ChatMember.CREATOR,
            ChatMember.ADMINISTRATOR,
        ]
        or (new_status == ChatMember.RESTRICTED and new_is_member is True)
    )

    return was_member, is_member


def greet_chat_members(update: Update, _: CallbackContext) -> None:
    """Greets new users in chats and announces when someone leaves, extracted from github,
    was strugging like an asshole"""
    result = extract_status_change(update.chat_member)
    if result is None:
        return

    was_member, is_member = result
    cause_name = update.chat_member.from_user.mention_html()
    member_name = update.chat_member.new_chat_member.user.mention_html()

    if not was_member and is_member:
        update.effective_chat.send_message(
            f"¡Bienvenido {member_name} a Open Source UC! ¡Escribeme por interno \'/start\' para iniciar tu experiencia en el grupo!",
            parse_mode=ParseMode.HTML,
        )
    elif was_member and not is_member:
        update.effective_chat.send_message(
            f"¡Esperamos volver a verte {member_name}, gracias por todo el aporte!",
            parse_mode=ParseMode.HTML,
        )


def track_chats(update: Update, context: CallbackContext) -> None:
    """Tracks the chats the bot is in."""
    result = extract_status_change(update.my_chat_member)
    if result is None:
        return
    was_member, is_member = result

    # Let's check who is responsible for the change
    cause_name = update.effective_user.full_name

    # Handle chat types differently:
    chat = update.effective_chat
    if chat.type == Chat.PRIVATE:
        if not was_member and is_member:
            logger.info("%s started the bot", cause_name)
            context.bot_data.setdefault("user_ids", set()).add(chat.id)
        elif was_member and not is_member:
            logger.info("%s blocked the bot", cause_name)
            context.bot_data.setdefault("user_ids", set()).discard(chat.id)
    elif chat.type in [Chat.GROUP, Chat.SUPERGROUP]:
        if not was_member and is_member:
            logger.info("%s added the bot to the group %s",
                        cause_name, chat.title)
            context.bot_data.setdefault("group_ids", set()).add(chat.id)
        elif was_member and not is_member:
            logger.info("%s removed the bot from the group %s",
                        cause_name, chat.title)
            context.bot_data.setdefault("group_ids", set()).discard(chat.id)
    else:
        if not was_member and is_member:
            logger.info("%s added the bot to the channel %s",
                        cause_name, chat.title)
            context.bot_data.setdefault("channel_ids", set()).add(chat.id)
        elif was_member and not is_member:
            logger.info("%s removed the bot from the channel %s",
                        cause_name, chat.title)
            context.bot_data.setdefault("channel_ids", set()).discard(chat.id)


def show_chats(update: Update, context: CallbackContext) -> None:
    """Shows which chats the bot is in"""
    user_ids = ", ".join(str(uid)
                         for uid in context.bot_data.setdefault("user_ids", set()))
    group_ids = ", ".join(str(gid)
                          for gid in context.bot_data.setdefault("group_ids", set()))
    channel_ids = ", ".join(
        str(cid) for cid in context.bot_data.setdefault("channel_ids", set()))
    text = (
        f"@{context.bot.username} is currently in a conversation with the user IDs {user_ids}."
        f" Moreover it is a member of the groups with IDs {group_ids} "
        f"and administrator in the channels with IDs {channel_ids}."
    )
    update.effective_message.reply_text(text)


PRONOMBRE = range(1)


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
