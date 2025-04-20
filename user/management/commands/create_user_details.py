from django.core.management.base import BaseCommand
from user.models import *
from django.db.models import Q



class Command(BaseCommand):
    help = "Create contacts and memebrs"

    def createUser(self,*args):
        values = args[0]
        username = values["username"]
        email = values['email']
        first_name = values["first_name"]
        last_name = values["last_name"]
        password = values["password"]
        admin = values["admin"]
        

        try:
            if not CustomUser.objects.filter(Q(email=email) & Q(username=username)).exists():
                if admin:
                    user1 = CustomUser.objects.create_superuser(
                        username=username,
                        email=email,
                        first_name = first_name,
                        last_name = last_name,
                        password = password
                    )
                else:
                    user1 = CustomUser.objects.create_user(
                        username=username,
                        email=email,
                        first_name = first_name,
                        last_name = last_name,
                        password = password
                    )
                self.stdout.write(self.style.SUCCESS(f"{email} successfully created"))
                
            else:
                self.stdout.write(self.style.ERROR(f"user: {email} already exists"))
        except:
            self.stdout.write(self.style.ERROR(f"user: {email} creations failed"))

    def createFellowship(self,*args):
        values = args[0]
        name = values["name"]
        description = values["description"]
        leader = values["leader"]
        
        # check if the leader exist
        try:
            user = CustomUser.objects.get(username=leader)
        except CustomUser.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"{leader} is not registered"))

        # create fellowship and handle errors
        try:
            if not Fellowship.objects.filter(name=name).exists():
                fellow = Fellowship.objects.create(
                    name=name,
                    description=description,
                    leader=user
                )
                self.stdout.write(self.style.SUCCESS(f"{name} successfully created"))
            else:
                self.stdout.write(self.style.ERROR(f"Fellowship: {name} already exists"))
        except:
            self.stdout.write(self.style.ERROR(f"Fellowship: {name} creations failed"))
        

    def handle(self, *args, **options):
        
        user1 = self.createUser({
            "username":"testuser1",
            "email":"nicardid@gmail.com",
            "first_name":"test1",
            "last_name":"test11",
            "password":"stringtest12",
            "admin":True
        })

        user2 = self.createUser({
            "username":"testuser2",
            "email":"nicardid+1@gmail.com",
            "first_name":"test2",
            "last_name":"test12",
            "password":"stringtest12",
            "admin":False
        })

        user3 = self.createUser({
            "username":"testuser3",
            "email":"nicardid+3@gmail.com",
            "first_name":"test3",
            "last_name":"test13",
            "password":"stringtest12",
            "admin":False
        })

        fellow1 = self.createFellowship(
            {
                "name":"Fellow1",
                "description":"fellowship 1",
                "leader":"testuser3"
            }
            
        )

        fellow2 = self.createFellowship(
            {
                "name":"Fellow2",
                "description":"fellowship 2",
                "leader":"testuser2"
            }
        )
        # return super().handle(*args, **options)
        # adminuser123