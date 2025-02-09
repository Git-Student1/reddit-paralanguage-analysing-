import os
import pandas as pd
from post_extractor import PostExtractor


class MasterFile:
    def __init__(self):
        # Get Path to data folder
        file_dir = os.path.dirname(os.path.abspath(__file__))
        csv_folder = 'data'
        folder_path = os.path.join(file_dir, csv_folder)
        self.master_file_path = os.path.join(folder_path, '_master.csv')

        self.postExtractor = PostExtractor()
        self.df = pd.read_csv(self.master_file_path)
    
    def update_master_file(self, postsToExtract):
        self.extractPosts(postsToExtract)
    
    def extractPosts(self, postsToExtract):
        for postToExtract in postsToExtract:
            post = self.postExtractor.extractPost(postToExtract)

            df = self.df

            if (post == None):
                continue

            df.loc[df.shape[0]] = [
                post.fullname,
                post.title,
                [],
                ""
            ]

            df.to_csv(self.master_file_path, index=False)
    
    def getColumnAsList(self, columnName):
        return self.df[columnName].to_list()

           


