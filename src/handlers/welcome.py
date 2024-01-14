"""Handler for greetings and info."""

from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.utils.formatting import Text

import src.text as text
from configs.bot_config import config


router = Router()


@router.message(F.text, Command("start"))
async def start_handler(message: types.Message):
    content = Text(
        "Hello ", message.from_user.full_name, "! Learn what can I do by writting /info."
    )
    await message.answer(**content.as_kwargs())


@router.message(F.text, Command("info"))
async def message_info(message: types.Message):
    await message.answer(text.TEXT_FOR_INFO)


@router.message(F.text, Command("about"))
async def message_about(message: types.Message):
    await message.answer(text.TEXT_ABOUT)


@router.message(F.text, Command("redirect"))
async def message_redicrect(message: types.Message):
    await message.answer(
        f"Use the full version of Playlist Selection service on: \n {config.service_uri}"
    )
