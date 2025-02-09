import praw
import emoji_analysis
from dotenv import load_dotenv
import os
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import statistics
import pandas as pd

class VaderAnalysis:
    def __init__(self, master_file):
        self.analyzer = SentimentIntensityAnalyzer()
        self.master_df: pd.DataFrame = master_file.df
        self.master_file_path = master_file.master_file_path

    def extract_mean_sentiment_score(self):
        master_df = self.master_df
        post_fullnames = master_df['postFullname'].to_list()

        score_dict = {}

        for full_name in post_fullnames:
            mean_sentiment_score = self.analyze_sentiment_in_post(full_name)
            score_dict[full_name] = mean_sentiment_score

        master_df['sentimentScore'] = master_df['postFullname'].apply(lambda full_name: score_dict[full_name])
        
        master_df.to_csv(self.master_file_path, index=False)


    def analyze_sentiment_in_post(self, fullname):
        file_dir = os.path.dirname(os.path.abspath(__file__))
        csv_folder = 'data'
        folder_path = os.path.join(file_dir, csv_folder)
        file_path = os.path.join(folder_path, f'{fullname}.csv')

        df = pd.read_csv(file_path)
        df['sentimentScore'] = df['commentContent'].apply(lambda content: self.analyzer.polarity_scores(content)['compound'])
        df.to_csv(file_path, index=False)

        return df['sentimentScore'].mean()