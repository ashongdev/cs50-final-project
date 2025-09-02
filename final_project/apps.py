from django.apps import AppConfig
from django.db.models.signals import post_migrate


class FinalProjectConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "final_project"

    def ready(self):
        from django.contrib.auth import get_user_model
        from django.db import OperationalError, ProgrammingError

        User = get_user_model()

        def create_mail_sender_user(sender, **kwargs):
            try:
                if not User.objects.filter(username="notebook").exists():
                    User.objects.create_superuser(
                        username="notebook",
                        email="notebook@gmail.com",
                        password="notebook",
                    )
            except (OperationalError, ProgrammingError):
                # Happens before migrations are applied
                pass

        post_migrate.connect(create_mail_sender_user, sender=self)
