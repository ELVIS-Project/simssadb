import zipfile
import io
import os
from django.db.models import QuerySet
from typing import Optional
from database.models.file import File
from database.models.feature_file import FeatureFile


def zip_files(files: QuerySet,
              zipfile_name: str,
              feature_files: Optional[QuerySet] = None) -> io.BytesIO:
    """Zips all files in a QuerySet of files without writing to disk

    Takes all the files in a QuerySet of files and zips them in memory, 
    returning a io.BytesIO in-memory buffer of bytes. The caller should close
    the buffer using its close() method.

    Parameters
    ----------
    files : QuerySet
        A QuerySet of Files
    zipfile_name : str
        The name of the final zip file
    feature_files: Optional[QuerySet]
        An optional QuerySet of Feature Files that are describe the features of the Files

    Raises
    ------
    TypeError: if the model of the QuerySet is not File or FeatureFile.

    Returns
    -------
    io.BytesIO
        An in-memory buffer with the zipfile. Should be closed by caller.
    """
    model_name = files.model.__name__
    if model_name != "File":
        raise TypeError("The QuerySet model is not File")

    in_memory = io.BytesIO()
    zip_file = zipfile.ZipFile(in_memory, mode="w")
    zip_subdir = zipfile_name

    for file in files:
        file_dir, file_name = os.path.split(file.file.url)
        zip_path = os.path.join(zip_subdir, file_name)
        zip_file.write(file.file.url, zip_path)

    if feature_files is not None:
        if feature_files.model.__name__ != "FeatureFile":
            raise TypeError("The QuerySet model is not FeatureFile")
        for feature_file in feature_files:
            file_dir, feature_file_name = os.path.split(feature_file.file.name)
            zip_path = os.path.join(zip_subdir, feature_file_name)
            zip_file.write(feature_file.file.name, zip_path)
    zip_file.close()

    return in_memory
