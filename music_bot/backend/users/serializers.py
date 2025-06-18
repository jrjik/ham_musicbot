from rest_framework import serializers

from users.models import TelegramUser


class TelegramUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelegramUser
        fields = ['telegram_id', 'items']

    def validate_items(self, value: list[str]) -> list[str]:
        """Нормализует список артистов: удаляет пустые, короткие, цифровые и дубликаты."""
        seen = set()
        cleaned = []

        for item in value:
            item = item.strip()
            if len(item) < 3:
                continue
            if item.isdigit():
                continue
            norm = item.lower()
            if norm in seen:
                continue
            seen.add(norm)
            cleaned.append(item)

        return cleaned
