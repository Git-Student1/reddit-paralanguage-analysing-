import enum
import os
import pandas as pd
import praw

from datetime import datetime




class MasterFile:
    para_vq_pitch = "vq_pitch"
    para_vq_rhythm = "vq_rhythm"
    para_vq_stress = "vq_stress"
    para_vq_emphasis = "vq_emphasis"
    para_vq_tempo = "vq_tempo"
    para_vq_volume = "vq_volume"
    para_vq_censorship = "vq_censorship"
    para_vq_spelling = "vq_spelling"
    para_vq_overall = "vq_overall"

    para_vs_alternants = "vs_alternants"
    para_vs_differentiators = "vs_differentiators"
    para_vs_overall = "vs_overall"

    para_tk_alphahaptics = "tk_alphahaptics"
    para_tk_bodily_emoticons = "tk_bodily_emoticons"
    para_tk_tactile_emojis = "tk_tactile_emojis"
    para_tk_overall = "tk_overall"

    para_vk_alphakinesics = "vk_alphakinesics"
    para_vk_bodily_emoticons = "vk_bodily_emoticons"
    para_vk_bodily_emojis = "vk_bodily_emojis"
    para_vk_overall = "vk_overall"

    para_a_nonbodily_emoticons = "a_nonbodily_emoticons"
    para_a_nonbodily_emojis = "a_nonbodily_emojis"
    para_a_formatting = "a_formatting"
    para_art_overall = "art_overall"

    para_emoji_count = "emoji_count"
    para_emoji_index = "emoji_index"
    para_emoticon_index = "emoticon_index"
    
    para_all_columns = [para_vq_pitch, para_vq_rhythm, para_vq_stress, para_vq_emphasis, para_vq_tempo, para_vq_volume, para_vq_censorship, para_vq_spelling, para_vq_overall, 
                    para_vs_alternants, para_vs_differentiators, para_vs_overall,
                    para_tk_alphahaptics, para_tk_bodily_emoticons, para_tk_tactile_emojis, para_tk_overall, 
                    para_vk_alphakinesics, para_vk_bodily_emoticons, para_vk_bodily_emojis, para_vk_overall, 
                    para_a_nonbodily_emoticons, para_a_nonbodily_emojis, para_a_formatting, para_art_overall, 
                    para_emoji_count, para_emoji_index, para_emoticon_index
                    ]

    def __init__(self, folder_path):
        self.master_file_path = os.path.join(folder_path, '_master.csv')
        self.post_full_name_cn = "postFullname"
        self.dateRetrieved_cn = "dateRetrieved"
        self.postTitle_cn = "postTitle"
        self.postEmojis_cn = "postEmojis"
        self.sentimentScore_cn = "sentimentScore"

        if os.path.exists(self.master_file_path):
            self.df = pd.read_csv(self.master_file_path, na_values=['', 'NA', 'NaN'])
        else:
            self.df = pd.DataFrame(columns = [self.post_full_name_cn, self.dateRetrieved_cn, self.postTitle_cn,self.postEmojis_cn, self.sentimentScore_cn ])
            # TODO: remove print statement
            print("no masterfile exsists")
    
    def update_master_file(self):
        self.df.to_csv(self.master_file_path, index=False)
        
    def contains_post_entry(self, post_fullname):
        return post_fullname in self.df[self.post_full_name_cn].values

    def contains_all_para_values(self, fullname:str):
        df_with_row_for_fullname = self.df[self.df[self.post_full_name_cn] == fullname]
        try :
            return not df_with_row_for_fullname[self.para_all_columns].isna().values.any()
        except KeyError:
            # in case there are no para columns
            return False

    
    def getColumnAsList(self, columnName):
        return self.df[columnName].to_list()

           


