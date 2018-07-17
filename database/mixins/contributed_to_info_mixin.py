class ContributedToInfoMixin(object):

    def __get_data_by_role(self, role):
        """
        Gets the data of all the ContributedTo relationships with a certain role

        :param role: The role of the Person in the ContributedTo relationship
        :return: An array of dictionaries containing information about the
        ContributedTo relationships
        """
        contributors_data = []
        relationships = self.contributed_to.iterator()
        for relationship in relationships:
            if relationship.role == role:
                contributors_data.append(relationship.summary())
        return contributors_data

    @property
    def composers(self):
        """Gets the data of all the COMPOSER relationships"""
        return self.__get_data_by_role('COMPOSER')

    @property
    def arrangers(self):
        """Gets the data of all the ARRANGER relationships"""
        return self.__get_data_by_role('ARRANGER')

    @property
    def authors(self):
        """Gets the data of all the AUTHOR relationships"""
        return self.__get_data_by_role('AUTHOR')

    @property
    def transcribers(self):
        """Gets the data of all the TRANSCRIBER relationships"""
        return self.__get_data_by_role('TRANSCRIBER')

    @property
    def improvisers(self):
        """Gets the data of all the IMPROVISER relationships"""
        return self.__get_data_by_role('IMPROVISER')

    @property
    def performers(self):
        """Gets the data of all the PERFORMER relationships"""
        return self.__get_data_by_role('PERFORMER')

    @property
    def dates_of_composition(self):
        """Gets the date of contribution of all the composers of this Work/Section/Part"""
        dates = []
        composers = self.composers
        for composer in composers:
            dates.append(composer['date'])
        return dates

    @property
    def places_of_composition(self):
        """Gets the place of contribution of all the composers of this Work/Section/Part"""
        places = []
        composers = self.composers
        for composer in composers:
            places.append(composer['location'])
        return places

    @property
    def certainty(self):
        """Returns True if all the relationships have certain == True"""
        certainties = self.contributed_to.values_list('certain', flat=True)
        print(certainties)
        if False in certainties:
            return False
        else:
            return True
