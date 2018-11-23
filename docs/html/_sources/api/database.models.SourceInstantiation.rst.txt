SourceInstantiation
===================

.. currentmodule:: database.models

.. autoclass:: SourceInstantiation
   :show-inheritance:

   .. rubric:: Attributes Summary

   .. autosummary::

      ~SourceInstantiation.id
      ~SourceInstantiation.manifested_by_audio_files
      ~SourceInstantiation.manifested_by_image_files
      ~SourceInstantiation.manifested_by_sym_files
      ~SourceInstantiation.manifested_by_text_files
      ~SourceInstantiation.objects
      ~SourceInstantiation.parts
      ~SourceInstantiation.sections
      ~SourceInstantiation.source
      ~SourceInstantiation.source_id
      ~SourceInstantiation.work
      ~SourceInstantiation.work_id

   .. rubric:: Methods Summary

   .. autosummary::

      ~SourceInstantiation.get_next_by_date_created
      ~SourceInstantiation.get_next_by_date_updated
      ~SourceInstantiation.get_previous_by_date_created
      ~SourceInstantiation.get_previous_by_date_updated

   .. rubric:: Attributes Documentation

   .. autoattribute:: id
   .. autoattribute:: manifested_by_audio_files
   .. autoattribute:: manifested_by_image_files
   .. autoattribute:: manifested_by_sym_files
   .. autoattribute:: manifested_by_text_files
   .. autoattribute:: objects
   .. autoattribute:: parts
   .. autoattribute:: sections
   .. autoattribute:: source
   .. autoattribute:: source_id
   .. autoattribute:: work
   .. autoattribute:: work_id

   .. rubric:: Methods Documentation

   .. automethod:: get_next_by_date_created
   .. automethod:: get_next_by_date_updated
   .. automethod:: get_previous_by_date_created
   .. automethod:: get_previous_by_date_updated
