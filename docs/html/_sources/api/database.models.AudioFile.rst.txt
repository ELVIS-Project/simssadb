AudioFile
=========

.. currentmodule:: database.models

.. autoclass:: AudioFile
   :show-inheritance:

   .. rubric:: Attributes Summary

   .. autosummary::

      ~AudioFile.encoded_with
      ~AudioFile.file
      ~AudioFile.id
      ~AudioFile.length
      ~AudioFile.manifests
      ~AudioFile.manifests_id
      ~AudioFile.objects
      ~AudioFile.recording_date
      ~AudioFile.validated_by

   .. rubric:: Methods Summary

   .. autosummary::

      ~AudioFile.get_next_by_date_created
      ~AudioFile.get_next_by_date_updated
      ~AudioFile.get_previous_by_date_created
      ~AudioFile.get_previous_by_date_updated

   .. rubric:: Attributes Documentation

   .. autoattribute:: encoded_with
   .. autoattribute:: file
   .. autoattribute:: id
   .. autoattribute:: length
   .. autoattribute:: manifests
   .. autoattribute:: manifests_id
   .. autoattribute:: objects
   .. autoattribute:: recording_date
   .. autoattribute:: validated_by

   .. rubric:: Methods Documentation

   .. automethod:: get_next_by_date_created
   .. automethod:: get_next_by_date_updated
   .. automethod:: get_previous_by_date_created
   .. automethod:: get_previous_by_date_updated
