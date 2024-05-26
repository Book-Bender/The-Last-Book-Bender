import numpy as np
import scipy as sp


class cf_model:
    def __init__(self, fp, fname):
        """
        assumes ratings data has users ratings shifted by means
        here mat has rows the books, columns the users.
        """
        self.mat = sp.sparse.load_npz(fp + fname)
        self.norms = np.sqrt(np.array(self.mat.power(2).sum(axis=0))).flatten()
        self.n_books, self.n_users = self.mat.shape

    def _context_to_vec(self, context):
        """
        utility. for transforming context into np array or scipy csc.
        """
        if type(context) not in [
            sp.sparse._csc.csc_matrix,
            sp.sparse._csr.csr_matrix,
            sp.sparse._coo.coo_matrix,
            np.ndarray,
            list,
            tuple,
            dict,
            int,
        ]:
            raise NotImplementedError("type not supported.")
        if type(context) is int:
            return self.mat[:, context]
        if type(context) in [sp.sparse._csr.csr_matrix, sp.sparse._coo.coo_matrix]:
            context = context.tocsc()
        if type(context) is np.ndarray:
            context = sp.sparse.csc_matrix(context)
        if type(context) is sp.sparse._csc.csc_matrix:
            if context.shape[0] == 1:
                context = context.transpose().tocsc()
            return context
        if len(context) == 0:
            vec = sp.sparse.csc_matrix(0)
            vec.resize((self.n_books, 1))
            return vec
        if type(context) is dict:  # assumes the form {book_id: rating}
            context = list(context.items())
        n = len(context)
        return sp.sparse.csc_matrix(
            (
                np.array([t[1] for t in context]),  # data
                (
                    np.array([t[0] for t in context]).astype(int),
                    np.zeros(n).astype(int),  # columns
                ),
            )
        )

    def _get_mean(self, context_vec):
        """
        utility. assumes context_vec is scipy sparse csc matrix or np array
        """
        if type(context_vec) is np.ndarray:
            return context_vec.mean()
        if type(context_vec) is sp.sparse._csc.csc_matrix:
            return context_vec.data.sum() / len(context_vec.data)

    def _process_context(self, context_vec):
        """
        utility. assumes context_vec is scipy sparse csc matrix or np array
        """
        mu = self._get_mean(context_vec)
        if type(context_vec) is np.ndarray:
            # center by mean
            supp = context_vec != 0
            context_vec[supp] = context_vec[supp] - mu + 10 ** (-8)
            # normalize
            s2 = (context_vec**2).sum()  # sum of elements squared
            context_vec[supp] = context_vec[supp] / np.sqrt(s2)
            return context_vec
        if type(context_vec) is sp.sparse._csc.csc_matrix:
            # center by mean
            context_vec.data = context_vec.data - mu + 10 ** (-8)
            # normalize
            s2 = (context_vec.data**2).sum()
            context_vec.data = context_vec.data / np.sqrt(s2)
            return context_vec

    def _top_k_neighbors(self, context, k=50):
        """
        get top k indices given context_vec;
        assumes context_vec is context processed by _process_context.
        """
        context_vec = self._process_context(self._context_to_vec(context))
        if (
            np.prod(context_vec.shape) != self.n_books
        ):  # otherwise would raise dimension mismatch
            context_vec.resize((self.n_books, 1))
        # the following inevitably a dense vector
        sim_scores = (self.mat.T @ context_vec).toarray().flatten() / np.maximum(
            self.norms, 10 ** (-30)
        )
        neighbors = np.argpartition(sim_scores, -k)[
            -k:
        ]  # note: this returns top k; needn't be sorted for better performance
        sim_scores = sim_scores[neighbors]
        return neighbors, sim_scores

    def _get_scores(self, context, k=50):
        """
        using the approximate formula for better vectorization; use nonnormalized
        """
        neighbors, sim_scores = self._top_k_neighbors(context, k=k)
        submat = self.mat[
            :, neighbors
        ].toarray()  # retrieve rating records of these neighbors
        numer = submat * sim_scores
        denom = (submat > 0) * sim_scores
        scores = numer.sum(axis=1) / np.maximum(denom.sum(axis=1), 10 ** (-30))
        return scores

    def get_top_m_recs_k_neighbors(self, context, k=50, m=100):
        """
        grabs top m books.
        if context is int, treated as an user_id;
        if context is scipy sparse array, np ndarray, dict, list/tuple of list/tuple
            treated as a rating vector.
        """
        scores = self._get_scores(context, k=k)
        top_m_inds = np.argpartition(scores, -m)[-m:]
        top_m_scores = scores[top_m_inds]
        return sorted(zip(top_m_scores, top_m_inds))[::-1]
