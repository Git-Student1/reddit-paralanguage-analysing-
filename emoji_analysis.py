import os
import emoji
from matplotlib import font_manager
import matplotlib
import matplotlib.axes
from matplotlib.ticker import MultipleLocator
import pandas as pd
import matplotlib.pyplot as plt
from helper import Helper
from master_file import MasterFile

class EmojiAnalysis:
    #TODO: remove tight coupling with masterfile
    def __init__(self, master_file:MasterFile):
        self.master_file = master_file
        self.master_df: pd.DataFrame = master_file.df
        self.master_file_path = master_file.master_file_path
        # change front to a font that can display emojis
        plt.rcParams['font.family'] = 'Segoe UI Emoji'
        #matplotlib.use("module://mplcairo.qt")
        #matplotlib.use('TkAgg') 


    def extract_emojis_to_master_and_post_file(self):
        """
        adds emojis to the MasterFile dataframe(df) and converts new df to masterfile, efectively updating the masterfile
        """
        print("--- start emoji analysis ---")
        # TODO: letz the masterfile take care of the infos, given the list of comments, return the emojis in it
        master_df = self.master_df
        post_fullnames = master_df['postFullname'].to_list()

        # analyze each posts emojis, then put them as a flattened list in the master file
        emoji_dict = {}
        for full_name in post_fullnames:
            emoji_list = self.__extract_emojis_from_posts(full_name)
            emoji_dict[full_name] = self.__flatten_emoji_list(emoji_list)
        master_df['postEmojis'] = master_df['postFullname'].apply(lambda full_name: emoji_dict[full_name])
        master_df.to_csv(self.master_file_path, index=False)





    def __visualize_emoji_use(self, emojis:list[list[str]], fullname:str):
        """
        create visualisation of the emoji usage
        """
        # Get the list of all available fonts
        #available_fonts = fm.findSystemFonts(fontpaths=None, fontext='ttf')
        plt.figure(dpi=240)
        flattened_emoji_list = self.__flatten_emoji_list(emojis)
        n = 20
        title = f"Emoji usage for thread {fullname}"
        title_most_common = f"Emoji usage for thread {fullname} - {n} most common"
        image_folder_path = Helper.get_folder_path_for_thread_image_files(post_fullname=fullname)
        file_path_all = os.path.join(image_folder_path, fullname)
        file_path_most_common = os.path.join(image_folder_path, f'{fullname}_most_common')
        
        if(len(flattened_emoji_list)!= 0 ):
            flattened_emoji_list = self.prossess_emojis_for_display(flattened_emoji_list)
            all = pd.Series(flattened_emoji_list).value_counts()
            number_of_comments = self.master_file.get_number_of_comments_for_thread(post_fullname=fullname)
            number_of_symbols = self.master_file.get_number_of_symbols_for_thread(post_fullname=fullname)
            Helper.plot_and_save_including_relative(series_or_df=all, title=title, file_path=file_path_all, relative_comment_divisor=number_of_comments, relative_symbol_divisor=number_of_symbols)
            if all.count()>20:
                most_common_only = self.get_df_with_n_highest_values(pd.Series(flattened_emoji_list).value_counts(), n)
                Helper.plot_and_save_including_relative(series_or_df=most_common_only, title=title_most_common, file_path=file_path_most_common, relative_comment_divisor=number_of_comments, relative_symbol_divisor=number_of_symbols)
        else:
            fig, ax = plt.subplots()
            fig.text(0.1, 0.1, 'No emojis present', fontsize=50, color='gray', alpha=0.5,
        rotation=45, ha='center', va='center', rotation_mode='anchor')
            Helper.postproccess_and_save_ax(ax=ax, title=title, file_path=file_path_all )
            #plt.show()
    
    def prossess_emojis_for_display(self, emoji_list:list[str]):
        return [f"{emoji.demojize(the_emoji)} {the_emoji}" for the_emoji in emoji_list]
         
    def __flatten_emoji_list(self, emoji_list: list[list]):
        return [item for sub_list in emoji_list for item in sub_list]

    def __extract_emojis_from_posts(self, fullname):
        """
        extracts emojis, adds them to a new column of the individual post csv file. \n
        :return: the list of emojis found
        """
        # TODO: remove coupling, only return list of emojios found
        folder_path = Helper.get_folder_path_for_thread_files(post_fullname=fullname)
        file_path = os.path.join(folder_path, f'{fullname}.csv')

        df = pd.read_csv(file_path)
        df['commentEmojis'] = df['commentContent'].apply(lambda content: self.__extract_emojis(content))
        df.to_csv(file_path, index=False)
       
        self.__visualize_emoji_use(df['commentEmojis'].tolist(), fullname=fullname)
        
        return df['commentEmojis'].to_list()
    

    def __extract_emojis(self, text):
        # This function uses the emoji library to extract emojis from the given text.
        return [char for char in text if emoji.is_emoji(char)]
    
    def get_df_with_n_highest_rows_for_each_column(self, df:pd.DataFrame, n:int):
        df_with_10_most_common_each = pd.DataFrame()
        for column in df.columns:
            df_with_10_most_common_each = pd.concat([df_with_10_most_common_each,df.nlargest(n, columns=[column])], axis=0)
        df_with_10_most_common_each = df_with_10_most_common_each.drop_duplicates()
        return df_with_10_most_common_each
    
    def get_df_with_n_highest_values(self, series:pd.Series, n:int):
        return series.nlargest(n)



    def __print_emojis(self, text):
        # Example text or thread (you can replace this with the thread content)

        # Extract emojis from the text
        emojis = self.__extract_emojis(text=text)

        # Read out the emojis
        if emojis:
            print("Emojis found:", emojis)
        else:
            print("No emojis found.")
