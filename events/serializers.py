from rest_framework import serializers
from .models import Events

class EventSerializers(serializers.ModelSerializer):
    class Meta:
        model = Events
        fields = "__all__"
        read_only_fields = [
            "id","created_at","updated_at"
        ]