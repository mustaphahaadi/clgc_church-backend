from rest_framework import serializers
from .models import PrayerRequest

class PrayerRequestSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()
    class Meta:
        model = PrayerRequest
        fields = "__all__"
        read_only_fields = ["author","created_at","updated_at"]

    def get_user_name(self,obj):
        return obj.author.username if obj.author else None
    
    def save(self, **kwargs):
        return super().save(**kwargs)