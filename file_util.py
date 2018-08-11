import logging
import os
import sys
import json
import errno

if sys.version_info[0] == 3:
    import pickle
else:
    import cPickle as pickle


class FileUtil:

    @staticmethod
    def validate_file(file_path, create_file=True):
        """
        Method to ensure that the file and exists at the path
        If it doesn't exist it will create a blank file and
        the necessary folders at the path provided.
        :param file_path: Path to the file to be validated
        :param create_file: will create folder by default. This flag enables creating a dummy file at the target path.
        :return: None
        """

        if not os.path.isfile(file_path):
            try:
                # Create the directories if they do not alread exist
                os.makedirs(os.path.dirname(file_path))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
            if create_file:
                file = open(file_path, 'w+')
                file.close()

    @staticmethod
    def validate_folder(folder_path):
        """
        Same as validate_file but for folders
        :param folder_path: Path to the folder
        :return: None
        """
        if not os.path.isdir(folder_path):
            try:
                os.makedirs(os.path.abspath(folder_path))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise

    @staticmethod
    def is_folder(folder_path):
        return os.path.isdir(folder_path)

    @staticmethod
    def is_file(file_path):
        return os.path.isfile(file_path)

    @staticmethod
    def get_files_in_folder(folder_path, return_full_path=True, recursive=False):
        """
        Simple function to return the contents of a directory
        :param folder_path: Path to the directory to be checked
        :param return_full_path: If the returned list should be full path or file name only
        :return: List of files in the folder.
        """
        folder_path = os.path.abspath(folder_path)
        files = []

        for file in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file) if return_full_path else file

            if FileUtil.is_folder(file_path):
                if recursive:
                    # If subfolder is present
                    files_in_subfolder = FileUtil.get_files_in_folder(file_path, return_full_path, recursive)
                    files.extend(files_in_subfolder)
            else:
                # Add files to list
                files. append(file_path)

        files.sort()

        return files

    @staticmethod
    def clear_folder(folder_path):
        """
        Clears all files at specified folder path
        :param folder_path:
        :return: None
        """
        for file_ in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                    # elif os.path.isdir(file_path): shutil.rmtree(file_path)
            except Exception as e:
                print(e)

    @staticmethod
    def dump_object(obj, file_path):
        """
        Dumps an object into the a file at the path provided
        :param obj: Object that needs to be dumped
        :param file_path: Path of target pickle file
        :return:
        """
        FileUtil.validate_file(file_path)
        with open(file_path, "wb") as file:
            pickle.dump(obj, file)

    @staticmethod
    def load_object(file_path):
        """
        Loads a pickled object from a file at the path provided
        :param file_path: Path of the target pickle file
        :return:
        """
        with open(file_path, "rb") as file:
            obj = pickle.load(file)
            logging.info("Loaded file @ path : {}".format(file_path))
        return obj

    @staticmethod
    def load_json(file_path):
        """ Load a json file with json.load() method."""
        with open(file_path, "rb") as file:
            obj = json.load(file)

        return obj


    @staticmethod
    def dump_json(obj, file_path, indent=None):
        """ Load a json file with json.load() method."""
        with open(file_path, "w") as file:
            json.dump(obj, file, indent=indent)

        return

    @staticmethod
    def append_text_to_file(str, file_path):
        """Dumps a string to a file with append mode"""
        with open(file_path, "a") as file:
            file.write(str)

        return
