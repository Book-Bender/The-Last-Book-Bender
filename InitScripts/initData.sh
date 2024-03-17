#!/usr/bin/env bash
outdir="Data/Raw"
book_url="https://raw.githubusercontent.com/malcolmosh/goodbooks-10k/master/books_enriched.csv"
ratings_url="https://raw.githubusercontent.com/malcolmosh/goodbooks-10k-extended/master/ratings.csv"
curl --create-dirs -O --output-dir $outdir $book_url
curl -O --output-dir $outdir $ratings_url
mkdir "Data/Dump"
