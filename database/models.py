from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.postgres.fields import ArrayField


class CustomBaseModel(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Profile(CustomBaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    institution = models.TextField(max_length=100, blank=True)
    title = models.TextField(max_length=100, blank=True)

    class Meta:
        db_table = 'profile'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class MusicalWork(CustomBaseModel):
    title = models.CharField(max_length=200, blank=False)
    alternative_titles = ArrayField(
            ArrayField(
                    models.CharField(max_length=200, blank=True)
            )
    )
    subtitle = models.CharField(max_length=200, blank=True)
    opus = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        db_table = 'musical_work'


class Genre(CustomBaseModel):
    name = models.CharField(max_length=200, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        db_table = 'genre'


class Section(CustomBaseModel):
    title = models.CharField(max_length=200)
    ordering = models.PositiveIntegerField()


    class Meta:
        db_table = 'section'


class Part(CustomBaseModel):
    title = models.CharField(max_length=200)
    ordering = models.PositiveIntegerField()


    class Meta:
        db_table = 'part'
