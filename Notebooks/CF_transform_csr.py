# script for transforming rating matrix
# after this, invoking knn with option l2 or euclidean (same thing) will get desired metric
import time

import numpy as np
import scipy as sp


# function names starting with make mutates the coo_matrix passed in
def make_mean_0(X: sp.sparse.coo_matrix, axis=0) -> None:
    """
    if axis=0, make each column (user) have mean 0
    with zero entries unmodified
    (this function mutates the underlying coo matrix)
    careful that sparsity might increase in this step
    """
    indexer = [X.row, X.col][1 - axis]
    v = np.array(X.sum(axis=axis)).flatten()
    c = np.bincount(indexer)
    X.data -= v[indexer] / np.maximum(c[indexer], 0.5)


def make_norm_1(X: sp.sparse.coo_matrix, axis=0) -> None:
    """
    if axis=0, make each column have 2-norm 1
    with zero entries unmodified
    assumes things smaller than 1e-40 are 0 (dataset-dependent)
    (this function mutates the underlying coo matrix)
    """
    indexer = [X.row, X.col][1 - axis]
    v = np.sqrt(np.array(X.power(2).sum(axis=axis)).flatten())
    X.data /= np.maximum(10 ** (-60), v[indexer])


def make_dilate(X: sp.sparse.coo_matrix, amount: float) -> None:
    """
    make each nonempty entry of X - a
    (this mutates the underlying coo matrix)
    for example, take a as baseline.
    """
    X.data -= np.float64(amount)


def make_standardize(X: sp.sparse.coo_matrix, axis=0) -> None:
    """
    x - mu / sigma
    if axis=0, this is for each column
    """
    make_mean_0(X, axis=axis)
    make_norm_1(X, axis=axis)


def make_pearson(X: sp.sparse.coo_matrix, axis=0) -> None:
    """
    prep for pearson
    pdist after pearson gives pearson
    same as make_mean_0
    """
    make_mean_0(X, axis=axis)


def make_pearson_inv_freq(X: sp.sparse.coo_matrix, axis=0) -> None:
    """
    prep for pearson with inverse item/user frequency
    (although it doesn't make too much sense for inverse user frequency)
    theoretically this will increase recommendation of new items
    (higher weight for less-read item)
    (see aggarwal's textbook)
    similar to inverse document frequency
    """
    indexer = [X.row, X.col][1 - axis]
    c = np.bincount(indexer)
    make_pearson(X, axis=axis)
    X.data /= np.maximum(c[indexer], 0.5)


def make_cosine(X: sp.sparse.coo_matrix, axis=0) -> None:
    """
    prep for cosine similarity
    the same as make norm 1
    """
    make_norm_1(X, axis=axis)


# function names starting with test are used to reality check the make functions
def test_mean_is_0(X: sp.sparse.coo_matrix, axis=0, tol=10 ** (-10)) -> np.bool_:
    """
    for axis=0, test if each mu=0
    should be true on outputs of make_mean_0
    """
    return np.abs(np.array(X.sum(axis=axis))).max() < tol


def test_norm_is_1(X: sp.sparse.coo_matrix, axis=0, tol=10 ** (-10)) -> np.bool_:
    """
    for axis=0, test if each has norm=1 or 0
    should be true on outputs of make_norm_1
    """
    v = np.sqrt(np.array(X.power(2).sum(axis=axis)))
    return np.all(np.minimum(v, np.abs(1 - v)) < tol)


# load ratings csr matrix
load_time_start = time.time()
book_sparse = sp.sparse.load_npz("../Data/Raw/ratings.npz")
print(f"load_time (npz): {time.time() - load_time_start} seconds")

# convert to coo
convert_time_start = time.time()
book_coo = book_sparse.astype(np.float64).tocoo()
print(f"coo_conversion and type_cast time: {time.time() - convert_time_start} seconds")

# example transform using dilate function
# baseline chosen to be 2.75 to make ratings of 1, 2 negative and 3, 4, 5 positive
# axis=0 targets users
transform_time_start = time.time()
make_dilate(book_coo, amount=2.75)
make_standardize(book_coo, axis=0)
# test if things are going correctly
print(f"Test mean is 0 among axis={0}: {test_mean_is_0(book_coo)}")
print(f"Test norm is 1 among axis={0}: {test_norm_is_1(book_coo)}")
print(f"coo_transformation time: {time.time() - transform_time_start} seconds")

# convert to csr
convert_time_start = time.time()
book_sparse = book_coo.tocsr()
print(f"csr_conversion time: {time.time() - convert_time_start} seconds")

# save results to npz file
save_time_start = time.time()
sp.sparse.save_npz("../Data/Raw/ratings_transformed.npz", book_sparse)
print(f"save_time: {time.time() - save_time_start} seconds")
