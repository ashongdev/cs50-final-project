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


# class IsArchived(models.Model):
#     note_id = models.ForeignKey(to=Note, on_delete=models.CASCADE)
#     updated_at = models.DateTimeField(auto_now=True)
#     is_archived = models.BooleanField(
#         default=True
#     )  # True because we only insert into this table when a note is archived, from then on, we just toggled `is_archived`


# class IsDeleted(models.Model):
#     note_id = models.ForeignKey(to=Note, on_delete=models.CASCADE)
#     updated_at = models.DateTimeField(auto_now=True)
#     is_deleted = models.BooleanField(default=True)  # same idea as IsArchived


class Tag(models.Model):
    note_id = models.ForeignKey(to=Note, on_delete=models.CASCADE)
    tag_name = models.TextField(blank=False, null=False)
