import os
from pathlib import PosixPath
from typing import Any

from constants import INPUT_STATE

os.environ.setdefault('HAMMETT_SETTINGS_MODULE', 'settings')
import unittest
from datetime import datetime, UTC

from hammett.core.constants import RenderConfig, DEFAULT_STATE
from hammett.test.base import BaseTestCase
from hammett.test.utils import catch_render_config
from telegram import Message

import screens

class ArtistAddTests(BaseTestCase):

    def get_message(self) -> Message:
        return Message(
            self.message_id,
            datetime.now(tz=UTC),
            self.chat,
            from_user=self.user,
            text='Artist, artist',
        )

    @catch_render_config()
    async def test_add_only_one_artist(self, actual: Any) -> None:

        await screens.add_artist.ArtistAdd().handle_text(self.update, self.context)

        expected_description = 'Пожалуйста, введите только *одного* исполнителя.'

        expected = self.prepare_final_render_config(RenderConfig(
            as_new_message=True,
            description=expected_description,
            cover=PosixPath('/Users/jrjik/Desktop/ham_musicbot/music_bot/bot/media/default_cover.jpg'),
        ))
        self.assertFinalRenderConfigEqual(expected, actual.final_render_config)

    async def test_changing_states_after_calling_move_along_route_handler(self) -> None:

        self.context.user_data['current_state'] = DEFAULT_STATE

        state = await screens.add_artist.ArtistAdd().move_along_route(self.update, self.context)
        self.assertEqual(state, INPUT_STATE)

class ArtistAddValidationTest(BaseTestCase):

    def get_message(self) -> Message:
        return Message(
            self.message_id,
            datetime.now(tz=UTC),
            self.chat,
            from_user=self.user,
            text='12',
        )
    @catch_render_config()
    async def test_name_validation(self, actual):
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