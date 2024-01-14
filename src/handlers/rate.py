"""Handler for rating command."""

from contextlib import suppress
from typing import Optional

from aiogram import Router, types
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder


router = Router()
# TODO: Поднять БД для рейтингов
user_data = {}


class RatingCallbackFactory(CallbackData, prefix="rate"):
    """Callback data for user rating command."""

    action: str
    value: Optional[int] = None


def get_rating_keyboard():
    """Get keyboard for user rating."""
    builder = InlineKeyboardBuilder()

    for rating in range(1, 6):
        builder.button(
            text=str(rating),
            callback_data=RatingCallbackFactory(action="update", value=rating),
        )
    builder.button(text="Confirm", callback_data=RatingCallbackFactory(action="finish"))
    builder.adjust(5)
    return builder.as_markup()


async def update_rating(message: types.Message, new_value: int):
    """User message update.

    Args:
        message: user message instance
        new_value: value to update
    """
    with suppress(TelegramBadRequest):
        await message.edit_text(
            f"Rate our bot: {new_value}", reply_markup=get_rating_keyboard()
        )


@router.message(Command("rate"))
async def rate_bot(message: types.Message):
    """Rate command implementation."""
    user_data[message.from_user.id] = None
    await message.answer("Rate our bot: ", reply_markup=get_rating_keyboard())


@router.callback_query(RatingCallbackFactory.filter())
async def callbacks_num_change_fab(
    callback: types.CallbackQuery,
    callback_data: RatingCallbackFactory,
):
    """Callback for rate command.

    Args:
        callback: callback instance
        callback_data: callback data to process
    """
    user_value = user_data.get(callback.from_user.id, 0)
    if callback_data.action == "update":
        user_data[callback.from_user.id] = callback_data.value
        await update_rating(callback.message, callback_data.value)
        callback.answer()
    else:
        await callback.message.edit_text(f"Your final rating: {user_value}")
        await callback.answer(text="Thanks for using our bot!", show_alert=True)
