"""Модуль содержит реализацию тестов функционала бота."""

import os
from pathlib import PosixPath
from typing import Any

import unittest
from datetime import UTC, datetime
from hammett.core.constants import DEFAULT_STATE, RenderConfig
from hammett.test.base import BaseTestCase
from hammett.test.utils import catch_render_config
from telegram import Message

import screens
from constants import INPUT_STATE


class ArtistAddTests(BaseTestCase):
    """Класс для тестирования проверки валидации при вводе исполнителя."""

    def get_message(self) -> Message:
        """Функция для передачи тестового сообщения на вход."""
        return Message(
            self.message_id,
            datetime.now(tz=UTC),
            self.chat,
            from_user=self.user,
            text='Artist, artist',
        )

    @catch_render_config()
    async def test_add_only_one_artist(self, actual: Any) -> None:
        """Проверка валидации введенного исполнителя."""
        await screens.add_artist.ArtistAdd().handle_text(self.update, self.context)

        expected_description = 'Пожалуйста, введите только *одного* исполнителя.'

        expected = self.prepare_final_render_config(RenderConfig(
            as_new_message=True,
            description=expected_description,
            cover=PosixPath('/Users/jrjik/Desktop/ham_musicbot/music_bot/bot/media/default_cover.jpg'),
        ))
        self.assertFinalRenderConfigEqual(expected, actual.final_render_config)

    async def test_changing_states_after_calling_move_along_route_handler(self) -> None:
        """Проверка переключения состояний."""
        self.context.user_data['current_state'] = DEFAULT_STATE

        state = await screens.add_artist.ArtistAdd().move_along_route(self.update, self.context)
        assert state == INPUT_STATE


class ArtistAddValidationTest(BaseTestCase):
    """Класс для тестирования проверки валидации."""

    def get_message(self) -> Message:
        """Функция для передачи тестового сообщения на вход."""
        return Message(
            self.message_id,
            datetime.now(tz=UTC),
            self.chat,
            from_user=self.user,
            text='12',
        )
    @catch_render_config()
    async def test_artist_validation(self, actual: Any) -> None:
        """Проверка валидации введенного исполнителя."""
        await screens.add_artist.ArtistAdd().handle_text(self.update, self.context)

        expected_description = 'Исполнитель должен быть минимум из 3 символов и содержать буквы.'

        expected = self.prepare_final_render_config(RenderConfig(
            as_new_message=True,
            description=expected_description,
            cover=PosixPath('/Users/jrjik/Desktop/ham_musicbot/music_bot/bot/media/default_cover.jpg'),
        ))
        self.assertFinalRenderConfigEqual(expected, actual.final_render_config)

if __name__ == '__main__':
    unittest.main()
