from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

    def __str__(self):
        return f"{self.pk}: {self.username}, {self.password} "


# Create your models here.
class Note(models.Model):
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    title = models.TextField(blank=False, null=False)
    content = models.TextField()
    is_deleted = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Code(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.IntegerField(blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.pk}: {self.code} for {self.user.username} "


class Tag(models.Model):
    note_id = models.ForeignKey(to=Note, on_delete=models.CASCADE)
    tag_name = models.TextField(blank=False, null=False)

    def __str__(self):
        return f"{self.pk}: NoteID: {self.note_id.pk} {self.tag_name} "
