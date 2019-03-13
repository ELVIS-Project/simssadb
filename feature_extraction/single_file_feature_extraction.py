import os
from music21 import *
import sys
import subprocess

jsymbolic_file = '/Users/gustavo/Development/simssadb/feature_extraction' \
                 '/jSymbolic_2_2_user/jSymbolic2.jar'
jsymbolic_config_file = '/Users/gustavo/Development/simssadb' \
                        '/feature_extraction/jSymbolic_2_2_user' \
                        '/jSymbolicDefaultConfigs.txt'


def driver(file_path):
    extract_features_setup(jsymbolic_file, jsymbolic_config_file, file_path)


def conversion(jar_file, config_file, path, feature_path, flog,
               num_of_non_processed_files, num_of_midi_file,
               num_of_midi_file_feature, num_of_converted_files, num_of_converted_files_feature):
    """
    Function that converts the symbolic file into midi using music21, and output the non-parsable result to a log file.
    :param jar_file:
    :param config_file:
    :param path:
    :param feature_path:
    :return:
    """

    parsable_format = ['.abc', '.krn', '.ly', '.mei', '.xml']  # We can test out MuseData as well
    print(path)
    filename_w_ext = os.path.basename(path)
    conversion_file_path = os.path.join(os.path.dirname(path), 'conversion')
    # This is the path to store the converted files
    if os.path.exists(conversion_file_path) is False: os.mkdir(conversion_file_path)
    file_name, extension = os.path.splitext(filename_w_ext)
    if extension == '.mid' or extension == '.midi':
        num_of_midi_file += 1
        num_of_midi_file_feature = extract_features(jar_file, config_file, path, feature_path, filename_w_ext,
                                                    num_of_midi_file_feature)
    elif extension.lower() in parsable_format:
        try:
            s = converter.parse(path)
            new_path = os.path.join(conversion_file_path, filename_w_ext) + '.midi'
            s.write('midi', fp=new_path)  # converted file within the same directory
            num_of_converted_files += 1
            filename_w_ext = os.path.basename(new_path)
            num_of_converted_files_feature = extract_features(jar_file, config_file, new_path, feature_path,
                                                              filename_w_ext,
                                                              num_of_converted_files_feature)
        except:
            print(path, file=flog)
            print(sys.exc_info()[0], file=flog)
    else:
        print(path + ' is not convertible by music21. Therefore it cannot be processed by jsymbolic', file=flog)
        num_of_non_processed_files += 1
    return num_of_non_processed_files, num_of_midi_file, num_of_midi_file_feature, num_of_converted_files, \
           num_of_converted_files_feature


def extract_features(jar_file, config_file, path, feature_path, file_name, num_of_files_feature_succeed):
    """
    Modular function that extract features either from a file or from a folder
    :param num_of_files_feature_succeed:
    :param file_name:
    :param jar_file:
    :param config_file:
    :param path: it is the path of the symbolic file
    :param feature_path:
    :return:
    """
    f_stdout = open(os.path.join(feature_path, 'extract_features_log.txt'), 'a')
    f_stderr = open(os.path.join(feature_path, 'extract_features_error_log.txt'), 'a')
    out = subprocess.Popen(['java', '-Xmx6g', '-jar', jar_file, '-configrun', config_file, path,
                            os.path.join(feature_path, file_name + '_feature_values.xml'),
                            os.path.join(feature_path, file_name + '_feature_descriptions.xml')],
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)
    stdout, stderr = out.communicate()
    if stderr is None or len(stderr) == 0:
        num_of_files_feature_succeed += 1
    else:
        print(stderr.decode("utf-8"), file=f_stderr)
    if stdout is not None:
        print(stdout.decode("utf-8"), file=f_stdout)
    f_stdout.close()
    f_stderr.close()
    print("The jar file used is: ", jar_file)
    print("The config file used is: ", config_file)
    print("The feature description file generated is: ", path + '_feature_descriptions.xml')
    print("The feature file generated is: ", path + '_feature_values.xml')
    print("The feature file generated is: ", path + '_feature_values.csv')
    print("The feature file generated is: ", path + '_feature_values.arff')
    return num_of_files_feature_succeed


