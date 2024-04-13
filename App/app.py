from flask import Flask

import pickle
import numpy as np
import torch
import pandas as pd
import transformers as ppb

app = Flask(__name__)


@app.route("/")
def bert_knn_recommendation():
    knn_model = pickle.load(open('Models/BERT-KNN.pkl', 'rb'))

    model_class, tokenizer_class, pretrained_weights = (ppb.BertModel, ppb.BertTokenizer, 'bert-base-uncased')
    query = 'I want a book similar to Harry Potter, with wizards and magic'

    # Load pretrained model/tokenizer
    tokenizer = tokenizer_class.from_pretrained(pretrained_weights)
    model = model_class.from_pretrained(pretrained_weights)
    tokenized = tokenizer.encode(str(query), add_special_tokens=True)

    max_len = 256
    padding = [0] * (max_len - len(tokenized))
    padded = np.array(tokenized + padding)
    attention_mask = np.where(padded != 0, 1, 0)

    device = torch.device('cpu')

    input_ids = torch.tensor(padded).unsqueeze_(0).to(device)
    attention_mask = torch.tensor(attention_mask).unsqueeze_(0).to(device)
    model = model.to(device)

    with torch.no_grad():
        last_hidden_states = model(input_ids, attention_mask=attention_mask)

    query_embeddings = last_hidden_states[0].cpu().data[:, 0, :].numpy()

    distances, indices = knn_model.kneighbors(query_embeddings)

    embeddings_pd_df = pd.read_json("Data/Embeddings/bert-embeddings-10k-small.json")
    i = 0
    k = 5
    recommendations = ""
    for book_rec in indices:
        j = 0
        recommendations += f"Top {k} recommendations for query {i}:"
        for index in book_rec:
            recommendations += f"\t{j}. {embeddings_pd_df.iloc[index]['title']}, score={distances[i][j]}"
            j += 1
        i += 1

    return recommendations
