import re
import praw
import emoji_analysis
from dotenv import load_dotenv
import os
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from nltk.tokenize import WhitespaceTokenizer 
from nltk.corpus import stopwords
import pandas as pd

from helper import Helper
from master_file import MasterFile


class VaderAnalysis:
    def __init__(self, master_file:MasterFile):
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

        master_df['sentimentScore'] = master_df['postFullname'].apply(lambda full_name: score_dict[full_name]['sentimentScore'])
        
        master_df.to_csv(self.master_file_path, index=False)


    def analyze_sentiment_in_post(self, fullname):
        folder_path = Helper.get_folder_path_for_thread_files(post_fullname=fullname)
        file_path = os.path.join(folder_path, f'{fullname}.csv')

        df = pd.read_csv(file_path)
        df['sentimentScore'] = df['commentContent'].apply(lambda content: self.analyzer.polarity_scores(self.get_tokenized_text(content))['compound'])
        df.to_csv(file_path, index=False)

        return {'sentimentScore': df['sentimentScore'].mean()}
    
    def get_tokenized_text(self, text):
        
        #print("--------------------------")
        #print(text)
        #print(self.analyzer.polarity_scores(text))
        #print("\n")
        tokenizer = WhitespaceTokenizer()
        tokens = tokenizer.tokenize(text)


        stop_words = set(stopwords.words('english'))
        filtered_tokens = [word.lower().strip(".?!,") for word in tokens if word.lower().strip(".?!,") not in stop_words]
        #print(filtered_tokens)
        #print("\n")

        sentence = " ".join(filtered_tokens)
        #print(sentence)
        #print("\n")


        #print(self.analyzer.polarity_scores(sentence))
        #print("\n")
        return sentence