def standard_output(ftotal, num_of_total_files, num_of_non_processed_files, num_of_midi_file, num_of_midi_file_feature,
                    num_of_converted_files, num_of_converted_files_feature):
    """
    Function to print these statistics into a log file
    :param ftotal:
    :param num_of_total_files:
    :param num_of_non_processed_files:
    :param num_of_midi_file:
    :param num_of_midi_file_feature:
    :param num_of_converted_files:
    :param num_of_converted_files_feature:
    :return:
    """

    print('There are', num_of_total_files, 'files,', num_of_total_files - num_of_non_processed_files, 'are processed.',
          num_of_non_processed_files, 'are not processed since their formats are not suppoted.')
    print('Among', num_of_total_files - num_of_non_processed_files, 'processed files,', num_of_midi_file,
          'are MIDI files,', num_of_midi_file_feature, 'manage to extract features.')
    print('Among', num_of_total_files - num_of_non_processed_files, 'processed files,',
          num_of_total_files - num_of_non_processed_files - num_of_midi_file,
          'are other files,', num_of_converted_files,
          'manage to convert into MIDI,', num_of_converted_files_feature, 'manage to extract features.')

    print('There are', num_of_total_files, 'files,', num_of_total_files - num_of_non_processed_files, 'are processed.',
          num_of_non_processed_files, 'are not processed since their formats are not suppoted.', file=ftotal)
    print('Among', num_of_total_files - num_of_non_processed_files, 'processed files,', num_of_midi_file,
          'are MIDI files,', num_of_midi_file_feature, 'manage to extract features.', file=ftotal)
    print('Among', num_of_total_files - num_of_non_processed_files, 'processed files,',
          num_of_total_files - num_of_non_processed_files - num_of_midi_file,
          'are other files,', num_of_converted_files,
          'manage to convert into MIDI,', num_of_converted_files_feature, 'manage to extract features.', file=ftotal)


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
    num_of_total_files = 0  # The number of files with the specified folder
    num_of_non_processed_files = 0  # The number of symbolic files that can be processed
    num_of_processed_files_succeed = 0
    num_of_midi_file = 0  # The number of files whose original format is midi
    num_of_midi_file_feature = 0  # The number of midi files whose features are extracted successfully
    num_of_converted_files = 0  # The number of processed files that are converted successfully
    num_of_converted_files_feature = 0  # The number of processed files that are converted
    # and the features are extracted successfully

    if os.path.isdir(path):  # The path is a folder
        ftotal = open(os.path.join(path, 'standard_output_log.txt'), 'w')
        flog = open(os.path.join(path, 'conversion_error_log.txt'), 'w')
        if feature_path == '':
            feature_path = os.path.join(path,
                                        'extracted_features')  # When doing on a folder, this function will create a separate folder
        if os.path.exists(feature_path) is False: os.mkdir(feature_path)
        for id, fn in enumerate(os.listdir(path)):
            if fn.find('.DS_Store') == -1 and fn.find('conversion_error_log.txt') == -1 \
                    and fn.find('extracted_features') == -1 and fn.find('conversion') == -1 \
                    and fn.find('standard_output_log.txt') == -1:  # Only convert the files that are already there
                num_of_total_files += 1  # The total number of files within the folder
                (num_of_non_processed_files, num_of_midi_file, num_of_midi_file_feature, num_of_converted_files, \
                 num_of_converted_files_feature) = conversion(jar_file, config_file, os.path.join(path, fn),
                                                              feature_path, flog,
                                                              num_of_non_processed_files, num_of_midi_file,
                                                              num_of_midi_file_feature, num_of_converted_files,
                                                              num_of_converted_files_feature)
        standard_output(ftotal, num_of_total_files, num_of_non_processed_files, num_of_midi_file,
                        num_of_midi_file_feature,
                        num_of_converted_files, num_of_converted_files_feature)
        flog.close()
    elif os.path.isfile(path):  # The path is a file
        flog = open(os.path.join(os.path.dirname(path), 'conversion_error_log.txt'), 'w')
        ftotal = open(os.path.join(os.path.dirname(path), 'standard_output_log.txt'), 'w')
        if feature_path == '':
            feature_path = os.path.join(os.path.dirname(path),
                                        'extracted_features')  # Use the file path as the feature path
        if os.path.exists(feature_path) is False: os.mkdir(feature_path)
        num_of_total_files += 1
        (num_of_non_processed_files, num_of_midi_file, num_of_midi_file_feature, num_of_converted_files, \
         num_of_converted_files_feature) = conversion(jar_file, config_file, path, feature_path, flog,
                                                      num_of_non_processed_files, num_of_midi_file,
                                                      num_of_midi_file_feature, num_of_converted_files,
                                                      num_of_converted_files_feature)
        standard_output(ftotal, num_of_total_files, num_of_non_processed_files, num_of_midi_file,
                        num_of_midi_file_feature,
                        num_of_converted_files, num_of_converted_files_feature)
        flog.close()
    else:
        print("The path you specified might not exist. Please specify a valid path, either a folder or a file!")


if __name__ == "__main__":
    # jsymbolic_file = input('please specify jsymbolic .jar file')
    # jsymbolic_config_file = input('please specify jsymbolic config file')
    jsymbolic_file = os.path.join(os.getcwd(), 'jSymbolic_2_2_user', 'jSymbolic2.jar')
    jsymbolic_config_file = os.path.join(os.getcwd(), 'jSymbolic_2_2_user', 'jSymbolicDefaultConfigs.txt')
    path = os.path.join(os.path.dirname(os.getcwd()), 'media', 'symbolic_music')
    # path = os.path.join(os.path.dirname(os.getcwd()), 'media', '000000000006640_Missa-L-homme-arme_Gloria-Credo-Sanctus-Agnus-dei_Brumel-Antoine_file1.mid')
    extract_features_setup(jsymbolic_file, jsymbolic_config_file, path)
