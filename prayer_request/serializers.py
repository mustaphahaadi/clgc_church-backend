from rest_framework import serializers
from .models import PrayerRequest

class PrayerRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrayerRequest
        fields = "__all__"
        read_only_fields = ["author"]