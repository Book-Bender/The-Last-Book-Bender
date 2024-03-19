# this script converts ratings.csv to a csr matrix and save as an npz object
import time

import pandas as pd
import scipy as sp


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


def density(
    df: pd.DataFrame, row_key: str = "book_id", col_key: str = "user_id"
) -> float:
    """
    Computes density of user-item matrix
        (number of nonzero entries / number of all entries)
    Assuming that the max of user_id, book_id are
    """
    return df.shape[0] / df[[row_key, col_key]].max().product()


def df_to_csr(
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
    return sp.sparse.coo_matrix((df[val_key], (df[row_key], df[col_key]))).tocsr()


# load csv
load_time_start = time.time()
ratings_df = load_ratings("../Data/Raw/ratings.csv")
print(f"load_time (csv): {time.time() - load_time_start} seconds")
print(f"density of array: {density(ratings_df)}")

# convert to sparse
convert_time_start = time.time()
book_sparse = df_to_csr(ratings_df)
print(f"convert_time (w/o pivot): {time.time() - convert_time_start} seconds")

# save csr to npz
save_time_start = time.time()
sp.sparse.save_npz("../Data/Raw/ratings.npz", book_sparse)
print(f"save_time: {time.time() - save_time_start} seconds")

# model = NearestNeighbors(algorithm="brute")  ## model
# model.fit(book_sparse)
#
# distances, suggestions = model.kneighbors(book_pivot.iloc[4, :].values.reshape(1, -1))
# for i in range(len(suggestions)):
#     print(book_pivot.index[suggestions[i]])
