import zipfile
import io
import os
from django.db.models import QuerySet
from database.models.file import File
from database.models.feature_file import FeatureFile


def zip_files(files: QuerySet, zipfile_name: str) -> io.BytesIO:
    """Zips all files in a QuerySet of files without writing to disk

    Takes all the files in a QuerySet of files and zips them in memory, 
    returning a io.BytesIO in-memory buffer of bytes. The caller should close
    the buffer using its close() method.

    Parameters
    ----------
    files : QuerySet
        A QuerySet of files (either content files or feature files)
    zipfile_name : str
        The name of the final zip file

    Raises
    ------
    TypeError: if the model of the QuerySet is not File or FeatureFile.

    Returns
    -------
    io.BytesIO
        An in-memory buffer with the zipfile. Should be closed by caller.
    """
    model_name = files.model.__name__
    if model_name != "File" and model_name != "FeatureFile":
        raise TypeError("The QuerySet model is not File or FeatureFile")

    in_memory = io.BytesIO()
    zip_file = zipfile.ZipFile(in_memory, mode="w")
    zip_subdir = zipfile_name

    for file in files:
        file_dir, file_name = os.path.split(file.file.url)
        zip_path = os.path.join(zip_subdir, file_name)
        zip_file.write(file.file.url, zip_path)
    zip_file.close()

    return in_memory
