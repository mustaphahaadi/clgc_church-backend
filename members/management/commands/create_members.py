from django.core.management.base import BaseCommand
from members.models import Member
from django.db.models import Q
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from members.serializers import MemberSerializer

class Command(BaseCommand):
    help = "Create members"

    def create_member(self, *args):
        values = args[0]
        try:
            if not Member.objects.filter(Q(phone=values['phone']) & Q(email=values['email'])).exists():
                Member.objects.create(
                    date=values["date"],
                    first_name=values['first_name'],
                    middle_name=values['middle_name'],
                    last_name=values['last_name'],
                    birthday=values['birthday'],
                    age=values['age'],
                    sex=values['sex'],
                    marital_status=values['marital_status'],
                    address=values['address'],
                    bus_stop=values['bus_stop'],
                    phone=values['phone'],
                    email=values['email'],
                    occupation=values['occupation'],
                    office_address=values['office_address'],
                    invited_by=values['invited_by'],
                    born_again=values['born_again'],
                    want_membership=values['want_membership'],
                    prayer_request=values['prayer_request']
                )
                self.stdout.write(self.style.SUCCESS(f"Member {values['email']} successfully created"))
            else:
                self.stdout.write(self.style.WARNING(f"Member {values['email']} already exists"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Member creation failed: {str(e)}"))

    def handle(self, *args, **options):
        member_data = {
            "date": "2025-03-02",
            "first_name": "Akwasi",
            "middle_name": "Appiag",
            "last_name": "Nsua",
            "birthday": "1990-01-01",
            "age": 33,
            "sex": "Male",
            "marital_status": "Single",
            "address": "123 Main St",
            "bus_stop": "Main & 1st",
            "phone": "555-1234",
            "email": "akw.ahh@example.com",
            "occupation": "Software Engineer",
            "office_address": "456 Tech St",
            "invited_by": "Friend",
            "born_again": True,
            "want_membership": True,
            "prayer_request": "Pray for my family"
        }
        
        self.create_member(member_data)





# This view handles the creation and listing of Member objects
class MemberListCreateView(ListCreateAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

# This view handles the retrieval, update, and deletion of Member objects
class MemberDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
