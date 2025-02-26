import os


class Helper:
    @classmethod
    def get_folderpath(cls):
        file_dir = os.path.dirname(os.path.abspath(__file__))
        csv_folder = 'data'
        folder_path = os.path.join(file_dir, csv_folder)
        return folder_path