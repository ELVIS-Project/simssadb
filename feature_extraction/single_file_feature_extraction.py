import os


def extract_features(jar_file, config_file, path, feature_path):
    """
    Modular function that extract features either from a file or from a folder
    :param jar_file:
    :param config_file:
    :param path:
    :param feature_path:
    :return:
    """
    print(path)
    # print('java -Xmx8192m -jar ' + jar_file + ' -configrun ' + config_file + ' ' + path + ' ' +
    #           path + '_feature_values.xml ' +
    #           path + '_feature_descriptions.xml >>' + feature_path + 'extract_features_log.txt 2'
    #                                                                                 '>>' + feature_path + 'extract_features_error_log.txt')
    os.system('java -Xmx8192m -jar ' + jar_file + ' -configrun ' + config_file + ' ' + path + ' ' +
              path + '_feature_values.xml ' +
              path + '_feature_descriptions.xml >>' + os.path.join(feature_path, 'extract_features_log.txt') + ' 2'
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
        if feature_path == '':
            feature_path = path  # Use the file path as the feature path
        if os.path.exists(feature_path) is False: os.mkdir(feature_path)
        for id, fn in enumerate(os.listdir(path)):
            extract_features(jar_file, config_file, os.path.join(path, fn), feature_path)
    elif os.path.isfile(path):  # The path is a file
        if feature_path == '':
            feature_path = os.path.dirname(path)  # Use the file path as the feature path
        if os.path.exists(feature_path) is False: os.mkdir(feature_path)
        extract_features(jar_file, config_file, path, feature_path)
    else:
        print("The path you specified might not exist. Please specify a valid path, either a folder or a file!")


if __name__ == "__main__":
    # jsymbolic_file = input('please specify jsymbolic .jar file')
    # jsymbolic_config_file = input('please specify jsymbolic config file')
    jsymbolic_file = os.path.join(os.getcwd(), 'jSymbolic_2_2_user', 'jSymbolic2.jar')
    jsymbolic_config_file = os.path.join(os.getcwd(), 'jSymbolic_2_2_user', 'jSymbolicDefaultConfigs.txt')
    path = os.path.join(os.path.dirname(os.getcwd()), 'media', 'F164_01_Pisano_Quanto_piu_OMRcorrIL.mid')
    extract_features_setup(jsymbolic_file, jsymbolic_config_file, path)
