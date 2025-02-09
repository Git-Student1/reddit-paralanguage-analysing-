import praw
import emoji_analysis
from dotenv import load_dotenv
import os
from post_extractor import PostExtractor
from master_file import MasterFile
from emoji_analysis import EmojiAnalysis
from vader_analysis import VaderAnalysis

postsToExtract = [
    "https://www.reddit.com/r/PokemonScarletViolet/comments/1ibivcl/anyone_else_think_the_loyal_three_are_super_ugly/"
]

masterFile = MasterFile()
masterFile.update_master_file(postsToExtract)

emojiAnalysis = EmojiAnalysis(masterFile)
emojiAnalysis.extract_emoji_from_master()

vaderAnalysis = VaderAnalysis(masterFile)
vaderAnalysis.extract_mean_sentiment_score()