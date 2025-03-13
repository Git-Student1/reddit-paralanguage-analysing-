import os
from helper import Helper
from master_file import MasterFile
from emoji_analysis import EmojiAnalysis
from post_extractor import PostExtractor
from vader_analysis import VaderAnalysis
from para_analysis import ParaAnalysis

postsToExtract = [
    "https://www.reddit.com/r/Republican/comments/1i7f49t/dear_anyone_still_using_reductio_ad_hitlerum_as_a/",
    "https://www.reddit.com/r/Piracy/comments/1itb0il/ublock_was_turned_off_i_guess_its_time_to_move/",
    "https://www.reddit.com/r/chemistry/comments/1iwzs71/found_this_old_looking_bottle_of_picric_acid_at/"#random one
]

folder_path = Helper.get_files_base_folderpath()


# Extract posts
post_extractor = PostExtractor()
masterFile = MasterFile(folder_path)
post_extractor.extract_posts(post_urls=postsToExtract, masterfile=masterFile)



emojiAnalysis = EmojiAnalysis(masterFile)
emojiAnalysis.extract_emojis_to_master_and_post_file()

vaderAnalysis = VaderAnalysis(masterFile)
vaderAnalysis.extract_mean_sentiment_score()

paraAnalysis = ParaAnalysis(master_file=masterFile)
paraAnalysis.extract_para_values()