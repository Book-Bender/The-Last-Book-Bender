# The-Last-Book-Bender-ETL 

## Dataset

We will be using the `good-books-10k-extended` [dataset](https://github.com/malcolmosh/goodbooks-10k-extended), and the `gutenberg` [datasets](http://aleph.gutenberg.org/).

The `good-books-10k-extended` has about 50k users, 10k books, 6M ratings.

## ETL 
1. For storing our files on cloud- we have used two approaches
   a. Google Drive
   b. GCP Bucket
2. We have used the files stored on our drive to run the code.
3. We have given the necessary permissions to all our team members to run the code on Google Drive .

## Path 
This is the path to Google Drive repo
/content/drive/MyDrive/CSE6242_project/

This is the path to our GCP bucket
gs://team054/

## Running the code
While running the code, we need to mount the drive . The code to implement this included in the BERT ETL final file.

## Files added in repository
a. books_enriched.csv (this is the Goodreads dataset)
b. combined_processed_files.txt (this is the Glutenberg file)
c. embeddings_pd_json.json (These are the embeddings we created)
