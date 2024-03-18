# The-Last-Book-Bender

## Dataset

We will be using the `good-books-10k-extended` [dataset](https://github.com/malcolmosh/goodbooks-10k-extended), and the `gutenberg` [datasets](http://aleph.gutenberg.org/).

## Getting started

1. Clone this repository:

```bash
git clone https://github.com/Book-Bender/The-Last-Book-Bender.git
```

2. Initialize dependencies, raw data by running:

```bash
sh InitScripts/init.sh
```

note that this will involve installing `torch` (you can modify it in the dependency file), which would take a while to download.

3. Using virtual envs: run

```bash
source ./.venv/bin/activate
```

If you are using `fish`, `csh` or `powershell` shells, the file might be `activate.fish`, `activate.csh`, `Activate.ps1`.

## Algorithms

CF with CBF (with BERT applied).

## Visualizations and Interactivities
