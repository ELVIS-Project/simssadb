class ContributedToInfoMixin(object):


    def get_info_by_role(self, role):
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
        return self.get_info_by_role('COMPOSER')


    @property
    def arrangers(self):
        return self.get_info_by_role('ARRANGER')


    @property
    def authors(self):
        return self.get_info_by_role('AUTHOR')


    @property
    def transcribers(self):
        return self.get_info_by_role('TRANSCRIBER')


    @property
    def improvisers(self):
        return self.get_info_by_role('IMPROVISER')


    @property
    def performers(self):
        return self.get_info_by_role('PERFORMERS')


    @property
    def dates_of_composition(self):
        """Gets the date of contribution of all the composers of this Work"""
        dates = []
        relationships = self.contributed_to.filter(role='COMPOSER')
        for relationship in relationships:
            dates.append(relationship.date)
        return dates


    @property
    def places_of_composition(self):
        """Gets the place of contribution of all the composers of this Work"""
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
