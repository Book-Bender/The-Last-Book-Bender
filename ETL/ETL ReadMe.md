# The-Last-Book-Bender-ETL 

## Dataset

We will be using the `good-books-10k-extended` [dataset](https://github.com/malcolmosh/goodbooks-10k-extended), and the `gutenberg` [datasets](http://aleph.gutenberg.org/).

The `good-books-10k-extended` has about 50k users, 10k books, 6M ratings.

## ETL 
1. For storing our files on cloud- we have used two approaches
   a. Google Drive
   b. GCP Bucket- We hit our lmits and moreover as a team we decided to use Collab so using drive was an easier option though we have our bucket still set         up.
2. We have used the files stored on our drive to run the code. bert_ETL_gutenberg_goodreads.ipynb is our final code.
3. We have given the necessary permissions to all our team members to run the code on Google Drive .

## Path 
This is the path to Google Drive repo
/content/drive/MyDrive/CSE6242_project/

This is the path to our GCP bucket
gs://team054/

## Running the code
While running the code, we need to mount the drive . The code to implement this is included in  **bert_ETL_gutenberg_goodreads.ipynb** file.

## Files added in repository
a. books_enriched.csv (this is the Goodreads dataset)
b. combined_processed_files.txt (this is the Glutenberg file)
c. embeddings_pd_json.json (These are the embeddings we created)
d. knn_model.pkl (pckled file)




