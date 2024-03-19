# modified from parts of the collaborative_filtering_alt.ipynb
import time

import numpy as np
import pandas as pd
import scipy as sp
from sklearn.neighbors import NearestNeighbors


def load_ratings(
    fp_ratings: str = "../Data/ratings.csv",
    seed: int = 6242,
    sample_size: None | int = None,
    fraction: None | int = None,
) -> pd.DataFrame:
    """
    fp_ratings: file path to ratings, might depend on where you call your script
        and where you place your ratings.csv
    seed: controls numpy random
    sample_size, fraction: options to pass for pd.DataFrame.sample (one of them as to be none)
        if both none, returns the full ratings dataframe
    """
    ratings_df = pd.read_csv(
        filepath_or_buffer=fp_ratings,
        dtype={"user_id": "Int32", "book_id": "Int16", "rating": "Int8"},
    )
    if sample_size is None and (fraction is None or fraction == 1):
        return ratings_df
    sampled_user_ids = (
        ratings_df["user_id"]
        .drop_duplicates()
        .sample(n=sample_size, frac=fraction, random_state=seed, replace=False)
    )
    return ratings_df.merge(sampled_user_ids, on="user_id")


def csr_data_len(m):
    """
    prints lenghts of data (data, indptr, indices) of a csr_matrix
    """
    print(len(m.data), len(m.indptr), len(m.indices))


def df_to_csr_nopivot(
    df: pd.DataFrame,
    row_key: str = "book_id",
    col_key: str = "user_id",
    val_key: str = "rating",
):
    """
    constructs csr matrix from df
    this implementation does not call the pivot_table
    df: the df to convert
    row_key, col_key, val_key: name of columns in df defining the coo matrix
        (that will be used to convert to csr)

    this implementation does not call the pivot_table
    however, for moderate amount of users,
    this implementation consumes more memory
    (possible reason: number of empty columns)
    """
    # convert df to sparse and
    return sp.sparse.coo_matrix((df.rating, (df.book_id, df.user_id))).tocsr()


def df_to_csr_pivot(
    df: pd.DataFrame,
    row_key: str = "book_id",
    col_key: str = "user_id",
    val_key: str = "rating",
):
    """
    constructs csr matrix from df
    this implementation uses pivot_table
    df: the df to convert
    row_key, col_key, val_key: name of columns in df defining the coo matrix
        (that will be used to convert to csr)
    this implementation calls the pivot_table
    """
    book_pivot = df.pivot_table(columns=col_key, index=row_key, values=val_key)
    book_pivot.fillna(0, inplace=True)
    return sp.sparse.csr_matrix(book_pivot.astype(float))


load_time_start = time.time()
ratings_df = load_ratings("../Data/Raw/ratings.csv", sample_size=5000)
print(f"load_time: {time.time() - load_time_start} seconds")

convert_time_start = time.time()
book_sparse = df_to_csr_nopivot(ratings_df)
print(f"convert_time (w/o pivot): {time.time() - convert_time_start} seconds")
csr_data_len(book_sparse)

convert_time_start = time.time()
book_sparse = df_to_csr_pivot(ratings_df)
print(f"convert_time (w pivot): {time.time() - convert_time_start} seconds")
csr_data_len(book_sparse)


# model = NearestNeighbors(algorithm="brute")  ## model
# model.fit(book_sparse)
#
# distances, suggestions = model.kneighbors(book_pivot.iloc[4, :].values.reshape(1, -1))
# for i in range(len(suggestions)):
#     print(book_pivot.index[suggestions[i]])
