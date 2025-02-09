import os
import emoji
import pandas as pd

class EmojiAnalysis:
    def __init__(self, master_file):
        self.master_df: pd.DataFrame = master_file.df
        self.master_file_path = master_file.master_file_path


    def extract_emoji_from_master(self):
        master_df = self.master_df

        post_fullnames = master_df['postFullname'].to_list()

        # analyze each posts emojis, then put them as a flattened list in the master file
        emoji_dict = {}

        for full_name in post_fullnames:
            emoji_list = self.analyze_emoji_in_posts(full_name)
            flattened_emoji_list =  [item for sub_list in emoji_list for item in sub_list]
            emoji_dict[full_name] = flattened_emoji_list

        master_df['postEmojis'] = master_df['postFullname'].apply(lambda full_name: emoji_dict[full_name])
        
        master_df.to_csv(self.master_file_path, index=False)


    def analyze_emoji_in_posts(self, fullname):
        file_dir = os.path.dirname(os.path.abspath(__file__))
        csv_folder = 'data'
        folder_path = os.path.join(file_dir, csv_folder)
        file_path = os.path.join(folder_path, f'{fullname}.csv')

        df = pd.read_csv(file_path)
        df['commentEmojis'] = df['commentContent'].apply(lambda content: self.extract_emojis(content))
        df.to_csv(file_path, index=False)

        return df['commentEmojis'].to_list()
    

    def extract_emojis(self, text):
        # This function uses the emoji library to extract emojis from the given text.
        return [char for char in text if emoji.is_emoji(char)]



    def print_emojis(self, text):
        # Example text or thread (you can replace this with the thread content)


        # Extract emojis from the text
        emojis = self.extract_emojis(text=text)

        # Read out the emojis
        if emojis:
            print("Emojis found:", emojis)
        else:
            print("No emojis found.")

    if __name__ == "__main__":
        print_emojis("Hello! 😊 How are you? 🤔 Let's party! 🎉")