from django.core.exceptions import ObjectDoesNotExist
import logging

from backend.users.models import UserList

logger = logging.getLogger(__name__)

async def get_user_list(user_id: int) -> list[str]:
    try:
        user_list = await UserList.objects.aget(user_id=user_id)
        return user_list.get_items_list()
    except ObjectDoesNotExist:
        return []
    except Exception as e:
        logger.exception(f"Error getting user list: {e}")
        return []

async def save_user_list(user_id: int, items: list[str]) -> bool:
    try:
        user_list, created = await UserList.objects.aget_or_create(
            user_id=user_id,
            defaults={'items': ', '.join(items) if items else ""}
        )
        if not created:
            user_list.set_items_list(items)
            await user_list.asave()
        return True
    except Exception as e:
        logger.exception(f"Error saving user list: {e}")
        return False