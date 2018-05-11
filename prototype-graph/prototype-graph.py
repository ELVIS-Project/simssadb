from neomodel import *
config.DATABASE_URL = 'bolt://neo4j:test@localhost:7687'


class MusicalInstance(StructuredNode):
    uid = UniqueIdProperty()
    title = StringProperty(required=True)
    instantiates_work = RelationshipTo('MusicalWork', 'INSTANCE_OF')
    instantiates_section = RelationshipTo('Section', 'INSTANCE_OF')
    instantiates_part = RelationshipTo('Part', 'INSTANCE_OF')

class Composer(StructuredNode):
    uid = UniqueIdProperty()
    name = StringProperty(required=True)
    composed_work = RelationshipTo('MusicalWork', 'COMPOSED')
    composed_section = RelationshipTo('Section', 'COMPOSED')
    composed_part = RelationshipTo('Part', 'COMPOSED')

class Genre(StructuredNode):
    uid = UniqueIdProperty()
    name = StringProperty(required=True)

class Author(StructuredNode):
    uid = UniqueIdProperty()
    name = StringProperty(required=True)
    belongs_to = RelationshipTo('Institution', 'BELONGS_TO')

class Institution(StructuredNode):
    uid = UniqueIdProperty()
    name = StringProperty(required=True)

class Location(StructuredNode):
    uid = UniqueIdProperty()
    name = StringProperty(required=True)

class MusicalWork(StructuredNode):
    uid = UniqueIdProperty()
    title = StringProperty(required=True)
    alternative_title = StringProperty(required=False)
    subtitle = StringProperty(required=False)
    date_composed = DateProperty(required=False)
    opus = StringProperty(required=False)
    genre = RelationshipTo('Genre', 'OF')
    composed_at = RelationshipTo('Location', 'COMPOSED_AT')


class Section(StructuredNode):
    uid = UniqueIdProperty()
    title = StringProperty(required=True)
    ordering = IntegerProperty(required=True)
    length = IntegerProperty(required=False)
    part_of = RelationshipTo('MusicalWork', 'PART_OF')



class Part(StructuredNode):
    uid = UniqueIdProperty()
    title = StringProperty(required=True)
    instrument = StringProperty(required=False)
    length = IntegerProperty(required=False)
    part_of_section = ('Section', 'PART_OF')
    part_of_work = ('MusicalWork', 'PART_OF')


class ImageEncoder(StructuredNode):
    uid = UniqueIdProperty()
    software_name = StringProperty(required=True)
    software_version = StringProperty(required=False)
    config_file = StringProperty(required=False)


class SymbolicEncoder(StructuredNode):
    uid = UniqueIdProperty()
    software_name = StringProperty(required=True)
    software_version = StringProperty(required=False)
    config_file = StringProperty(required=False)


class SymbolicMusic(StructuredNode):
    uid = UniqueIdProperty()
    file_type = StringProperty(required=True)
    file_name = StringProperty(required=True)
    file_size = IntegerProperty(required=True)
    version = StringProperty(required=True)
    # For now this is simply going to be a absolute path for a file.
    # In Django we will use a FileField
    file = StringProperty(required=True)
    date_added = DateProperty(required=False)
    encoding_date = DateProperty(required=False)
    encoded_with = RelationshipTo('SymbolicEncoder', 'ENCODED_WITH', cardinality=One)


class Image(StructuredNode):
    uid = UniqueIdProperty()
    file_type = StringProperty(required=True)
    file_name = StringProperty(required=True)
    file_size = IntegerProperty(required=True)
    version = StringProperty(required=True)
    # For now this is simply going to be a absolute path for a file.
    # In Django we will use a FileField
    file = StringProperty(required=True)
    date_added = DateProperty(required=False)
    added_by = StringProperty(required=False)
    encoding_date = DateProperty(required=False)
    compression_type = StringProperty(required=False)
    color_mode = StringProperty(required=False)
    gama_correction = StringProperty(required=False)
    color_calibration = StringProperty(required=False)
    pixel_array = IntegerProperty(required=False)
    spatial_resolution = IntegerProperty(required=False)
    encoded_with = RelationshipTo('ImageEncoder', 'ENCODED_WITH', cardinality=One)


class ResearchCorpus(StructuredNode):
    uid = UniqueIdProperty()
    name = StringProperty(required=True)
    date_created = DateProperty(required=False)
    contains = RelationshipTo('SymbolicMusic', 'CONTAINS', cardinality=OneOrMore)


class ExperimentalStudy(StructuredNode):
    uid = UniqueIdProperty()
    title = StringProperty(required=True)
    date_performed = StringProperty(required=False)
    published = BooleanProperty(default=False)
    date_published = DateProperty(required=False)
    link = StringProperty(required=False)
    uses = RelationshipTo('ResearchCorpus', 'USES', cardinality=One)


class ExtractedFeature(StructuredNode):
    uid = UniqueIdProperty()
    name = StringProperty(required=True)
    value = ArrayProperty(required=True)
    extractor_software = StringProperty(required=False)
    feature_of = RelationshipFrom('SymbolicMusic', 'FEATURE_OF', cardinality=One)


# Named it MusicalSource because there is a Source class defined in the package
class MusicalSource(StructuredNode):
    uid = UniqueIdProperty()
    title = StringProperty(required=True)
    publisher = StringProperty(required=False)
    date_of_publication = DateProperty(required=False)
    physical_or_electronic = StringProperty(required=False)
    encoded_with = RelationshipTo('SymbolicEncoder', 'ENCODED_WITH', cardinality=One)
    source_of = RelationshipTo('MusicalInstance', 'SOURCE_OF', cardinality=One)


class Page(StructuredNode):
    uid = UniqueIdProperty()
    page_number = IntegerProperty(required=True)
    page_of = RelationshipTo('Source', 'PART_OF', cardinality=One)


class Archive(StructuredNode):
    uid = UniqueIdProperty()
    name = StringProperty(required=True)
    link = StringProperty(required=False)
    contains_source = RelationshipTo('Source', 'CONTAINS')
    contains_collection = RelationshipTo('SourceCollection', 'CONTAINS')


class SourceCollection(StructuredNode):
    uid = UniqueIdProperty()
    title = StringProperty(required=True)
    date_of_publication = StringProperty(required=False)
    contains_source = RelationshipTo('Source', 'CONTAINS')


class Validator(StructuredNode):
    uid = UniqueIdProperty()
    software = StringProperty(required=True)
    software_version = StringProperty(required=True)
    config_file = StringProperty(required=False)
    validates_source = RelationshipTo('Source', 'VALIDATES')
    validates_sym = RelationshipTo('SymbolicMusic', 'VALIDATES')
    validates_image = RelationshipTo('Image', 'VALIDATES')


install_all_labels()

