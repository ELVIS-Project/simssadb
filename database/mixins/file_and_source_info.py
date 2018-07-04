class FileAndSourceInfoMixin(object):
    """
    A mixin for Work/Section/Part to access information about Sources and Files
    """

    @property
    def symbolic_files(self):
        """Gets all the Symbolic Files related to this Work/Section/Part"""
        files = []
        sources = self.sources.all()
        for source in sources:
            files.extend(list(source.manifested_by_sym_files.all()))
        return files

    @property
    def symbolic_music_formats(self):
        """Gets the formats of all the Symbolic Files related to this Work/Section/Part"""
        formats = set()
        files = self.symbolic_files
        for file in files:
            formats.add(file.file_type)
        return formats

    @property
    def image_files(self):
        """Gets all the Image Files related to this Work/Section/Part"""
        files = []
        sources = self.sources.all()
        for source in sources:
            files.extend(list(source.manifested_by_image_files.all()))
        return files

    @property
    def image_formats(self):
        """Gets the formats of all the Image Files related to this Work/Section/Part"""
        formats = set()
        files = self.image_files
        for file in files:
            formats.add(file.file_type)
        return formats

    @property
    def text_files(self):
        """Gets all the Symbolic Files related to this Work/Section/Part"""
        files = []
        sources = self.sources.all()
        for source in sources:
            files.extend(list(source.manifested_by_text_files.all()))
        return files

    @property
    def text_formats(self):
        """Gets the formats of all the Image Files related to this Work/Section/Part"""
        formats = set()
        files = self.text_files
        for file in files:
            formats.add(file.file_type)
        return formats

    @property
    def audio_files(self):
        """Gets all the Symbolic Files related to this Work/Section/Part"""
        files = []
        sources = self.sources.all()
        for source in sources:
            files.extend(list(source.manifested_by_audio_files.all()))
        return files

    @property
    def audio_formats(self):
        """Gets the formats of all the Image Files related to this Work/Section/Part"""
        formats = set()
        files = self.audio_files
        for file in files:
            formats.add(file.file_type)
        return formats

    @property
    def encoders(self):
        """Gets all the Encoders for files related to this Work/Section/Part"""
        encoders = set()
        sources = self.sources.all()
        for source in sources:
            encoders.update(list(source.encoders.all()))
        return encoders

    @property
    def validators(self):
        """Gets all the Validators for files related to this Work/Section/Part"""
        validators = set()
        sources = self.sources.all()
        for source in sources:
            validators.update(list(source.validators.all()))
        return validators

    @property
    def features(self):
        """Gets all the Features extracted from files related to this Work/Section/Part"""
        features = []
        sym_files = self.symbolic_files
        for file in sym_files:
            for feature in file.extractedfeature_set.all():
                features.append(feature)
        return features

    @property
    def collections_of_sources(self):
        """Gets all the Collections of Sources related to this Work/Section/Part"""
        collections = set()
        sources = self.sources.all()
        for source in sources:
            collections.add(source.part_of_collection)
        return collections

    @property
    def languages(self):
        """Gets all the languages of the Sources and Text Files related to this Work/Section/Part"""
        languages = set()
        sources = self.sources.all()
        # This is a bit ugly, but I'm not sure how to do it better
        for source in sources:
            if source.languages:
                for language in source.languages:
                    languages.add(language)
            for text_file in source.manifested_by_text_files.all():
                if text_file.languages:
                    for language in text_file.languages:
                        languages.add(language)
        return languages
