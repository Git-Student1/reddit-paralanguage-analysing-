import os
import sys

from matplotlib import pyplot as plt
from matplotlib.ticker import MultipleLocator
import pandas as pd
from master_file import MasterFile
from para_paralanguage_classifier import para_output


class ParaAnalysis:

    def __init__(self, master_file:MasterFile, fast_analysis=False):
        self.master_df: pd.DataFrame = master_file.df
        self.master_file_path = master_file.master_file_path
        self.PARA = para_output()
        self.fast_analysis = fast_analysis


    def extract_para_values(self):
        print("--- starting para analysis ---")
        master_df = self.master_df
        post_fullnames = master_df['postFullname'].to_list()

        for full_name in post_fullnames:
            print(f"Analyzing: {full_name}")
            self.analyze_sentiment_in_post(full_name)
            #print("Done!\n\n")
        
        #master_df.to_csv(self.master_file_path, index=False)


    def analyze_sentiment_in_post(self, fullname):
        file_dir = os.path.dirname(os.path.abspath(__file__))
        csv_folder = 'data'
        folder_path = os.path.join(file_dir, csv_folder)
        file_path_post_df = os.path.join(folder_path, f'{fullname}.csv')
        file_path_para_df = os.path.join(folder_path, f'{fullname}_para.csv')
        file_path_para_image = os.path.join(folder_path,f'{fullname}_para.png')

        if os.path.exists(file_path_para_df):
            print(f"para analysis already exists for file {fullname}. Skipping")
            return

        post_df = pd.read_csv(file_path_post_df)

        # ask for fast or slow analysis
        fast_analysis_text = input("Fast para analysis(J/N)")
        if fast_analysis_text.lower() == "j": fast_analysis = True
        elif fast_analysis_text.lower() == "n": fast_analysis= False
        else:
            print("Proceeding without fast analysis")
            fast_analysis= False
        
        # do the fast or slow analysis 
        if not fast_analysis:
            total_comments = len(post_df["commentContent"])
            output = []
            for i, comment in enumerate(post_df["commentContent"], start=1):
                output.append(self.para(comment))

                sys.stdout.write(f"\rProcessing comment {i}/{total_comments} ({(i/total_comments)*100:.2f}%) ")
                sys.stdout.flush()
            print()
        else:
            text_to_analyse = post_df["commentContent"].str.cat(sep =", ")
            output = [self.para(text_to_analyse)]
        


        # Convert the list of dictionaries to a DataFrame
        df_para_analysis = pd.DataFrame(output)

        # Create graphic for paralanguage use analysis
        df_para_analysis_compressed =  df_para_analysis.drop(["commentContent"], axis=1,).agg(['sum'])
        df_para_analysis_compressed.info()
        print(df_para_analysis_compressed.T.columns)
        ax = df_para_analysis_compressed.T.plot.barh()
        ax.bar_label(ax.containers[0]) # adds count number to each bar in the graphic
        ax.yaxis.set_major_locator(MultipleLocator(1)) # sets min. spacing to one, as the count of a paralanguage occuring is always an integer
        ax.set_title( f"Paralanguage usage for thread {fullname}")
        plt.tight_layout()
        plt.savefig(file_path_para_image)


        df_para_analysis.to_csv(file_path_para_df, index=False)

    
    def para(self, input_text):
        data = {
            # General
            "commentContent": input_text,

            # Voice Quality
            "vq_pitch": self.PARA.compute_vq_pitch(input_text)["vq_pitch"],
            "vq_rhythm": self.PARA.compute_vq_rhythm(input_text)["vq_rhythm"],
            "vq_stress": self.PARA.compute_vq_stress(input_text)["vq_stress"],
            "vq_emphasis": self.PARA.compute_vq_emphasis(input_text)["vq_emphasis"],
            "vq_tempo": self.PARA.compute_vq_tempo(input_text)["vq_tempo"],
            "vq_volume": self.PARA.compute_vq_volume(input_text)["vq_volume"],
            "vq_censorship": self.PARA.compute_vq_censorship(input_text)["vq_censorship"],
            "vq_spelling": self.PARA.compute_vq_spelling(input_text)["vq_spelling"],
            "vq_overall": self.PARA.compute_VQ(input_text)["Voice Qualities"],

            # Vocalizations
            "vs_alternants": self.PARA.compute_vs_alternants(input_text)["vs_alternants"],
            "vs_differentiators": self.PARA.compute_vs_differentiators(input_text)["vs_differentiators"],
            "vs_overall": self.PARA.compute_VS(input_text)["Vocalizations"],

            # Tactile Kinesics
            "tk_alphahaptics": self.PARA.compute_tk_alphahaptics(input_text)["tk_alphahaptics"],
            "tk_bodily_emoticons": self.PARA.compute_tk_bodilyemoticons(input_text)["tk_tactile_emoticons"],
            "tk_tactile_emojis": self.PARA.compute_tk_tactileemojis(input_text)["tk_tactile_emojis"],
            "tk_overall": self.PARA.compute_TK(input_text)["Tactile Kinesics"],

            # Visual Kinesics
            "vk_alphakinesics": self.PARA.compute_vk_alphakinesics(input_text)["vk_alphakinesics"],
            "vk_bodily_emoticons": self.PARA.compute_vk_bodilyemoticons(input_text)["vk_bodily_emoticons"],
            "vk_bodily_emojis": self.PARA.compute_vk_bodilyemojis(input_text)["vk_bodily_emojis"],
            "vk_overall": self.PARA.compute_VK(input_text)["Visual Kinesics"],

            # Artifacts
            "a_nonbodily_emoticons": self.PARA.compute_a_nonbodilyemoticons(input_text)["a_nonbodily_emoticons"],
            "a_nonbodily_emojis": self.PARA.compute_a_nonbodilyemojis(input_text)["a_nonbodily_emojis"],
            "a_formatting": self.PARA.compute_a_formatting(input_text)["a_formatting"],
            "art_overall": self.PARA.compute_ART(input_text)["Artifacts"],

            # Aggregate Variables 
            "emoji_count": self.PARA.compute_total_emoji_raw_count(input_text)["Emoji_Count"],
            "emoji_index": self.PARA.compute_total_emoji_count(input_text)["Emoji_Index"],
            "emoticon_index": self.PARA.compute_total_emoticon_count(input_text)["Emoticon_Index"],

            # Preserve the original commentContent for merging
            "commentContent": input_text
        }
        return data