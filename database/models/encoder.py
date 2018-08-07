"""Define and Encoder model"""
from database.models.encoder_validator_base_model import \
    EncoderValidatorBaseModel


class Encoder(EncoderValidatorBaseModel):
    """A User or Software that encoded a file using a workflow.

    Attributes
    ----------
    Encoder.work_flow_text : models.TextField
        A description of the workflow that was used to encode a File

    Encoder.work_flow_file : models.FileField
        A file that describes or defines the workflow that was used to encode
        or validate a File in the database

    Encoder.notes : models.TextField
        Any extra notes or remarks

    Encoder.user : models.ForeignKey
        The User that encoded a File

    Encoder.software : models.ForeignKey
        The User that encoded a File

    See Also
    --------
    database.models.CustomBaseModel
    database.models.EncoderValidatorBaseModel
    database.models.User
    database.models.Software

    """

    class Meta(EncoderValidatorBaseModel.Meta):
        db_table = 'encoder'

    def __str__(self):
        if self.user_id is not None:
            return "{0} (Encoder)".format(self.user)
        if self.software_id is not None:
            return "{0}".format(self.software)

    def _prepare_summary(self):
        """Prepare a dictionary that summarizes an instance of this model.

        Useful when listing many instances in a list-type view

        Returns
        -------
        summary : dict
            A dictionary containing the essential data to display this object
            in a list-type view

        See Also
        --------
        database.models.CustomBaseModel.summary: the property that validates
        the returned dictionary and exposes it to other classes

        """
        summary = {
            'display': self.__str__(),
            'url':     self.get_absolute_url()
            }
        return summary

    def get_related(self):
        """Get a dictionary listing the related objects of this instance.

        Returns
        -------
        related : dict
            A dictionary of dictionaries listing the related objects of this
            instance. Each entry of related is a dictionary with the following
            entries:
            * list: an iterable of related objects
            * model_name: the name to be displayed when listing these objects
            * model_count: the number of objects in the iterable

        """
        related = {
            'sym_files': {
                'list':        self.symbolicmusicfile_set.all(),
                'model_name':  'Symbolic Music Files Encoded',
                'model_count': self.symbolicmusicfile_set.count()
                }
            }

        return related

    def detail(self):
        """Get all the data about this instance relevant to a user.

        Useful when displaying this object in a detail-type view.

        Returns
        -------
        detail_dict : dict
            A dictionary containing the relevant data about this instance.

        Warnings
        --------
        This method causes database calls and can be expensive, avoid using in a
        loop.

        """
        detail_dict = {
            'title':         self.__str__(),
            'workflow':      self.work_flow_text,
            'workflow_file': self.work_flow_file,
            'user':          self.user,
            'software':      self.software,
            'notes':         self.notes,
            'related':       self.get_related(),
            }

        return detail_dict
