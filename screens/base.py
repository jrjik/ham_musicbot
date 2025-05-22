"""Модуль содержит базовые модули для экранов."""

from hammett.core import Button, Screen
from hammett.core.constants import SourceTypes


class BaseScreen(Screen):
    """В классе содержится кнопка возврата на StartScreen."""

    @staticmethod
    def _get_back_button() -> 'Button':
        from screens.start_screen import StartScreen

        return Button(
            '⬅️ В главное меню',
            source=StartScreen,
            source_type=SourceTypes.MOVE_SOURCE_TYPE,
        )
