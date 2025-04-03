from rest_framework import serializers
from .models import Sermon

class SermonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sermon
        fields = [
            "title","description","speaker","mp3","video"
        ]