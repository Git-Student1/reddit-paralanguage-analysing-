import emoji


def extract_emojis(text):
    # This function uses the emoji library to extract emojis from the given text.
    return [char for char in text if emoji.is_emoji(char)]



def print_emojis(text):
    # Example text or thread (you can replace this with the thread content)


    # Extract emojis from the text
    emojis = extract_emojis(text=text)

    # Read out the emojis
    if emojis:
        print("Emojis found:", emojis)
    else:
        print("No emojis found.")

if __name__ == "__main__":
    print_emojis("Hello! 😊 How are you? 🤔 Let's party! 🎉")