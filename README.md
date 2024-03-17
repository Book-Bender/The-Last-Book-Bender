# The-Last-Book-Bender

## Dataset

We will be using the `good-books-10k-extended` [dataset](https://github.com/malcolmosh/goodbooks-10k-extended).

## Getting started

1. Clone this repository:

```bash
git clone https://github.com/Book-Bender/The-Last-Book-Bender.git
```

2. Initialize dependencies, raw data by running:

```bash
sh InitScript/init.sh
```

note that this will involve installing `torch` (you can modify it in the dependency file).

## Algorithms

We use Collborative filtering (CF), Content-Based filtering with BERT (CFB) for distance metrics.

For information retrieval, we use KNN, or by going through an additional step of clustering.

## Visualizations and Interactivities

We visualize the clusters using D3 (probably).

