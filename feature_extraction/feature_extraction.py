import os
from music21 import *
import sys
import subprocess
import argparse
import datetime
import re
jsymbolic_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'jSymbolic_2_2_user', 'jSymbolic2.jar')
jsymbolic_config_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'jSymbolic_2_2_user', 'jSymbolicDefaultConfigs.txt')


def driver(file_path):
    extracted = extract_features_setup(jsymbolic_file, jsymbolic_config_file, file_path)
    return extracted

def conversion(jar_file, config_file, path, feature_path, flog, ftotal,
               num_of_non_processed_files, num_of_midi_file,
               num_of_midi_file_feature, num_of_converted_files, num_of_converted_files_feature):
    """
    Function that converts the symbolic file into midi using music21, and output the non-parsable result to a log file.
    :param num_of_non_processed_files:
    :param num_of_midi_file:
    :param num_of_converted_files_feature:
    :param num_of_converted_files:
    :param num_of_midi_file_feature:
    :param jar_file:
    :param config_file:
    :param path:
    :param feature_path:
    :return:
    """

    parsable_format = ['.abc', '.krn', '.ly', '.mei', '.xml']  # We can test out MuseData as well
    print(path)
    filename_w_ext = os.path.basename(path)
    print('--------------------', file=ftotal)
    print('Breakdown for the file:', filename_w_ext, file=ftotal)
    conversion_file_path = os.path.join(os.path.dirname(path), 'conversion')
    # This is the path to store the converted files
    if os.path.exists(conversion_file_path) is False: os.mkdir(conversion_file_path)
    file_name, extension = os.path.splitext(filename_w_ext)
    if extension.lower() == '.mid' or extension.lower() == '.midi':
        num_of_midi_file += 1
        num_of_midi_file_feature, extracted = extract_features(ftotal, jar_file, config_file, path, feature_path, filename_w_ext,
                                                    num_of_midi_file_feature)
    elif extension.lower() in parsable_format:
        try:
            s = converter.parse(path)
            new_path = os.path.join(conversion_file_path, filename_w_ext) + '.midi'
            s.write('midi', fp=new_path)  # converted file within the same directory
            print('It manages to convert to midi', file=ftotal)
            num_of_converted_files += 1
            filename_w_ext = os.path.basename(new_path)
            num_of_converted_files_feature, extracted = extract_features(ftotal, jar_file, config_file, new_path, feature_path,
                                                              filename_w_ext,
                                                              num_of_converted_files_feature)
        except:
            print(path, file=flog)
            print(sys.exc_info()[0], file=flog)
            print('It fails to convert to midi', file=ftotal)
    else:
        print(path + ' is not convertible by music21. Therefore it cannot be processed by jsymbolic', file=flog)
        print('It is not processed', file=ftotal)
        num_of_non_processed_files += 1
    return num_of_non_processed_files, num_of_midi_file, num_of_midi_file_feature, num_of_converted_files, \
           num_of_converted_files_feature, extracted


