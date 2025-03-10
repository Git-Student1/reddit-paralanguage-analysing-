import os

from comparison_json_reader import ComparisonJsonReader
from multithread_operations import MultiThreadOperations
from helper import Helper
from master_file import MasterFile
import pandas as pd


# post groups that wil lbe compared
print(f"WARNING: If one group has a 0 for every para language aspect check if the post names in {__file__} are seperated by a semicolon")
"""post_group1 = [ 
 "t3_1i7f49t",
 #random one
]

post_group2 =[
"t3_1itb0il"
]
#TODO: remove code dublication with main.py
"""

folder_path = Helper.get_folderpath()
#get subfolders with comparison data
subfolder_names = ComparisonJsonReader.get_relevant_subfolders_for_comparison(folder_path=folder_path)
for subfolder in subfolder_names:
    operations = MultiThreadOperations(MasterFile(folder_path=folder_path))
    json_reader = ComparisonJsonReader(data_folder_path=folder_path, data_subfolder_name=subfolder )
    post_group1 = json_reader.get_threads_group_1()
    post_group2 = json_reader.get_threads_group_2()
    if len(post_group1) ==0:
        print("no comparison possible because of a lack of files to compare") 
    elif len(post_group2) ==0:
        operations.grouping(post_group=post_group1, group_name=json_reader.get_name_group_1())
    else:
        operations.compare_groups(post_group1=post_group1, post_group2=post_group2, post_group_name1=json_reader.get_name_group_1(), post_group_name2=json_reader.get_name_group_2())


