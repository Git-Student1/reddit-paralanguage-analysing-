import praw
from dotenv import load_dotenv
import os
import pandas as pd
load_dotenv()  

class PostExtractor:
    def __init__(self):
        # Initialize PRAW with your credentials
        self.reddit = praw.Reddit(
        client_id= os.getenv("CLIENT_ID"), 
        client_secret=os.getenv("CLIENT_SECRET"), 
        user_agent=os.getenv("USER_AGENT"))

        # Get Path to data folder
        self.file_dir = os.path.dirname(os.path.abspath(__file__))
        self.csv_folder = 'data'
        self.folder_path = os.path.join(self.file_dir, self.csv_folder)

    def extractPost(self, post_url):
        if (not post_url):
            print("Entered empty string.")
            quit()
        

        # Definself.reddite the subreddit and post you want to pull comments from
        #post_url = "https://www.reddit.com/r/democrats/comments/1i7tbbz/please_do_not_let_conservatives_cover_for_elon/"
        post = self.reddit.submission(url=post_url)
        post.comments.replace_more(limit=None)  # This ensures you load all comments, including 'MoreComments' objects

        file_path = os.path.join(self.folder_path, f'{post.fullname}.csv')

        if (f'{post.fullname}.csv' in os.listdir(self.folder_path)):
            print(f'Already extracted: {post.fullname}.csv')
            return None

        # Prepare columns for csv
        data = {
            'userName': [],
            'userKarma': [],
            'commentContent': [],
            'commentEmojis': [],
            'sentimentScore': [],
        }

        for comment in post.comments.list():
            if isinstance(comment, praw.models.Comment):
                # Ensure the comment author exists (i.e. they are not a deleted account)
                if comment.author:
                    # Fetch the user's profile and get their karma
                    user = self.reddit.redditor(comment.author.name)
                    
                    if (comment.author.name):
                        data["userName"].append(comment.author.name)
                    else:
                        data["userName"].append("")

                    if hasattr(user, 'link_karma'): 
                        data["userKarma"].append(user.link_karma + user.comment_karma)
                    else:
                        data["userKarma"].append("")
                    
                    if (comment.body):
                        data["commentContent"].append(comment.body)
                    else:
                        data["commentContent"].append("")
                    
                    data["sentimentScore"].append("")
                    data["commentEmojis"].append([])
            
                    # Extract Emojis?
                    print(f"Comment by: {comment.author.name}")
                    if hasattr(user, 'link_karma'): print(f"User karma: {user.link_karma + user.comment_karma}")  # Total karma (link + comment karma)
                    print(f"Comment content: {comment.body}")
                else:
                    print("Comment by: [deleted]")
                    print("User karma: N/A (deleted user)\n")


        # Create Pandas DataFrame and save csv
        df = pd.DataFrame(data=data)
        df.to_csv(file_path, index=False)

        return post