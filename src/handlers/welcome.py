"""Handler for greetings and info."""

from aiogram import F, Router, types  # , html, types
from aiogram.filters import Command
from aiogram.utils.formatting import Text  # Bold

import text
from configs.bot_config import config


# from aiogram.utils.i18n import gettext


router = Router()


@router.message(F.text, Command("start"))
async def start_handler(msg: types.Message):
    content = Text(
        "Hello ", msg.from_user.full_name, "! Learn what can I do by writting /info."
    )
    await msg.answer(**content.as_kwargs())


@router.message(F.text, Command("info"))
async def message_info(msg: types.Message):
    await msg.answer(text.TEXT_FOR_INFO)


@router.message(F.text, Command("about"))
async def message_about(msg: types.Message):
    await msg.answer(text.TEXT_ABOUT)


@router.message(F.text, Command("redirect"))
async def message_redicrect(msg: types.Message):
    await msg.answer(
        "Use the full version of Playlist Selection service on: \n %s", config.service_uri
    )
