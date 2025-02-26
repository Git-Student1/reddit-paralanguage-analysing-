import os
import sys

from matplotlib import pyplot as plt
from matplotlib.ticker import MultipleLocator
import pandas as pd
from master_file import MasterFile
from para_paralanguage_classifier import para_output


class ParaAnalysis:

    def __init__(self, master_file:MasterFile, fast_analysis=False):
        self.masterfile = master_file
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

        if os.path.exists(file_path_para_df) and self.masterfile.contains_all_para_values(fullname=fullname):
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

        # create summary of total paralanguage use
        df_para_analysis_compressed =  df_para_analysis.drop(["commentContent"], axis=1,).agg(['sum'])
        print(df_para_analysis_compressed.columns.tolist())
        
        # add summary to masterfile
        for column in df_para_analysis_compressed.columns.tolist():
            value = df_para_analysis_compressed.iloc[0][column]
            self.master_df.loc[self.master_df[self.masterfile.post_full_name_cn] == fullname, column] =  value
        self.masterfile.update_master_file()
        
        # Create graphic for summary for paralanguage use analysis
        ax = df_para_analysis_compressed.T.plot.barh()
        ax.bar_label(ax.containers[0]) # adds count number to each bar in the graphic
        ax.yaxis.set_major_locator(MultipleLocator(1)) # sets min. spacing to one, as the count of a paralanguage occuring is always an integer
        ax.set_title( f"Paralanguage usage for thread {fullname}")
        plt.tight_layout()
        plt.savefig(file_path_para_image)

        df_para_analysis.to_csv(file_path_para_df, index=False)

    
    def para(self, input_text):
        m = MasterFile
        data = {
            # General
            "commentContent": input_text,

            # Voice Quality
            m.para_vq_pitch: self.PARA.compute_vq_pitch(input_text)["vq_pitch"],
            m.para_vq_rhythm: self.PARA.compute_vq_rhythm(input_text)["vq_rhythm"],
            m.para_vq_stress: self.PARA.compute_vq_stress(input_text)["vq_stress"],
            m.para_vq_emphasis: self.PARA.compute_vq_emphasis(input_text)["vq_emphasis"],
            m.para_vq_tempo: self.PARA.compute_vq_tempo(input_text)["vq_tempo"],
            m.para_vq_volume: self.PARA.compute_vq_volume(input_text)["vq_volume"],
            m.para_vq_censorship: self.PARA.compute_vq_censorship(input_text)["vq_censorship"],
            m.para_vq_spelling: self.PARA.compute_vq_spelling(input_text)["vq_spelling"],
            m.para_vq_overall: self.PARA.compute_VQ(input_text)["Voice Qualities"],

            # Vocalizations
            m.para_vs_alternants: self.PARA.compute_vs_alternants(input_text)["vs_alternants"],
            m.para_vs_differentiators: self.PARA.compute_vs_differentiators(input_text)["vs_differentiators"],
            m.para_vs_overall: self.PARA.compute_VS(input_text)["Vocalizations"],

            # Tactile Kinesics
            m.para_tk_alphahaptics: self.PARA.compute_tk_alphahaptics(input_text)["tk_alphahaptics"],
            m.para_tk_bodily_emoticons: self.PARA.compute_tk_bodilyemoticons(input_text)["tk_tactile_emoticons"],
            m.para_tk_tactile_emojis: self.PARA.compute_tk_tactileemojis(input_text)["tk_tactile_emojis"],
            m.para_tk_overall: self.PARA.compute_TK(input_text)["Tactile Kinesics"],

            # Visual Kinesics
            m.para_vk_alphakinesics: self.PARA.compute_vk_alphakinesics(input_text)["vk_alphakinesics"],
            m.para_vk_bodily_emoticons: self.PARA.compute_vk_bodilyemoticons(input_text)["vk_bodily_emoticons"],
            m.para_vk_bodily_emojis: self.PARA.compute_vk_bodilyemojis(input_text)["vk_bodily_emojis"],
            m.para_vk_overall: self.PARA.compute_VK(input_text)["Visual Kinesics"],

            # Artifacts
            m.para_a_nonbodily_emoticons: self.PARA.compute_a_nonbodilyemoticons(input_text)["a_nonbodily_emoticons"],
            m.para_a_nonbodily_emojis: self.PARA.compute_a_nonbodilyemojis(input_text)["a_nonbodily_emojis"],
            m.para_a_formatting: self.PARA.compute_a_formatting(input_text)["a_formatting"],
            m.para_art_overall: self.PARA.compute_ART(input_text)["Artifacts"],

            # Aggregate Variables 
            m.para_emoji_count: self.PARA.compute_total_emoji_raw_count(input_text)["Emoji_Count"],
            m.para_emoji_index: self.PARA.compute_total_emoji_count(input_text)["Emoji_Index"],
            m.para_emoticon_index: self.PARA.compute_total_emoticon_count(input_text)["Emoticon_Index"],

            # Preserve the original commentContent for merging
            "commentContent": input_text
        }
        return data