from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework_jwt.settings import api_settings

from .models import CustomUser


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(instance)
        token = jwt_encode_handler(payload)

        instance.jwt_token = token
        instance.save()
