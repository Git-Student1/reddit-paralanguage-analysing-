import os
import pandas as pd
import praw

from datetime import datetime

class MasterFile:
    def __init__(self, folder_path):
        self.master_file_path = os.path.join(folder_path, '_master.csv')
        self.post_full_name_columnname = "postFullname"
        if os.path.exists(self.master_file_path):
            self.df = pd.read_csv(self.master_file_path)
        else:
            self.df = pd.DataFrame(columns = [self.post_full_name_columnname,"dateRetrieved", "postTitle","postEmojis","sentimentScore"])
            # TODO: remove print statement
            print("no masterfile exsists")
    
    def update_master_file(self):
        self.df.to_csv(self.master_file_path, index=False)
        
    def contains_post_entry(self, post_fullname):
        return post_fullname in self.df[self.post_full_name_columnname].values


    
    def getColumnAsList(self, columnName):
        return self.df[columnName].to_list()

           


