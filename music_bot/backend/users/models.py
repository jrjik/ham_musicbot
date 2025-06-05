from django.db import models


class UserList(models.Model):
    user_id = models.BigIntegerField(primary_key=True)
    items = models.TextField()

    def get_items_list(self) -> list[str]:
        return [item.strip() for item in self.items.split(',')] if self.items else []

    def set_items_list(self, items: list[str]):
        self.items = ', '.join(items)