
from ast import literal_eval
from matplotlib import pyplot as plt
import pandas as pd
from emoji_analysis import EmojiAnalysis
from master_file import MasterFile


class MultiThreadOperations:
    def __init__(self, masterfile:MasterFile) -> None:
        self.masterfile = masterfile
        self.emoji_analysis = EmojiAnalysis(master_file=masterfile)

    def grouping(self, post_group:list[str]):
        emoji_value_counts = self.__get_df_emojis_count(post_group)
        title = f"grouping for {post_group}"
        self.__create_plot_for_df(emoji_value_counts, "emoji " + title)
        #PARA
        df = self.__get_df_sum_para(post_group=post_group)
        
        self.__create_plot_for_df(df=df, title="para "+ title)
        

    def compare_groups(self, post_group1:list[str], post_group2:list[str]):
        title = f"comparison for {post_group1} and {post_group2}"
        emoji_value_counts_1 = self.__get_df_emojis_count(post_group1)
        emoji_value_counts_2 = self.__get_df_emojis_count(post_group2)
        emoji_value_counts_2 = emoji_value_counts_2.rename({0:1}, axis=1)
        result = pd.concat([emoji_value_counts_1, emoji_value_counts_2], axis=1)
        self.__create_plot_for_df(result, title="emoji "+ title)
        
        #PARA
        df_group1_grouped = self.__get_df_sum_para(post_group=post_group1)
        df_group2_grouped = self.__get_df_sum_para(post_group=post_group2)
        df_group2_grouped = df_group2_grouped.rename({0:1}, axis=1)
        result = pd.concat([df_group1_grouped, df_group2_grouped], axis=1)
        
        self.__create_plot_for_df(df=result, title="para " +title)

    def __get_df_sum_para(self, post_group:list[str]):
        # only the para language values
        df = self.masterfile.df[self.masterfile.para_all_columns + [self.masterfile.post_full_name_cn]]
        # only the values from the group 
        df = df[df[self.masterfile.post_full_name_cn].notna() & df[self.masterfile.post_full_name_cn].isin( post_group)]
        return pd.DataFrame(df.agg("sum"))
    
    def __create_plot_for_df(self, df:pd.DataFrame, title:str):
        pfn = self.masterfile.post_full_name_cn
        #print(df.head())
        df.columns = df.columns.astype(str)
        for column in df.columns:
            df.rename({column.__str__(): str(df.loc[pfn, column])}, axis=1, inplace=True, errors='raise')
        df = df.drop(pfn)
        #print(result.to_string())
        ax = df.plot.barh(figsize=(15,10))
        ax.bar_label(ax.containers[0])
        ax.set_title(title)
        plt.subplots_adjust(top=0.9, bottom=0.1, left=0.3, right=0.9)
        plt.show()

    def __get_df_emojis_count(self, post_group:list[str]):
        # only the para language values
        df = self.masterfile.df[[self.masterfile.post_full_name_cn, self.masterfile.postEmojis_cn]]
        # only the values from the group 
        df = df[df[self.masterfile.post_full_name_cn].notna() & df[self.masterfile.post_full_name_cn].isin( post_group)]
        df[self.masterfile.postEmojis_cn].tolist()
        df[self.masterfile.postEmojis_cn] = df[self.masterfile.postEmojis_cn].apply(literal_eval)
        flattened_list = [item for sublist in df[self.masterfile.postEmojis_cn] for item in sublist]
        flattened_list = self.emoji_analysis.prossess_emojis_for_display(flattened_list)
        emoji_count_df = pd.DataFrame({0:pd.Series(flattened_list).value_counts()})
        #same structure as in para analysis for easy processing
        emoji_count_df.loc[self.masterfile.post_full_name_cn] = [", ".join(post_group)]
        return emoji_count_df

    
   


        



