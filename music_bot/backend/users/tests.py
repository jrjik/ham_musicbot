from rest_framework import status
from rest_framework.test import APITestCase


class UserListAPITests(APITestCase):
    def test_user_list_empty_by_default(self) -> None:
        user_id = 123
        response = self.client.get(f'/api/users/{user_id}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_add_artist(self) -> None:
        user_id = 123
        payload = {'telegram_id': user_id, 'items': 'Radiohead'}

        response = self.client.post('/api/users/', data=payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        get_response = self.client.get(f'/api/users/{user_id}/')
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        self.assertIn('Radiohead', get_response.json()['items'])
