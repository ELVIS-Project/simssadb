# Generated by Django 4.2.1 on 2023-05-31 13:24

from django.db import migrations
from database.models.contribution_musical_work import ContributionMusicalWork
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model

def create_permission(apps, schema_editor):
    Permission = apps.get_model('auth', 'Permission')
    ContentType = apps.get_model('contenttypes', 'ContentType')

    content_type = ContentType.objects.get(app_label='database', model=ContributionMusicalWork._meta.model_name)

    permission = Permission.objects.create(
        codename='creation_access',
        name='Can access creation forms',
        content_type=content_type,
    )
    
    User = get_user_model()
    User.objects.filter(is_superuser=True).update(user_permissions=[permission])

def remove_permission(apps, schema_editor):
    Permission = apps.get_model('auth', 'Permission')

    Permission.objects.filter(codename='creation_access').delete()

class Migration(migrations.Migration):

    dependencies = [
        ('database', '0001_initial'), 
    ]

    operations = [
        migrations.RunPython(create_permission, remove_permission),
    ]
