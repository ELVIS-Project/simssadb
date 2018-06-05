from django.contrib import admin
from .models import CustomBaseModel, Profile, MusicalWork, Genre, Section, Part
# Register your models here.
admin.site.register(Profile)
admin.site.register(MusicalWork)
admin.site.register(Genre)
admin.site.register(Section)
admin.site.register(Part)
