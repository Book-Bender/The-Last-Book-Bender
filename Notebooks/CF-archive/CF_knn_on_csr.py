import time

import numpy as np
import scipy as sp
from matplotlib import pyplot as plt
from sklearn.neighbors import NearestNeighbors

# fit model
book_sparse_all = sp.sparse.load_npz("../Data/Raw/ratings.npz").astype(np.float64)
book_sparse_train = sp.sparse.load_npz("../Data/Raw/ratings_train.npz").astype(
    np.float64
)
book_sparse_test = sp.sparse.load_npz("../Data/Raw/ratings_test.npz").astype(np.float64)
book_sparse_transformed_train = sp.sparse.load_npz(
    "../Data/Raw/ratings_train_transformed.npz"
)
book_sparse_transformed_test = sp.sparse.load_npz(
    "../Data/Raw/ratings_test_transformed.npz"
)


true_shape = book_sparse_all.shape
book_sparse_transformed_test.resize(true_shape)
book_sparse_transformed_train.resize(true_shape)

n_neighbors = 5

model = NearestNeighbors(metric="cosine", n_neighbors=n_neighbors)
model.fit(book_sparse_transformed_train.transpose())
# model.fit(book_sparse_transformed_train)

predict_time = time.time()
distances, suggestions = model.kneighbors(book_sparse_transformed_test.transpose())
# distances, suggestions = model.kneighbors(book_sparse_transformed_test)
print(f"predict_time: {time.time() - predict_time} seconds")

# predict ratings: this is used to evaluate performance

# formula: for user u in train, N_u the nbd of u (given by knn), i an item
#   then we predict: u rates item i with mu_u + A / B
#   where B is sum of |sim(u, v)| for v in N_u
#   and A is sum of sim(u, v)(r_uv - mu_v)
# here we predict only on things with ground truth
#   that is: if u does not have rating for i, we don't predict for that
# note that cosine distance function is 1 - u.v/|u||v|,
#   so sim(u, v) is 1 - dist(u, v)
# however, due to sparsity issue, B might be sparse
#   especially if we do CF on users (too many users)
# in this case A is also zero, so the rating is mu_u

mu = book_sparse_all.mean(axis=0)
sim = 1 - distances

book_sparse_test_coo = book_sparse_test.tocoo()
row, col, data = (
    book_sparse_test_coo.row,  # item
    book_sparse_test_coo.col,  # user
    book_sparse_test_coo.data,
)

print(mu)
print(mu.shape)

err = 0
k = 0
for i, u, d in zip(row, col, data):
    k += 1
    print(k)
    pred = mu[u]
    base = d
    B = np.max(np.sum(np.abs(sim[u, :])), 10 ** (-30))
    A = 0
    for _ in range(n_neighbors):
        v = sim[u, _]
        A += sim[i, u] * (book_sparse_transformed_train[i, v] - mu[v])
    err += np.abs(base + A / B - pred)

print(err)
