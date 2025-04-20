from django.test import TestCase
from user.models import CustomUser
from django.contrib.auth.models import AnonymousUser
from .models import PrayerRequest

# Create your tests here.
class PrayerRequestTests(TestCase):
    def setUp(self):
        test_user = CustomUser.objects.create_user(
            username="test1",
            email="test1@mail.com",
            password="test12345678"
        ) 
        return super().setUp()

    def test_model_creation(self):
        user = CustomUser.objects.get(username="test1")
        prayer_request = PrayerRequest.objects.create(
            title= "Healing for Sarah",
            description= "Please pray for my sister Sarah who is recovering from surgery.",
            author= user,
            prayer_count= 12,
            isAnswered= False,
            isPrivate= False
        )
        is_created = PrayerRequest.objects.filter(title="Healing for Sarah").exists()
        self.assertTrue(is_created)

    def test_model_creation_anon_user(self):
        """
        This should fail if user is anonymous
        """
        try:
            prayer_request = PrayerRequest.objects.create(
                title= "Healing for Sarah",
                description= "Please pray for my sister Sarah who is recovering from surgery.",
                author= AnonymousUser,
                prayer_count= 12,
                isAnswered= False,
                isPrivate= False
            )
            is_created = PrayerRequest.objects.filter(title="Healing for Sarah").exists()
            self.assertTrue(is_created)
        except ValueError as e:
            return False
    
    def test_input_required_fields_only(self):
        user = CustomUser.objects.get(username="test1")
        prayer_request = PrayerRequest.objects.create(
            title= "Healing for Sarah",
            description= "Please pray for my sister Sarah who is recovering from surgery.",
            author= user,
        )
        is_created = PrayerRequest.objects.filter(title="Healing for Sarah").exists()
        self.assertTrue(is_created)