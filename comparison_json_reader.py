
import json
import os


class ComparisonJsonReader:
    __group_name_1="gr1"
    __group_name_2="gr2"
    __thead_ids = "theadIds"
    __group_name = "name"
    __comparing_file_name = "comparison.json"

    def __init__(self, data_folder_path, data_subfolder_name) -> None:
        with open(f"{data_folder_path}\\{data_subfolder_name}\\{self.__comparing_file_name}") as comparison_file:
            self.data = json.load(comparison_file)
    
    def __get_group_threads(self, name:str)-> list[str]:
        return self.data[name][self.__thead_ids]
    
    def __get_group_name(self, name:str):
        return self.data[name][self.__group_name]

    def get_name_group_1(self):
        return self.__get_group_name(self.__group_name_1)
    def get_name_group_2(self):
        return self.__get_group_name(self.__group_name_2)
    
    def get_threads_group_1(self):
        return self.__get_group_threads(self.__group_name_1)
    def get_threads_group_2(self):
        return self.__get_group_threads(self.__group_name_2)
    @classmethod
    def get_comparison_file_name(cls):
        return cls.__comparing_file_name

    @classmethod
    def get_relevant_subfolders_for_comparison(cls, folder_path):
        subfolder_names =  [s_folder.name
             for s_folder in os.scandir(folder_path) if s_folder.is_dir()
             for file in os.scandir(os.path.join(folder_path, s_folder)) if  file.is_file() and file.name.endswith(ComparisonJsonReader.get_comparison_file_name())
             ]
        """input_result = input("which comparson should be made? \n" + 
                            "0: all \n" +
                            "\n".join([f"{int(i)+1}: {val}" for i, val in enumerate(subfolder_names)]) +"\n")"""
        input_result = "0"
        try :
            if (int(input_result)< 0 or int(input_result)> len(subfolder_names)):
                raise ValueError(f"Value not in range. Given: {input_result}")

            subfolder_names = [subfolder_names[int(input_result)-1]]

        except ValueError as e:
            raise ValueError(f"invalid input: {input_result}\n '{e}'")
        return subfolder_names

            