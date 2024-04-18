# The-Last-Book-Bender

# About
The Last Book Bender is our book recommendation system that seeks to inspire a love for reading. Our goal is to create a welcoming environment where individuals of all ages and backgrounds can discover enriching literary experiences tailored to their interests and aspirations. With the proliferation of attention-grabbing sources of entertainment, our aim is to sustain peoples' passion for reading by facilitating the discovery of their next book and ensure that it is a page turner. Our objective is to develop and visualize a book recommendation system that suggests books to read by comparing content and using machine learning techniques.

Our team found ways to enhance current methods by employing larger datasets and algorithms customized for the Goodreads rating scale. Through implementing BERT embeddings and a collaborative filtering algorithm optimized for a 1 to 5 scale, we created a more accurate book recommendation system tailored to user queries. Our project promotes new discoveries in the literary world for readers and bolsters engagement in libraries. With a focus on accessibility and scalability, we seek to establish a cost-effective approach for wider adaptation of our application.

# Setup
## Conda and Requirements
    conda create --name DVA_Final python=3.9 \
    conda activate DVA_Final \
    pip install -r App/requirements.txt

# Flask Application
Run `flask --app App/app run`

## Dataset

We will be using the `good-books-10k-extended` [dataset](https://github.com/malcolmosh/goodbooks-10k-extended), and the `Gutenberg Project` [datasets](http://aleph.gutenberg.org/).

The `good-books-10k-extended` has about 50k users, 10k books, 6M ratings. The Guteberg Project includes over 70,000 ebooks, and you can read more about their work here: https://www.gutenberg.org/

The good-books dataset is available for immediate download, while the Gutenberg dataset takes a bit more time and effort. 

We developed a simple script, "Gutenberg Parser.py" to scrape the books, apply basic filters to remove audio books and non-Enlgish language books.
The script was also used to transform the data, choosing a few fields, and condesing the content of th ebooks into a 512 word normalized sample, usable with BERT.
You are welcome to remove block comments at line 60 to execute a short run for testing. There is one additional block comment at line 180/181 to remove, in that case. 

We developed also a simple collaborative filtering model based on the `good-books-10k-extended` dataset. The model is given in `Notebooks/cf_model.py`, the initialization data (processed user-item matrix, with rows indexed by `book_id`, columns indexed by `user_id`, is given in `Data/Raw/ratings_for_cf.npz`. The metrics we chose to use is an approximate version of the adjusted cosine similarity, based on an 10-fold CV we ran testing with different metrics (other metrics are the basic cosine similarity paired with rating remapping methods or fixed baseline adjustments).

## Visualizations and Interactivities
