import os

import matplotlib
from matplotlib import pyplot as plt
import matplotlib.axes
from matplotlib.ticker import MultipleLocator
import pandas as pd


class Helper:
    @classmethod
    def get_folderpath(cls):
        file_dir = os.path.dirname(os.path.abspath(__file__))
        csv_folder = 'data'
        folder_path = os.path.join(file_dir, csv_folder)
        return folder_path
    @classmethod
    def postproccess_and_save_ax(self, ax:matplotlib.axes.Axes, title: str, file_path: str):
        ax.set_title(title) 
        plt.tight_layout()
        plt.savefig(file_path)
    @classmethod
    def create_ax(self, series_or_df:pd.Series|pd.DataFrame):
            if type(series_or_df)== pd.Series:
                max = series_or_df.max()
            else:
                max = series_or_df.values.max()
            series_or_df.max()
            ax = series_or_df.plot(kind='barh',)
            ax.bar_label(ax.containers[0]) # type: ignore # adds count number to each bar in the graphic
            ax.xaxis.set_major_locator(MultipleLocator(max/10)) # sets min. spacing to one, as the count of an emoji is always an integer
            return ax
    @classmethod
    def plot_and_save(self, series_or_df:pd.Series|pd.DataFrame, title: str, file_path: str):
        ax = self.create_ax(series_or_df=series_or_df)
        self.postproccess_and_save_ax(ax=ax, title=title, file_path=file_path)