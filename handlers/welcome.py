"""Handler for greetings and info."""

from aiogram import types, F, Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram import html
from aiogram.utils.i18n import gettext as _
from aiogram.utils.formatting import Text, Bold
import text

router = Router()


@router.message(Command("start"))
async def start_handler(msg: Message):
    content = Text(
        "Hello ",
        msg.from_user.full_name,
        "! Learn what can I do by writting /info."
    )
    await msg.answer(
        **content.as_kwargs()
    )


@router.message(Command("info"))
async def message_info(msg: Message):
    await msg.answer(
        text.TEXT_FOR_INFO
    )


@router.message(Command("about"))
async def message_about(msg: Message):
    await msg.answer(
        text.TEXT_ABOUT
    )


@router.message(Command("redirect"))
async def message_redicrect(msg: Message):
    await msg.answer(
        "Use the full version of Playlist Selection service on: \n http://0.0.0.0:5000/"
    )