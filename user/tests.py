from django.test import TestCase
from .models import *
# Create your tests here.

class CustomUserTests(TestCase):
    user1 = ""
    user2 = ""

    def setUp(self):
        self.user1 = CustomUser(
            first_name="test1",
            last_name="test1",
            password="test1234",
            email="test1@email.com"
        )

        self.user2 = CustomUser(
            first_name="test2",
            last_name="test2",
            password="test1234",
            email="test1@email.com"
        )

        return super().setUp()
    
    def test_create_user(self):
        self.user1.username = "test1email"
        self.user1.save()
        is_created = CustomUser.objects.get(username="test1email");
        self.assertTrue(is_created)
    
    def test_unique_username(self):
        try:
            self.user1.username = "test1email"
            self.user2.username = "test1email11"
            user1 = self.use1.save()
            user2 = self.user2.save()
            is_unique = CustomUser.objects.filter(username="test1email");
            self.assertTrue(len(is_unique) == 1)
        except:
            return 
    
class FellowshipTests(TestCase):

    def setUp(self):
        user = CustomUser.objects.create(
            first_name="test2",
            last_name="test2",
            password="test1234",
            username="test1username",
            email="test1@email.com"
        )
        return super().setUp()
    
    def test_create_fellowship(self):
        user = CustomUser.objects.get(username="test1username")
        fellow = Fellowship.objects.create(
            name="fellow1",
            description="fellow description",
            leader=user
        )
        is_created = Fellowship.objects.filter(name="fellow1").exists();
        self.assertTrue(is_created)