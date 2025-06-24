
import logging

from music_bot.bot.exceptions import RequestFailed
from telegram.ext import ApplicationHandlerStop

logger = logging.getLogger(__name__)


async def error_handler(update, context) -> None:
    exc = context.error

    if isinstance(exc, RequestFailed):
        logger.warning('Ошибка запроса: %s', exc)

        if update and update.callback_query:
            await update.callback_query.answer('Произошла ошибка при обращении к серверу.')
        elif update and update.message:
            await update.message.reply_text('Произошла ошибка при обработке запроса.')

        raise ApplicationHandlerStop
