from peewee import *
import sqlite3

db = SqliteDatabase('test.db')

class BaseModel(Model):
  class Meta:
    database = db

class MusicalInstance(BaseModel):
  title = CharField()

class MusicalWork(BaseModel):
  title = CharField()
  alternative_title = CharField(null = True)
  subtitle = CharField(null = True)
  composer = CharField(null = True)
  date_composed = DateField(null = True)
  place_composed = CharField(null = True)
  opus = CharField(null = True)
  genre = CharField(null = True)

class Section(BaseModel):
  title = CharField()
  ordering = IntegerField (constraints = [Check('ordering > 0')], null = True)
  length = IntegerField(null = True)

class Part(BaseModel):
  title = CharField()
  instrument = CharField(null = True)
  length = IntegerField(null = True)

class ImageEncoder(BaseModel):
  software_name = CharField()
  software_version = CharField()
  config_file = CharField(null = True)

class SymbolicEncoder(BaseModel):
  software_name = CharField()
  software_version = CharField()
  config_file = CharField(null = True)

class SymbolicMusic(BaseModel):
  file_type = CharField()
  file_type = CharField()
  file_size = BigIntegerField()
  version = CharField()
  file = CharField() #For now this is simply going to be an string of the absolute path for a file. In Django we will use a FileField
  date_added = DateField()
  added_by = CharField(null = True)
  musical_instance = ForeignKeyField(MusicalWork)
  encoder = ForeignKeyField(SymbolicEncoder, null = True)
  encoding_date = DateField()

class Image(BaseModel):
  file_type = CharField()
  file_type = CharField()
  file_size = BigIntegerField()
  version = CharField()
  file = CharField() #For now this is simply going to be an string of the absolute path for a file. In Django we will use a FileField
  date_added = DateField()
  added_by = CharField(null = True)
  musical_instance = ForeignKeyField(MusicalWork)
  encoder = ForeignKeyField(ImageEncoder, null = True)
  encoding_date = DateField()
  compression_type = CharField(null = True)
  color_mode = CharField(null = True)
  gama_correction = CharField(null = True)
  color_calibration = CharField(null = True)
  pixel_array = IntegerField(null = True)
  spatial_resolution = IntegerField(null = True)

class ResearchCorpus(BaseModel):
  name = CharField()
  curator = CharField(null = True)
  date_created = DateField()

class ExperimentalStudy(BaseModel):
  title = CharField()
  contributor = CharField(null = True)
  institution = CharField(null = True)
  date_performed = CharField(null = True)
  published = BooleanField(default = False)
  date_published = DateField(null = True)
  link = CharField(null = True)
  corpus_used = ForeignKeyField(ResearchCorpus, null = False)

class ExtractedFeature(BaseModel):
  name = CharField()
  value = IntegerField()
  extractor_softwar= CharField(null = True)
  symbolic_file = ForeignKeyField(SymbolicMusic)

class MusicalSource(BaseModel):
  title = CharField()
  publisher = CharField(null = True)
  date_of_publication = DateField(null = True)
  place_of_publication = DateField(null = True)
  physical_or_electronic = CharField(null = True)
  musical_instance = ForeignKeyField(MusicalInstance)

class Page(BaseModel):
  page_number = IntegerField(constraints = [Check('page_number > 0')])
  source = ForeignKeyField(MusicalSource)

class Archive(BaseModel):
  name = CharField()
  institution = CharField(null = True)
  location = CharField(null = True)
  link = CharField(null = True)

class SourceCollection(BaseModel):
  title = CharField()
  author = CharField(null = True)
  date_of_publication = CharField(null = True)
  place_of_publication = CharField(null = True)

class Validator(BaseModel):
  software = CharField()
  software_version = CharField()
  config_file = CharField(null = True)

  