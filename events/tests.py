from django.test import TestCase
from .models import Events
from django.utils import timezone
from datetime import timedelta

# Create your tests here.
class EventTests(TestCase):
    # create events
    def test_create_event(self):
        event = Events.objects.create(
            title="Community Outreach",
            date=timezone.now(),
            time=str(timedelta(minutes=2)),
            location="Downtown Park",
            description="Help us serve the community with food, clothing, and prayer.",
            category="outreach",
            image="https://images.unsplash.com/photo-1593113630400-ea4288922497?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1170&q=80"
        )

        is_created = Events.objects.filter(title="Community Outreach").exists();
        self.assertTrue(is_created)

    def test_create_event_str_date(self):
        event = Events.objects.create(
            title="Community Outreach",
            date="2025-12-22",
            time=str(timedelta(minutes=2)),
            location="Downtown Park",
            description="Help us serve the community with food, clothing, and prayer.",
            category="outreach",
            image="https://images.unsplash.com/photo-1593113630400-ea4288922497?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1170&q=80"
        )

        is_created = Events.objects.filter(title="Community Outreach").exists();
        self.assertTrue(is_created)
    
    # def test_save_image(self):
    #     event = Events.objects.create(
    #         title="Community Outreach",
    #         date="2025-12-22",
    #         time=str(timedelta(minutes=2)),
    #         location="Downtown Park",
    #         description="Help us serve the community with food, clothing, and prayer.",
    #         category="outreach",
    #         image="https://images.unsplash.com/photo-1593113630400-ea4288922497?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1170&q=80"
    #     )

    #     is_created = Events.objects.filter(title="Community Outreach").exists();
    #     self.assertTrue(is_created)