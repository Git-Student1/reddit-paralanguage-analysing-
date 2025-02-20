import os
from master_file import MasterFile
from emoji_analysis import EmojiAnalysis
from post_extractor import PostExtractor
from vader_analysis import VaderAnalysis
from para_analysis import ParaAnalysis

postsToExtract = [
    "https://www.reddit.com/r/Republican/comments/1i7f49t/dear_anyone_still_using_reductio_ad_hitlerum_as_a/"
]
# Get Path to data folder
file_dir = os.path.dirname(os.path.abspath(__file__))
csv_folder = 'data'
folder_path = os.path.join(file_dir, csv_folder)


# Extract posts
post_extractor = PostExtractor(folder_path=folder_path)
masterFile = MasterFile(folder_path)
post_extractor.extract_posts(post_urls=postsToExtract, masterfile=masterFile)



emojiAnalysis = EmojiAnalysis(masterFile)
emojiAnalysis.extract_emojis_to_master_and_post_file()

vaderAnalysis = VaderAnalysis(masterFile)
vaderAnalysis.extract_mean_sentiment_score()

paraAnalysis = ParaAnalysis(master_file=masterFile)
paraAnalysis.extract_para_values()