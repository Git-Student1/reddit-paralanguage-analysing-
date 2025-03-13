from itertools import pairwise
import os

import matplotlib
from matplotlib import pyplot as plt
import matplotlib.axes
from matplotlib.container import BarContainer
from matplotlib.text import Annotation
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
    def __create_ax(cls, series_or_df:pd.Series|pd.DataFrame, bigger_plot:bool):

            if type(series_or_df)== pd.Series:
                max = series_or_df.max()
            else:
                max = series_or_df.values.max()
            if bigger_plot:
                ax = series_or_df.plot.barh(figsize=(15,13))
            else: 
                ax = series_or_df.plot.barh()
            # fixing overlapping annotations
            bar_contaioners:list[BarContainer] = []
            bar_annotations:list[list[Annotation]] = []
            for container in ax.containers: 
                if (type(container) != BarContainer):
                    raise TypeError("plot has to be a barplot")
                annotations = ax.bar_label(container=container, padding=5) 
                bar_contaioners.append(container)
                bar_annotations.append(annotations)
            cls.__fix_overlapping_annotations_for_boxplot(bar_contaioners, bar_annotations)

            return ax
    @classmethod
    def __fix_overlapping_annotations_for_boxplot(cls, bar_contaioners:list[BarContainer], bar_annotations:list[list[Annotation]]):
        # inspired by https://www.dontusethiscode.com/blog/2023-06-14_stacked_barlabels.html, adapted and simplified
        for (bar_annotations_upper, bar_annotations_lower) in pairwise(bar_annotations):
            for (annotation_upper, annotation_lower)  in zip(bar_annotations_upper, bar_annotations_lower):
                # if the stacked text overlap, bottom align the top label and reset the
                #   xytext value (accessed via xyann)
                if annotation_upper.get_window_extent().overlaps(annotation_lower.get_window_extent()):
                    annotation_lower.set_ha('left')
                    annotation_lower.xyann = (0, 0)        
    @classmethod
    def plot_and_save(cls, series_or_df:pd.Series|pd.DataFrame, title: str, file_path: str, bigger_plot:bool):
        """
            file_path: WITHOUT png ending
        """
        ax = cls.__create_ax(series_or_df=series_or_df, bigger_plot=bigger_plot)
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
    def plot_and_save_including_relative(cls, series_or_df:pd.Series|pd.DataFrame, title: str, file_path: str, relative_comment_divisor:float, relative_symbol_divisor:float, bigger_plot:bool=False, relative_comment_divisor2:float=0,  relative_symbol_divisor2:float=0):
            """
            file_path: WITHOUT png ending
            """

            cls.plot_and_save(series_or_df=series_or_df, title=title, file_path=file_path, bigger_plot=bigger_plot)

            if(relative_comment_divisor2==0) or type(series_or_df)==pd.Series:
                series_or_df_relative_comment=series_or_df/relative_comment_divisor
                series_or_df_relative_symbol = series_or_df/relative_symbol_divisor
            else:
                column_0 = series_or_df.columns[0]
                column_1 = series_or_df.columns[1]

                series_or_df_relative_comment = series_or_df.copy()
                series_or_df_relative_comment[column_0] = series_or_df_relative_comment[column_0].div(relative_comment_divisor)
                series_or_df_relative_comment[column_1] = series_or_df_relative_comment[column_1].div(relative_comment_divisor)
                
                series_or_df_relative_symbol = series_or_df.copy()
                series_or_df_relative_symbol[column_0] = series_or_df_relative_symbol[column_0].div(relative_symbol_divisor)
                series_or_df_relative_symbol[column_1] = series_or_df_relative_symbol[column_1].div(relative_symbol_divisor)
           
            cls.plot_and_save(series_or_df=series_or_df_relative_comment, title=title + " relative(comment)", file_path=file_path+"_relative_comment", bigger_plot=bigger_plot)
            cls.plot_and_save(series_or_df=series_or_df_relative_symbol, title=title + " relative(symbol)", file_path=file_path+"_relative_symbol",bigger_plot=bigger_plot)
            