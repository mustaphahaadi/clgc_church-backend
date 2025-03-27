from django.test import TestCase
from .models import Member

# Create your tests here.

class MemberModelTest(TestCase):
    def test_create_member(self):
        member = Member.objects.create(
            first_name='John',
            last_name='Doe',
            email='john@example.com'
        )
        self.assertEqual(member.first_name, 'John')
