
from matplotlib import pyplot as plt
import pandas as pd
from master_file import MasterFile


class MultiThreadOperations:
    def __init__(self, masterfile:MasterFile) -> None:
        self.masterfile = masterfile

    def grouping(self, post_group:list[str]):
        #TODO: remove coupling with compare_groups method
        df = self.__get_df_sum(post_group=post_group)
        title = f"grouping for {post_group}"
        self.__create_plot_for_df(df=df, title=title)

    def __get_df_sum(self, post_group:list[str]):
        # only the para language values
        df = self.masterfile.df[self.masterfile.para_all_columns + [self.masterfile.post_full_name_cn]]
        # only the values from the group 
        df = df[df[self.masterfile.post_full_name_cn].notna() & df[self.masterfile.post_full_name_cn].isin( post_group)]
        return pd.DataFrame(df.agg("sum"))
    
    def __create_plot_for_df(self, df:pd.DataFrame, title:str):
        pfn = self.masterfile.post_full_name_cn
        df.columns = df.columns.astype(str)
        for column in df.columns:
            df.rename({column.__str__(): str(df.loc[pfn, column])}, axis=1, inplace=True, errors='raise')
        df = df.drop(pfn)
        #print(result.to_string())
        ax = df.plot.barh()
        ax.bar_label(ax.containers[0])
        ax.set_title(title)
        plt.subplots_adjust(top=0.9, bottom=0.1, left=0.3, right=0.9)
        plt.show()

    def compare_groups(self, post_group1:list[str], post_group2:list[str]):

        df_group1_grouped = self.__get_df_sum(post_group=post_group1)
        df_group2_grouped = self.__get_df_sum(post_group=post_group2)
        result = pd.concat([df_group1_grouped, df_group2_grouped], axis=1)
        title = f"comparison for {post_group1} and {post_group2}"
        self.__create_plot_for_df(df=result, title=title)
        


        



