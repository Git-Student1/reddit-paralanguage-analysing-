import os
import emoji
from matplotlib import font_manager
import matplotlib
from matplotlib.ticker import MultipleLocator
import pandas as pd
import matplotlib.pyplot as plt
from helper import Helper
from master_file import MasterFile

class EmojiAnalysis:
    #TODO: remove tight coupling with masterfile
    def __init__(self, master_file:MasterFile):
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

    def __visualize_emoji_use(self, emojis:list[list], fullname:str):
        """
        create visualisation of the emoji usage
        """
        # Get the list of all available fonts
        #available_fonts = fm.findSystemFonts(fontpaths=None, fontext='ttf')
        plt.figure(dpi=240)

        flattened_emoji_list = self.__flatten_emoji_list(emojis)
        if(len(flattened_emoji_list)!= 0 ):
            flattened_emoji_list = [f"{emoji.demojize(the_emoji)} {the_emoji}" for the_emoji in flattened_emoji_list]
            ax = pd.Series(flattened_emoji_list).value_counts().plot(kind='barh', )
            ax.bar_label(ax.containers[0]) # adds count number to each bar in the graphic
            ax.xaxis.set_major_locator(MultipleLocator(1)) # sets min. spacing to one, as the count of an emoji is always an integer
        else:
            fig, ax = plt.subplots()
            fig.text(0.1, 0.1, 'No emojis present', fontsize=50, color='gray', alpha=0.5,
         rotation=45, ha='center', va='center', rotation_mode='anchor')
        ax.set_title( f"Emoji usage for thread {fullname}") 
        plt.tight_layout()
        plt.savefig(f'data/{fullname}.png')
            #plt.show()

         
    def __flatten_emoji_list(self, emoji_list: list[list]):
        return [item for sub_list in emoji_list for item in sub_list]

    def __extract_emojis_from_posts(self, fullname):
        """
        extracts emojis, adds them to a new column of the individual post csv file. \n
        :return: the list of emojis found
        """
        # TODO: remove coupling, only return list of emojios found
        folder_path = Helper.get_folderpath()
        file_path = os.path.join(folder_path, f'{fullname}.csv')

        df = pd.read_csv(file_path)
        df['commentEmojis'] = df['commentContent'].apply(lambda content: self.__extract_emojis(content))
        df.to_csv(file_path, index=False)
       
        self.__visualize_emoji_use(df['commentEmojis'].tolist(), fullname=fullname)
        
        return df['commentEmojis'].to_list()
    

    def __extract_emojis(self, text):
        # This function uses the emoji library to extract emojis from the given text.
        return [char for char in text if emoji.is_emoji(char)]



    def __print_emojis(self, text):
        # Example text or thread (you can replace this with the thread content)

        # Extract emojis from the text
        emojis = self.__extract_emojis(text=text)

        # Read out the emojis
        if emojis:
            print("Emojis found:", emojis)
        else:
            print("No emojis found.")
