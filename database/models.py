from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.postgres.fields import ArrayField
from django.urls import reverse

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


class MusicalWork(models.Model):
    #author = models.ForeignKey('auth.User', on_delete=models.DO_NOTHING)  # author connects the superuser on the website
    title = models.CharField(max_length=200, blank=False)
    alternative_titles = models.CharField(max_length=200, blank=False)
    subtitle = models.CharField(max_length=200, blank=True)
    opus = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse("musicalwork_detail", kwargs={'pk': self.pk})  # After creating a post, go to 'post_detail' page,
        # with the primary key you just created
    class Meta:
        db_table = 'musical_work'

    def __str__(self):
        return self.title


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
