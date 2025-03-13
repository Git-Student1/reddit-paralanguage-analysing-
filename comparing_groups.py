import os

from comparison_json_reader import ComparisonJsonReader
from emoji_analysis import EmojiAnalysis
from multithread_operations import MultiThreadOperations
from helper import Helper
from master_file import MasterFile
import pandas as pd

from para_analysis import ParaAnalysis
from post_extractor import PostExtractor
from vader_analysis import VaderAnalysis


# post groups that wil lbe compared
print(f"WARNING: If one group has a 0 for every para language aspect check if the post names in {__file__} are seperated by a semicolon")
#TODO: remove code dublication with main.py


base_folder_path = Helper.get_files_base_folderpath()
#get subfolders with comparison data
subfolder_names = ComparisonJsonReader.get_relevant_subfolders_for_comparison(folder_path=base_folder_path)

for subfolder in subfolder_names:
    subfolder_path = os.path.join(base_folder_path, subfolder)
    json_reader = ComparisonJsonReader(data_folder_path=base_folder_path, data_subfolder_name=subfolder )
    post_urls_group1 = json_reader.get_threads_group_1()
    post_urls_group2 = json_reader.get_threads_group_2()


    masterfile = MasterFile(folder_path=subfolder_path)
    operations = MultiThreadOperations(masterfile)
    post_extractor = PostExtractor()
    postsToExtract = post_urls_group1 + post_urls_group2
    post_extractor.extract_posts(post_urls=postsToExtract, masterfile=masterfile)

    emojiAnalysis = EmojiAnalysis(masterfile)
    emojiAnalysis.extract_emojis_to_master_and_post_file()

    vaderAnalysis = VaderAnalysis(masterfile)
    vaderAnalysis.extract_mean_sentiment_score()

    paraAnalysis = ParaAnalysis(master_file=masterfile)
    paraAnalysis.extract_para_values()

    post_names_group_1 = post_extractor.get_post_fullnames_from_url(post_urls_group1)
    post_names_group_2 = post_extractor.get_post_fullnames_from_url(post_urls_group2)



    print("--- start comparison ---")
    if len(post_names_group_1) ==0:
        print("no comparison possible because of a lack of files to compare") 
    elif len(post_names_group_2) ==0:
        operations.grouping(post_group=post_names_group_1, group_name=json_reader.get_name_group_1(), save_folder=subfolder_path)
    else:
        operations.compare_groups(post_group1=post_names_group_1, post_group2=post_names_group_2, post_group_name1=json_reader.get_name_group_1(), post_group_name2=json_reader.get_name_group_2(), save_folder=subfolder_path)
    print("--- all done ---")

