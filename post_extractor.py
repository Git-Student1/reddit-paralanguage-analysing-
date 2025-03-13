from datetime import datetime
import logging
import sys
import praw
from dotenv import load_dotenv
import os
import pandas as pd

from helper import Helper
from master_file import MasterFile
load_dotenv()  

class PostExtractor:
    def __init__(self):
        # Initialize PRAW with your credentials
        self.reddit = praw.Reddit(
        client_id= os.getenv("CLIENT_ID"), 
        client_secret=os.getenv("CLIENT_SECRET"), 
        user_agent=os.getenv("USER_AGENT"))
        self.post_symbols_counts = {}
        self.posts_newly_downladed = []


    
    def extract_posts(self, post_urls:list[str], masterfile:MasterFile):
        print("--- start post extraction ---")
        posts = [self.__extract_post_and_write_thread_file(post_to_extract) for post_to_extract in post_urls]
        self.__update_master_file(posts, masterfile)
    


    def __extract_post_and_write_thread_file(self, post_url):
        print("start loading posts")
        post = self.__load_posts(post_url)
        print("end loading posts")
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
        if not self.__post_already_extracted(post):
            post.comments.replace_more(limit=None)  # This ensures you load all comments, including 'MoreComments' objects
        return post
    
    def get_post_fullnames_from_url(self, urls:list[str]):
        postnames = []
        for url in urls:
            postnames.append(self.reddit.submission(url=url).fullname)
        return postnames
    
    def __post_already_extracted(self, post: praw.reddit.Submission):
        return f'{post.fullname}.csv' in os.listdir(Helper.get_folder_path_for_thread_files(post.fullname))

    
    def __write_thread_file(self, post: praw.reddit.Submission):
        # dont write to file if file for it already exist
        if (self.__post_already_extracted(post)):
            print(f'Already extracted: {post.fullname}.csv')
            return
        
        file_path = Helper.get_file_path_for_thread_file(post_fullname=post.fullname)
        # Prepare columns for csv
        data = {
            'userName': [],
            'userKarma': [],
            'commentContent': [],
            'commentEmojis': [],
            'sentimentScore': []
        }
        
        total_comments = len(post.comments.list())
        comment_symbols_count = 0
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
                        comment_symbols_count+= len(comment.body)
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
        self.post_symbols_counts[post.fullname] = comment_symbols_count
        self.posts_newly_downladed.append(post.fullname)
    

    def __update_master_file(self, posts: list[praw.reddit.Submission], masterfile:MasterFile):
        """
        updates master-df  and  master-file
        """



        for post in posts:

            if post != None and (not masterfile.contains_post_entry(post.fullname) or post.fullname in self.posts_newly_downladed ):
                try:
                    post_comments_count = self.post_symbols_counts[post.fullname]
                except KeyError:
                    post_comments_count = len("".join(pd.read_csv(Helper.get_file_path_for_thread_file(post_fullname=post.fullname))["commentContent"]))
                list_with_existing_row =  masterfile.df.loc[masterfile.df[masterfile.post_full_name_cn] == post.fullname]
                


                new_row = {masterfile.post_full_name_cn: post.fullname,
                           masterfile.dateRetrieved_cn: datetime.today().strftime('%d-%m-%Y %H:%M:%S'),
                           masterfile.postTitle_cn : post.title,
                           masterfile.postEmojis_cn: "[]",
                           masterfile.sentimentScore_cn:"",
                           masterfile.number_of_comments: len(post.comments.list()),
                           masterfile.number_of_symbols: post_comments_count
                           }
                if post.fullname in masterfile.df[masterfile.post_full_name_cn].values:
                    print(len(list(new_row.keys())))
                    print(len(list(new_row.values())))
                    masterfile.df.loc[masterfile.df[masterfile.post_full_name_cn] == post.fullname, list(new_row.keys())] = list(new_row.values())
                else:
                    new_row_df = pd.DataFrame([new_row])
                    masterfile.df = pd.concat([masterfile.df, new_row_df], ignore_index=True)
        masterfile.update_master_file()
    