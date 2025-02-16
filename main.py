from master_file import MasterFile
from emoji_analysis import EmojiAnalysis
from vader_analysis import VaderAnalysis

postsToExtract = [
    "https://www.reddit.com/r/Republican/comments/1i7f49t/dear_anyone_still_using_reductio_ad_hitlerum_as_a/"
]

masterFile = MasterFile()
masterFile.update_master_file(postsToExtract)

emojiAnalysis = EmojiAnalysis(masterFile)
emojiAnalysis.extract_emoji_from_master()

vaderAnalysis = VaderAnalysis(masterFile)
vaderAnalysis.extract_mean_sentiment_score()