import bz2
import pickle
import _pickle as cPickle

import numpy as np
import scipy as sp
from sklearn.neighbors import NearestNeighbors
import torch
import transformers as ppb
from flask import Flask, jsonify
from flask.helpers import send_from_directory
from flask_cors import CORS, cross_origin
from data.cf.cf_model import cf_model

# data
titles = np.array(pickle.load(open("data/titles.pkl", "rb")))

embeddings = np.vstack([np.load(open(f"data/embeddings_{_}.npy", "rb")) for _ in range(6)])
ratings = sp.sparse.load_npz(open("data/ratings_for_sample.npz", "rb"))

# models
knn_model = NearestNeighbors(n_neighbors=7, algorithm="ball_tree").fit(embeddings)
# knn_model = cPickle.load(bz2.BZ2File("data/knn_model_compress.pkl.pbz2", "rb"))
# knn_model = cPickle.load(bz2.BZ2File("data/test_knn.pkl.pbz2", "rb"))
# knn_model = pickle.load(open("data/BERT-KNN.pkl", "rb"))
knn_model.radius = None

cf_model = cf_model()
bert_model_class, bert_tokenizer_class, bert_pretrained_weights = (
    ppb.BertModel,
    ppb.BertTokenizer,
    "bert-base-uncased",
)
bert_tokenizer = bert_tokenizer_class.from_pretrained(bert_pretrained_weights)
bert_model = bert_model_class.from_pretrained(bert_pretrained_weights)

app = Flask(__name__, static_folder="dist", static_url_path="")
CORS(app)


@app.route("/")
def serve():
    return send_from_directory(app.static_folder, "index.html")


@app.route("/api/cbf/<query>", methods=["GET"])
@cross_origin()
def bert_knn_recommendation(query):
    # Load pretrained models and data
    device = torch.device("cpu")

    # Load pretrained BERT/tokenizer
    tokenizer = bert_tokenizer
    model = bert_model

    # Tokenize query
    query = " ".join(query.split(" ")[:256])  # get the first 256 words
    tokenized = tokenizer.encode(query, add_special_tokens=True)

    max_len = len(tokenized)
    padding = [0] * (max_len - len(tokenized))
    padded = np.array(tokenized + padding)
    attention_mask = np.where(padded != 0, 1, 0)

    # Embed query with BERT
    input_ids = torch.tensor(padded).unsqueeze_(0).to(device)
    attention_mask = torch.tensor(attention_mask).unsqueeze_(0).to(device)
    model = model.to(device)

    with torch.no_grad():
        last_hidden_states = model(input_ids, attention_mask=attention_mask)

    query_embeddings = last_hidden_states[0].cpu().data[:, 0, :].numpy()

    # Compute KNN scores and fill up the response JSON
    data = {}
    k = 7
    distances, indices = knn_model.kneighbors(query_embeddings, n_neighbors=k)

    i = 0
    for book_rec in indices:
        j = 0
        for index in book_rec:
            data[j] = {
                "title": titles[index],
                "score": distances[i][j],
                "pandas_index": str(index),
            }
            j += 1

    # Return payload
    return jsonify(data)


@app.route("/api/cf/<query>", methods=["GET"])
@cross_origin()
def cf_recommendation(query):
    # Query is just a user index
    # Load pretrained models and data
    model = cf_model
    k = 200  # size of neighbors to detect from
    m = 7  # number of recommendations that we want
    opts = {"context": int(query), "k": k, "m": m}

    # Compute KNN scores and fill up the response JSON
    res = model.get_top_m_recs_k_neighbors(**opts)
    incs = [r[0] for r in res]
    inds = [r[1] for r in res]
    return jsonify(
        [
            {"score": inc, "pandas_index": str(ind), "title": str(titles[ind])}
            for inc, ind in zip(incs, inds)
        ]
    )


@app.route("/api/cbf_lib/<book_id>", methods=["GET"])
@cross_origin()
def bert_knn_recommendation_from_library(book_id):
    # Compute KNN scores and fill up the response JSON
    data = {}
    query = np.expand_dims(embeddings[int(book_id), :], 0)
    k = 7
    distances, indices = knn_model.kneighbors(query, n_neighbors=k)
    i = 0
    recommendations = ""
    for book_rec in indices:
        j = 0
        recommendations += f"Top {k} recommendations for query {i}:"
        for index in book_rec:
            if str(index) != str(book_id):
                data[j] = {
                    "title": titles[index],
                    "score": distances[i][j],
                    "pandas_index": str(index),
                }
            j += 1
    # Return payload
    return jsonify(data)


@app.route("/api/sample_users", methods=["GET"])
@cross_origin()
def sample_users():
    # randomly sample 9 users
    k = 9
    m = ratings.shape[1]
    cols = np.random.randint(1, m, k)
    ratings_coo = ratings[:, cols].tocoo()
    return jsonify(
        result=[
            {
                "u": str(i),
                "b": j,
                "r": str(k),
            }
            for i, j, k in zip(
                cols[ratings_coo.col], titles[ratings_coo.row], ratings_coo.data
            )
        ]
    )


if __name__ == "__main__":
    app.run(debug=True)
