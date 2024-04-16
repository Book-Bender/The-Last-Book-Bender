import string
import unicodedata
import pandas as pd

import nltk
from nltk.corpus import stopwords
from ast import literal_eval

nltk.download("punkt")
nltk.download("stopwords")

# Read the CSV file from the URL
base2_url = "https://raw.githubusercontent.com/malcolmosh/goodbooks-10k/master/books_enriched.csv"
good_books_df = pd.read_csv(base2_url, index_col=[0], converters={"genres": literal_eval})

# Select the desired columns
df = good_books_df[['authors', 'title', 'average_rating', 'description']]

# Function to normalize text
def normalize_text(text):
    text = text.lower()  # Convert to lowercase
    text = text.translate(
        str.maketrans("", "", string.punctuation)
    )  # Remove punctuation except hyphens
    text = text.translate(str.maketrans("", "", string.digits))  # Remove digits
    text = (
        unicodedata.normalize("NFKD", text)
        .encode("ASCII", "ignore")
        .decode("utf-8-sig")
    )  # Normalize Unicode characters

    # Remove words that consist of only hyphens
    words = text.split()
    filtered_words = [
        word for word in words if not all(char == "-" for char in word)
    ]
    text = " ".join(filtered_words)

    return text

# Capitalize the first letter of each word in 'title' and 'authors' columns
df['title'] = df['title'].str.title()
df['authors'] = df['authors'].str.title()

# Iterate over each row and process the description
new_df = []
for index, row in df.iterrows():
    file_content = row['description']

    # Check if the description field is not null and not empty
    if isinstance(file_content, str) and file_content.strip():
        normalized_text = normalize_text(file_content)
        words = nltk.word_tokenize(normalized_text)

        # Check if the file has more than 512 words, the limit for BERT
        if len(words) > 512:
            # Remove common words
            stop_words = set(stopwords.words("english"))
            filtered_words = [
                word for word in words if word.lower() not in stop_words
            ]

            # Check if the file still has more than 512 words
            if len(filtered_words) > 512:
                middle_index = (
                    len(filtered_words) // 2
                )  # Find the middle word index
                selected_words = filtered_words[
                    max(0, middle_index - 256) : middle_index + 256
                ]  # Take 256 words on either side of the middle word
                df.at[index, 'description'] = " ".join(
                    selected_words
                )  # Join the selected words back into text
            else:
                # Join the filtered words back into text
                df.at[index, 'description'] = " ".join(filtered_words)
        else:
            # Join the normalized words back into text
            df.at[index, 'description'] = " ".join(words)

# Save the DataFrame to a local CSV file
df.to_csv('Data/good-reads-10k-transformed.txt', index=False)
