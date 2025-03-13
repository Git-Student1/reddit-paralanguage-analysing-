
from ast import literal_eval
from itertools import pairwise
from matplotlib import pyplot as plt
from matplotlib.container import BarContainer
from matplotlib.text import Annotation
import pandas as pd
from emoji_analysis import EmojiAnalysis
from helper import Helper
from master_file import MasterFile



class MultiThreadOperations:
    def __init__(self, masterfile:MasterFile) -> None:
        self.masterfile = masterfile
        self.emoji_analysis = EmojiAnalysis(master_file=masterfile)
        self.summary_columns = MasterFile.summary_columns.copy()
        self.summary_columns.append(self.masterfile.post_full_name_cn)
        

    def grouping(self, post_group:list[str], group_name:str, save_folder:str):
        title = f"grouping for group {group_name}: {post_group}"
        #Emoji
        file_name = "grouping"
        emoji_value_counts = self.__get_df_emojis_count(post_group)
        emoji_value_counts = self.__prepare_df_for_plot_creation(df=emoji_value_counts)
        self.__create_plot_for_df(emoji_value_counts, "emoji " + title, save_folder=save_folder,  file_name="emoji "+file_name, group1=post_group)
        self.__create_plot_for_df(df=self.emoji_analysis.get_df_with_n_highest_rows_for_each_column(emoji_value_counts, 10), title="emoji(10 most common each) " +title, save_folder=save_folder, file_name="emoji_"+file_name+"_most_common", group1=post_group)

        #PARA
        df = self.__get_df_sum_para(post_group=post_group)
        df_summary = df.T[self.summary_columns].T
        df = self.__prepare_df_for_plot_creation(df=df)
        df_summary = self.__prepare_df_for_plot_creation(df=df_summary)
        self.__create_plot_for_df(df=df, title="para "+ title, save_folder=save_folder,  file_name="para_"+file_name, group1=post_group)
        self.__create_plot_for_df(df=df_summary, title="para summary"+ title, save_folder=save_folder,  file_name="para_summary_"+file_name, group1=post_group)

    def compare_groups(self, post_group1:list[str], post_group2:list[str], post_group_name1:str, post_group_name2:str, save_folder:str):
        title = f"comparison for group '{post_group_name1}' {post_group1} and group '{post_group_name2}' {post_group2}"
        #Emoji
        file_name = "comparison"
        emoji_value_counts_1 = self.__get_df_emojis_count(post_group1)
        emoji_value_counts_2 = self.__get_df_emojis_count(post_group2)
        emoji_value_counts_2 = emoji_value_counts_2.rename({0:1}, axis=1)
        #concat converts dtype to object aka string
        result = pd.concat([emoji_value_counts_1, emoji_value_counts_2], axis=1)#pd.concat([emoji_value_counts_1, emoji_value_counts_2.reindex(emoji_value_counts_1.index.join(emoji_value_counts_2.index, how='outer'))])
        result = self.__prepare_df_for_plot_creation(df=result)
        self.__create_plot_for_df(result, 
                                  title="emoji "+ title, 
                                  save_folder=save_folder,
                                      file_name="emoji "+file_name,
                                      group1=post_group1, 
                                      group2=post_group2, bigger_plot=True)
        self.__create_plot_for_df(df=self.emoji_analysis.get_df_with_n_highest_rows_for_each_column(result, 10), 
                                  title="emoji(10 most common each) " +title, 
                                  save_folder=save_folder, 
                                  file_name="emoji "+file_name+" most common",
                                  group1=post_group1, 
                                  group2=post_group2)
        #PARA
        df_group1_grouped = self.__get_df_sum_para(post_group=post_group1)
        df_group2_grouped = self.__get_df_sum_para(post_group=post_group2)
        df_group2_grouped = df_group2_grouped.rename({0:1}, axis=1)
        result = pd.concat([df_group1_grouped, df_group2_grouped], axis=1)
        df_summary = result.T[self.summary_columns].T

        result = self.__prepare_df_for_plot_creation(df=result)
        df_summary = self.__prepare_df_for_plot_creation(df=df_summary)
        self.__create_plot_for_df(df=result, title="para " +title, save_folder=save_folder, file_name="para "+file_name,group1=post_group1, group2=post_group2 )
        self.__create_plot_for_df(df=df_summary, title="para summary"+ title, save_folder=save_folder,  file_name="para_summary_"+file_name, group1=post_group1,group2=post_group2)

        

    def __get_df_sum_para(self, post_group:list[str]):
        # only the para language values
        df = self.masterfile.df[self.masterfile.para_all_columns + [self.masterfile.post_full_name_cn]]
        # only the values from the group 
        df = df[df[self.masterfile.post_full_name_cn].notna() & df[self.masterfile.post_full_name_cn].isin( post_group)]
        return pd.DataFrame(df.agg("sum"))
    
    def __prepare_df_for_plot_creation(self, df:pd.DataFrame):
        """
        renames columns, removes unessasary row, and converts column values to int
        """
        pfn = self.masterfile.post_full_name_cn
        df.columns = df.columns.astype(str)
        for column in df.columns:
            df = df.rename({column.__str__(): str(df.loc[pfn, column])}, axis=1, inplace=False, errors='raise')
        df = df.drop(pfn, inplace=False)
        for column in df.columns:
            df[column] = df[column].astype(float)
        return df

    def __create_plot_for_df(self, df:pd.DataFrame, title:str, save_folder:str, file_name:str, group1:list[str], group2:list[str]=[], bigger_plot:bool=False):
        print(f"start new comparison plot creation: {title}")
        file_path = f"{save_folder}/{file_name}"
        number_of_comments = self.masterfile.get_number_of_comments_for_group(post_fullnames=group1)
        number_of_symbols = self.masterfile.get_number_of_symbols_for_group(post_fullnames=group1)
            
        #TODO: make sure that there are not multiple images of the same analysis with only different order of post names!
        if group2==[]:
            Helper.plot_and_save_including_relative(series_or_df=df, title=title, file_path=file_path, bigger_plot=bigger_plot, relative_comment_divisor=number_of_comments, relative_symbol_divisor=number_of_symbols)
        
        else: 
            number_of_comments2 = self.masterfile.get_number_of_comments_for_group(post_fullnames=group2)
            number_of_symbols2 = self.masterfile.get_number_of_symbols_for_group(post_fullnames=group2)
            Helper.plot_and_save_including_relative(series_or_df=df, title=title, 
                                                    file_path=file_path, bigger_plot=True, 
                                                    relative_comment_divisor=number_of_comments, 
                                                    relative_symbol_divisor=number_of_symbols, 
                                                    relative_comment_divisor2=number_of_comments2, 
                                                    relative_symbol_divisor2=number_of_symbols2,)
    



    def __get_df_emojis_count(self, post_group:list[str]):
        # only the para language values
        df = self.masterfile.df[[self.masterfile.post_full_name_cn, self.masterfile.postEmojis_cn]]
        # only the values from the group 
        df = df[df[self.masterfile.post_full_name_cn].notna() & df[self.masterfile.post_full_name_cn].isin( post_group)]
        df[self.masterfile.postEmojis_cn].tolist()
        #df[self.masterfile.postEmojis_cn] = df[self.masterfile.postEmojis_cn].apply(literal_eval)
        flattened_list = [item for sublist in df[self.masterfile.postEmojis_cn] for item in sublist]
        flattened_list = self.emoji_analysis.prossess_emojis_for_display(flattened_list)
        #let the df have the same structure as df in para analysis for easy processing
        emoji_count_df = pd.DataFrame({0:pd.Series(flattened_list).value_counts()})
        
        #emoji_count_df[0] = pd.to_numeric(emoji_count_df[0])
        #emoji_count_df[0] = emoji_count_df[0].astype(int)
        
        #name row 
        emoji_count_df.loc[self.masterfile.post_full_name_cn] = [", ".join(post_group)]
        return emoji_count_df

    
   


        



