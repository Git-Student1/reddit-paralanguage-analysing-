import os
from comparison import MultiThreadOperations
from master_file import MasterFile
import pandas as pd

# post groups that wil lbe compared
print("WARNING: If one group has a 0 for every para language aspect check if the posts are seperated by a semicolon")
post_group1 = [ 
 "t3_1i7f49t",
 "t3_1iwzs71"#random one
]

post_group2 =[
#"t3_1itb0il"
]
#TODO: remove code dublication with main.py
file_dir = os.path.dirname(os.path.abspath(__file__))
csv_folder = 'data'
folder_path = os.path.join(file_dir, csv_folder)
operations = MultiThreadOperations(MasterFile(folder_path=folder_path))
if len(post_group1) ==0:
    print("no comparison possible because of a lack of files to compare") 
elif len(post_group2) ==0:
    operations.grouping(post_group=post_group1)
else:
    operations.compare_groups(post_group1=post_group1, post_group2=post_group2)


