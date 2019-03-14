import os
from music21 import *
import sys

proj_path = "/Users/Gustavo/Development/simssadb"

# This is so mpythoy local_settings.py gets loaded.
os.chdir(proj_path)

# This is so Django knows where to find stuff.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "simssadb.settings")

sys.path.append(os.getcwd())

from django.core.wsgi import get_wsgi_application
from django.conf import settings
application = get_wsgi_application()

from database.models import SymbolicMusicFile

def conversion(jar_file, config_file, path, feature_path, flog):
    """
    Function that converts the symbolic file into midi using music21, and output the non-parsable result to a log file.
    :param jar_file:
    :param config_file:
    :param path:
    :param feature_path:
    :return:
    """

    parsable_format = ['.abc', '.krn', '.ly', '.mei', '.xml'] # We can test out MuseData as well
    print(path)
    filename_w_ext = os.path.basename(path)
    conversion_file_path = os.path.join(os.path.dirname(path), 'conversion')
    # This is the path to store the converted files
    if os.path.exists(conversion_file_path) is False: os.mkdir(conversion_file_path)
    file_name, extension = os.path.splitext(filename_w_ext)
    if extension == '.mid' or extension == '.midi':
        extract_features(jar_file, config_file, path, feature_path, filename_w_ext)
    elif extension.lower() in parsable_format:
        try:
            s = converter.parse(path)
            new_path = os.path.join(conversion_file_path, filename_w_ext) + '.midi'
            s.write('midi', fp = new_path) # converted file within the same directory
            filename_w_ext = os.path.basename(new_path)
            extract_features(jar_file, config_file, new_path, feature_path, filename_w_ext)
        except:
            print(path, file=flog)
            print(sys.exc_info()[0], file=flog)
    else:
        print(path + ' is not convertible by music21. Therefore it cannot be processed by jsymbolic', file=flog)


def extract_features(jar_file, config_file, path, feature_path, file_name):
    """
    Modular function that extract features either from a file or from a folder
    :param jar_file:
    :param config_file:
    :param path: it is the path of the symbolic file
    :param feature_path:
    :return:
    """

    os.system('java -Xmx8192m -jar ' + jar_file + ' -configrun ' + config_file + ' ' + path + ' ' +
              os.path.join(feature_path, file_name + '_feature_values.xml ') +
              os.path.join(feature_path, file_name + '_feature_descriptions.xml') + '>>' + os.path.join(feature_path, 'extract_features_log.txt') + ' 2'
                                                                                    '>>' + os.path.join(feature_path, 'extract_features_error_log.txt')) # Do we need to get rid of the extension?
    print("The jar file used is: ", jar_file)
    print("The config file used is: ", config_file)
    print("The feature description file generated is: ", path + '_feature_descriptions.xml')
    print("The feature file generated is: ", path + '_feature_values.xml')
    print("The feature file generated is: ", path + '_feature_values.csv')
    print("The feature file generated is: ", path + '_feature_values.arff')


def extract_features_setup(jar_file, config_file, path, feature_path=''):
    """
    Function to extract features either for all the files in the folder or one file whose path is specified
    :param path: Either a folder or a file path
    :param feature_path: a folder where you want to store the feature files. If not specified, it will be the same with
    'path'
    :param jar_file: Path where you store the .jar file
    :param config_file: Path where you store the config file
    :return:
    """
    if os.path.isdir(path):  # The path is a folder
        flog = open(os.path.join(path, 'conversion_log.txt'), 'w')
        if feature_path == '':
            feature_path = os.path.join(path, 'extracted_features')  # When doing on a folder, this function will create a separate folder
        if os.path.exists(feature_path) is False: os.mkdir(feature_path)
        for id, fn in enumerate(os.listdir(path)):
            if fn.find('.DS_Store') == -1 and fn.find('conversion_log.txt') == -1 \
                    and fn.find('extracted_features') == -1 and fn.find('conversion') == -1: # Only convert the files that are already there
                conversion(jar_file, config_file, os.path.join(path, fn), feature_path, flog)
        flog.close()
    elif os.path.isfile(path):  # The path is a file
        flog = open(os.path.join(os.path.dirname(path), 'conversion_log.txt'), 'w')
        if feature_path == '':
            feature_path = os.path.join(os.path.dirname(path), 'extracted_features')  # Use the file path as the feature path
        if os.path.exists(feature_path) is False: os.mkdir(feature_path)
        conversion(jar_file, config_file, path, feature_path, flog)
        flog.close()
    else:
        print("The path you specified might not exist. Please specify a valid path, either a folder or a file!")



# jsymbolic_file = input('please specify jsymbolic .jar file')
# jsymbolic_config_file = input('please specify jsymbolic config file')
jsymbolic_file = os.path.join(os.getcwd(), 'feature_extraction/jSymbolic_2_2_user', 'jSymbolic2.jar')
jsymbolic_config_file = os.path.join(os.getcwd(), 'feature_extraction/jSymbolic_2_2_user', 'jSymbolicDefaultConfigs.txt')
path = SymbolicMusicFile.objects.first().file.path
extract_features_setup(jsymbolic_file, jsymbolic_config_file, path)
