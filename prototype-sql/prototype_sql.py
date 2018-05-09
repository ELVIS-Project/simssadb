from peewee import *
import sqlite3

db = SqliteDatabase('test.db')

class BaseModel(Model):
  class Meta:
    database = db

# Musical_Instance(**instance_id**, title)
class MusicalInstance(BaseModel):
  title = CharField()

# Musical_Work(**work_id**, title, alternative_title, subtitle, composer, date_composed, place_composed, opus, genre)
class MusicalWork(BaseModel):
  title = CharField()
  alternative_title = CharField(null = True)
  subtitle = CharField(null = True)
  composer = CharField(null = True)
  date_composed = DateField(null = True)
  place_composed = CharField(null = True)
  opus = CharField(null = True)
  genre = CharField(null = True)

# Section(**section_id**, title, ordering, length)
class Section(BaseModel):
  title = CharField()
  ordering = IntegerField (constraints = [Check('ordering > 0')], null = True)
  length = IntegerField(null = True)

#Part(**part_id**, title, instrument, length)
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

#Symbolic_Music(**sym_id**, file_name, file_type, file_size, date_added, added_by, version, file,*instance_id*, *sym_encoder_id*, encoding_date)
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