def extract_features(ftotal, jar_file, config_file, path, feature_path, file_name, num_of_files_feature_succeed):
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
    extracted = False
    f_stdout = open(os.path.join(feature_path, 'extract_features_log.txt'), 'a')
    f_stderr = open(os.path.join(feature_path, 'extract_features_error_log.txt'), 'a')
    out = subprocess.Popen(['java', '-Xmx6g', '-jar', jar_file, '-configrun', config_file, path,
                            os.path.join(feature_path, file_name + '_feature_values.xml'),
                            os.path.join(feature_path, file_name + '_feature_descriptions.xml')],
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)
    stdout, stderr = out.communicate()
    if stderr is None or len(stderr) == 0:
        extracted = True
        num_of_files_feature_succeed += 1
        print('It manages to extract features', file=ftotal)
        print("The jar file used is: ", jar_file)
        print("The config file used is: ", config_file)
        print("The feature description file generated is: ", path + '_feature_descriptions.xml')
        print("The feature file generated is: ", path + '_feature_values.xml')
        print("The feature file generated is: ", path + '_feature_values.csv')
        print("The feature file generated is: ", path + '_feature_values.arff')
    else:
        print('It fails to extract features', file=ftotal)
        print(stderr.decode("utf-8"), file=f_stderr)
        print('Feature extraction failed, please take a look at the log file!')
    if stdout is not None:
        print(stdout.decode("utf-8"), file=f_stdout)
    f_stdout.close()
    f_stderr.close()
    return num_of_files_feature_succeed, extracted


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
    ftotal.close()

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
    num_of_midi_file = 0  # The number of files whose original format is midi
    num_of_midi_file_feature = 0  # The number of midi files whose features are extracted successfully
    num_of_converted_files = 0  # The number of processed files that are converted successfully
    num_of_converted_files_feature = 0  # The number of processed files that are converted
    # and the features are extracted successfully

    if os.path.isdir(path):  # The path is a folder
        time = re.sub('[-: ]', '', str(datetime.datetime.now())).split('.')[0]
        ftotal = open(os.path.join(path, 'standard_output_log_batch' + time +'.txt'), 'w')
        flog = open(os.path.join(path, 'conversion_error_log_batch' + time +'.txt'), 'w')
        if feature_path == '':
            feature_path = os.path.join(path,
                                        'extracted_features')  # When doing on a folder, this function will create a separate folder
        if os.path.exists(feature_path) is False: os.mkdir(feature_path)
        for id, fn in enumerate(os.listdir(path)):
            if fn.find('.DS_Store') == -1 \
                    and fn.find('extracted_features') == -1 and fn.find('conversion') == -1 \
                    and fn.find('log') == -1:  # Only convert the files that are already there
                num_of_total_files += 1  # The total number of files within the folder
                (num_of_non_processed_files, num_of_midi_file, num_of_midi_file_feature, num_of_converted_files, \
                 num_of_converted_files_feature, extracted) = conversion(jar_file, config_file, os.path.join(path, fn),
                                                              feature_path, flog, ftotal,
                                                              num_of_non_processed_files, num_of_midi_file,
                                                              num_of_midi_file_feature, num_of_converted_files,
                                                              num_of_converted_files_feature)
        standard_output(ftotal, num_of_total_files, num_of_non_processed_files, num_of_midi_file,
                        num_of_midi_file_feature,
                        num_of_converted_files, num_of_converted_files_feature)
        flog.close()
        return extracted
    elif os.path.isfile(path):  # The path is a file
        flog = open(os.path.join(os.path.dirname(path), 'conversion_error_log.txt'), 'a')
        ftotal = open(os.path.join(os.path.dirname(path), 'standard_output_log.txt'), 'a')
        if feature_path == '':
            feature_path = os.path.join(os.path.dirname(path),
                                        'extracted_features')  # Use the file path as the feature path
        if os.path.exists(feature_path) is False: os.mkdir(feature_path)
        num_of_total_files += 1
        (num_of_non_processed_files, num_of_midi_file, num_of_midi_file_feature, num_of_converted_files, \
         num_of_converted_files_feature, extracted) = conversion(jar_file, config_file, path, feature_path, flog, ftotal,
                                                      num_of_non_processed_files, num_of_midi_file,
                                                      num_of_midi_file_feature, num_of_converted_files,
                                                      num_of_converted_files_feature)
        standard_output(ftotal, num_of_total_files, num_of_non_processed_files, num_of_midi_file,
                        num_of_midi_file_feature,
                        num_of_converted_files, num_of_converted_files_feature)
        flog.close()
        return extracted
    else:
        print("The path you specified might not exist. Please specify a valid path, either a folder or a file!")
        return False # Falst path feature is not extracted


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-j', '--jsymbolic_file',
                        help='The path of where the jsymbolic jar file is stored',
                        type=str, default=os.path.join(os.getcwd(), 'jSymbolic_2_2_user', 'jSymbolic2.jar'))
    parser.add_argument('-c', '--jsymbolic_config_file',
                        help='The path of where the jsymbolic config file is stored',
                        type=str, default=os.path.join(os.getcwd(), 'jSymbolic_2_2_user', 'jSymbolicDefaultConfigs.txt'))
    parser.add_argument('-p', '--path',
                        help='The path of either a file or a folder where you want to extract features for all the '
                             'files within',
                        type=str,
                        default=os.path.join(os.path.dirname(os.getcwd()), 'media', 'symbolic_music',
                                             'F164_01_Pisano_Quanto_piu_OMRcorrIL.mid'))
    args = parser.parse_args()
    extracted = extract_features_setup(args.jsymbolic_file, args.jsymbolic_config_file, args.path)
    print(extracted)
