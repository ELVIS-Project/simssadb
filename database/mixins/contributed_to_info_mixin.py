class ContributedToInfoMixin(object):

    def __get_info_by_role(self, role):
        """
        Gets the data of all the ContributedTo relationships with a certain role

        :param role: The role of the Person in the ContributedTo relationship
        :return: An array of dictionaries containing information about the
        ContributedTo relationships
        """
        contributors_info = []
        role_dict_name = role.lower()
        relationships = self.contributed_to.filter(role=role)
        for relationship in relationships:
            info = {role_dict_name: relationship.person,
                    'date':         relationship.date,
                    'location':     relationship.location,
                    'certain':      relationship.certain}
            contributors_info.append(info)
        return contributors_info


    @property
    def composers(self):
        """Gets the data of all the COMPOSER relationships"""
        return self.__get_info_by_role('COMPOSER')


    @property
    def arrangers(self):
        """Gets the data of all the ARRANGER relationships"""
        return self.__get_info_by_role('ARRANGER')


    @property
    def authors(self):
        """Gets the data of all the AUTHOR relationships"""
        return self.__get_info_by_role('AUTHOR')


    @property
    def transcribers(self):
        """Gets the data of all the TRANSCRIBER relationships"""
        return self.__get_info_by_role('TRANSCRIBER')


    @property
    def improvisers(self):
        """Gets the data of all the IMPROVISER relationships"""
        return self.__get_info_by_role('IMPROVISER')


    @property
    def performers(self):
        """Gets the data of all the PERFORMER relationships"""
        return self.__get_info_by_role('PERFORMER')


    @property
    def dates_of_composition(self):
        """Gets the date of contribution of all the composers of this Work/Section/Part"""
        dates = []
        relationships = self.contributed_to.filter(role='COMPOSER')
        for relationship in relationships:
            dates.append(relationship.date)
        return dates


    @property
    def places_of_composition(self):
        """Gets the place of contribution of all the composers of this Work/Section/Part"""
        places = []
        relationships = self.contributed_to.filter(role='COMPOSER')
        for relationship in relationships:
            places.append(relationship.location)
        return places


    @property
    def certainty(self):
        """Returns True if all the relationships have certain == True"""
        for relationship in self.contributed_to.all():
            if not relationship.certain:
                return False
        return True
