from typing import Optional, Tuple

from telegram import ChatMember, ChatMemberUpdated, ParseMode, Update
from telegram.ext import CallbackContext


def extract_status_change(
    chat_member_update: ChatMemberUpdated,
) -> Optional[Tuple[bool, bool]]:
    """Takes a ChatMemberUpdated instance and extracts whether
    the 'old_chat_member' was a member
    of the chat and whether the 'new_chat_member' is a member of the chat.
    Returns None, if the status didn't change."""
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
