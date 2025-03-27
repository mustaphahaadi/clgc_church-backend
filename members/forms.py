from django import forms
from .models import Testimony

class TestimonyForm(forms.ModelForm):
    class Meta:
        model = Testimony
        fields = ['category', 'testimony', 'image', 'video']
        widgets = {
            'testimony': forms.Textarea(attrs={'rows': 6, 'placeholder': 'Share your testimony here...'}),
            'video': forms.TextInput(attrs={'placeholder': 'https://example.com/your-video'}),
        }