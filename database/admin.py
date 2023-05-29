"""Register models in the Django admin site"""
from django.contrib import admin
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Group, User
from database.models.musical_work import MusicalWork
from database.models.section import Section
from database.models.part import Part
from database.models.genre_as_in_style import GenreAsInStyle
from database.models.genre_as_in_type import GenreAsInType
from database.models.geographic_area import GeographicArea
from database.models.instrument import Instrument
from database.models.file import File
from database.models.research_corpus import ResearchCorpus
from database.models.experimental_study import ExperimentalStudy
from database.models.extracted_feature import ExtractedFeature
from database.models.source import Source
from database.models.person import Person
from database.models.archive import Archive
from database.models.contribution_musical_work import ContributionMusicalWork
from database.models.encoding_workflow import EncodingWorkFlow
from database.models.software import Software
from database.models.validation_workflow import ValidationWorkFlow
from database.models.feature_type import FeatureType
from database.models.source_instantiation import SourceInstantiation
from database.models.type_of_section import TypeOfSection

"""
Reserve permission to creation forms to admin until ready for production
"""
content_type = ContentType.objects.get(app_label='database', model=ContributionMusicalWork._meta.model_name)
if Permission.objects.filter(content_type=content_type) == None:
    permission = Permission.objects.create(
        codename='creation_access',
        name='Can access creation forms',
        content_type=content_type,
    )
    admin_user = User.objects.get(email='reb@miz.com')
    admin_user.user_permissions.add(permission)

@admin.register(MusicalWork)
class MusicalWorkAdmin(admin.ModelAdmin):
    list_display = ("date_created","date_updated")
    search_fields = ("variant_titles",)
    list_filter = ("date_created","date_updated")

@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ("title","musical_work","parent_section","child_sections","source_instantiations","date_created","date_updated")
    search_fields = ("title",)
    list_filter = ("date_created","date_updated")

@admin.register(Part)
class PartAdmin(admin.ModelAdmin):
    list_display = ("name","musical_work","section","date_created","date_updated")
    search_fields = ("name","date_created","date_updated")
    list_filter = ("date_created","date_updated")

@admin.register(GenreAsInStyle)
class GenreAsInStyleAdmin(admin.ModelAdmin):
    list_display = ("name","date_created","date_updated")
    search_fields = ("name","date_created","date_updated")
    list_filter = ("date_created","date_updated")

@admin.register(GenreAsInType)
class GenreAsInTypeAdmin(admin.ModelAdmin):
    list_display = ("name","date_created","date_updated")
    search_fields = ("name","date_created","date_updated")
    list_filter = ("date_created","date_updated")

@admin.register(GeographicArea)
class GeographicAreaAdmin(admin.ModelAdmin):    
    list_display = ("name","authority_control_url","date_created","date_updated")
    search_fields = ("name","date_created","date_updated")
    list_filter = ("date_created","date_updated")

@admin.register(Instrument)
class InstrumentAdmin(admin.ModelAdmin):
    list_display = ("name","date_created","date_updated")
    search_fields = ("name","date_created","date_updated")
    list_filter = ("date_created","date_updated")

@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ("file","file_type","instantiates","date_created","date_updated")
    search_fields = ("file","date_created","date_updated")
    list_filter = ("date_created","date_updated")

@admin.register(ResearchCorpus)
class ResearchCorpusAdmin(admin.ModelAdmin):
    list_display = ("title","date_created","date_updated")
    search_fields = ("title","date_created","date_updated")
    list_filter = ("date_created","date_updated")

@admin.register(ExperimentalStudy)
class ExperimentalStudyAdmin(admin.ModelAdmin):
    list_display = ("title","date_created","date_updated")
    search_fields = ("title","date_created","date_updated")
    list_filter = ("date_created","date_updated")

@admin.register(ExtractedFeature)
class ExtractedFeatureAdmin(admin.ModelAdmin):
    list_display = ("extracted_with","date_created","date_updated")
    search_fields = ("extracted_with","date_created","date_updated")
    list_filter = ("date_created","date_updated")

@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = ("title","parent_source","child_source","source_instantiations","date_created","date_updated")
    search_fields = ("title","date_created","date_updated")
    list_filter = ("date_created","date_updated")

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("given_name","surname","date_created","date_updated")
    search_fields = ("given_name","surname","date_created","date_updated")
    list_filter = ("given_name","surname","date_created","date_updated")

@admin.register(Archive)
class ArchiveAdmin(admin.ModelAdmin):
    list_display = ("name","url","date_created","date_updated")
    search_fields = ("name","date_created","date_updated")
    list_filter = ("name","date_created","date_updated")

@admin.register(ContributionMusicalWork)
class ContributionMusicalWorkAdmin(admin.ModelAdmin):
    list_display = ("contributed_to_work","person","role","date_created","date_updated")
    search_fields = ("contributed_to_work","person","role","date_created","date_updated")
    list_filter = ("role","date_created","date_updated")

@admin.register(EncodingWorkFlow)
class EncodingWorkFlowAdmin(admin.ModelAdmin):
    list_display = ("encoder_names","encoding_software","date_created","date_updated")
    search_fields = ("encoder_names","encoding_software","date_created","date_updated")
    list_filter = ("date_created","date_updated")

@admin.register(Software)
class SoftwareAdmin(admin.ModelAdmin):
    list_display = ("name","version","date_created","date_updated")
    search_fields = ("name","version","date_created","date_updated")
    list_filter = ("date_created","date_updated")

@admin.register(ValidationWorkFlow)
class ValidationWorkFlowAdmin(admin.ModelAdmin):
    list_display = ("validator_names","validator_software","date_created","date_updated")
    search_fields = ("validator_names","validator_software","date_created","date_updated")
    list_filter = ("date_created","date_updated")

@admin.register(FeatureType)
class FeatureTypeAdmin(admin.ModelAdmin):
    list_display = ("name","date_created","date_updated")
    search_fields = ("name","date_created","date_updated")
    list_filter = ("date_created","date_updated")

@admin.register(SourceInstantiation)
class SourceInstantiationAdmin(admin.ModelAdmin):
    list_display = ("source","work","date_created","date_updated")
    search_fields = ("source","work","date_created","date_updated")
    list_filter = ("date_created","date_updated")

@admin.register(TypeOfSection)
class TypeOfSectionAdmin(admin.ModelAdmin):
    list_display = ("name","date_created","date_updated")
    search_fields = ("name","date_created","date_updated")
    list_filter = ("date_created","date_updated")
