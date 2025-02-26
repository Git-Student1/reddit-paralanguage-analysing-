
from matplotlib import pyplot as plt
import pandas as pd
from master_file import MasterFile


class MultiThreadOperations:
    def __init__(self, masterfile:MasterFile) -> None:
        self.masterfile = masterfile

    def grouping(self, post_group:list[str]):
        #TODO: remove coupling with compare_groups method
        pfn = self.masterfile.post_full_name_cn
        df = self.masterfile.df[self.masterfile.para_all_columns + [self.masterfile.post_full_name_cn]]
        df = df[df[self.masterfile.post_full_name_cn].notna() & df[self.masterfile.post_full_name_cn].isin( post_group)]
        df = pd.DataFrame(df.agg("sum"))
        df.columns = df.columns.astype(str)
        for column in df.columns:
            df.rename({column.__str__(): str(df.loc[pfn, column])}, axis=1, inplace=True, errors='raise')
        df = df.drop(pfn)
        #print(result.to_string())
        ax = df.plot.barh()
        ax.bar_label(ax.containers[0])
        ax.set_title( f"grouping for {post_group}")
        plt.subplots_adjust(top=0.9, bottom=0.1, left=0.3, right=0.9)
        plt.show()

        

    def compare_groups(self, post_group1:list[str], post_group2:list[str]):
        # only the para language values
        pfn = self.masterfile.post_full_name_cn
        df = self.masterfile.df[self.masterfile.para_all_columns + [self.masterfile.post_full_name_cn]]
        #print(df.to_string())
        # only the values from the groups to compare 
        df_group1 = df[df[self.masterfile.post_full_name_cn].notna() & df[self.masterfile.post_full_name_cn].isin( post_group1)]
        df_group2 = df[df[self.masterfile.post_full_name_cn].isin( post_group2)]
        print(df_group1.to_string())
        df_group1_grouped = df_group1.agg("sum")
        df_group2_grouped = df_group2.agg("sum")
        #print(df_group1_grouped)
        #print(df_group2_grouped)
        result = pd.concat([df_group1_grouped, df_group2_grouped], axis=1)
        #print(result.columns.tolist())
        result.columns = result.columns.astype(str)
        for column in result.columns:
            result.rename({column.__str__(): str(result.loc[pfn, column])}, axis=1, inplace=True, errors='raise')
        result = result.drop(pfn)
        #print(result.to_string())
        ax = result.plot.barh()
        ax.bar_label(ax.containers[0])
        ax.set_title( f"comparison for {post_group1} and {post_group2}")
        plt.subplots_adjust(top=0.9, bottom=0.1, left=0.3, right=0.9)
        plt.show()
        


        



