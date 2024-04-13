from flask import Flask, render_template, jsonify
from flask_cors import CORS

import pickle
import numpy as np
import torch
import pandas as pd
import transformers as ppb

app = Flask(__name__)
CORS(app)


@app.route("/")
def content_based_recommendation():
    return render_template('content_recommendation.html')


@app.route("/recommend/<query>", methods=['GET'])
def bert_knn_recommendation(query):
    # Load pretrained models and data
    device = torch.device('cpu')
    embeddings_pd_df = pd.read_json("Data/Embeddings/bert-embeddings-10k-small.json")
    knn_model = pickle.load(open('Models/BERT-KNN.pkl', 'rb'))
    model_class, tokenizer_class, pretrained_weights = (ppb.BertModel, ppb.BertTokenizer, 'bert-base-uncased')

    # Load pretrained BERT/tokenizer
    tokenizer = tokenizer_class.from_pretrained(pretrained_weights)
    model = model_class.from_pretrained(pretrained_weights)

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
    distances, indices = knn_model.kneighbors(query_embeddings)
    i = 0
    k = 5
    recommendations = ""
    for book_rec in indices:
        j = 0
        recommendations += f"Top {k} recommendations for query {i}:"
        for index in book_rec:
            data[j] = {
                "title": embeddings_pd_df.iloc[index]['title'],
                "score": distances[i][j]
            }
            j += 1

    # Return payload
    return jsonify(data)
