from rest_framework.test import APITestCase
from rest_framework import status

class UserListAPITests(APITestCase):

    def test_user_list_empty_by_default(self) -> None:
        user_id = 123
        response = self.client.get(f'/api/users/{user_id}/artists/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), [])

    def test_user_add_artist(self) -> None:
        user_id = 123
        response = self.client.post(f'/api/users/{user_id}/artists/', data={'name': 'Radiohead'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        get_response = self.client.get(f'/api/users/{user_id}/artists/')
        self.assertIn('Radiohead', get_response.json())