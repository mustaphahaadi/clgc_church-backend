from django.core.management.base import BaseCommand
from members.models import Contact
from django.db.models import Q
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from members.serializers import ContactSerializer



class Command(BaseCommand):
    help = "Create contacts and memebrs"

    def createContact(self,*args):
        values = args[0]
        name = values["name"]
        email = values['email']
        message = values['message']
        phone = values['phone']
        subject = values['subject']

        try:
            if not Contact.objects.filter(Q(phone=phone) & Q(email=email)).exists():
                contact1 = Contact.objects.create(
                    name=name,
                    email=email,
                    message=message,
                    phone=phone,
                    subject=subject,
                )

                self.stdout.write(self.style.SUCCESS(f"{email} successfully created"))
            else:
                self.stdout.write(self.style.ERROR(f"contact {email} already exists"))
        except:
            self.stdout.write(self.style.ERROR(f"Contact {email} creations failed"))

        

    def handle(self, *args, **options):
        
        careate = self.createContact({
            "name":"test1",
            "email":"test1@mail.com",
            "message":"test message successfull",
            "phone":"0209117002",
            "subject":"test subject"
        })

        # return super().handle(*args, **options)



# This view handles the creation and listing of Contact objects
class ContactListCreateView(ListCreateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]