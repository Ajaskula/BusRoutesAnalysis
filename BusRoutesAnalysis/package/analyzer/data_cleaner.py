"""Modul for deleting stored data."""

import os
import shutil

class DataCleaner:
    """
    Class for deleting stored data.
    """
    def __init__(self):
        pass

    @staticmethod
    def delete_all_data(self):
        """
        Method for deleting all stored data.
        """
        current_path = os.path.dirname(os.path.abspath(__file__))
        folder_to_delete = os.path.join(current_path,'..','..', 'data')
        folder_to_delete = os.path.normpath(folder_to_delete)

        shutil.rmtree(folder_to_delete, ignore_errors=True)

    @staticmethod
    def delete_folder(self, folder_name: str):
        """
        Method for deleting a folder.
        """
        current_path = os.path.dirname(os.path.abspath(__file__))
        folder_to_delete = os.path.join(current_path,'..','..', 'data', folder_name)
        folder_to_delete = os.path.normpath(folder_to_delete)

        shutil.rmtree(folder_to_delete, ignore_errors=True)