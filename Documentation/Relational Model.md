# Relational Model

This is a proposed relational model. The syntax is Table_Name(attribute1, attribute2, ...,attributeN). Attributes in **bold** represents a Primary Key, while attributes in *italics* are foreign keys.

## Entity Tables

Musical_Instance(**instance_id**, title)

Musical_Work(**work_id**, title, alternative_title, subtitle, composer, date_composed,
            place_composed, opus, genre)

Section(**section_id**, title, ordering, length)

Part(**part_id**, title, instrument, length)

Symbolic_Music(**sym_id**, file_name, file_type, file_size, date_added, added_by, version, file,
              *instance_id*, *sym_encoder_id*, encoding_date)

Image(**image_id**, file_type, file_size, date_added, added_by, color_mode, date_created,
      compression_type, color_mode, gama_correction, color_calibration, pixel_array, spatial_resolution, file, *instance_id*, *im_encoder_id*, encoding_date)

Image_Encoder(**im_encoder_id**, software_name, software_version, config_file)

Research_Corpus(**corpus_id**, name, curator, date_created)

Experimental_Study(**study_id**, title, author, contributors, institution, date_perfomed,
                  published, date_published, link, *corpus_id*)

Extracted_Feature(**feature_id**, *symm_id*, name, value, extractor_software)

Symbolic_Encoder(**sym_encoder_id**, software_name, software_version, config_file)

Source(**source_id**, title, publisher, date_of_publication, place_of_publication,
      physical_or_electronic, *instance_id*)

Page(**page_id**, page_number, *source_id*)

Archive(**archive_id**, name, institution, location, link)

Source_Collection(**source_collection_id**, title, author, date_of_publication,
                place_of_publication)

Validator(**validator_id**, software, version, config_file)

## Relationship Tables

Section_In_Work(*work_id*, *section_id*)

Part_In_Section(*section_id*, *part_id*)

Part_In_Work(*work_id*, *part_id*)

Instance_of_Work(*instance_id*, *work_id*)

Instance_of_Section(*instance_id*, *section_id*)

Instance_of_Part(*instance_id*, *part_id*)

Source_Encoder(*source_id*, *sym_encoder_id*, encoding_date)

Image_Of_Page(*image_id*, *page_id*)

Page_Encoder(*page_id*, *im_encoder_id*, encoding_date)

Sym_Music_In_Corpus(*corpus_id*, *sym_id*, date_added)

Source_In_Archive(*archive_id*, *source_id*)

Source_In_Collection(*collection_id*, *source_id*)

Collection_In_Archive(*archive_id*, *collection_id*)

Validates_Image(*image_id*, *validator_id*, validation_date)

Validates_Source(*source_id*, *validator_id*, validation_date)

Validates_Sym_Music(*sym_id*, *validator_id*, validation_date)

## Issues

In a relational model, there is not a way to enforce a participation constraint in a many-to-many relationship. In particular:

* No way to enforce that Musical_Instance participates in at least one instantiates relationship with one of Musical_Work, Section or Part
* No way to enforce that Musical_Instance has at least one source (that is, can't guarantee that each tuple in the Musical_Instance table is referenced at least once in the Source table)
* No way to enforce that Research_Corpus participates in the Sym_In_Corpus relationship
* No way to enforce that Image participates in the Image_Of_Page relationship
* No way to enforce that Archive participates in Source_In_Archive
* No way to enforce that Source_Collection participates in Source_In_Collection