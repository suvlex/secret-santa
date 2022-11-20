from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self) -> None:
        from core.models import User
        from fieldsignals import post_save_changed
        from .signals import change_member

        post_save_changed.connect(change_member, sender=User, fields=['email'])