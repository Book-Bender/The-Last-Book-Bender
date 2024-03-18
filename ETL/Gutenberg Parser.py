import csv
import os
import random
import re
import string
import unicodedata

import nltk
import requests
from bs4 import BeautifulSoup
from nltk.corpus import stopwords

nltk.download("punkt")
nltk.download("stopwords")

# URL of the website source for books from the Gutenberg project
base_url = "http://aleph.gutenberg.org/"


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

    # Remove single-character words and words with a single character on either side of a hyphen
    words = text.split()
    filtered_words = [
        word for word in words if not all(char == "-" for char in word)
    ]  # Remove words that only contain hyphens
    text = " ".join(filtered_words)

    return text


# Read the numeric subdirectories from books.csv (skipping the first line)
with open("books.csv", "r", encoding="utf-8") as file:
    csv_reader = csv.reader(file)
    next(csv_reader)  # Skip the header line
    book_data = [row[2] for row in csv_reader]  # Extract the subdirectory

# Create directories to store the downloaded files
original_dir = "original_books"
processed_dir = "processed_books"
os.makedirs(original_dir, exist_ok=True)
os.makedirs(processed_dir, exist_ok=True)

# Take a random sample of 1000 items from book_data to ensure diversity
sample_size = 1000
sampled_book_data = random.sample(book_data, sample_size)

processed_count = 0  # Counter for successfully processed files

# Iterate over each book
for subdir in sampled_book_data:
    # Construct the URL for the subdirectory
    subdir_parts = [
        char for char in subdir[:-1]
    ]  # Split the subdirectory into individual digits (except the last)
    subdir_url = base_url + "/".join(subdir_parts) + "/" + subdir + "/"

    # Send a GET request to the subdirectory URL, and parse the HTML content
    response = requests.get(subdir_url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Check if any link in the subdirectory contains "mp3" thus avoiding downloading audio files
    mp3_link = soup.find("a", href=lambda href: href and "mp3" in href.lower())

    if mp3_link:
        print(f"Skipping subdirectory: {subdir} (Contains 'mp3' folder)")
        continue

    # Find the first link to a txt file in the subdirectory
    txt_link = soup.find("a", href=lambda href: href and href.endswith(".txt"))

    if txt_link:
        file_name = txt_link["href"]
        file_url = subdir_url + file_name

        # Send a GET request to download the file
        file_response = requests.get(file_url)
        file_content = file_response.text

        # Check if "Language: English" is present in the file content
        if re.search(r"Language: English", file_content):
            # Extract the author using regex
            author_match = re.search(r"Author: (.+)", file_content)
            author = author_match.group(1).strip() if author_match else ""

            # Extract the title using regex
            title_match = re.search(r"Title: (.+)", file_content)
            title = title_match.group(1).strip() if title_match else ""

            # Save the original file with the title and author name
            original_file_name = f"{normalize_text(title)}-{normalize_text(author)}.txt"
            original_file_path = os.path.join(original_dir, original_file_name)
            with open(original_file_path, "w", encoding="utf-8-sig") as file:
                file.write(file_content)

            # Normalize the text and tokenize into words
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
                    processed_content = " ".join(
                        selected_words
                    )  # Join the selected words back into text
                else:
                    # Join the filtered words back into text
                    processed_content = " ".join(filtered_words)
            else:
                # Join the normalized words back into text
                processed_content = " ".join(words)

            # Save the processed file with reduced word count
            processed_file_name = (
                f"{os.path.splitext(file_name)[0]}-{title}-{author}.txt"
            )
            processed_file_path = os.path.join(processed_dir, processed_file_name)
            with open(processed_file_path, "w", encoding="utf-8-sig") as file:
                file.write(processed_content)

            processed_count += (
                1  # Increment the counter for successfully processed files
            )
            print(f"Downloaded and processed: {file_name}")
        else:
            print(f"Skipping file: {file_name} (Language is not English)")
    else:
        print(f"No .txt file found in subdirectory: {subdir}")

    if processed_count >= sample_size:
        break  # Stop downloading and processing once the desired sample size is reached

# Combine all processed files into a single file
combined_file_path = "combined_processed_files.txt"

with open(combined_file_path, "w", encoding="utf-8-sig", newline="") as combined_file:
    combined_file.write(
        "book_id,author,title,content,\n"
    )  # Write the first line with column names

    for file_name in os.listdir(processed_dir):
        file_path = os.path.join(processed_dir, file_name)
        with open(file_path, "r", encoding="utf-8-sig") as file:
            processed_text = file.read()

        base_name = os.path.splitext(file_name)[0]
        # title, author = base_name.split("-")[-2:-1]

        # Extract the numeric book_id from the base_name
        book_id = "".join(filter(str.isdigit, base_name))

        # If the book_id is empty, use the original base_name
        if not book_id:
            book_id = base_name

        combined_file.write(f"{book_id},{author},{title},{processed_text},\n")
        combined_file.write("\n")  # Add a blank line between each processed file

print("Download, processing, and combining completed.")
