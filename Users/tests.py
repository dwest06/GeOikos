from django.test import TestCase
from .models import User
from django.test import Client
from .views import (
    login_user,
    logout_user,
    create_user,
    modify_user,
    delete_user
)

# class UserTestCase(TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.user = User.objects.create(email="test@test.com", username="test", password="test1234")
        

#     def test_login_user(self):
#         """Login test user"""
#         print(User.objects.all())
#         response = self.client.post('/users/login', {'email' : 'test@test.com', "password" : "test1234"})
#         self.assertEquals(True, True )

#     def test_logout_user(self):
#         """Logout test user"""
#         self.client.post('/users/login', {'email' : 'test@test.com', "password" : "test1234"})
#         response = self.client.get('/users/logout')
#         print('response logout', response)
#         self.assertEquals(True, True)

#     def test_create_user(self):
#         """Create test user"""
#         response = self.client.post('/users/create-user', {
#             'email' : 'test1@test.com', 
#             "username" : "test1",
#             "password1" : "test1234",
#             "password2" : "test1234"
#         })
#         user = User.objects.get(email="test1@test.com")
#         self.assertEquals(user.username, 'test1')
#         self.assertEquals(user.status, 'IN')
    
#     def test_modify_user(self):
#         """Modify first name and last name test user"""
#         # response = self.client.post('/users/login', {'email' : 'test@test.com', "password" : "test1234"})
#         response = self.client.post('/users/modify-user/' + str(self.user.pk), {
#             'first_name' : 'Testing',
#             'last_name' : 'Alphonsi'
#         })
#         print(response.status_code)
#         self.assertEquals(self.user.first_name, 'Testing')
#         self.assertEquals(self.user.last_name, 'Alphonsi')
    
#     def test_delete_user(self):
#         """Delete test user"""
#         response = self.client.post('/users/delete-user', {
#             'email' : 'test1@test.com', 
#             "username" : "test1",
#             "password1" : "test1234",
#             "password2" : "test1234"
#         })
#         user = User.objects.get(email="test1@test.com")
#         self.assertEquals(user.username, 'test1')
#         self.assertEquals(user.status, 'IN')