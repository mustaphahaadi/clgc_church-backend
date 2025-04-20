from rest_framework import serializers
from .models import Sermon

class SermonSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()
    class Meta:
        model = Sermon
        fields = [
            "id",
            "title","description",
            "speaker","mp3",
            "video","user_name",
            "series","video_link",
            "scriptures","thumbnail","created_at"
        ]

        read_only_fields = ["reated_at",]
    
    def get_user_name(self, obj):
        if obj.speaker:
            if obj.speaker.first_name and obj.speaker.last_name:
                return f"{obj.speaker.first_name} {obj.speaker.last_name}"
            return obj.speaker.username
        return "Anonymous"