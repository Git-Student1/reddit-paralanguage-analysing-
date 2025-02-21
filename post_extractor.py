from datetime import datetime
import sys
import praw
from dotenv import load_dotenv
import os
import pandas as pd

from master_file import MasterFile
load_dotenv()  

class PostExtractor:
    def __init__(self, folder_path):
        # Initialize PRAW with your credentials
        self.reddit = praw.Reddit(
        client_id= os.getenv("CLIENT_ID"), 
        client_secret=os.getenv("CLIENT_SECRET"), 
        user_agent=os.getenv("USER_AGENT"))
        self.folder_path = folder_path

    
    def extract_posts(self, post_urls:list[str], masterfile:MasterFile):
        posts = [self.__extract_post_and_write_thread_file(post_to_extract) for post_to_extract in post_urls]
        self.__update_master_file(posts, masterfile)
    


    def __extract_post_and_write_thread_file(self, post_url):
        post = self.__load_posts(post_url)
        self.__write_thread_file(post)
        return post
    
    def __load_posts(self, post_url)-> praw.reddit.Submission:
        """
        Extracts comments from posts url and puts them into a file.
        """
        if (not post_url):
            print("Entered empty string.")
            quit()
        # Definself.reddite the subreddit and post you want to pull comments from
        #post_url = "https://www.reddit.com/r/democrats/comments/1i7tbbz/please_do_not_let_conservatives_cover_for_elon/"
        post = self.reddit.submission(url=post_url)   
        post.comments.replace_more(limit=None)  # This ensures you load all comments, including 'MoreComments' objects
        return post

    
    def __write_thread_file(self, post: praw.reddit.Submission):
        # dont write to file if file for it already exist
        if (f'{post.fullname}.csv' in os.listdir(self.folder_path)):
            print(f'Already extracted: {post.fullname}.csv')
            return
        
        file_path = os.path.join(self.folder_path, f'{post.fullname}.csv')
        # Prepare columns for csv
        data = {
            'userName': [],
            'userKarma': [],
            'commentContent': [],
            'commentEmojis': [],
            'sentimentScore': []
        }
        
        total_comments = len(post.comments.list())

        for i, comment in enumerate(post.comments.list(), start=1):
            if isinstance(comment, praw.models.Comment):
                sys.stdout.write(f"\rProcessing comment {i}/{total_comments} ({(i/total_comments)*100:.2f}%) ")
                sys.stdout.flush()
                # Ensure the comment author exists (i.e. they are not a deleted account)
                if comment.author:
                    # Fetch the user's profile and get their karma
                    #user = self.reddit.redditor(comment.author.name)
                    
                    if (comment.author.name):
                        data["userName"].append(comment.author.name)
                    else:
                        data["userName"].append("")

                    #if hasattr(comment.author, 'link_karma'): 
                    #    data["userKarma"].append(comment.author.link_karma + comment.author.comment_karma)
                    #else:
                    data["userKarma"].append("")
                    
                    if (comment.body):
                        data["commentContent"].append(comment.body)
                    else:
                        data["commentContent"].append("")
                    
                    data["sentimentScore"].append("")
                    data["commentEmojis"].append([])
            
                    # Extract Emojis?
                    #print(f"Comment by: {comment.author.name}")
                    #if hasattr(comment.author, 'link_karma'): print(f"User karma: {comment.author.link_karma + comment.author.comment_karma}")  # Total karma (link + comment karma)
                    #print(f"Comment content: {comment.body}")
                #else:
                #    print("Comment by: [deleted]")
                #    print("User karma: N/A (deleted user)\n")

                    
        # Create Pandas DataFrame and save csv
        df = pd.DataFrame(data=data)
        df.to_csv(file_path, index=False)

    def __update_master_file(self, posts: list[praw.reddit.Submission], masterfile:MasterFile):
        """
        updates master-df  and  master-file
        """
        for post in posts:
            if post != None and not masterfile.contains_post_entry(post.fullname):
                masterfile.df.loc[masterfile.df.shape[0]] = [
                    post.fullname,
                    datetime.today().strftime('%d-%m-%Y %H:%M:%S'),
                    post.title,
                    [],
                    ""
                ]
        masterfile.update_master_file()
    