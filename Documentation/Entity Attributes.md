# Entity Attributes

The following are ideas for the attributes of each entity. There are no relationships specified, i.e. a musical work containing
a section. Those relationships are already defined in the Entity Relationship Model. Not all of these fields are mandatory, but we could decide on
which ones are and probably enforce them on the database.

## Musical Work

* Title
* Alternative title
* Subtitle
* Composer (Could probably be another entity with an ID and a way to link all the alternative spellings)
* Date of composition
* Place of composition
* Opus
* Genre (I know that this is complicated but I figured I should add a field for it!)
* Number of sections

## Section

* Name
* Ordering inside of musical work (i.e 1st movement, 2nd movement, etc)
* Length (in bars? Maybe bars does not apply to all kinds of music)
* Instrumentation? (But this could also be represented by the instruments/voices of each part)

## Part

* Instrument/Voice
* Length (in bars? Same problem as above)

## Musical Instance

This is abstract, I'm not too sure on how to add attributes. I understood it to be a connector between musical work, image or symbolic file and source

## Symbolic Music

* File type
* File size
* Date added
* Added by
* Version (i.e. XML version 1.0, MEI version 3.0)
* Link to the file (URI?)

## Image

* File type
* File size
* Date added
* Added by
* Color mode
* Date created
* Compression type
* Color mode
* Gama correction
* Color calibration
* Pixel array (Pixel width vs height)
* Spatial resolution (in ppi, pixels per inch)
* Link to the file (URI?)

## Image Encoder

Maybe some of the metadata above can go in here?

* Software name
* Software version
* Configuration file (not too sure about this)
* Encoding date

## Research Corpus

* Curator (or should I name it author?)
* Number of pieces
* Date created

## Experimental Study

* Author
  * (Maybe we should create a entity for authors? It could contain some basic info like name, title, institution, email, and many entities could reference it)
* Contributors (list)
* Institution
* Date performed
* Published (Y/N)
* Date published
* Link to study

## Extracted Feature

* Name
* Value (encoded as an array)
* Extractor software (maybe this could also be an entity and would similar attributes to both encoder entities)

## Symbolic Encoder

* Software
* Version
* Configuration file (not too sure about this)
* Encoding date

## Source

* Title
* Publisher
* Date of publication
* Place of publication
* Number of pages
* Physical/Electronic

## Page

* Page number

## Archive

* Title
* Institution
* Location
* Link

## Collection of Sources

* Title
* Author
* Date of publication
* Place of publication
* Number of sources

## Validator

* Software
* Version
* Configuration file (not too sure about this)
* Encoding date
* If it is a person we could add
  * Name
  * Institution

References:

[Technical Guidelines for Digitizing Archival Materials for Electronic Access: Creation of Production Master Files](https://www.archives.gov/files/preservation/technical/guidelines.pdf)