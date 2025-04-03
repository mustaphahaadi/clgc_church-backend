from rest_framework.validators import ValidationError

def validate_vdieo_size(value):
    if value:
        if value.size > 5 * 1024 * 1024:  # 5MB limit
            raise ValidationError('Video file too large. Size should not exceed 5MB.')
    return value