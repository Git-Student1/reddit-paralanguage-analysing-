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
        if os.path.exists(self.master_file_path):
            self.df = pd.read_csv(self.master_file_path)
        else:
            self.df = pd.DataFrame(columns = ["postFullname","postTitle","postEmojis","sentimentScore"])
            # TODO: remove print statement
            print("no masterfile exsists")
    
    def update_master_file(self, postsToExtract):
        #TODO: change it to not always extract the post as it takes too long. Use the information from the extracted and saved posts to create the masterfile
        self.extractPosts(postsToExtract)

    
    def extractPosts(self, postsToExtract):
        for postToExtract in postsToExtract:
            post = self.postExtractor.extractPost(postToExtract)

            df = self.df

            if (post != None):
                df.loc[df.shape[0]] = [
                    post.fullname,
                    post.title,
                    [],
                    ""
                ]

            df.to_csv(self.master_file_path, index=False)
    
    def getColumnAsList(self, columnName):
        return self.df[columnName].to_list()

           


