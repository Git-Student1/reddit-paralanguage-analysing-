import os

import matplotlib
from matplotlib import pyplot as plt
import matplotlib.axes
from matplotlib.ticker import MultipleLocator
import pandas as pd


class Helper:
    @classmethod
    def get_files_base_folderpath(cls):
        file_dir = os.path.dirname(os.path.abspath(__file__))
        csv_folder = 'data'
        folder_path = os.path.join(file_dir, csv_folder)
        return folder_path
    @classmethod
    def postproccess_and_save_ax(self, ax:matplotlib.axes.Axes, title: str, file_path: str):
        ax.set_title(title) 
        plt.tight_layout()
        plt.savefig(file_path)
        plt.clf()
        matplotlib.pyplot.close()

    @classmethod
    def __create_ax(self, series_or_df:pd.Series|pd.DataFrame):
            print(series_or_df)

            if type(series_or_df)== pd.Series:
                max = series_or_df.max()
            else:
                max = series_or_df.values.max()
            series_or_df.max()
            ax = series_or_df.plot(kind='barh',)
            ax.bar_label(ax.containers[0]) # type: ignore # adds count number to each bar in the graphic
            #ax.xaxis.set_major_locator(MultipleLocator(max/6)) # sets min. spacing to one, as the count of an emoji is always an integer
            return ax
    @classmethod
    def plot_and_save(cls, series_or_df:pd.Series|pd.DataFrame, title: str, file_path: str):
        """
            file_path: WITHOUT png ending
        """
        ax = cls.__create_ax(series_or_df=series_or_df)
        cls.postproccess_and_save_ax(ax=ax, title=title, file_path=file_path+".png")
    
    @classmethod
    def get_file_path_for_thread_file(cls, post_fullname):
        file_path = os.path.join(cls.get_folder_path_for_thread_files(post_fullname=post_fullname), f'{post_fullname}.csv')
        return file_path
    @classmethod
    def get_folder_path_for_thread_image_files(cls, post_fullname:str):
        folder_path =os.path.join(cls.get_files_base_folderpath(),post_fullname)
        os.makedirs(folder_path, exist_ok=True)
        return folder_path
    
    @classmethod
    def get_folder_path_for_thread_files(cls, post_fullname:str):
        folder_path =os.path.join(cls.get_files_base_folderpath(),post_fullname)
        os.makedirs(folder_path, exist_ok=True)
        return folder_path

    @classmethod
    def plot_and_save_including_relative(cls, series_or_df:pd.Series|pd.DataFrame, title: str, file_path: str, relative_comment_divisor:float, relative_symbol_divisor:float ):
            """
            file_path: WITHOUT png ending
            """
            print(relative_comment_divisor)
            cls.plot_and_save(series_or_df=series_or_df, title=title, file_path=file_path)
            cls.plot_and_save(series_or_df=series_or_df/relative_comment_divisor, title=title + " relative(comment)", file_path=file_path+"_relative_comment")
            cls.plot_and_save(series_or_df=series_or_df/relative_symbol_divisor, title=title + " relative(symbol)", file_path=file_path+"_relative_symbol")