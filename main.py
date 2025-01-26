import praw
import OAuth2Util
import emoji_analysis
from dotenv import load_dotenv
import os


load_dotenv()  
# Initialize PRAW with your credentials
reddit = praw.Reddit(
    client_id= os.getenv("CLIENT_ID"), 
    client_secret=os.getenv("CLIENT_SECRET"), 
    user_agent=os.getenv("USER_AGENT")
)

print (f"app access is read only: {reddit.read_only}")
subreddit = reddit.subreddit("redditdev")
print (f"name of subreddit: {subreddit.display_name}")  # output: redditdev
print(f"tilte of subreddit: {subreddit.title}")         # output: reddit development
print(f"description of subreddit: {subreddit.description}")

# Define the subreddit and post you want to pull comments from
post_url = "https://www.reddit.com/r/informatik/comments/1i7zwp0/gutes_buch_%C3%BCber_softwarearchitektur/"
post = reddit.submission(url=post_url)





# Fetch all the comments
post.comments.replace_more(limit=None)  # This ensures you load all comments, including 'MoreComments' objects
all_comments = []
for comment in post.comments.list():
    all_comments.append(comment.body)
    if isinstance(comment, praw.models.Comment):
        # Ensure the comment author exists (i.e. they are not a deleted account)
        if comment.author:
            # Fetch the user's profile and get their karma
            user = reddit.redditor(comment.author.name)
            print(f"Comment by: {comment.author.name}")
            print(f"User karma: {user.link_karma + user.comment_karma}")  # Total karma (link + comment karma)
            print(f"Comment content: {comment.body}\n")
        else:
            print("Comment by: [deleted]")
            print("User karma: N/A (deleted user)\n")
    

# Print all comments
for comment in all_comments:
    print(comment)

emoji_analysis.print_emojis("\n".join(all_comments))