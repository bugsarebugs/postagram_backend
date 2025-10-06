from rest_framework import status 
from core.fixtures.user import user 
from core.fixtures.post import post 

class TestUserViewSet:
    endpoint = '/api/user/'

    def test_list(self, client, user):
        client.force_authenticate(user=user)
        response = client.get(self.endpoint)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 1 

    def test_retrieve(self, client, user):
        client.force_authenticate(user=user)
        response = client.get(self.endpoint + str(user.public_id) + '/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['username'] == user.username 
        assert response.data['first_name'] == user.first_name 
        assert response.data['last_name'] == user.last_name 

    def test_create(self, client, user):
        client.force_authenticate(user=user)
        data = {
            "username" : "mimi",
            "email" : "mimiexample@gmail.com",
            "first_name": "jamaahuyu",
            "last_name": "jautena",
            "password": "motherfucker21"
        } 
        response = client.post(self.endpoint, data, format='json')
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_update(self, client, user):
        client.force_authenticate(user=user)
        updated_data = {
            "username": "updateduser",
            "email": "updated@example.com",
            "first_name": "UpdatedFirstName",
            "last_name": "UpdatedLastName"
        }
        response = client.patch(self.endpoint + str(user.public_id) + '/', updated_data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['username'] == updated_data['username']
        assert response.data['email'] == updated_data['email']
        assert response.data['first_name'] == updated_data['first_name']
        assert response.data['last_name'] == updated_data['last_name']

